# Generate interview questions based on job description provided
from openai import OpenAI

class InterviewPrep:
    def __init__(self):
        self.client = OpenAI() # Let the SDK read the api_key automatically

    def generate_questions(self, job_description: str, num_questions: int = 8) -> str:
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