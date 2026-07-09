# Glitch in the Alibi v2

A generative AI detective game. Two AI suspects share an identical,
pre-arranged alibi for a murder. One of them is lying. You search the
crime scene for physical evidence, cross-examine both suspects, watch
a live suspicion meter as you catch them in contradictions — then make
exactly one accusation. How well you investigated, not just who you
name, decides your ending.

---

## What's new in v2

- **Evidence board** — search locations around the case for physical
  clues. Completely free (no API calls), and each clue you find gives
  you a smart, pre-written question you can fire at a suspect with one
  click.
- **Live suspicion meter** — a lightweight, zero-cost contradiction
  detector watches the guilty suspect's answers for phrases that clash
  with the real scene facts, and the meter visibly climbs as you catch
  them. The closer you read, the more it rewards you.
- **Multiple endings** — your ending depends on whether you accused
  correctly, how much evidence you gathered, and whether your
  suspicion levels were actually pointing at the right person before
  you pulled the trigger. Possible outcomes: Flawless case, Solid
  case, Lucky guess, Wrongful accusation, Blind accusation.
- **AI-generated cases** — alongside 5 hand-written cases, you can
  generate a brand new case (victim, scene, suspects, alibi, evidence)
  with a single AI call. Infinite replayability, costs exactly 1
  question out of your daily budget.
- **Quota-aware by design** — a visible "questions asked" counter,
  fewer tokens per suspect reply, and a graceful stonewalling fallback
  if you do run out of quota mid-game, so the evidence board and
  accusation always stay playable even if the chat goes quiet.

---

## How the core mechanic works

Every case randomly assigns one suspect as **guilty** (lying) and one
as **innocent** (truthful); both share the same alibi story.

- The **innocent** suspect is given the real, hard environmental facts
  of where they claim to have been and stays consistent with them no
  matter how granular the question gets.
- The **guilty** suspect was never actually there, so when pressed for
  specific sensory detail, the model has nothing real to draw on and
  **confabulates** plausible-sounding details on the spot — which
  tend to clash with the truth. That clash, an LLM hallucinating under
  pressure, is the whole game.
- The **suspicion meter** is driven by a keyword-matching heuristic
  authored alongside each case's hard facts (in `cases.py`), not an
  extra API call — so it's instant and completely free, though
  necessarily approximate rather than a full semantic check.

---

## Project structure

```
glitch-in-the-alibi-v2/
├── app.py                          # Main Streamlit application
├── cases.py                        # Hand-written case library (5 cases)
├── requirements.txt
├── .gitignore
└── .streamlit/
    └── secrets.toml.example
```

---

## Run it locally

1. **Install Python 3.10+.**

2. From inside this folder:

   ```bash
   pip install -r requirements.txt
   ```

3. **Get a free Gemini API key**: [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey).

4. **Set up secrets**:

   ```bash
   cp .streamlit/secrets.toml.example .streamlit/secrets.toml
   ```

   Edit `.streamlit/secrets.toml` and paste your real key:

   ```toml
   GEMINI_API_KEY = "AIza...your real key..."
   ```

5. **Run it**:

   ```bash
   streamlit run app.py
   ```

   Opens at `http://localhost:8501`.

---

## Deploy for free (Streamlit Community Cloud)

1. Push this folder to a new GitHub repo. `.streamlit/secrets.toml` is
   gitignored — only the `.example` file should be committed.
2. Go to [share.streamlit.io](https://share.streamlit.io), sign in
   with GitHub, click "New app," point it at this repo with main file
   `app.py`.
3. Before deploying, open Advanced settings and add your secret in the
   same TOML format as above (or add it later under the app's
   Settings → Secrets).
4. Deploy. You'll get a public URL like
   `https://your-app-name.streamlit.app`. Every `git push` triggers an
   automatic redeploy.

---

## Managing the free quota

Free Gemini API keys are capped by Google, and the exact daily limit
varies by account — sometimes as low as ~20 requests/day on brand new
accounts, more typically in the hundreds once Google raises your tier.
This build is designed around that reality:

- **The questions counter** in the sidebar tracks how many suspect
  replies you've used this session, against a rough ~18/day budget
  marker, so you're never caught off guard.
- **The evidence board never costs anything** — search as much as you
  want, free, always.
- **If quota does run out mid-game**, suspects fall back to short
  generic stonewalling lines instead of crashing, so you can still
  finish investigating with what you've got and make your accusation.
- **"AI-generated" cases cost exactly 1 question** to create — use the
  "Standard" button instead for unlimited free case variety from the
  hand-written library.

If you hit a hard wall:
- Wait for the daily reset (midnight Pacific time).
- Check actual usage at [ai.dev/rate-limit](https://ai.dev/rate-limit).
- Generate a fresh API key under a different Google account.
- Enable billing on your Google AI Studio project — Flash-Lite is
  extremely cheap per request, and a hobby project like this typically
  costs pennies even at heavy use, while unlocking much higher limits.
- Swap `MODEL_NAME` near the top of `app.py` to whichever current
  Gemini model shows the best quota for your account at
  [ai.google.dev/gemini-api/docs/rate-limits](https://ai.google.dev/gemini-api/docs/rate-limits).

---

## Extending it

- **Add more hand-written cases**: append entries to `CASE_LIBRARY` in
  `cases.py` following the existing schema (victim, scene, suspects,
  hard_facts with contradiction_triggers, evidence). No other code
  changes needed.
- **Tune contradiction sensitivity**: edit `contradiction_triggers`
  lists per fact in `cases.py`, or adjust the suspicion delta values
  in `app.py`'s `update_suspicion` calls.
- **Tune how fast suspects crack**: adjust the `pressure_note`
  thresholds (currently 40 and 70) in `build_system_prompt()`.
- **Add more evidence per case**: more `evidence` entries per case
  means a higher bar for the "flawless"/"solid case" endings, since
  the evidence_ratio thresholds (0.66 / 0.33) are relative to however
  many evidence items that case has.
