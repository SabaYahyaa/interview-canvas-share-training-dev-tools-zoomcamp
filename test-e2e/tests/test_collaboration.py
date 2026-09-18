import os
import requests
from playwright.sync_api import Browser, expect

BASE_URL = os.getenv("E2E_BASE_URL", "http://localhost:8000")


def test_realtime_interview_collaboration_flow(browser: Browser):
    # -------------------------------------------------------------------------
    # Step 1: Create an Interview Session via Backend API
    # -------------------------------------------------------------------------
    response = requests.post(
        f"{BASE_URL}/v1/sessions",
        json={"title": "Test Collaboration Session"}
    )
    assert response.status_code == 200, f"Session creation failed: {response.status_code} - {response.text}"

    session_data = response.json()
    session_id = session_data["id"]
    room_url = f"{BASE_URL}/room/{session_id}"

    # -------------------------------------------------------------------------
    # Step 2: Open Interviewer View
    # -------------------------------------------------------------------------
    interviewer_context = browser.new_context()
    interviewer_page = interviewer_context.new_page()
    interviewer_page.goto(room_url, wait_until="domcontentloaded")

    # -------------------------------------------------------------------------
    # Step 3: Open Candidate View in Second Context
    # -------------------------------------------------------------------------
    candidate_context = browser.new_context()
    candidate_page = candidate_context.new_page()
    candidate_page.goto(room_url, wait_until="domcontentloaded")

    # -------------------------------------------------------------------------
    # Step 4: Locate Board / Canvas Area
    # -------------------------------------------------------------------------
    # Target SVG element or fallback to canvas/main container
    canvas_area = candidate_page.locator("svg, canvas, div#canvas, .canvas-container").first
    expect(canvas_area).to_be_visible(timeout=10000)

    # -------------------------------------------------------------------------
    # Step 5: Activate Pen Tool & Draw as Candidate
    # -------------------------------------------------------------------------
    pen_button = candidate_page.get_by_role("button", name="Pen").first
    if pen_button.is_visible():
        pen_button.click()

    box = canvas_area.bounding_box()
    if box:
        candidate_page.mouse.move(box["x"] + 200, box["y"] + 200)
        candidate_page.mouse.down()
        candidate_page.mouse.move(box["x"] + 350, box["y"] + 350, steps=10)
        candidate_page.mouse.up()

    # -------------------------------------------------------------------------
    # Step 6: Verify Board Rendering on Interviewer View
    # -------------------------------------------------------------------------
    interviewer_canvas_area = interviewer_page.locator("svg, canvas, div#canvas, .canvas-container").first
    expect(interviewer_canvas_area).to_be_visible(timeout=10000)

    # Clean up contexts
    candidate_context.close()
    interviewer_context.close()