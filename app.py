# app.py
import streamlit as st
import pdfplumber
import matplotlib.pyplot as plt
from ai_engine import analyze_resume_vs_jd, optimize_resume_for_job


# ---------------- STREAMLIT SETTINGS ----------------
st.set_page_config(page_title="AI Resume Matcher (GenAI)", layout="centered")
st.title("🤖 AI Resume & Job Matching Assistant (Generative AI)")

st.write("""
Upload your resume as a PDF and paste a job description.  
The AI will analyze your fit, show recruiter-style feedback,  
and even rewrite your resume summary for better alignment.
""")

tabs = st.tabs(["📄 Resume–JD Analyzer", "✍️ Resume Optimizer"])

# ---------------- HELPER FUNCTION ----------------
def extract_text_from_pdf(uploaded_file):
    """Extract text from uploaded PDF resume"""
    try:
        with pdfplumber.open(uploaded_file) as pdf:
            text = "\n".join([page.extract_text() or "" for page in pdf.pages])
        return text.strip()
    except Exception as e:
        return f"Error reading PDF: {e}"


# ---------------- TAB 1: MATCH ANALYSIS ----------------
with tabs[0]:
    st.subheader("📄 Resume–Job Fit Analysis")

    resume_file = st.file_uploader("Upload Resume (PDF only)", type=["pdf"])
    job_desc = st.text_area("💼 Paste Job Description", height=250, placeholder="Paste the job description here...")

    if st.button("🔍 Analyze with AI"):
        if not resume_file or not job_desc:
            st.warning("Please upload a resume and paste a job description.")
        else:
            with st.spinner("Extracting text from your resume... 🧾"):
                resume_text = extract_text_from_pdf(resume_file)

            with st.spinner("AI is analyzing your resume... 🤖"):
                result = analyze_resume_vs_jd(resume_text, job_desc)

            if "error" in result:
                st.error(f"Error: {result['error']}")
            else:
                st.success(f"🎯 Match Score: {result.get('match_score', 'N/A')}%")

                st.subheader("✅ Strengths")
                for s in result.get("strengths", []):
                    st.markdown(f"- {s}")

                st.subheader("⚠️ Gaps / Missing Skills")
                for g in result.get("gaps", []):
                    st.markdown(f"- {g}")

                st.subheader("💬 Recommendation")
                st.info(result.get("recommendation", "No recommendation available."))

                st.subheader("🧠 AI Summary")
                st.write(result.get("summary", ""))

                # Visual match chart
                if "match_score" in result:
                    st.subheader("📊 Visual Match Score")
                    plt.bar(["Match Score"], [result["match_score"]], color="green")
                    plt.ylim(0, 100)
                    plt.ylabel("Score (%)")
                    plt.title("Resume–JD Fit Score")
                    st.pyplot(plt)


# ---------------- TAB 2: RESUME OPTIMIZER ----------------
with tabs[1]:
    st.subheader("✍️ AI Resume Optimizer")

    resume_file_opt = st.file_uploader("Upload Resume (PDF only)", type=["pdf"], key="resume_opt")
    job_desc_opt = st.text_area("💼 Paste Target Job Description", height=250, placeholder="Paste the job description you want to optimize for...")

    if st.button("✨ Generate Optimized Summary"):
        if not resume_file_opt or not job_desc_opt:
            st.warning("Please upload a resume and paste the job description.")
        else:
            with st.spinner("Extracting resume content... 🧾"):
                resume_text_opt = extract_text_from_pdf(resume_file_opt)

            with st.spinner("AI is optimizing your resume summary... ✨"):
                optimized_summary = optimize_resume_for_job(resume_text_opt, job_desc_opt)

            st.success("✅ Optimized Resume Summary:")
            st.write(optimized_summary)