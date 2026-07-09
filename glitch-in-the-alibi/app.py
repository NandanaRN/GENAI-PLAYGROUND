"""
Glitch in the Alibi v2 - Hybrid Edition
---------------------------------------
Combines your rich custom HTML/CSS component layout with the 
Python Streamlit game state engine and google-genai SDK backend.
"""

import json
import random
import time
import streamlit as st
from google import genai
from google.genai import types
from google.genai.errors import ClientError

from cases import CASE_LIBRARY

# ------------------------------------------------------------------
# PAGE CONFIG + HOOK UP CUSTOM FRONTEND WRAPPER
# ------------------------------------------------------------------
st.set_page_config(
    page_title="Glitch in the Alibi",
    page_icon="🕵️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Dark immersive UI overrides for the outer Streamlit shell
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Share+Tech+Mono&family=Inter:wght@400;500;600&display=swap');
    
    .stApp, [data-testid="stHeader"] {
        background-color: #0D0D0F !important;
        color: #E8E6DF !important;
    }
    div[data-testid="stSidebar"] {
        background-color: #16161A !important;
        border-right: 1px solid #2A2A34 !important;
    }
    /* Hide standard Streamlit margins for complete game view immersion */
    [data-testid="block-container"] {
        padding: 1rem 2rem !important;
    }
    
    /* Neon-noir UI Card Classes */
    .game-header-box {
        background: #16161A;
        border: 1px solid #2A2A34;
        border-radius: 6px;
        padding: 1rem 1.5rem;
        margin-bottom: 1rem;
    }
    .case-badge {
        font-family: 'Share Tech Mono', monospace;
        color: #E8C547;
        font-size: 11px;
        letter-spacing: 0.15em;
    }
    .case-title {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 28px;
        letter-spacing: 0.05em;
        margin-top: 2px;
    }
    .brief-card {
        background: #1E1E24;
        border: 1px solid #2A2A34;
        border-left: 4px solid #E05C3A;
        border-radius: 4px;
        padding: 1.2rem;
        font-family: 'Inter', sans-serif;
    }
    .fact-label {
        font-family: 'Share Tech Mono', monospace;
        font-size: 10px;
        color: #7A7870;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        margin-bottom: 2px;
    }
    .fact-val {
        font-family: 'Inter', sans-serif;
        font-size: 13px;
        color: #E8E6DF;
    }
    .meter-track {
        background: #1A1A20;
        border-radius: 2px;
        height: 6px;
        overflow: hidden;
        margin-top: 4px;
    }
    .meter-fill {
        height: 100%;
        border-radius: 2px;
        transition: width 0.4s;
    }
</style>
""", unsafe_allow_html=True)

MODEL_NAME = "gemini-2.5-flash-lite"
MAX_QUESTIONS_PER_SUSPECT = 15

# ------------------------------------------------------------------
# BACKEND INITIALIZATION
# ------------------------------------------------------------------
@st.cache_resource
def get_client():
    api_key = st.secrets.get("GEMINI_API_KEY", None)
    if not api_key:
        st.error("No GEMINI_API_KEY found in Streamlit secrets. Add it under Settings -> Secrets to initialize.")
        st.stop()
    return genai.Client(api_key=api_key)

def get_handwritten_case():
    return json.loads(json.dumps(random.choice(CASE_LIBRARY)))

def new_case():
    case = get_handwritten_case()
    guilty_idx = random.choice([0, 1])
    
    st.session_state.case = case
    st.session_state.case_number = f"GA-{random.randint(10000, 99999)}"
    st.session_state.suspects = [
        {"name": case["suspects"][0], "role": "guilty" if guilty_idx == 0 else "innocent", "history": [], "questions_left": MAX_QUESTIONS_PER_SUSPECT, "emoji": case.get("suspect_emojis", ["👩‍💼", "👨‍💼"])[0], "title": case.get("suspect_roles", ["Suspect A", "Suspect B"])[0]},
        {"name": case["suspects"][1], "role": "guilty" if guilty_idx == 1 else "innocent", "history": [], "questions_left": MAX_QUESTIONS_PER_SUSPECT, "emoji": case.get("suspect_emojis", ["👩‍💼", "👨‍💼"])[1], "title": case.get("suspect_roles", ["Suspect A", "Suspect B"])[1]},
    ]
    st.session_state.active_suspect = 0
    st.session_state.verdict = None
    st.session_state.evidence_found = set()
    st.session_state.suspicion = {0: 0, 1: 0}
    st.session_state.searched_locations = set()

if "case" not in st.session_state:
    new_case()

case = st.session_state.case

# ------------------------------------------------------------------
# GAME HEADER UI COMPONENT
# ------------------------------------------------------------------
st.markdown(f"""
<div class="game-header-box">
    <div class="case-badge">CASE FILE #{st.session_state.case_number}</div>
    <div class="case-title">THE {case['victim'].split(' ')[-1].upper()} MURDER</div>
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------
# MAIN UI SPLIT: LEFT SIDEBAR (Dossier) | RIGHT ACTION PANEL (Interrogation)
# ------------------------------------------------------------------
col_left, col_right = st.columns([1, 2], gap="medium")

with col_left:
    st.markdown("### 📋 Case Briefing")
    st.markdown(f"""
    <div class="brief-card">
        <div style="font-size: 24px; margin-bottom: 4px;">{case.get('emoji', '💀')}</div>
        <div style="font-weight: 600; font-size: 16px;">{case['victim']}</div>
        <div style="color: #A0A0AA; font-size: 12px; margin-bottom: 8px;">VICTIM — DECEASED</div>
        <div style="font-size: 13px; color: #D4D4D8; line-height: 1.5;">{case['victim_detail']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("")
    sub_col1, sub_col2 = st.columns(2)
    with sub_col1:
        st.markdown(f'<div class="fact-label">Time of death</div><div class="fact-val">{case["time_of_death"]}</div>', unsafe_allow_html=True)
    with sub_col2:
        st.markdown(f'<div class="fact-label">Cause of death</div><div class="fact-val">{case.get("method", "Blunt Trauma")}</div>', unsafe_allow_html=True)
        
    st.markdown(f'<div class="fact-label" style="margin-top:12px;">Crime Scene</div><div class="fact-val">{case["scene"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="fact-label" style="margin-top:12px;">Shared Alibi</div><div class="fact-val" style="color: #E8C547;">"{case["shared_alibi"]}"</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🔍 Evidence Track")
    locations = sorted(set(ev["location"] for ev in case["evidence"]))
    for loc in locations:
        searched = loc in st.session_state.searched_locations
        if not searched:
            if st.button(f"Search Area: {loc}", key=f"search_{loc}", use_container_width=True):
                st.session_state.searched_locations.add(loc)
                st.rerun()
        else:
            for ev in [e for e in case["evidence"] if e["location"] == loc]:
                st.session_state.evidence_found.add(ev["id"])
                st.markdown(f"""
                <div style="background: #1E1E24; border: 1px solid #4CAF7D; border-radius:4px; padding: 8px 12px; margin-bottom: 6px;">
                    <div style="font-family: 'Share Tech Mono', monospace; font-size:10px; color:#4CAF7D;">REVEALED // {loc.upper()}</div>
                    <div style="font-size:13px; font-weight:600; color:#E8E6DF;">{ev['name']}</div>
                    <div style="font-size:12px; color:#A1A1AA; line-height:1.4; margin-top:2px;">{ev['reveal_text']}</div>
                </div>
                """, unsafe_allow_html=True)

with col_right:
    # Suspect selection buttons rendered using dynamic tabs matching your front-end file layout
    sus_tabs = st.tabs([f"{s['emoji']} {s['name']}" for s in st.session_state.suspects])
    
    for idx, tab in enumerate(sus_tabs):
        with tab:
            st.session_state.active_suspect = idx
            suspect = st.session_state.suspects[idx]
            
            # Suspicion Level Bar Meter
            level = st.session_state.suspicion[idx]
            bar_color = "#E05C3A" if level >= 65 else ("#E8C547" if level >= 35 else "#4CAF7D")
            
            st.markdown(f"""
            <div style="display:flex; justify-content:space-between; font-family:'Share Tech Mono', monospace; font-size:11px; margin-top:8px;">
                <span style="color:#7A7870;">SUSPICION READOUT</span>
                <span style="color:{bar_color}; font-weight:700;">{level}%</span>
            </div>
            <div class="meter-track"><div class="meter-fill" style="width:{level}%; background:{bar_color};"></div></div>
            <div style="font-family:'Share Tech Mono', monospace; font-size:11px; color:#E8C547; margin-top:6px;">
                Questions Remaining: {suspect['questions_left']} / {MAX_QUESTIONS_PER_SUSPECT}
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Interrogation Transcript Container
            for turn in suspect["history"]:
                if turn["role"] == "user":
                    st.markdown(f'<div style="text-align: right; margin-bottom: 8px;"><span style="background: rgba(232,197,71,0.12); border: 1px solid rgba(232,197,71,0.2); border-radius: 4px; padding: 6px 12px; display: inline-block; max-width: 75%; font-size: 13px; text-align: left;">{turn["content"]}</span></div>', unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="margin-bottom: 12px;">
                        <div style="font-family: 'Share Tech Mono', monospace; font-size: 9px; color: #7A7870; margin-bottom: 2px;">{suspect['name'].upper()}</div>
                        <div style="background: #1E1E24; border: 1px solid #2A2A34; border-radius: 4px; padding: 8px 12px; font-size: 13px; line-height: 1.5;">{turn['content']}</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Input flow control mapping
            if suspect["questions_left"] <= 0:
                st.error("Question cap reached for this suspect. File an official accusation or turn to the alternative target profile.")
            else:
                user_query = st.chat_input(f"Question {suspect['name']}...", key=f"chat_input_{idx}")
                if user_query:
                    suspect["questions_left"] -= 1
                    suspect["history"].append({"role": "user", "content": user_query})
                    
                    # Logic Engine Call Wrapper
                    with st.spinner("Processing statement data..."):
                        client = get_client()
                        try:
                            # Build context arrays matching model schema expectations
                            facts_block = "\n".join(f"- {hf['fact']}" for hf in case["hard_facts"])
                            other_name = st.session_state.suspects[1 - idx]["name"]
                            
                            system_instruction = f"You are {suspect['name']}, {suspect['title']}. Investigated for killing {case['victim']}. "
                            if suspect["role"] == "innocent":
                                system_instruction += f"You are INNOCENT. Alibi (TRUE): {case['shared_alibi']} with {other_name}. Environmental realities:\n{facts_block}\nRespond consistently in 1-3 sentences."
                            else:
                                system_instruction += f"You are GUILTY. False Alibi: {case['shared_alibi']}. You don't know the layout facts:\n{facts_block}\nCONFABULATE fabricated physical sensory elements automatically when pushed. Respond in 1-3 sentences."
                            
                            history_contents = []
                            for h_turn in suspect["history"][:-1]:
                                h_role = "user" if h_turn["role"] == "user" else "model"
                                history_contents.append(types.Content(role=h_role, parts=[types.Part.from_text(text=h_turn["content"])]))
                                
                            chat = client.chats.create(
                                model=MODEL_NAME,
                                config=types.GenerateContentConfig(
                                    system_instruction=system_instruction,
                                    temperature=0.7,
                                    max_output_tokens=220
                                ),
                                history=history_contents
                            )
                            
                            response = chat.send_message(user_query)
                            reply_text = response.text.strip()
                            suspect["history"].append({"role": "model", "content": reply_text})
                            
                            # Real-time keyword dynamic scoring verification
                            if suspect["role"] == "guilty":
                                matched = False
                                for hf in case["hard_facts"]:
                                    for trigger in hf.get("contradiction_triggers", []):
                                        if trigger.lower() in reply_text.lower():
                                            st.session_state.suspicion[idx] = min(100, st.session_state.suspicion[idx] + 20)
                                            st.toast(f"🚨 Contradiction caught! Profile suspicion spiking.")
                                            matched = True
                                            break
                                if not matched:
                                    st.session_state.suspicion[idx] = min(100, st.session_state.suspicion[idx] + 2)
                            else:
                                st.session_state.suspicion[idx] = max(0, st.session_state.suspicion[idx] - 1)
                                
                            st.rerun()
                        except ClientError as e:
                            st.error(f"Inference pipeline rate limited or rejected. Details: {e}")

    # ------------------------------------------------------------------
    # ACCUSATION SUBMISSION BAR BLOCK
    # ------------------------------------------------------------------
    st.markdown("---")
    st.markdown("### 🔨 File Final Arrest Warrant")
    accuse_col1, accuse_col2 = st.columns(2)
    with accuse_col1:
        if st.button(f"Accuse {st.session_state.suspects[0]['name']}", use_container_width=True, type="primary"):
            st.session_state.verdict = 0
            st.rerun()
    with accuse_col2:
        if st.button(f"Accuse {st.session_state.suspects[1]['name']}", use_container_width=True, type="primary"):
            st.session_state.verdict = 1
            st.rerun()

# ------------------------------------------------------------------
# VERDICT SHEET MODAL LAYER OVERRIDE
# ------------------------------------------------------------------
if st.session_state.verdict is not None:
    chosen_idx = st.session_state.verdict
    guilty_idx = 0 if st.session_state.suspects[0]["role"] == "guilty" else 1
    success = (chosen_idx == guilty_idx)
    
    st.markdown("---")
    if success:
        st.markdown('<div class="stamp-win">CASE RESOLVED // CLOSED</div>', unsafe_allow_html=True)
        st.success(f"Excellent work, detective! **{st.session_state.suspects[chosen_idx]['name']}** cracked under pressure. Your accusation was completely correct.")
    else:
        st.markdown('<div class="stamp-lose">CASE FILED // FAILED</div>', unsafe_allow_html=True)
        st.error(f"Case bungled. You arrested an innocent civilian. The actual killer walked away free.")
        
    if st.button("Initialize New Investigation Assignment", type="secondary"):
        new_case()
        st.rerun()