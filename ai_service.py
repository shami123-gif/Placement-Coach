import os
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "openai/gpt-oss-20b"


def ask_ai(prompt: str) -> str:
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is missing from the .env file.")

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are Placement Coach, an expert career assistant. "
                    "Give clear, practical and professional career advice."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        "temperature": 0.3,
        "max_tokens": 2000,
    }

    response = requests.post(
        GROQ_URL,
        headers=headers,
        json=data,
        timeout=60,
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"Groq API error {response.status_code}: {response.text}"
        )

    result = response.json()

    return result["choices"][0]["message"]["content"]


def analyze_resume(resume_text: str, job_description: str) -> str:
    prompt = f"""
Analyze the following resume against the target job description.

RESUME:
{resume_text}

TARGET JOB DESCRIPTION:
{job_description}

Return the result ONLY in the following Markdown format.

# Resume Analysis

## 📊 Overall Resume Score
Give a score out of 100.

## 🎯 ATS Score
Give a score out of 100.

## 💪 Strong Skills
- List the candidate's strong skills.
- Use one skill per bullet point.

## ❌ Missing Skills
- List important skills missing from the resume.
- Use one skill per bullet point.

## 🔑 Missing Keywords
- List important missing job-related keywords.
- Use one keyword per bullet point.

## ⚠️ Weak Areas
- List weaknesses or areas that need improvement.
- Use one point per bullet.

## 💡 Suggestions to Improve
1. Give the first improvement suggestion.
2. Give the second improvement suggestion.
3. Give the third improvement suggestion.
4. Give additional suggestions if necessary.

## ✅ Final Recommendation
Give a short professional recommendation.

IMPORTANT RULES:
- Do NOT use HTML.
- Do NOT use <br>, <br/>, or <br />.
- Do NOT create an HTML table.
- Use only Markdown headings, bullet points and numbered lists.
- Keep the formatting clean and professional.
- Make the analysis specific to the resume and target job.
"""

    return ask_ai(prompt)

def rewrite_bullet(bullet: str) -> str:
    prompt = f"""
Rewrite this resume bullet point to make it professional,
achievement-focused and ATS-friendly.

Original bullet:
{bullet}

Return only the improved bullet point.
"""

    return ask_ai(prompt)


def generate_interview_questions(
    resume_text: str,
    job_description: str
) -> str:

    prompt = f"""
Create interview preparation questions based on the candidate's
resume and target job.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Generate:

1. 5 HR interview questions
2. 5 technical interview questions
3. 5 questions specifically based on the resume
4. Short guidance for answering each question

Keep the questions relevant to the candidate and job.
"""

    return ask_ai(prompt)


def match_job(resume_text: str, job_description: str) -> str:

    prompt = f"""
Compare the candidate's resume with the target job description.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Return the result ONLY in the following Markdown format.

# Job Match Analysis

## 🎯 Job Match Score
Give a score out of 100.

## 💪 Matching Skills
- List skills from the resume that match the job.
- Use one skill per bullet point.

## ❌ Missing Skills
- List important skills required by the job but missing from the resume.
- Use one skill per bullet point.

## 🔑 Matching Keywords
- List important job keywords already present in the resume.
- Use one keyword per bullet point.

## ⚠️ Missing Keywords
- List important job keywords missing from the resume.
- Use one keyword per bullet point.

## 📋 Experience Match
Explain briefly how well the candidate's experience matches the job requirements.

## 💡 Recommendations
1. Give the most important recommendation.
2. Give the second recommendation.
3. Give additional recommendations if needed.

## ✅ Final Recommendation
Give a short professional recommendation about the candidate's suitability for this job.

IMPORTANT RULES:
- Do NOT use HTML.
- Do NOT use <br>, <br/>, or <br />.
- Do NOT create an HTML table.
- Use only Markdown headings, bullet points and numbered lists.
- Keep the result clean and professional.
- Make the analysis specific to the resume and target job.
"""

    return ask_ai(prompt)

def generate_interview_questions(
    resume_text: str,
    job_description: str
) -> str:

    prompt = f"""
You are an expert placement and interview coach.

Create interview preparation questions based on the candidate's
resume and target job description.

RESUME:
{resume_text}

TARGET JOB DESCRIPTION:
{job_description}

Return the result ONLY in the following Markdown format.

# Interview Preparation

## 👨‍💼 HR Interview Questions

1. Question
   - Guidance: Give short guidance for answering.

2. Question
   - Guidance: Give short guidance for answering.

3. Question
   - Guidance: Give short guidance for answering.

4. Question
   - Guidance: Give short guidance for answering.

5. Question
   - Guidance: Give short guidance for answering.

## 💻 Technical Interview Questions

1. Question
   - Guidance: Give short guidance for answering.

2. Question
   - Guidance: Give short guidance for answering.

3. Question
   - Guidance: Give short guidance for answering.

4. Question
   - Guidance: Give short guidance for answering.

5. Question
   - Guidance: Give short guidance for answering.

## 📄 Resume-Based Questions

1. Question
   - Guidance: Give short guidance for answering.

2. Question
   - Guidance: Give short guidance for answering.

3. Question
   - Guidance: Give short guidance for answering.

4. Question
   - Guidance: Give short guidance for answering.

5. Question
   - Guidance: Give short guidance for answering.

## 🎯 Interview Tips

- Give practical interview preparation tips.
- Keep the tips specific to the candidate and target job.

IMPORTANT RULES:
- Do NOT use HTML.
- Do NOT use <br>, <br/>, or <br />.
- Use only Markdown headings, numbered lists and bullet points.
- Keep the questions specific to the resume and target job.
- Keep guidance short and practical.
"""

    return ask_ai(prompt)