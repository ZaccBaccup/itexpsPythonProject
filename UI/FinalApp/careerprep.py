# Generate cover letter or interview questions based on job description provided
import pdfplumber
import os
from openai import OpenAI
from config import OUTPUT_DIR  # Assuming OUTPUT_DIR is defined in your config.py

class CareerPrep:
    def __init__(self, output_dir=OUTPUT_DIR):
        self.client = OpenAI()  # Let the SDK read the api_key automatically
        self.output_dir = output_dir

        # Ensure the directory exists
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        # Full path to CSV
        self.csv_file = os.path.join(self.output_dir, "resume.txt")

    def extract_resume_text(self, resume_path: str) -> str:
        """
        Extracts text from the given resume PDF file.
        Returns the extracted text as a string.
        """
        resume_text = ""
        try:
            with pdfplumber.open(resume_path) as pdf:
                # Loop through all pages and extract text
                for page in pdf.pages:
                    resume_text += page.extract_text()
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
        return resume_text

    def generate_questions(self, job_description: str, num_questions: int = 10) -> str:
        """
        Generate interview questions based on a job description.
        Returns a formatted string of questions.
        """

        prompt = f"""
        You are an expert technical recruiter.

        Based on the following job description, generate {num_questions} realistic interview questions.

        Job Description:
        {job_description}

        Requirements:
        - Mix of behavioral and technical questions
        - Make them relevant to the role
        - Do not include answers
        - Format as a numbered list
        """

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You generate high-quality interview questions."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )

        return response.choices[0].message.content
    
    def generate_cover_letter(self, job_description: str, candidate_info: dict, today: str, tone: str = "professional") -> str:
        """
        Generate a tailored cover letter based on a job description.
        Returns a formatted cover letter string.
        """

        resume_path = os.path.join(self.output_dir, "resume.pdf")
        resume_text = self.extract_resume_text(resume_path)

        prompt = f"""
        You are an expert career coach and professional resume writer.
        
        Write a strong, tailored cover letter based on the job description below.
        
        Job Description:
        {job_description}
       
        Candidate Information (USE EXACT VALUES ONLY — DO NOT MODIFY OR SUBSTITUTE):
        Name: {candidate_info['name']}
        Email: {candidate_info['email']}
        Phone: {candidate_info['phone']}
        
        Resume:
        {resume_text[:1000]}  # (limit text for context, adjust as needed)
        
        STRICT REQUIREMENTS:
        - DO NOT use placeholders like [Your Name], [Your Email], [Your Phone], [Date], [Current Date] or any brackets
        - You MUST write the actual candidate details exactly as provided above
        - Add today's date written out in full (e.g., April 21, 2026) after the candidate details
        - DO NOT include [Company Address] [City, State, Zip] if blank
        - DO NOT include any bracketed text anywhere in the output
        - DO NOT include generic template fields
        - DO NOT leave any missing fields
        - This must be a final, ready-to-send cover letter
        
        FORMAT:
        - Full letter with professional formatting
        - Include candidate contact info at top
        - Include today's date in this format: Month Day, Year (e.g., April 21, 2026) after the candidate details
        - Include employer contact info
        - 3–5 paragraphs max
        - Professional tone
        """

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert professional cover letter writer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )

        return response.choices[0].message.content