import streamlit as st
from datetime import datetime
from zoneinfo import ZoneInfo

from database import (
    sign_up,
    sign_in,
    sign_out,
    save_analysis_history,
    get_analysis_history,
    delete_analysis_history,
    delete_all_analysis_history
) 
from pdf_utils import ( 
    extract_text_from_pdf,
    create_pdf_report
)
from ai_service import (
   analyze_resume,
   match_job,
   generate_interview_questions)


# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Placement Coach",
    page_icon="🎓",
    layout="wide"
)


# -----------------------------
# Custom CSS
# -----------------------------
st.markdown(
    """
    <style>
    /* Base layout */
    .stApp {
        background: var(--background-color);
        color: var(--text-color);
    }

    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: 800;
        color: var(--text-color);
        margin-top: 20px;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        color: var(--text-color);
        opacity: 0.8;
        margin-bottom: 30px;
    }

    /* Cards */
    .card, .feature-card {
        background: var(--secondary-background-color);
        color: var(--text-color);
        padding: 25px;
        border-radius: 18px;
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.12);
        margin-bottom: 20px;
    }

    .feature-card {
        text-align: center;
    }

    .feature-icon {
        font-size: 35px;
    }

    .feature-title {
        font-size: 20px;
        font-weight: 700;
        color: var(--text-color);
    }

    /* Input fields */
    div[data-testid="stTextInput"] input,
    div[data-testid="stTextArea"] textarea {
        color: var(--text-color);
        background: var(--secondary-background-color);
        border-radius: 10px;
    }

    /* Buttons */
    div.stButton > button {
        width: 100%;
        border-radius: 10px;
        min-height: 45px;
        font-weight: 600;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: var(--secondary-background-color);
    }

    /* Tables and result text */
    [data-testid="stMarkdownContainer"] {
        color: var(--text-color);
    }

    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# Session State
# -----------------------------
if "user" not in st.session_state:
    st.session_state.user = None

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None


# =========================================================
# LOGIN / SIGNUP
# =========================================================

if st.session_state.user is None:

    st.markdown(
        '<div class="main-title">🎓 Placement Coach</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">AI Resume & Interview Hub</div>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="card">', unsafe_allow_html=True)

    login_tab, signup_tab = st.tabs(
        ["🔐 Login", "📝 Sign Up"]
    )

    # -------------------------
    # Login
    # -------------------------
    with login_tab:

        st.subheader("Welcome Back")

        email = st.text_input(
            "Email",
            placeholder="Enter your email",
            key="login_email"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
            key="login_password"
        )

        if st.button(
            "Login",
            key="login_button"
        ):

            if not email or not password:

                st.warning(
                    "Please enter email and password."
                )

            else:

                try:

                    response = sign_in(
                        email,
                        password
                    )

                    if response.user:

                        st.session_state.user = response.user

                        st.success(
                            "Login successful!"
                        )

                        st.rerun()

                except Exception as e:

                    st.error(
                        f"Login failed: {e}"
                    )

    # -------------------------
    # Signup
    # -------------------------
    with signup_tab:

        st.subheader("Create Your Account")

        signup_email = st.text_input(
            "Email",
            placeholder="Enter your email",
            key="signup_email"
        )

        signup_password = st.text_input(
            "Password",
            type="password",
            placeholder="Create a password",
            key="signup_password"
        )

        signup_confirm = st.text_input(
            "Confirm Password",
            type="password",
            placeholder="Confirm your password",
            key="signup_confirm"
        )

        if st.button(
            "Create Account",
            key="signup_button"
        ):

            if not signup_email or not signup_password:

                st.warning(
                    "Please fill all required fields."
                )

            elif signup_password != signup_confirm:

                st.error(
                    "Passwords do not match."
                )

            elif len(signup_password) < 6:

                st.error(
                    "Password must contain at least 6 characters."
                )

            else:

                try:

                    response = sign_up(
                        signup_email,
                        signup_password
                    )

                    if response.user:

                        st.success(
                            "Account created successfully! "
                            "You can now login."
                        )

                except Exception as e:

                    st.error(
                        f"Signup failed: {e}"
                    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )

    st.info(
        "🤖 AI Powered Placement Assistant\n\n"
        "Analyze your resume, match jobs and "
        "prepare for interviews with AI."
    )


# =========================================================
# DASHBOARD
# =========================================================

else:

    user = st.session_state.user

    # -------------------------
    # Header
    # -------------------------

    st.markdown(
        '<div class="main-title">🎓 Placement Coach</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Your AI Placement Dashboard</div>',
        unsafe_allow_html=True
    )

    # -------------------------
    # Sidebar
    # -------------------------

    with st.sidebar:

        st.title("🎓 Placement Coach")

        st.write(
            f"👤 {user.email}"
        )

        st.divider()

        menu = st.radio(
            "Navigation",
            [
                "🏠 Dashboard",
                "📄 Resume Analysis",
                "🎯 Job Matching",
                "💼 Interview Preparation",
                "📜 History"
            ]
        )

        st.divider()

        if st.button(
            "Logout",
            key="logout_button"
        ):

            try:
                sign_out()
            except Exception:
                pass

            st.session_state.user = None
            st.session_state.analysis_result = None

            st.rerun()


    # =====================================================
    # DASHBOARD HOME
    # =====================================================

    if menu == "🏠 Dashboard":

        st.subheader("Welcome to your Dashboard 👋")

        st.write(
            "Improve your resume and prepare for your placement "
            "with AI-powered tools."
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.markdown(
                """
                <div class="feature-card">
                    <div class="feature-icon">📄</div>
                    <div class="feature-title">
                        Resume Analysis
                    </div>
                    <p>
                        Get AI-powered resume feedback.
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:

            st.markdown(
                """
                <div class="feature-card">
                    <div class="feature-icon">🎯</div>
                    <div class="feature-title">
                        Job Matching
                    </div>
                    <p>
                        Compare your resume with a job.
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col3:

            st.markdown(
                """
                <div class="feature-card">
                    <div class="feature-icon">💼</div>
                    <div class="feature-title">
                        Interview Prep
                    </div>
                    <p>
                        Practice AI-generated questions.
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )


    # =====================================================
    # RESUME ANALYSIS
    # =====================================================

    elif menu == "📄 Resume Analysis":

        st.subheader("📄 AI Resume Analysis")

        st.write(
            "Upload your resume and enter the target job "
            "description to get detailed AI feedback."
        )

        # ---------------------------------------------
        # INPUT SECTION
        # ---------------------------------------------

        with st.container(border=True):

            resume_file = st.file_uploader(
                "📄 Upload Resume PDF",
                type=["pdf"],
                key="resume_analysis_file"
            )

            job_description = st.text_area(
                "💼 Target Job Description",
                placeholder=(
                    "Paste the complete job description here..."
                ),
                height=200,
                key="resume_job_description"
            )

            analyze_button = st.button(
                "🤖 Analyze Resume",
                key="analyze_resume_button"
            )

        # ---------------------------------------------
        # AI ANALYSIS
        # ---------------------------------------------

        if analyze_button:

            if resume_file is None:

                st.warning(
                    "⚠️ Please upload your resume PDF."
                )

            elif not job_description.strip():

                st.warning(
                    "⚠️ Please enter the target job description."
                )

            else:

                try:

                    with st.spinner(
                        "🤖 AI is analyzing your resume..."
                    ):

                        resume_text = extract_text_from_pdf(
                            resume_file
                        )

                        result = analyze_resume(
                            resume_text,
                            job_description
                        )

                        st.session_state.analysis_result = result

                        # Save analysis to user history
                        if st.session_state.user:
                            save_analysis_history(
                               st.session_state.user.id,
                               "Resume Analysis",
                                result
                                 )

                    st.success(
                        "✅ Resume analysis completed!"
                    )

                except Exception as e:

                    st.error(
                        f"❌ Analysis failed: {e}"
                    )

        # ---------------------------------------------
        # AI ANALYSIS RESULT
        # ---------------------------------------------

        if st.session_state.analysis_result:

            st.divider()

            st.subheader("📊 AI Resume Analysis")

            result = st.session_state.analysis_result

            # Clean unwanted HTML
            result = (
                result
                .replace("<br>", "\n")
                .replace("<br/>", "\n")
                .replace("<br />", "\n")
            )

            # -----------------------------------------
            # PARSE AI RESPONSE
            # -----------------------------------------

            sections = {}
            current_section = None

            for line in result.splitlines():

                line = line.strip()

                if not line:
                    continue

                if line.startswith("# "):
                    continue

                if line.startswith("## "):

                    current_section = (
                        line.replace("## ", "").strip()
                    )

                    sections[current_section] = []

                elif current_section:

                    sections[current_section].append(line)

            # -----------------------------------------
            # SCORE CARDS
            # -----------------------------------------

            score1 = sections.get(
                "📊 Overall Resume Score",
                []
            )

            score2 = sections.get(
                "🎯 ATS Score",
                []
            )

            score_value = (
                score1[0]
                if score1
                else "N/A"
            )

            ats_value = (
                score2[0]
                if score2
                else "N/A"
            )

            col1, col2 = st.columns(2)

            with col1:

                with st.container(border=True):

                    st.markdown("### 📊 Resume Score")

                    st.metric(
                        label="Overall Score",
                        value=score_value
                    )

                    st.caption(
                        "Overall quality of your resume"
                    )

            with col2:

                with st.container(border=True):

                    st.markdown("### 🎯 ATS Score")

                    st.metric(
                        label="ATS Compatibility",
                        value=ats_value
                    )

                    st.caption(
                        "How well your resume matches ATS systems"
                    )

            st.write("")

            # -----------------------------------------
            # SKILLS
            # -----------------------------------------

            col1, col2 = st.columns(2)

            with col1:

                with st.container(border=True):

                    st.markdown("### 💪 Strong Skills")

                    skills = sections.get(
                        "💪 Strong Skills",
                        []
                    )

                    if skills:

                        for item in skills:
                            st.markdown(item)

                    else:

                        st.info(
                            "No strong skills found."
                        )

            with col2:

                with st.container(border=True):

                    st.markdown("### ❌ Missing Skills")

                    skills = sections.get(
                        "❌ Missing Skills",
                        []
                    )

                    if skills:

                        for item in skills:
                            st.markdown(item)

                    else:

                        st.info(
                            "No missing skills found."
                        )

            st.write("")

            # -----------------------------------------
            # MISSING KEYWORDS
            # -----------------------------------------

            with st.container(border=True):

                st.markdown("### 🔑 Missing Keywords")

                keywords = sections.get(
                    "🔑 Missing Keywords",
                    []
                )

                if keywords:

                    for item in keywords:
                        st.markdown(item)

                else:

                    st.info(
                        "No missing keywords found."
                    )

            st.write("")

            # -----------------------------------------
            # WEAK AREAS
            # -----------------------------------------

            with st.container(border=True):

                st.markdown("### ⚠️ Areas to Improve")

                weak_areas = sections.get(
                    "⚠️ Weak Areas",
                    []
                )

                if weak_areas:

                    for item in weak_areas:
                        st.markdown(item)

                else:

                    st.info(
                        "No major weak areas found."
                    )

            st.write("")

            # -----------------------------------------
            # SUGGESTIONS
            # -----------------------------------------

            with st.container(border=True):

                st.markdown("### 💡 Suggestions to Improve")

                suggestions = sections.get(
                    "💡 Suggestions to Improve",
                    []
                )

                if suggestions:

                    for item in suggestions:
                        st.markdown(item)

                else:

                    st.info(
                        "No suggestions available."
                    )

            st.write("")

            # -----------------------------------------
            # FINAL RECOMMENDATION
            # -----------------------------------------

            with st.container(border=True):

                st.markdown(
                    "### ✅ Final Recommendation"
                )

                recommendation = sections.get(
                    "✅ Final Recommendation",
                    []
                )

                if recommendation:

                    for item in recommendation:
                        st.markdown(item)

                else:

                    st.info(
                        "No final recommendation available."
                    )

            st.write("")

            # -----------------------------------------
            # DOWNLOAD RESUME ANALYSIS PDF
            # -----------------------------------------

            st.write("")

            with st.container(border=True):

                st.markdown("### 📥 Download Report")

                try:

                    pdf_file = create_pdf_report(
                        "Placement Coach - Resume Analysis",
                        st.session_state.analysis_result
                    )

                    st.download_button(
                        label="📥 Download Resume Analysis PDF",
                        data=pdf_file.getvalue(),
                        file_name="Placement_Coach_Resume_Analysis.pdf",
                        mime="application/pdf",
                        key="download_resume_analysis_pdf"
                    )

                except Exception as e:

                    st.error(
                        f"❌ PDF generation failed: {e}"
                    )


            # =====================================================
    # JOB MATCHING
    # =====================================================

    elif menu == "🎯 Job Matching":

        st.subheader("🎯 AI Job Matching")

        st.write(
            "Upload your resume and enter a target job description "
            "to check how well your profile matches the job."
        )

        with st.container(border=True):

            resume_file = st.file_uploader(
                "📄 Upload Resume PDF",
                type=["pdf"],
                key="job_match_resume"
            )

            job_description = st.text_area(
                "💼 Target Job Description",
                placeholder="Paste the complete job description here...",
                height=220,
                key="job_match_description"
            )

            match_button = st.button(
                "🎯 Analyze Job Match",
                key="job_match_button"
            )

        if match_button:

            if resume_file is None:
                st.warning("⚠️ Please upload your resume PDF.")

            elif not job_description.strip():
                st.warning("⚠️ Please enter the target job description.")

            else:

                try:

                    with st.spinner("🤖 AI is analyzing your job match..."):

                        resume_text = extract_text_from_pdf(
                            resume_file
                        )

                        result = match_job(
                            resume_text,
                            job_description
                        )

                        st.session_state.job_match_result = result
                        # Save job matching to user history
                        if st.session_state.user:
                            save_analysis_history(
                                st.session_state.user.id,
                                 "Job Matching",
                                 result
                            )

                    st.success("✅ Job matching completed!")

                except Exception as e:

                    st.error(
                        f"❌ Job matching failed: {e}"
                    )

        # ---------------------------------------------
        # JOB MATCH RESULT
        # ---------------------------------------------

        if st.session_state.get("job_match_result"):

            st.divider()

            st.subheader("📊 Job Match Analysis")

            result = st.session_state.job_match_result

            result = (
                result
                .replace("<br>", "\n")
                .replace("<br/>", "\n")
                .replace("<br />", "\n")
            )

            sections = {}
            current_section = None

            for line in result.splitlines():

                line = line.strip()

                if not line:
                    continue

                if line.startswith("# "):
                    continue

                if line.startswith("## "):

                    current_section = (
                        line.replace("## ", "").strip()
                    )

                    sections[current_section] = []

                elif current_section:

                    sections[current_section].append(line)

            # ---------------------------------------------
            # JOB MATCH SCORE
            # ---------------------------------------------

            score = sections.get(
                "🎯 Job Match Score",
                []
            )

            score_value = (
                score[0]
                if score
                else "N/A"
            )

            with st.container(border=True):

                st.markdown("### 🎯 Job Match Score")

                st.metric(
                    label="Resume ↔ Job Match",
                    value=score_value
                )

            st.write("")

            # ---------------------------------------------
            # MATCHING + MISSING SKILLS
            # ---------------------------------------------

            col1, col2 = st.columns(2)

            with col1:

                with st.container(border=True):

                    st.markdown("### 💪 Matching Skills")

                    for item in sections.get(
                        "💪 Matching Skills",
                        ["No matching skills found."]
                    ):

                        st.markdown(item)

            with col2:

                with st.container(border=True):

                    st.markdown("### ❌ Missing Skills")

                    for item in sections.get(
                        "❌ Missing Skills",
                        ["No missing skills found."]
                    ):

                        st.markdown(item)

            st.write("")

            # ---------------------------------------------
            # KEYWORDS
            # ---------------------------------------------

            col1, col2 = st.columns(2)

            with col1:

                with st.container(border=True):

                    st.markdown("### 🔑 Matching Keywords")

                    for item in sections.get(
                        "🔑 Matching Keywords",
                        ["No matching keywords found."]
                    ):

                        st.markdown(item)

            with col2:

                with st.container(border=True):

                    st.markdown("### ⚠️ Missing Keywords")

                    for item in sections.get(
                        "⚠️ Missing Keywords",
                        ["No missing keywords found."]
                    ):

                        st.markdown(item)

            st.write("")

            # ---------------------------------------------
            # EXPERIENCE MATCH
            # ---------------------------------------------

            with st.container(border=True):

                st.markdown("### 📋 Experience Match")

                for item in sections.get(
                    "📋 Experience Match",
                    ["No experience match information available."]
                ):

                    st.markdown(item)

            st.write("")

            # ---------------------------------------------
            # RECOMMENDATIONS
            # ---------------------------------------------

            with st.container(border=True):

                st.markdown("### 💡 Recommendations")

                for item in sections.get(
                    "💡 Recommendations",
                    ["No recommendations available."]
                ):

                    st.markdown(item)

            st.write("")

            # ---------------------------------------------
            # FINAL RECOMMENDATION
            # ---------------------------------------------

            with st.container(border=True):

                st.markdown("### ✅ Final Recommendation")

                for item in sections.get(
                    "✅ Final Recommendation",
                    ["No final recommendation available."]
                ):

                    st.markdown(item)
                    # -----------------------------------------
            # DOWNLOAD JOB MATCHING PDF
            # -----------------------------------------

            st.write("")

            with st.container(border=True):

                st.markdown("### 📥 Download Job Match Report")

                try:

                    pdf_file = create_pdf_report(
                        "Placement Coach - Job Matching Report",
                        st.session_state.job_match_result
                    )

                    st.download_button(
                        label="📥 Download Job Matching PDF",
                        data=pdf_file.getvalue(),
                        file_name="Placement_Coach_Job_Matching.pdf",
                        mime="application/pdf",
                        key="download_job_matching_pdf"
                    )

                except Exception as e:

                    st.error(
                        f"❌ PDF generation failed: {e}"
                    )

            # =====================================================
    # INTERVIEW PREPARATION
    # =====================================================

    elif menu == "💼 Interview Preparation":

        st.subheader("💼 AI Interview Preparation")

        st.write(
            "Upload your resume and enter the target job description "
            "to generate personalized interview questions."
        )

        with st.container(border=True):

            resume_file = st.file_uploader(
                "📄 Upload Resume PDF",
                type=["pdf"],
                key="interview_resume"
            )

            job_description = st.text_area(
                "💼 Target Job Description",
                placeholder=(
                    "Paste the complete job description here..."
                ),
                height=220,
                key="interview_description"
            )

            interview_button = st.button(
                "🤖 Generate Interview Questions",
                key="interview_button"
            )

        if interview_button:

            if resume_file is None:

                st.warning(
                    "Please upload your resume PDF."
                )

            elif not job_description.strip():

                st.warning(
                    "Please enter the target job description."
                )

            else:

                try:

                    with st.spinner(
                        "AI is preparing your interview questions..."
                    ):

                        resume_text = extract_text_from_pdf(
                            resume_file
                        )

                        result = generate_interview_questions(
                            resume_text,
                            job_description
                        )

                        st.session_state.interview_result = result

                        # Save job matching to user history
                        if st.session_state.user:
                         save_analysis_history(
                          st.session_state.user.id,
                          "INTERVIEW PREPARATION",
                           result
                     )

                    st.success(
                        "Interview preparation completed!"
                    )

                except Exception as e:

                    st.error(
                        f"Interview preparation failed: {e}"
                    )

        # =================================================
        # INTERVIEW RESULT
        # =================================================

        if "interview_result" in st.session_state:

            result = st.session_state.interview_result

            st.markdown("---")

            st.subheader("🎓 Interview Preparation")

            sections = {}
            current_section = None

            for line in result.splitlines():

                line = line.strip()

                if line.startswith("## "):

                    current_section = line[3:].strip()
                    sections[current_section] = []

                elif current_section and line:

                    sections[current_section].append(line)

            # HR Questions
            if "👨‍💼 HR Interview Questions" in sections:

                with st.container(border=True):

                    st.markdown(
                        "### 👨‍💼 HR Interview Questions"
                    )

                    for item in sections[
                        "👨‍💼 HR Interview Questions"
                    ]:

                        st.markdown(item)

            # Technical Questions
            if "💻 Technical Interview Questions" in sections:

                with st.container(border=True):

                    st.markdown(
                        "### 💻 Technical Interview Questions"
                    )

                    for item in sections[
                        "💻 Technical Interview Questions"
                    ]:

                        st.markdown(item)

            # Resume Questions
            if "📄 Resume-Based Questions" in sections:

                with st.container(border=True):

                    st.markdown(
                        "### 📄 Resume-Based Questions"
                    )

                    for item in sections[
                        "📄 Resume-Based Questions"
                    ]:

                        st.markdown(item)

            # Interview Tips
            if "🎯 Interview Tips" in sections:

                with st.container(border=True):

                    st.markdown(
                        "### 🎯 Interview Tips"
                    )

                    for item in sections[
                        "🎯 Interview Tips"
                    ]:

                        st.markdown(item)

                       # -----------------------------------------
            # DOWNLOAD INTERVIEW PREPARATION PDF
            # -----------------------------------------

            st.write("")

            with st.container(border=True):

                st.markdown("### 📥 Download Interview Report")

                try:

                    pdf_file = create_pdf_report(
                        "Placement Coach - Interview Preparation Report",
                        st.session_state.interview_result
                    )

                    st.download_button(
                        label="📥 Download Interview Preparation PDF",
                        data=pdf_file.getvalue(),
                        file_name="Placement_Coach_Interview_Preparation.pdf",
                        mime="application/pdf",
                        key="download_interview_preparation_pdf"
                    )

                except Exception as e:

                    st.error(
                        f"❌ PDF generation failed: {e}"
                    ) 

      # =====================================================
    # HISTORY
    # =====================================================

    elif menu == "📜 History":

        st.subheader("📜 Analysis History")

        user = st.session_state.user

        if not user:
            st.warning("Please login to view your history.")

        else:
            try:
                history_response = get_analysis_history(user.id)
                history = history_response.data or []

                if not history:
                    st.info("📭 No analysis history found yet.")

                else:
                    st.write(f"Found **{len(history)}** history record(s).")

                    # Select records to delete
                    st.markdown("### 🗑️ Manage History")

                    selected_ids = []

                    for item in history:
                        record_id = str(item["id"])
                        analysis_type = item.get(
                            "analysis_type", "Analysis"
                        )
                        created_at = item.get("created_at", "")

                        try:
                            dt = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
                            dt_ist = dt.astimezone(ZoneInfo("Asia/Kolkata"))
                            created_at_display = dt_ist.strftime("%d %b %Y, %I:%M %p")
                        except (ValueError, TypeError):
                            created_at_display = created_at
                         
                            
                        selected = st.checkbox(
                            f"Select: {analysis_type} — {created_at_display}IST",
                            key=f"history_select_{record_id}"
                        )

                        if selected:
                            selected_ids.append(record_id)

                    col1, col2 = st.columns(2)

                    with col1:
                        if st.button(
                            "🗑️ Delete Selected",
                            key="delete_selected_history",
                            disabled=not selected_ids
                        ):
                            st.session_state.confirm_delete_selected = True

                    with col2:
                        if st.button(
                            "⚠️ Delete All History",
                            key="delete_all_history"
                        ):
                            st.session_state.confirm_delete_all = True

                    if st.session_state.get("confirm_delete_selected", False):
                        st.warning(
                            f"Delete {len(selected_ids)} selected record(s)?"
                        )

                        confirm_col, cancel_col = st.columns(2)

                        with confirm_col:
                            if st.button(
                                "✅ Confirm Selected Delete",
                                key="confirm_selected_delete"
                            ):
                                for record_id in selected_ids:
                                    delete_analysis_history(
                                        user.id, record_id
                                    )

                                st.session_state.confirm_delete_selected = False
                                st.success("Selected history deleted.")
                                st.rerun()

                        with cancel_col:
                            if st.button(
                                "❌ Cancel",
                                key="cancel_selected_delete"
                            ):
                                st.session_state.confirm_delete_selected = False
                                st.rerun()

                    if st.session_state.get("confirm_delete_all", False):
                        st.error(
                            "This will delete all your history records. "
                            "This action cannot be undone."
                        )

                        confirm_col, cancel_col = st.columns(2)

                        with confirm_col:
                            if st.button(
                                "🗑️ Confirm Delete All",
                                key="confirm_delete_all_button"
                            ):
                                delete_all_analysis_history(user.id)
                                st.session_state.confirm_delete_all = False
                                st.success("All your history was deleted.")
                                st.rerun()

                        with cancel_col:
                            if st.button(
                                "❌ Cancel",
                                key="cancel_delete_all_button"
                            ):
                                st.session_state.confirm_delete_all = False
                                st.rerun()

                    st.divider()
                    st.markdown("### 📚 Saved Reports")

                    for item in history:
                        analysis_type = item.get(
                            "analysis_type", "Analysis"
                        )
                        created_at = item.get("created_at", "")
                        try:
                            dt = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
                            dt_ist = dt.astimezone(ZoneInfo("Asia/Kolkata"))
                            created_at_display = dt_ist.strftime("%d %b %Y, %I:%M %p")
                        except (ValueError, TypeError):
                            created_at_display = created_at
                        result = item.get("result", "")

                        with st.container(border=True):
                            st.markdown(f"### 📄 {analysis_type}")
                            st.caption(f"🕒 {created_at_display} IST")

                            with st.expander("👁️ View Result"):
                                st.markdown(result)

                            # PDF Download Button
                            try:
                                pdf_file = create_pdf_report(
                                    f"Placement Coach - {analysis_type}",
                                    result
                                )

                                safe_name = (
                                    analysis_type
                                    .replace(" ", "_")
                                    .replace("/", "_")
                                )

                                st.download_button(
                                    label=f"📥 Download {analysis_type} PDF",
                                    data=pdf_file.getvalue(),
                                    file_name=f"Placement_Coach_{safe_name}.pdf",
                                    mime="application/pdf",
                                    key=f"history_pdf_{item.get('id')}"
                                )

                            except Exception as e:
                                st.error(
                                    f"PDF generation failed: {e}"
                                )

            except Exception as e:
                st.error(f"Could not load history: {e}")

            

    # =====================================================
    # JOB MATCHING
    # =====================================================

    