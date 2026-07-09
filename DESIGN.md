GLITCH IN THE ALIBI v2 — ARCHITECTURE NOTES
=============================================

CORE PROBLEM WITH v1:
- Every single chat message = 1 API call. A real interrogation session
  (10-15 questions per suspect x 2 suspects) burns 20-30 calls easily.
  On a 20/day free quota, the game is unplayable past one session.

QUOTA STRATEGY FOR v2:
1. Case generation (victim/scene/suspects/facts) = templated, NOT an API
   call by default. We ship a larger hand-written library (10 cases) and
   recombine elements (names, objects, relationships) programmatically
   for huge variety without spending any quota on it.
2. Optional "AI Case Generator" mode = ONE api call that generates an
   entire case structure as JSON. One call buys a whole game session.
   This is the procedural option, opt-in, clearly labeled as using 1 call.
3. Suspect dialogue = still live AI per message (this is the core
   gameplay loop, can't fake it) — but:
   - Shorter max_output_tokens to reduce cost/risk
   - A visible "Questions remaining today" counter so the player
     manages their own budget instead of getting surprised by a 429
   - Graceful degradation: if quota runs out mid-game, suspects fall
     back to a small set of pre-written "stonewalling" lines so the
     game doesn't hard-crash — player can still use the evidence
     board and make their final accusation.
4. Evidence/clue descriptions = templated from data, not AI-generated.
   Keeps the clue system completely free regardless of quota state.

DATA MODEL:

Case = {
  id, victim, scene, time_of_death, weapon/method,
  suspects: [ {name, relationship_to_victim, personality_tag} x2 ],
  shared_alibi: str,
  hard_facts: [ str x 5-7 ],          # ground truth of alibi location
  evidence: [                          # NEW — physical clue system
    {
      id, name, description, location_found,
      unlocks_question_hint: str,      # suggested question to ask once found
      relevance: "supports_innocent" | "supports_guilty" | "red_herring",
      reveal_text: str                 # flavor text shown on discovery
    }
    ... 4-6 per case
  ],
  red_herring_facts: [ str ]           # facts that seem suspicious but aren't
}

GAME STATE additions over v1:
  - evidence_found: set of evidence ids discovered this session
  - suspicion: { suspect_idx: int (0-100) }  # rises on contradiction catches
  - contradiction_log: [ {suspect_idx, question, claim, conflicts_with} ]
  - questions_asked_count: int (for quota budget display)
  - ending_type: computed at verdict time from:
      - correct/incorrect accusation
      - evidence_found coverage (did they find enough clues?)
      - suspicion accuracy (was their suspicion meter pointing the
        right direction before they accused?)
    => possible endings: "Flawless Case" / "Lucky Guess" / "Case Closed"
       / "Wrongful Accusation" / "Killer Walks - No Evidence"

EVIDENCE SYSTEM UX:
  - A "Search the scene" panel/tab alongside suspects
  - Click to "search" a location (kitchen, alley, study, etc per case)
  - Reveals 1-2 evidence items with flavor text, costs NO api call
  - Each evidence item, once found, appears as a clickable "ask about
    this" chip in the chat input area — clicking it pre-fills a smart
    question into the input box (still costs 1 api call to ask, but
    the player chose to spend it deliberately)

SUSPICION METER:
  - Starts neutral (50/50 split, or 0 for both)
  - We detect "contradiction catches" with a LIGHTWEIGHT heuristic,
    not an extra API call: after each suspect reply, check if reply
    text contains any keyword overlap with hard_facts that CONTRADICTS
    (e.g. fact says "radio was silent/broken" and reply contains
    "radio was playing" / "music" / "the radio" + positive claim).
  - This is necessarily fuzzy — simplest robust approach: maintain a
    small set of "trigger phrases" per hard fact in the case data,
    authored alongside the fact itself, so detection is reliable
    without needing another model call.
  - Each hard_fact in case data gets a `contradiction_triggers: [str]`
    list of phrases that, if they appear in the GUILTY suspect's
    reply, count as a caught contradiction. Authored by us per case
    since we know exactly what the fabricated lie is likely to
    sound like (LLMs improvising "what a kitchen sounds like" tend to
    reach for recognizable tropes - radio playing, music, sizzling,
    etc.) — confirmed empirically usable since the guilty prompt
    explicitly tells the model to confabulate around the SAME hard
    facts list, so its lies orbit predictable territory.
  - Imperfect by nature (this is fundamentally fuzzy text matching)
    but good enough to drive a meter that *feels* responsive and
    rewards close reading, which is the design goal — not perfect
    NLU.

ENDING LOGIC (deterministic, no API call):
  won = accused_idx == guilty_idx
  evidence_ratio = len(evidence_found) / len(case.evidence)
  suspicion_correct = suspicion[guilty_idx] > suspicion[innocent_idx]

  if won and evidence_ratio >= 0.66 and suspicion_correct:
      ending = "flawless"
  elif won and (evidence_ratio >= 0.33 or suspicion_correct):
      ending = "solid_case"
  elif won:
      ending = "lucky_guess"
  elif not won and evidence_ratio < 0.33:
      ending = "blind_accusation"
  else:
      ending = "wrongful_accusation"
