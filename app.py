import google.generativeai as genai
import streamlit as st

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash")

st.set_page_config(page_title="Eureka", page_icon="⚡", layout="centered")

st.markdown("""
<style>
.stChatMessage { border-radius: 12px; padding: 4px; }
.stChatInput input { border-radius: 20px; }
header { visibility: hidden; }
.advisor-card {
    padding: 16px;
    border-radius: 12px;
    margin: 8px 0;
    border-left: 4px solid;
}
</style>
""", unsafe_allow_html=True)

st.markdown("# ⚡ EUREKA")
st.markdown("### *Pitch your idea. Three voices. No filter.*")
st.markdown("---")

ADVISORS = {
    "🦈 Shark": {
        "color": "#FF4444",
        "prompt": """You are Shark, a ruthless venture capitalist who has seen 1000 pitches and funded 5.
You are brutally honest, hate buzzwords, and only care about money and defensibility.
Rules: One sharp question or comment at a time. Under 80 words. No encouragement unless truly earned. Talk like a real person, not a report."""
    },
    "🎖️ Uncle Sam": {
        "color": "#F5A623", 
        "prompt": """You are Uncle Sam, a warm but sharp startup coach who genuinely wants founders to succeed.
You find real strengths others miss, but you're not a yes-man — you push founders to think bigger.
Rules: One question or insight at a time. Under 80 words. Be human, warm, and specific. No bullet points."""
    },
    "❄️ Jon Snow": {
        "color": "#4A9EFF",
        "prompt": """You are Jon Snow, an everyday person who knows nothing about startups but knows exactly what he'd pay for and use.
You speak for the average customer — skeptical, practical, and honest about what actually matters to real people.
Rules: One reaction or question at a time. Under 80 words. Be real, casual, and specific."""
    }
}

if "histories" not in st.session_state:
    st.session_state.histories = {
        name: [
            {"role": "user", "parts": [data["prompt"]]},
            {"role": "model", "parts": ["Understood. Ready."]}
        ]
        for name, data in ADVISORS.items()
    }
    st.session_state.messages = []
    st.session_state.started = False

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("🦈 **Shark**\n\nThe ruthless investor")
with col2:
    st.markdown("🎖️ **Uncle Sam**\n\nThe startup coach")
with col3:
    st.markdown("❄️ **Jon Snow**\n\nThe real customer")

st.markdown("---")

if not st.session_state.started:
    st.markdown("**Describe your startup idea below and all three will respond.**")

for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.write(message["content"])
    else:
        name = message["advisor"]
        color = ADVISORS[name]["color"]
        with st.chat_message("assistant"):
            st.markdown(f"<span style='color:{color}; font-weight:bold'>{name}</span>", unsafe_allow_html=True)
            st.write(message["content"])

if prompt := st.chat_input("Pitch your idea..."):
    st.session_state.started = True
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.write(prompt)

    for name, data in ADVISORS.items():
        st.session_state.histories[name].append({"role": "user", "parts": [prompt]})
        
        chat = model.start_chat(history=st.session_state.histories[name])
        response =
