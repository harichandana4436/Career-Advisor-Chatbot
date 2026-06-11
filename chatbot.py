import os
import pdfplumber
import google.generativeai as genai
from dotenv import load_dotenv

from prompts import (
    SYSTEM_PROMPT,
    RESUME_ANALYZER_PROMPT,
    INTERVIEW_GENERATOR_PROMPT,
    ROADMAP_GENERATOR_PROMPT,
    RESUME_BASED_INTERVIEW_PROMPT,
    HR_INTERVIEW_PROMPT
)
from utils.logger import logger

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=SYSTEM_PROMPT
)


def get_career_advice(user_query):
    try:
        logger.info(f"User Query: {user_query}")
        response = model.generate_content(user_query)
        logger.info("Response Generated Successfully")
        return response.text

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return f"ERROR: {str(e)}"


def analyze_resume(pdf_file):
    try:
        text = ""
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""

        if not text.strip():
            return "Could not extract text from the resume. Please upload a text-based PDF."

        prompt = RESUME_ANALYZER_PROMPT + f"\n\nResume Content:\n{text}"

        logger.info("Resume analysis requested")
        response = model.generate_content(prompt)
        logger.info("Resume analysis completed")

        return response.text

    except Exception as e:
        logger.error(f"Resume analysis error: {str(e)}")
        return f"Error analyzing resume: {str(e)}"


def analyze_resume_and_generate_questions(pdf_file):
    try:
        text = ""
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""

        if not text.strip():
            return None, None, "Could not extract text from the resume. Please upload a text-based PDF."

        # Step 1 — Analyze resume
        resume_prompt = RESUME_ANALYZER_PROMPT + f"\n\nResume Content:\n{text}"
        logger.info("Resume analysis started")
        resume_response = model.generate_content(resume_prompt)
        resume_feedback = resume_response.text
        logger.info("Resume analysis completed")

        # Step 2 — Generate technical interview questions
        interview_prompt = RESUME_BASED_INTERVIEW_PROMPT + f"\n\nResume Content:\n{text}"
        logger.info("Resume-based interview question generation started")
        interview_response = model.generate_content(interview_prompt)
        interview_questions = interview_response.text
        logger.info("Resume-based interview questions generated")

        return resume_feedback, interview_questions, None

    except Exception as e:
        logger.error(f"Resume analysis + interview generation error: {str(e)}")
        return None, None, f"Error: {str(e)}"


def generate_hr_questions_from_resume(pdf_file):
    try:
        text = ""
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""

        if not text.strip():
            return None, "Could not extract text from resume. Please upload a text-based PDF."

        prompt = HR_INTERVIEW_PROMPT + f"\n\nResume Content:\n{text}"

        logger.info("HR interview question generation started")
        response = model.generate_content(prompt)
        logger.info("HR interview questions generated")

        return response.text, None

    except Exception as e:
        logger.error(f"HR interview generation error: {str(e)}")
        return None, f"Error: {str(e)}"


def generate_interview_questions(job_role):
    try:
        prompt = INTERVIEW_GENERATOR_PROMPT + f"\n\nJob Role: {job_role}"

        logger.info(f"Interview questions requested for: {job_role}")
        response = model.generate_content(prompt)
        logger.info("Interview questions generated")

        return response.text

    except Exception as e:
        logger.error(f"Interview generation error: {str(e)}")
        return f"Error generating questions: {str(e)}"


def generate_roadmap(goal, timeframe):
    try:
        prompt = ROADMAP_GENERATOR_PROMPT + f"\n\nGoal: {goal}\nTimeframe: {timeframe}"

        logger.info(f"Roadmap requested: {goal} in {timeframe}")
        response = model.generate_content(prompt)
        logger.info("Roadmap generated")

        return response.text

    except Exception as e:
        logger.error(f"Roadmap generation error: {str(e)}")
        return f"Error generating roadmap: {str(e)}"