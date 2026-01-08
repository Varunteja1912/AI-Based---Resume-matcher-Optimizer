# ai_engine.py
import json
from openai import OpenAI

# 🔑 Hard-coded API key  (for local testing only)
client = OpenAI(api_key="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")

def analyze_resume_vs_jd(resume_text, job_text):
    """
    Uses GPT to analyze how well a resume fits a job description.
    Returns structured JSON with match score, strengths, gaps, and recommendation.
    """
    prompt = f"""
You are an AI HR assistant who screens candidates for AI/Tech roles.

Compare the following resume and job description carefully.
Think like a recruiter. Evaluate skill fit, experience alignment, and relevance.

Return ONLY valid JSON in this format:
{{
  "match_score": <number between 0 and 100>,
  "strengths": ["Top 3 strengths"],
  "gaps": ["Top 3 missing skills or weak areas"],
  "recommendation": "Interview / Consider / Reject",
  "summary": "Short summary of candidate fit"
}}

Resume:
{resume_text[:3000]}

Job Description:
{job_text}
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=400
        )
        text_output = response.choices[0].message.content.strip()
        try:
            data = json.loads(text_output)
        except json.JSONDecodeError:
            data = {"summary": text_output}
        return data
    except Exception as e:
        return {"error": str(e)}


def optimize_resume_for_job(resume_text, job_text):
    """
    Uses GPT to rewrite or enhance resume content
    for better alignment with the target job description.
    """
    prompt = f"""
You are an expert AI resume writer.

Given the resume and job description below, rewrite the resume summary
to make it more aligned with the job requirements.
Keep it realistic, professional, and under 6 lines.

Return your improved summary clearly under the header: "Optimized Resume Summary".

Resume:
{resume_text[:2500]}

Job Description:
{job_text}
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=300
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"