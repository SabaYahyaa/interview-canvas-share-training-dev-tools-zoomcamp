import type {
  CanvasDocument,
  CanvasElement,
  GuestLink,
  InterviewSession,
  Participant,
  Role,
  User,
} from "./types";

// Dynamically resolve API and WebSocket bases for local & production deployments
const getApiBase = () => {
  const envApi = typeof import.meta !== "undefined" && import.meta.env?.VITE_API_URL;
  if (envApi) return envApi.replace(/\/$/, "");
  if (typeof window !== "undefined") return window.location.origin;
  return "";
};

const getWsBase = () => {
  const envWs = typeof import.meta !== "undefined" && import.meta.env?.VITE_WS_URL;
  if (envWs) return envWs.replace(/\/$/, "");
  if (typeof window !== "undefined") {
    const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
    return `${protocol}//${window.location.host}`;
  }
  return "";
};

const API_BASE = getApiBase();
const WS_BASE = getWsBase();

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
  const formattedPath = safePath.startsWith("/") ? safePath : `/${safePath}`;
  
  // Guarantees clean relative resolution (/v1/...) when API_BASE is empty
  const url = API_BASE ? `${API_BASE}${formattedPath}` : formattedPath;

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

  const json = await res.json();
  return json as T;
}

// Helper to sanitize session IDs and prevent routing to /undefined
function validateId(id: string, paramName: string = "id"): string {
  if (!id || id === "undefined" || id === "null" || id.trim() === "") {
    throw new Error(`Invalid ${paramName} provided: "${id}"`);
  }
  return encodeURIComponent(id);
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
  
  getSession: (id: string) => 
    request<SessionDetail>(`/v1/sessions/${validateId(id)}`),
  
  createSession: async (input: {
    title: string;
    prompt: string;
    duration_minutes: number;
    scheduled_at: string | null;
  }): Promise<InterviewSession> => {
    const rawResponse = await request<any>("/v1/sessions", {
      method: "POST",
      body: JSON.stringify(input),
    });

    // Extract InterviewSession if response is wrapped as { session: {...} } or { data: {...} }
    const session: InterviewSession = rawResponse?.session ?? rawResponse?.data ?? rawResponse;
    if (!session || !session.id) {
      throw new Error("Backend response from POST /v1/sessions is missing a valid session 'id'.");
    }
    return session;
  },

  updateSession: (id: string, patch: Partial<InterviewSession>) =>
    request<InterviewSession>(`/v1/sessions/${validateId(id)}`, {
      method: "PATCH",
      body: JSON.stringify(patch),
    }),

  startSession: (id: string) =>
    request<InterviewSession>(`/v1/sessions/${validateId(id)}/start`, { method: "POST" }),

  endSession: (id: string) =>
    request<InterviewSession>(`/v1/sessions/${validateId(id)}/end`, { method: "POST" }),

  archiveSession: (id: string) =>
    request<InterviewSession>(`/v1/sessions/${validateId(id)}/archive`, { method: "POST" }),

  duplicateSession: (id: string) =>
    request<InterviewSession>(`/v1/sessions/${validateId(id)}/duplicate`, {
      method: "POST",
    }),

  createGuestLink: (id: string, role_granted: Exclude<Role, "owner"> = "candidate") =>
    request<GuestLink>(`/v1/sessions/${validateId(id)}/guest-links`, {
      method: "POST",
      body: JSON.stringify({ role_granted }),
    }),

  revokeGuestLink: (id: string, linkId: string) =>
    request<boolean>(
      `/v1/sessions/${validateId(id)}/guest-links/${validateId(linkId, "linkId")}`,
      { method: "DELETE" }
    ),

  inspectToken: (token: string) =>
    request<TokenInspection>(`/v1/join/${validateId(token, "token")}`),

  join: (token: string, display_name: string) =>
    request<{ participant: Participant; session: InterviewSession }>(
      `/v1/join/${validateId(token, "token")}`,
      { method: "POST", body: JSON.stringify({ display_name }) }
    ),

  joinAsOwner: (sessionId: string) =>
    request<Participant>(`/v1/sessions/${validateId(sessionId)}/participants`, {
      method: "POST",
    }),

  removeParticipant: (sessionId: string, participantId: string) =>
    request<boolean>(
      `/v1/sessions/${validateId(sessionId)}/participants/${validateId(participantId, "participantId")}`,
      { method: "DELETE" }
    ),

  leave: (sessionId: string, participantId: string) =>
    request<boolean>(
      `/v1/sessions/${validateId(sessionId)}/participants/${validateId(participantId, "participantId")}`,
      { method: "DELETE" }
    ),

  getCanvas: (sessionId: string) =>
    request<CanvasDocument>(`/v1/sessions/${validateId(sessionId)}/canvas`),

  saveCanvas: (sessionId: string, elements: CanvasElement[], actor: string) =>
    request<string>(`/v1/sessions/${validateId(sessionId)}/canvas`, {
      method: "PUT",
      body: JSON.stringify({ elements, actor }),
    }),

  getAudit: (sessionId: string) =>
    request<AuditEvent[]>(`/v1/sessions/${validateId(sessionId)}/audit`),
};