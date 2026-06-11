import streamlit as st
from chatbot import (
    get_career_advice,
    analyze_resume,
    analyze_resume_and_generate_questions,
    generate_interview_questions,
    generate_hr_questions_from_resume,
    generate_roadmap
)

st.set_page_config(
    page_title="Career Advisor Chatbot",
    page_icon="💼",
    layout="wide"
)

# --------------------
# CSS
# --------------------
st.markdown("""
<style>
.stApp {
    background: #020817;
}
.main-title {
    text-align: center;
    font-size: 60px;
    font-weight: 700;
    color: white;
}
.sub-title {
    text-align: center;
    color: #94a3b8;
    font-size: 24px;
    margin-bottom: 30px;
}
.block-container {
    padding-top: 1rem;
}
.stButton button {
    width: 100%;
    border-radius: 12px;
    padding: 12px;
    margin-bottom: 10px;
}
.welcome-card {
    background: #071327;
    border: 1px solid #23314f;
    padding: 30px;
    border-radius: 20px;
}
.feature-card {
    background: #071327;
    border: 1px solid #23314f;
    padding: 24px;
    border-radius: 16px;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# --------------------
# Session State
# --------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Chat"

# --------------------
# Sidebar
# --------------------
with st.sidebar:

    st.markdown("# 💼 CareerBot")
    st.write("Your AI-powered career guidance companion")
    st.divider()

    st.subheader("🔧 Features")

    if st.button("💬 Career Chat"):
        st.session_state.active_tab = "Chat"
        st.rerun()

    if st.button("📄 Resume Analyzer"):
        st.session_state.active_tab = "Resume"
        st.rerun()

    if st.button("🎯 Interview Prep"):
        st.session_state.active_tab = "Interview"
        st.rerun()

    if st.button("🗺️ Roadmap Generator"):
        st.session_state.active_tab = "Roadmap"
        st.rerun()

    st.divider()

    if st.session_state.active_tab == "Chat":
        st.subheader("💡 Try asking:")
        questions = [
            "How do I write a resume with no experience?",
            "How should I answer 'Tell me about yourself'?",
            "What skills do I need for a Data Science role?",
            "How do I negotiate a salary offer?",
            "How do I switch careers into tech?"
        ]
        for q in questions:
            if st.button(q):
                st.session_state.messages.append({
                    "role": "user",
                    "content": q
                })
                answer = get_career_advice(q)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })
                st.rerun()

    st.divider()

    if st.button("🗑 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# --------------------
# Header
# --------------------
st.markdown(
    '<div class="main-title">💼 Career Advisor Chatbot</div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="sub-title">Your AI-powered career guidance companion</div>',
    unsafe_allow_html=True
)

# --------------------
# Tab: Career Chat
# --------------------
if st.session_state.active_tab == "Chat":

    if len(st.session_state.messages) == 0:
        st.markdown("""
        <div class="welcome-card">
        <h2>👋 Hi! I'm CareerBot, your AI-powered career advisor.</h2>
        I can help you with:
        <ul>
        <li>📄 Resume writing & optimization</li>
        <li>🎯 Interview preparation</li>
        <li>🗺 Career path planning</li>
        <li>💡 Skill gap analysis & upskilling</li>
        <li>💰 Salary negotiation tips</li>
        </ul>
        <b>What career challenge can I help you with today?</b>
        </div>
        """, unsafe_allow_html=True)

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    prompt = st.chat_input("Ask me anything about your career...")

    if prompt:
        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })

        with st.spinner("Analyzing career opportunities..."):
            answer = get_career_advice(prompt)

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })

        st.rerun()

# --------------------
# Tab: Resume Analyzer
# --------------------
elif st.session_state.active_tab == "Resume":

    st.markdown("## 📄 Resume Analyzer")
    st.write("Upload your resume to get feedback, technical interview questions, and HR interview questions.")

    st.markdown('<div class="feature-card">', unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload your resume (PDF only)",
        type=["pdf"]
    )

    if uploaded_file:
        st.success(f"✅ File uploaded: {uploaded_file.name}")

        col1, col2, col3 = st.columns(3)

        with col1:
            analyze_btn = st.button("🔍 Analyze Resume + Technical Questions")

        with col2:
            hr_btn = st.button("🤝 Generate HR Interview Questions")

        with col3:
            all_btn = st.button("⚡ Generate Everything at Once")

        # ---------- Analyze Resume + Technical Questions ----------
        if analyze_btn:
            with st.spinner("Analyzing resume and generating technical questions..."):
                resume_feedback, interview_questions, error = analyze_resume_and_generate_questions(uploaded_file)

            if error:
                st.error(error)
            else:
                st.markdown("---")
                st.markdown("### 📊 Resume Feedback")
                st.markdown(resume_feedback)
                st.download_button(
                    label="📥 Download Resume Feedback",
                    data=resume_feedback,
                    file_name="resume_feedback.txt",
                    mime="text/plain",
                    key="dl_feedback"
                )

                st.markdown("---")
                st.markdown("### 🎯 Technical Interview Questions Based on Your Resume")
                st.info("Questions generated from your actual skills, projects, and experience.")
                st.markdown(interview_questions)
                st.download_button(
                    label="📥 Download Technical Questions",
                    data=interview_questions,
                    file_name="technical_interview_questions.txt",
                    mime="text/plain",
                    key="dl_technical"
                )

        # ---------- HR Interview Questions ----------
        if hr_btn:
            with st.spinner("Generating HR interview questions from your resume..."):
                hr_questions, error = generate_hr_questions_from_resume(uploaded_file)

            if error:
                st.error(error)
            else:
                st.markdown("---")
                st.markdown("### 🤝 HR Interview Questions Based on Your Resume")
                st.info("These HR questions are personalized based on your background, goals, and experience.")
                st.markdown(hr_questions)
                st.download_button(
                    label="📥 Download HR Questions",
                    data=hr_questions,
                    file_name="hr_interview_questions.txt",
                    mime="text/plain",
                    key="dl_hr"
                )

        # ---------- Generate Everything at Once ----------
        if all_btn:
            with st.spinner("Generating complete interview preparation pack..."):
                resume_feedback, interview_questions, error1 = analyze_resume_and_generate_questions(uploaded_file)
                hr_questions, error2 = generate_hr_questions_from_resume(uploaded_file)

            if error1 or error2:
                st.error(error1 or error2)
            else:
                st.markdown("---")
                st.markdown("### 📊 Resume Feedback")
                st.markdown(resume_feedback)
                st.download_button(
                    label="📥 Download Resume Feedback",
                    data=resume_feedback,
                    file_name="resume_feedback.txt",
                    mime="text/plain",
                    key="dl_all_feedback"
                )

                st.markdown("---")
                st.markdown("### 🎯 Technical Interview Questions")
                st.info("Questions generated from your actual skills, projects, and experience.")
                st.markdown(interview_questions)
                st.download_button(
                    label="📥 Download Technical Questions",
                    data=interview_questions,
                    file_name="technical_interview_questions.txt",
                    mime="text/plain",
                    key="dl_all_technical"
                )

                st.markdown("---")
                st.markdown("### 🤝 HR Interview Questions")
                st.info("Personalized HR questions based on your background and career goals.")
                st.markdown(hr_questions)
                st.download_button(
                    label="📥 Download HR Questions",
                    data=hr_questions,
                    file_name="hr_interview_questions.txt",
                    mime="text/plain",
                    key="dl_all_hr"
                )

                st.markdown("---")
                combined = f"RESUME FEEDBACK\n{'='*50}\n{resume_feedback}\n\nTECHNICAL INTERVIEW QUESTIONS\n{'='*50}\n{interview_questions}\n\nHR INTERVIEW QUESTIONS\n{'='*50}\n{hr_questions}"
                st.download_button(
                    label="📥 Download Complete Interview Pack",
                    data=combined,
                    file_name="complete_interview_pack.txt",
                    mime="text/plain",
                    key="dl_all_combined"
                )

    st.markdown('</div>', unsafe_allow_html=True)

# --------------------
# Tab: Interview Prep
# --------------------
elif st.session_state.active_tab == "Interview":

    st.markdown("## 🎯 Interview Question Generator")
    st.write("Select a job role and get tailored interview questions with expected answers.")

    st.markdown('<div class="feature-card">', unsafe_allow_html=True)

    job_roles = [
        "Data Scientist",
        "Machine Learning Engineer",
        "AI Engineer",
        "Data Analyst",
        "Python Developer",
        "Backend Developer",
        "Frontend Developer",
        "Full Stack Developer",
        "DevOps Engineer",
        "Business Analyst"
    ]

    col1, col2 = st.columns([2, 1])

    with col1:
        selected_role = st.selectbox("Select Job Role", job_roles)

    with col2:
        custom_role = st.text_input("Or enter custom role")

    final_role = custom_role.strip() if custom_role.strip() else selected_role

    if st.button("🎯 Generate Interview Questions"):
        with st.spinner(f"Generating questions for {final_role}..."):
            result = generate_interview_questions(final_role)

        st.markdown(f"### 📋 Interview Questions for {final_role}")
        st.markdown(result)

        st.download_button(
            label="📥 Download Questions",
            data=result,
            file_name=f"{final_role}_interview_questions.txt",
            mime="text/plain"
        )

    st.markdown('</div>', unsafe_allow_html=True)

# --------------------
# Tab: Roadmap Generator
# --------------------
elif st.session_state.active_tab == "Roadmap":

    st.markdown("## 🗺️ Learning Roadmap Generator")
    st.write("Enter your career goal and timeframe to get a personalized week-by-week roadmap.")

    st.markdown('<div class="feature-card">', unsafe_allow_html=True)

    goal = st.text_input(
        "What is your career goal?",
        placeholder="e.g. Become a Machine Learning Engineer"
    )

    timeframe = st.selectbox(
        "Timeframe",
        ["1 month", "2 months", "3 months", "6 months", "1 year"]
    )

    if st.button("🗺️ Generate Roadmap"):
        if not goal.strip():
            st.warning("Please enter your career goal.")
        else:
            with st.spinner("Building your personalized roadmap..."):
                result = generate_roadmap(goal, timeframe)

            st.markdown(f"### 📍 Your Roadmap: {goal} in {timeframe}")
            st.markdown(result)

            st.download_button(
                label="📥 Download Roadmap",
                data=result,
                file_name="career_roadmap.txt",
                mime="text/plain"
            )

    st.markdown('</div>', unsafe_allow_html=True)