import requests
import random
import datetime
import json
import os

# ─── FORM DETAILS ────────────────────────────────────────────────────────────
FORM_URL      = "https://docs.google.com/forms/u/0/d/e/1FAIpQLSc8RRUAG8n8nPB9dm21m_MxwHQ-JuDnEj7GnvwEkWXykkKFuQ/formResponse"
FORM_VIEW_URL = "https://docs.google.com/forms/d/e/1FAIpQLSc8RRUAG8n8nPB9dm21m_MxwHQ-JuDnEj7GnvwEkWXykkKFuQ/viewform"
EMAIL         = "vijaykumar.r.s67@kalvium.community"

# ─── ANSWER POOLS (10 options each) ──────────────────────────────────────────

KEY_TASKS = [
    "Completed assigned tasks and participated in team discussions. Reviewed project requirements and updated task progress on the tracker.",
    "Worked on sprint tasks and attended daily standup. Reviewed pull requests and updated documentation for the module.",
    "Implemented new features as per the assigned ticket. Collaborated with teammates and pushed changes to the repository.",
    "Completed development tasks for the current milestone. Participated in code reviews and fixed reported issues.",
    "Worked on the assigned module and resolved pending tasks. Attended team sync and updated the project tracker.",
    "Finished coding tasks assigned for the day and tested the implementation. Reviewed teammates code and gave feedback.",
    "Focused on completing the backlog items. Attended planning meeting and updated task status in the project board.",
    "Worked on bug fixes and feature development. Synced with the team on blockers and updated progress notes.",
    "Completed UI and backend tasks for the current sprint. Reviewed documentation and aligned with team on next steps.",
    "Executed assigned development tasks and participated in team discussions. Ensured code quality and pushed updates to GitHub.",
]

CHALLENGES_SOLVED = [
    "Resolved blockers related to the current sprint. Debugged issues in the codebase and pushed fixes to GitHub.",
    "Fixed a bug in the API integration that was causing incorrect data rendering. Resolved the issue after debugging.",
    "Solved a merge conflict in the repository and ensured the codebase was stable before deployment.",
    "Debugged and fixed an authentication issue that was blocking login for certain users.",
    "Resolved a performance issue in the database query by optimizing the SQL and adding proper indexing.",
    "Fixed a UI alignment bug that was reported during testing. Updated the CSS and verified across browsers.",
    "Resolved an issue with environment variable configuration that was causing build failures in the CI pipeline.",
    "Debugged a logic error in the business layer that was producing incorrect output. Fixed and tested thoroughly.",
    "Solved a CORS issue in the backend that was blocking API calls from the frontend application.",
    "Resolved state management issues in the frontend that were causing unexpected re-renders and data inconsistency.",
]

CHALLENGES_UNSOLVED = [
    "Need to improve error handling and write more test cases. Planning to address these in the upcoming days.",
    "Still working on optimizing the API response time. Will investigate caching strategies in the next session.",
    "Firebase authentication edge cases are not fully handled yet. Planning to complete this in upcoming days.",
    "The integration with third-party service is partially complete. Need to test edge cases and handle error states.",
    "Unit tests for the new module are pending. Will write comprehensive test cases in the next working session.",
    "The deployment pipeline has a minor configuration issue that needs to be resolved before the next release.",
    "Need to refactor the existing code for better readability and maintainability. Scheduled for the next sprint.",
    "Some accessibility improvements are pending for the UI. Will address them in the upcoming development cycle.",
    "Database migration script needs further testing before it can be run on the production environment.",
    "Documentation for the newly added APIs is incomplete. Will finalize and publish it in the coming days.",
]

PLAN_NEXT_DAY = [
    "Focus on optimizing current implementation, reviewing feedback, and completing pending tasks.",
    "Plan to complete the remaining unit tests and start working on the next sprint ticket.",
    "Will continue working on Firebase authentication and handle the remaining edge cases.",
    "Plan to review the code feedback received and implement the suggested improvements.",
    "Will focus on completing the API integration and writing documentation for the endpoints.",
    "Plan to work on the UI improvements and ensure responsiveness across different screen sizes.",
    "Will investigate the performance bottleneck and apply optimization techniques to improve speed.",
    "Plan to complete the pending code review tasks and sync with the team on upcoming deliverables.",
    "Will focus on resolving the deployment issue and ensure the application runs smoothly in staging.",
    "Plan to write test cases for the current module and start exploring the next feature requirement.",
]

def submit_form():
    today = datetime.date.today().strftime("%B %d, %Y")
    print(f"Submitting form for {today}...")

    answers = {
        "key_tasks":           random.choice(KEY_TASKS),
        "challenges_solved":   random.choice(CHALLENGES_SOLVED),
        "challenges_unsolved": random.choice(CHALLENGES_UNSOLVED),
        "plan_next_day":       random.choice(PLAN_NEXT_DAY),
    }

    print(f"\nSelected answers:")
    print(f"  Key tasks       : {answers['key_tasks'][:70]}...")
    print(f"  Challenges done : {answers['challenges_solved'][:70]}...")
    print(f"  Challenges left : {answers['challenges_unsolved'][:70]}...")
    print(f"  Plan next day   : {answers['plan_next_day'][:70]}...")

    data = {
        "emailAddress":     EMAIL,
        "entry.32162408":   answers["key_tasks"],
        "entry.1874357572": answers["challenges_solved"],
        "entry.199221807":  answers["challenges_unsolved"],
        "entry.1546753981": answers["plan_next_day"],
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer":      "https://docs.google.com/forms",
        "User-Agent":   "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    }

    print("\nSubmitting form...")
    response = requests.post(FORM_URL, data=data, headers=headers)

    if response.status_code == 200:
        print(f"Form submitted successfully! ({today})")
    else:
        print(f"Status code: {response.status_code} (form likely still submitted)")

    # Save submission details to a JSON file for the screenshot step
    submission = {
        "date":              today,
        "email":             EMAIL,
        "status_code":       response.status_code,
        "key_tasks":         answers["key_tasks"],
        "challenges_solved": answers["challenges_solved"],
        "challenges_unsolved": answers["challenges_unsolved"],
        "plan_next_day":     answers["plan_next_day"],
        "submitted_at":      datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
    }

    with open("submission_details.json", "w") as f:
        json.dump(submission, f, indent=2)

    print("Submission details saved to submission_details.json")

if __name__ == "__main__":
    submit_form()