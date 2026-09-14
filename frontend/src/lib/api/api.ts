import type {
  CanvasDocument,
  CanvasElement,
  GuestLink,
  InterviewSession,
  Participant,
  Role,
  User,
} from "./types";

const API_BASE = "http://localhost:8091";
const WS_BASE = "ws://localhost:8091";

export type RoomMessage =
  | { type: "document_update"; sessionId: string; elements: CanvasElement[]; actor: string }
  | {
      type: "presence_update";
      sessionId: string;
      participant: Participant;
      cursor?: { x: number; y: number } | null;
    }
  | { type: "presence_leave"; sessionId: string; participantId: string }
  | { type: "permission_changed"; sessionId: string; session: InterviewSession }
  | { type: "session_ended"; sessionId: string };

export type ConnectionState = "connected" | "reconnecting";

interface SessionDetail {
  session: InterviewSession;
  participants: Participant[];
  link: GuestLink | null;
}

interface SessionListItem extends InterviewSession {
  participants: Participant[];
  link: GuestLink | null;
}

interface TokenInspection {
  session: InterviewSession;
  link: GuestLink;
  activeCount: number;
}

interface AuditEvent {
  id: string;
  session_id: string;
  event: string;
  at: string;
  actor: string;
}

// --- HTTP REQUEST HELPER ---

async function request<T>(
  path: string,
  options: RequestInit = {}
): Promise<T> {
  const safePath = typeof path === "string" ? path : "";
  const url = `${API_BASE}${safePath}`;

  const res = await fetch(url, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
  });

  if (!res.ok) {
    const errorBody = await res.json().catch(() => ({}));
    throw new Error(errorBody.detail || `Request failed with status ${res.status}`);
  }

  return res.json() as Promise<T>;
}

// --- REALTIME WEBSOCKET MANAGEMENT ---

interface RoomConnection {
  socket: WebSocket | null;
  subscribers: Set<(message: RoomMessage) => void>;
  connectionSubscribers: Set<(state: ConnectionState) => void>;
  connectionState: ConnectionState;
}

const rooms = new Map<string, RoomConnection>();

function setConnectionState(room: RoomConnection, state: ConnectionState) {
  if (room.connectionState === state) return;
  room.connectionState = state;
  room.connectionSubscribers.forEach((sub) => sub(state));
}

function connectWebSocket(sessionId: string, room: RoomConnection) {
  if (room.socket && (room.socket.readyState === WebSocket.OPEN || room.socket.readyState === WebSocket.CONNECTING)) {
    return;
  }

  const ws = new WebSocket(`${WS_BASE}/ws/rooms/${encodeURIComponent(sessionId)}`);
  room.socket = ws;

  ws.onopen = () => {
    setConnectionState(room, "connected");
  };

  ws.onmessage = (event) => {
    try {
      const msg: RoomMessage = JSON.parse(event.data);
      room.subscribers.forEach((handler) => handler(msg));
    } catch (e) {
      console.error("[WS] Parse error:", e);
    }
  };

  ws.onclose = () => {
    setConnectionState(room, "reconnecting");
    room.socket = null;
    // Automatic reconnect after 2s
    setTimeout(() => {
      if (rooms.has(sessionId)) {
        connectWebSocket(sessionId, room);
      }
    }, 2000);
  };

  ws.onerror = () => {
    setConnectionState(room, "reconnecting");
  };
}

function getRoom(sessionId: string): RoomConnection {
  let room = rooms.get(sessionId);
  if (!room) {
    room = {
      socket: null,
      subscribers: new Set(),
      connectionSubscribers: new Set(),
      connectionState: "reconnecting",
    };
    rooms.set(sessionId, room);
  }
  return room;
}

export function publish(message: RoomMessage) {
  const room = getRoom(message.sessionId);
  if (room.socket && room.socket.readyState === WebSocket.OPEN) {
    room.socket.send(JSON.stringify(message));
  }
}

export function subscribe(sessionId: string, handler: (message: RoomMessage) => void) {
  if (typeof window === "undefined") return () => {};
  const room = getRoom(sessionId);
  room.subscribers.add(handler);
  connectWebSocket(sessionId, room);

  return () => {
    room.subscribers.delete(handler);
    if (room.subscribers.size === 0 && room.connectionSubscribers.size === 0) {
      if (room.socket) room.socket.close();
      rooms.delete(sessionId);
    }
  };
}

export function subscribeConnection(sessionId: string, handler: (state: ConnectionState) => void) {
  if (typeof window === "undefined") return () => {};
  const room = getRoom(sessionId);
  room.connectionSubscribers.add(handler);
  handler(room.connectionState);

  return () => {
    room.connectionSubscribers.delete(handler);
    if (room.subscribers.size === 0 && room.connectionSubscribers.size === 0) {
      if (room.socket) room.socket.close();
      rooms.delete(sessionId);
    }
  };
}

// --- PUBLIC API METHODS ---

export const api = {
  getCurrentUser: () => request<User>("/v1/me"),
  listSessions: () => request<SessionListItem[]>("/v1/sessions"),
  getSession: (id: string) => request<SessionDetail>(`/v1/sessions/${encodeURIComponent(id)}`),
  createSession: (input: {
    title: string;
    prompt: string;
    duration_minutes: number;
    scheduled_at: string | null;
  }) => request<InterviewSession>("/v1/sessions", { method: "POST", body: JSON.stringify(input) }),
  updateSession: (id: string, patch: Partial<InterviewSession>) =>
    request<InterviewSession>(`/v1/sessions/${encodeURIComponent(id)}`, {
      method: "PATCH",
      body: JSON.stringify(patch),
    }),
  startSession: (id: string) =>
    request<InterviewSession>(`/v1/sessions/${encodeURIComponent(id)}/start`, { method: "POST" }),
  endSession: (id: string) =>
    request<InterviewSession>(`/v1/sessions/${encodeURIComponent(id)}/end`, { method: "POST" }),
  archiveSession: (id: string) =>
    request<InterviewSession>(`/v1/sessions/${encodeURIComponent(id)}/archive`, { method: "POST" }),
  duplicateSession: (id: string) =>
    request<InterviewSession>(`/v1/sessions/${encodeURIComponent(id)}/duplicate`, {
      method: "POST",
    }),
  createGuestLink: (id: string, role_granted: Exclude<Role, "owner"> = "candidate") =>
    request<GuestLink>(`/v1/sessions/${encodeURIComponent(id)}/guest-links`, {
      method: "POST",
      body: JSON.stringify({ role_granted }),
    }),
  revokeGuestLink: (id: string, linkId: string) =>
    request<boolean>(
      `/v1/sessions/${encodeURIComponent(id)}/guest-links/${encodeURIComponent(linkId)}`,
      { method: "DELETE" }
    ),
  inspectToken: (token: string) =>
    request<TokenInspection>(`/v1/join/${encodeURIComponent(token)}`),
  join: (token: string, display_name: string) =>
    request<{ participant: Participant; session: InterviewSession }>(
      `/v1/join/${encodeURIComponent(token)}`,
      { method: "POST", body: JSON.stringify({ display_name }) }
    ),
  joinAsOwner: (sessionId: string) =>
    request<Participant>(`/v1/sessions/${encodeURIComponent(sessionId)}/participants`, {
      method: "POST",
    }),
  removeParticipant: (sessionId: string, participantId: string) =>
    request<boolean>(
      `/v1/sessions/${encodeURIComponent(sessionId)}/participants/${encodeURIComponent(participantId)}`,
      { method: "DELETE" }
    ),
  leave: (sessionId: string, participantId: string) =>
    request<boolean>(
      `/v1/sessions/${encodeURIComponent(sessionId)}/participants/${encodeURIComponent(participantId)}`,
      { method: "DELETE" }
    ),
  getCanvas: (sessionId: string) =>
    request<CanvasDocument>(`/v1/sessions/${encodeURIComponent(sessionId)}/canvas`),
  saveCanvas: (sessionId: string, elements: CanvasElement[], actor: string) =>
    request<string>(`/v1/sessions/${encodeURIComponent(sessionId)}/canvas`, {
      method: "PUT",
      body: JSON.stringify({ elements, actor }),
    }),
  getAudit: (sessionId: string) =>
    request<AuditEvent[]>(`/v1/sessions/${encodeURIComponent(sessionId)}/audit`),
};