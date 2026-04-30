# Blockchain Dashboard Project

Use this repository to build your blockchain dashboard project.
Update this README every week.

## Student Information

| Field | Value |
|---|---|
| Student Name | Juan Hevia Losa |
| GitHub Username | @juanhevia |
| Project Title | Blockchain Dashboard Project |
| Chosen AI Approach | Difficulty Predictor (Time Series) |

## Module Tracking

| Module | Status |
|---|---|
| M1: PoW Monitor | Completed |
| M2: Block Header | Completed |
| M3: Difficulty | Completed |
| M4: AI Integration | Not started |

## Current Progress

- Checkpoint reached: Repository structure maintained and M1, M2, and M3 modules fully integrated into the Streamlit dashboard.
- M1 successfully connects API output to theory (calculated Target and leading zeros from the 'bits' field).
- Resolved initial API rate-limiting issues by switching to Mempool.space.

## Next Step

- Start developing M4 (AI Integration) and prepare the historical dataset for the Machine Learning model.

## Main Problem or Blocker

- No active blockers at the moment. API connection is stable.

## How to Run
```bash
pip install -r requirements.txt
streamlit run app.py

<!-- student-repo-auditor:teacher-feedback:start -->
## Teacher Feedback

### Kick-off Review

Review time: 2026-04-29 20:44 CEST
Status: Amber

Strength:
- I can see the dashboard structure integrating the checkpoint modules.

Improve now:
- The README should now reflect the checkpoint more explicitly, including progress, blockers, and updated module status.

Next step:
- Update the README so progress, blockers, module status, and next step match the checkpoint format exactly.
<!-- student-repo-auditor:teacher-feedback:end -->
