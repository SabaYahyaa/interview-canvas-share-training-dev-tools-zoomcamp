import os
import re
from playwright.sync_api import Browser, expect

BASE_URL = os.getenv("E2E_BASE_URL", "http://localhost:3000")


def test_realtime_interview_collaboration_flow(browser: Browser):
    # -------------------------------------------------------------------------
    # Step 1: Log in as Interviewer (Session 1)
    # -------------------------------------------------------------------------
    interviewer_context = browser.new_context()
    interviewer_page = interviewer_context.new_page()

    interviewer_page.goto(f"{BASE_URL}/login")

    interviewer_page.fill('input[type="email"]', "interviewer@example.com")
    interviewer_page.fill('input[type="password"]', "password123")
    interviewer_page.click('button[type="submit"]')

    interviewer_page.wait_for_url("**/dashboard")

    # -------------------------------------------------------------------------
    # Step 2: Create an Interview Session
    # -------------------------------------------------------------------------
    interviewer_page.click('a[href="/interviews/new"], button:has-text("New Interview")')
    interviewer_page.fill('input[name="title"], #title', "E2E System Design Interview")
    interviewer_page.fill('textarea[name="prompt"], #prompt', "Design a URL shortener.")
    interviewer_page.click('button[type="submit"]')

    interviewer_page.wait_for_url(re.compile(r"/room/[a-zA-Z0-9-]+"))
    room_url = interviewer_page.url
    session_id = room_url.split("/room/")[1]
    assert session_id

    # -------------------------------------------------------------------------
    # Step 3: Share / Extract the Join Link
    # -------------------------------------------------------------------------
    interviewer_page.click('button:has-text("Share"), button:has-text("Invite")')

    join_link_input = interviewer_page.locator('input[readonly], input[value*="/join/"]')
    expect(join_link_input).to_be_visible()
    join_url = join_link_input.input_value()
    assert "/join/" in join_url

    # -------------------------------------------------------------------------
    # Step 4: Join from a separate client as Candidate (Session 2)
    # -------------------------------------------------------------------------
    candidate_context = browser.new_context()
    candidate_page = candidate_context.new_page()

    candidate_page.goto(join_url)
    expect(candidate_page.locator("h1")).to_contain_text("E2E System Design Interview")

    candidate_page.fill('input#name, input[name="name"]', "Alice Candidate")
    candidate_page.click('button[type="submit"]')

    candidate_page.wait_for_url(re.compile(f"/room/{session_id}"))
    expect(candidate_page.locator('text="Alice Candidate"')).to_be_visible()

    # -------------------------------------------------------------------------
    # Step 5: Change the canvas as Candidate (Session 2)
    # -------------------------------------------------------------------------
    candidate_canvas = candidate_page.locator("canvas").first
    expect(candidate_canvas).to_be_visible()

    box = candidate_canvas.bounding_box()
    if box:
        candidate_page.mouse.move(box["x"] + 100, box["y"] + 100)
        candidate_page.mouse.down()
        candidate_page.mouse.move(box["x"] + 250, box["y"] + 250, steps=10)
        candidate_page.mouse.up()

    # -------------------------------------------------------------------------
    # Step 6: Verify Interviewer sees the change (Session 1)
    # -------------------------------------------------------------------------
    expect(
        interviewer_page.locator('text="Alice Candidate"').or_(
            interviewer_page.locator('[title*="Alice"]')
        )
    ).to_be_visible()

    interviewer_page.wait_for_timeout(1000)

    interviewer_canvas = interviewer_page.locator("canvas").first
    expect(interviewer_canvas).to_be_visible()

    candidate_context.close()
    interviewer_context.close()