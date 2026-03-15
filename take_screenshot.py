"""
Generates a proof screenshot of the submission details.
"""
import json
import datetime
import os
from playwright.sync_api import sync_playwright

def take_screenshot():
    today = datetime.date.today().strftime("%Y-%m-%d")

    try:
        with open("submission_details.json") as f:
            details = json.load(f)
    except Exception:
        details = {"error": "No submission details found"}

    status_color = "#4CAF50" if details.get("success") else "#f44336"
    status_text  = "SUCCESS" if details.get("success") else "CHECK REQUIRED"

    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
  body {{ margin: 0; padding: 30px; background: #f0f4f8; font-family: 'Segoe UI', Arial, sans-serif; }}
  .card {{ background: white; border-radius: 16px; padding: 32px; max-width: 860px;
           margin: auto; box-shadow: 0 4px 20px rgba(0,0,0,0.12); }}
  .header {{ background: {status_color}; color: white; padding: 24px; border-radius: 10px;
             text-align: center; margin-bottom: 28px; }}
  .header h1 {{ margin: 0; font-size: 26px; }}
  .header p  {{ margin: 6px 0 0; opacity: 0.9; font-size: 15px; }}
  .badge {{ display: inline-block; background: white; color: {status_color};
            padding: 4px 14px; border-radius: 20px; font-weight: bold; font-size: 13px; margin-top: 10px; }}
  .meta {{ display: flex; gap: 12px; margin-bottom: 24px; flex-wrap: wrap; }}
  .meta-item {{ background: #f1f8e9; padding: 12px 16px; border-radius: 10px; flex: 1; min-width: 160px; }}
  .meta-item label {{ font-size: 11px; color: #777; display: block; text-transform: uppercase; margin-bottom: 4px; }}
  .meta-item span  {{ font-weight: bold; color: #2e7d32; font-size: 14px; }}
  .field {{ margin-bottom: 18px; border-left: 4px solid {status_color}; padding-left: 14px; }}
  .field label {{ font-weight: bold; color: #555; font-size: 12px; text-transform: uppercase; display: block; margin-bottom: 4px; }}
  .field p {{ margin: 0; color: #333; font-size: 14px; line-height: 1.6; }}
  .footer {{ text-align: center; margin-top: 24px; color: #aaa; font-size: 12px; }}
</style>
</head>
<body>
<div class="card">
  <div class="header">
    <h1>{'✅' if details.get('success') else '⚠️'} Daily Journal Form</h1>
    <p>Simulated Work Daily Journal — Automated Submission</p>
    <span class="badge">{status_text}</span>
  </div>

  <div class="meta">
    <div class="meta-item">
      <label>Date</label>
      <span>{details.get('date', today)}</span>
    </div>
    <div class="meta-item">
      <label>Email</label>
      <span>{details.get('email', 'N/A')}</span>
    </div>
    <div class="meta-item">
      <label>Submitted At (UTC)</label>
      <span>{details.get('submitted_at', 'N/A')}</span>
    </div>
    <div class="meta-item">
      <label>HTTP Status</label>
      <span>{details.get('status_code', 'N/A')}</span>
    </div>
  </div>

  <div class="field">
    <label>Key Tasks for the Day</label>
    <p>{details.get('key_tasks', 'N/A')}</p>
  </div>
  <div class="field">
    <label>Challenges Solved</label>
    <p>{details.get('challenges_solved', 'N/A')}</p>
  </div>
  <div class="field">
    <label>Challenges Unsolved</label>
    <p>{details.get('challenges_unsolved', 'N/A')}</p>
  </div>
  <div class="field">
    <label>Plan for Next Day</label>
    <p>{details.get('plan_next_day', 'N/A')}</p>
  </div>

  <div class="footer">Auto-submitted via GitHub Actions · {details.get('submitted_at', '')}</div>
</div>
</body>
</html>"""

    html_path = os.path.abspath("proof.html")
    with open(html_path, "w") as f:
        f.write(html)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 920, "height": 750})
        page.goto(f"file://{html_path}")
        page.wait_for_timeout(1000)
        screenshot_path = f"form-confirmation-{today}.png"
        page.screenshot(path=screenshot_path, full_page=True)
        print(f"Screenshot saved: {screenshot_path}")
        browser.close()

if __name__ == "__main__":
    take_screenshot()
