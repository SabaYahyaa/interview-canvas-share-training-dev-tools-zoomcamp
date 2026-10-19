import json
import os
import uvicorn
from fastapi import FastAPI, BackgroundTasks, Request

app = FastAPI(title="Automatic Incident Responder")

# Ensure directory exists for saving evidence payloads
INCIDENTS_DIR = os.path.join(os.path.dirname(__file__), "incidents")
os.makedirs(INCIDENTS_DIR, exist_ok=True)


def process_alert_and_run_agent(incident_id: str, alert_data: dict):
    """Saves the alert payload and triggers the automated responder agent."""
    # Save the raw evidence payload
    evidence_path = os.path.join(INCIDENTS_DIR, f"{incident_id}.json")
    with open(evidence_path, "w") as f:
        json.dump(alert_data, f, indent=2)

    print(f"[Responder] Evidence saved to: {evidence_path}")
    
    # Placeholder for running the AI coding assistant in headless mode
    print(f"[Responder] Triggering AI agent in headless mode for incident: {incident_id}...")


@app.get("/health")
async def health_check():
    """Health check endpoint to verify the responder service status."""
    return {"status": "ok", "service": "incident-responder"}


@app.post("/alerts")
async def receive_alert(request: Request, background_tasks: BackgroundTasks):
    """Webhook endpoint receiving Grafana alerts on POST /alerts (Port 8001)."""
    # Parses the incoming HTTP request body sent by Grafana into a Python dictionary.
    payload = await request.json()
    alerts = payload.get("alerts", [])

    for alert in alerts:
        labels = alert.get("labels", {})
        alertname = labels.get("alertname", "UnknownAlert")
        incident_id = f"inc_{alertname.lower()}"

        print(f"[Responder] Firing alert received: {alertname}")
        
        # Process in background task so POST /alerts responds immediately
        # Offloads saving evidence and running the agent to an asynchronous background worker. 
        # This guarantees POST /alerts responds immediately with an HTTP 200 to Grafana,
        # so Grafana doesn't experience a connection timeout waiting for an AI agent to run.
        background_tasks.add_task(process_alert_and_run_agent, incident_id, alert)

    return {"status": "alert_received", "processed": len(alerts)}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
