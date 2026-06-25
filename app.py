import google.generativeai as genai
import streamlit as st

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash")

def pitch_analyzer(idea):
    prompt = f"""You are a startup analysis tool. Analyze this business idea and return EXACTLY this structure:

INVESTOR VERDICT (50 words max - brutal and specific):
[your response]

COACH TAKE (50 words max - find real strengths):
[your response]

CUSTOMER REACTION (50 words max - honest skepticism):
[your response]

SCORE: [X/10]

SCORE REASONING (one sentence):
[your response]

ONE THING THAT WOULD MAKE THIS FUNDABLE:
[your response]

Idea: {idea}"""
    return model.generate_content(prompt).text

def assignment_shortcut(brief):
    prompt = f"""You are an academic strategist. Analyze this assignment brief and return EXACTLY this structure:

WHAT THIS ASSIGNMENT IS REALLY ASKING (one sentence):
[your response]

OUTLINE (3-4 bullet points):
[your response]

KEY ARGUMENTS TO MAKE:
[your response]

WHAT TO RESEARCH (3 specific things):
[your response]

COMMON MISTAKE TO AVOID:
[your response]

FIRST SENTENCE TO GET YOU STARTED:
[your response]

Assignment Brief: {brief}"""
    return model.generate_content(prompt).text

# UI
st.title("⚡ EUREKA by Advit")
st.markdown("Your personal AI toolkit.")

tool = st.selectbox("What do you want to do?", ["Analyze a business idea", "Break down an assignment"])

if tool == "Analyze a business idea":
    idea = st.text_area("Enter your business idea:")
    if st.button("Analyze"):
        with st.spinner("Thinking..."):
            st.write(pitch_analyzer(idea))

elif tool == "Break down an assignment":
    brief = st.text_area("Paste your assignment brief:")
    if st.button("Break it down"):
        with st.spinner("Thinking..."):
            st.write(assignment_shortcut(brief))
