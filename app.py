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
</style>
""", unsafe_allow_html=True)

st.markdown("# ⚡ EUREKA")
st.markdown("### *Pitch your idea. Three voices. No filter.*")
st.markdown("---")

ADVISORS = {
    "🦈 Shark": {
        "color": "#FF4444",
        "prompt": "You are Shark, a ruthless venture capitalist who has seen 1000 pitches and funded 5. You are brutally honest, hate buzzwords, and only care about money and defensibility. Rules: One sharp question or comment at a time. Under 80 words. No encouragement unless truly earned. Talk like a real person."
    },
    "🎖️ Uncle Sam": {
        "color": "#FF6B6B",
        "prompt": "You are Uncle Sam, a warm but sharp startup coach who genuinely wants founders to succeed. You find real strengths others miss, but you are not a yes-man. Rules: One question or insight at a time. Under 80 words. Be human, warm, and specific. No bullet points."
    },
    "❄️ Jon Snow": {
        "color": "#8B7355",
        "prompt": "You are Jon Snow, an everyday person who knows nothing about startups but knows exactly what he would pay for. You speak for the average customer, skeptical and practical. Rules: One reaction or question at a time. Under 80 words. Be real and casual."
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

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("🦈 **Shark**\nThe ruthless investor")
with col2:
    st.markdown("🎖️ **Uncle Sam**\nThe startup coach")
with col3:
    st.markdown("❄️ **Jon Snow**\nThe real customer")

st.markdown("---")

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
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    for name, data in ADVISORS.items():
        st.session_state.histories[name].append({"role": "user", "parts": [prompt]})
        chat = model.start_chat(history=st.session_state.histories[name])
        response = chat.send_message(prompt)
        reply = response.text
        st.session_state.histories[name].append({"role": "model", "parts": [reply]})
        st.session_state.messages.append({"role": "assistant", "advisor": name, "content": reply})
        with st.chat_message("assistant"):
            st.markdown(f"<span style='color:{color}; font-weight:bold'>{name}</span>", unsafe_allow_html=True)
            st.write(reply)
