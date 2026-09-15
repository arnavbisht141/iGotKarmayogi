# LMS Learner Experience Audit

Date: 2026-09-15
Scope: the learner journey from course page to lesson player, practice activities, final assessment and certificate.
Method: walked the flow as demo official Aarav Sharma (Agricultural Statistics & Crop Estimation Surveys), read the player, assessment and learning API code, and queried the live Supabase data.

Severity: **P0** blocks learning or breaks trust in results. **P1** clearly visible quality problem. **P2** polish or scale item.

## Fixed in this pass

| # | Sev | Area | Issue found | Fix |
|---|-----|------|-------------|-----|
| 1 | P0 | Assessment integrity | 72 of 93 final-exam questions were exact copies of the in-lesson practice questions, so learners saw every exam answer (with explanation) before the exam. | Separate exam bank generated from each course's lesson content by the LLM (`scripts/build_assessment_bank.py`). Practice questions are excluded, options are shuffled to balance the answer position, and the bank is stored in `app/core/assessment_bank.json` and loaded by the seed. |
| 2 | P0 | Assessment depth | 18 exams had 4 questions in 15 minutes (3.75 min per question), CPI had 2 questions in 20 minutes, NSS 4 in 25. | 15 questions for multi-lesson courses, 10 for single-lesson courses. Time limit is computed from question count at 1.25 min per question, rounded up to 5 minutes (15 questions = 20 min, 10 questions = 15 min). |
| 3 | P0 | Assessment timer | The timer was a static label ("15:00 mins"). It never counted down and nothing happened when time ran out. | Live countdown (mm:ss, turns red in the last minute) with auto-submit at zero. |
| 4 | P0 | Lesson video | The only video lesson pointed at a sample MP4 that now returns HTTP 403, so the player showed a broken black box. | All 24 courses now have a public YouTube video on a matching lesson, each id verified via YouTube oEmbed, and the dead MP4 was replaced. Lab lessons show the video above the lab launcher. The player falls back to a clear "video could not be loaded" state if a file source fails. |
| 5 | P0 | Lesson reading | Lesson bodies are Markdown (89 lessons) but were printed raw, so learners saw `#` and `-` characters. The `prose` classes did nothing because the typography plugin was not installed. | `react-markdown` + `remark-gfm` renderer with `@tailwindcss/typography`, tables scroll horizontally, links open in a new tab, and the duplicate title heading is removed. |
| 6 | P1 | Assessment | Three courses (Data Quality Frameworks, Digital Governance & PFMS, Python for Public Policy) had no final assessment, so they could never be completed or certified. | Assessments created from the question bank. |
| 7 | P1 | Assessment | Submitting with unanswered questions gave no warning. | Inline confirmation showing how many are unanswered, with "Review answers" and "Submit anyway". |
| 8 | P1 | Certificate | The certificate preview after passing used a random id (`KARM-CERT-11-4821`) that did not match the id on the profile (`KARM-CERT-11-0005`), and hard-coded 6 hours for every course. | The API returns the real certificate id and course duration. |
| 9 | P1 | Assessment | Questions were always in the same order, making retakes a memory test. | Question order is shuffled on every sitting (grading is by question id). |
| 10 | P1 | Player | Lesson changes did not update the URL, so reload, back button and shared links always reopened the last lesson. | Lesson id lives in `?lessonId=`; the page scrolls to top on lesson change. |
| 11 | P1 | Player | Switching lessons took about 3 seconds with no feedback; the endpoint committed before building its response, which expired eager loads and re-queried every module. | Eager loading, commit after the response is built, and a busy state on the lesson pane. |
| 12 | P1 | Progress | Answering a practice question correctly before marking the lesson complete was not recorded. | Progress row is created when missing. |
| 13 | P2 | Errors | Failures used browser `alert()` pop-ups. | Inline error messages in the player and assessment. |

## Open items to plan

| # | Sev | Area | Issue | Recommendation |
|---|-----|------|-------|----------------|
| A | P0 | Assessment integrity | The timer and time limit are enforced only in the browser. A learner can reload to restart the clock, and the API accepts a submission at any time. | Record `started_at` on an attempt when the exam opens and reject or cap submissions after the limit plus a grace period on the server. |
| B | P1 | Assessment integrity | Unlimited retakes on the same fixed pool. | Keep a larger pool (for example 30 per course) and draw 15 per sitting, add a cool-down between attempts, and show the attempts count. |
| C | P1 | Content | Every course has one video, but most are third-party explainers (ONS, UNStats, IBM, freeCodeCamp and others) rather than MoSPI's own training, and no course has more than one. Legacy courses 2 to 5 have a single lesson each despite 4 to 8 listed hours. | Commission or license MoSPI / NSSTA recordings per module and expand the thin courses. Do not publish placeholder URLs. |
| D | P1 | Content quality | Exam questions are LLM-generated from lesson text. A spot check found them accurate and grounded, but they have not had a subject-expert review, and correct options tend to be the longest. | Faculty review pass per course before real certification use; add a "report this question" link. |
| E | P1 | Completion rules | Passing the exam marks the course 100% complete even if lessons were skipped, and "Take assessment" is offered from the last lesson regardless of progress. | Decide the policy (test-out allowed or not) and gate the exam or the certificate accordingly. |
| F | P1 | Session | An expired token on the player shows "Lesson content unavailable" instead of sending the learner to sign in. | Redirect to login with a return URL on 401 from any learner page. |
| G | P2 | Video | Watching a video is not tracked; completion is a manual button. | Use the YouTube IFrame API to record watch progress and resume position. |
| H | P2 | Assessment UX | Submit is only available on the last question, no flag-for-review, no pause or save on connection loss. | Add a sticky submit, question flags, and persist answers locally during the attempt. |
| I | P2 | Learning features | No notes, bookmarks, transcripts, downloadable resources, or discussion per lesson (common in Coursera-style LMS). | Prioritise transcripts and downloadable notes for low-bandwidth field staff. |
| J | P2 | Accessibility | Lesson list items and options rely on colour for state; practice activity has no keyboard radio-group semantics. | Use `radiogroup` semantics and visible state labels. |
