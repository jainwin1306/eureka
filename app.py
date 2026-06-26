import google.generativeai as genai
import streamlit as st

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.0-flash")

st.set_page_config(page_title="Percival", page_icon="⚔️", layout="centered")

st.markdown("""
<style>
.stChatMessage { border-radius: 12px; padding: 4px; }
.stChatInput input { border-radius: 20px; }
header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

st.markdown("# ⚔️ PERCIVAL")
st.markdown("### *Your personal college assistant*")
st.markdown("---")

tool = st.selectbox("What do you need?", [
    "📝 Assignment Breaker",
    "📚 Study Summariser",
    "🔍 Research Assistant",
    "✍️ Essay Reviewer",
    "🧠 Quiz Me"
])

if tool == "📝 Assignment Breaker":
    brief = st.text_area("Paste your assignment brief:")
    if st.button("Break it down"):
        with st.spinner("Thinking..."):
            prompt = f"""You are an academic strategist. Analyze this assignment brief and return EXACTLY this structure:

WHAT THIS IS REALLY ASKING (one sentence):
OUTLINE (3-4 bullet points):
KEY ARGUMENTS TO MAKE:
WHAT TO RESEARCH (3 specific things):
COMMON MISTAKE TO AVOID:
FIRST SENTENCE TO GET YOU STARTED:

Brief: {brief}"""
            st.write(model.generate_content(prompt).text)

elif tool == "📚 Study Summariser":
    notes = st.text_area("Paste your notes or textbook section:")
    if st.button("Summarise"):
        with st.spinner("Summarising..."):
            prompt = f"""You are an academic summariser. Return EXACTLY this structure:

CORE CONCEPT (one sentence):
5 POINT SUMMARY:
3 LIKELY EXAM QUESTIONS:
ONE THING MOST STUDENTS MISS:

Notes: {notes}"""
            st.write(model.generate_content(prompt).text)

elif tool == "🔍 Research Assistant":
    topic = st.text_area("What topic do you need to research?")
    if st.button("Find angles"):
        with st.spinner("Researching..."):
            prompt = f"""You are a research strategist. Return EXACTLY this structure:

THE MOST INTERESTING ANGLE ON THIS TOPIC:
3 ARGUMENTS FOR:
3 ARGUMENTS AGAINST:
3 SPECIFIC THINGS TO GOOGLE:
ONE EXPERT OR SOURCE TO LOOK UP:

Topic: {topic}"""
            st.write(model.generate_content(prompt).text)

elif tool == "✍️ Essay Reviewer":
    essay = st.text_area("Paste your essay or draft:")
    if st.button("Review it"):
        with st.spinner("Reviewing..."):
            prompt = f"""You are a strict but fair professor. Review this essay and return EXACTLY this structure:

OVERALL VERDICT (one sentence):
STRONGEST PART:
WEAKEST PART:
3 SPECIFIC IMPROVEMENTS:
GRADE IF SUBMITTED NOW (A/B/C/D and why):

Essay: {essay}"""
            st.write(model.generate_content(prompt).text)

elif tool == "🧠 Quiz Me":
    topic = st.text_area("What topic or notes should I quiz you on?")
    num_questions = st.slider("How many questions?", 3, 10, 5)
    
    if "quiz" not in st.session_state:
        st.session_state.quiz = None
        st.session_state.answers = {}
        st.session_state.submitted = False

    if st.button("Generate Quiz"):
        with st.spinner("Creating your quiz..."):
            prompt = f"""Create a quiz with exactly {num_questions} questions on this topic.

Format EXACTLY like this for each question:
Q1: [question]
A) [option]
B) [option]
C) [option]
D) [option]
ANSWER: [correct letter]

Topic: {topic}"""
            st.session_state.quiz = model.generate_content(prompt).text
            st.session_state.answers = {}
            st.session_state.submitted = False

    if st.session_state.quiz:
        st.markdown("---")
        st.markdown("### Your Quiz")
        st.write(st.session_state.quiz)
        
        st.markdown("---")
        user_answers = st.text_input("Type your answers in order (e.g. A,B,C,D,A):")
        
        if st.button("Submit Answers"):
            with st.spinner("Marking..."):
                prompt = f"""Here is a quiz and the student's answers. Mark them and give feedback.

Quiz:
{st.session_state.quiz}

Student answers (in order): {user_answers}

Return EXACTLY this structure:
SCORE: [X out of {num_questions}]
BREAKDOWN: (go through each question, say if correct or wrong and why)
WHAT TO REVIEW:"""
                st.write(model.generate_content(prompt).text)
