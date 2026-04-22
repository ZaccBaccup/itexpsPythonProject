# Create a pdf resume from user input (uploaded txt/csv or pasted content)
from openai import OpenAI
import os
from fpdf import FPDF
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from config import OUTPUT_DIR # config.py has the directory where csv files are stored

class ResumeBuilder:
    def __init__(self, output_dir=OUTPUT_DIR):
        self.output_dir = output_dir
        # Ensure the directory exists
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        self.client = OpenAI() # Let the SDK read the api_key automatically

    def generate_resume(self, exp_content: str, jd_content: str, candidate_info: dict) -> str:
        """
        Generate a tailored resume using OpenAI, then create a PDF.
        Returns the PDF file path.
        """
        
        prompt = f"""
        You are an expert resume writer.
        
        Create a professional, ATS-friendly resume based on the following information.
        
        Candidate Information (USE EXACT VALUES ONLY — DO NOT MODIFY OR SUBSTITUTE):
        Name: {candidate_info['name']}
        Email: {candidate_info['email']}
        Phone: {candidate_info['phone']}
        
        Candidate Experience / Input:
        {exp_content}
        
        Job Description:
        {jd_content}
        
        STRICT REQUIREMENTS:
        - DO NOT use placeholders like [Your Name], [Your Email], [Your Phone], [Your Address], [City, State, Zip], [LinkedIn Profile URL] or any brackets
        - Use clear section headings: Name, Professional Summary, Skills, Experience, Education
        - Uppercase each section heading
        - Using Candidate Experience above, tailor the resume to match the Job Description above
        - You MUST write the actual candidate details exactly as provided above
        - Categorize the skills to improve readability and show structure - separated by comma, not bullet points
        - DO NOT use asterisks (*)
        - DO NOT list skills as a flat bullet list
        - DO NOT include any bracketed text anywhere in the output
        - DO NOT include a References section or contact information from the Job Description above
        - Add the experience dates next to the role, in parenthesis
        - This must be a final, ready-to-send resume
        
        Structure the resume like this:
        NAME
        Email
        Phone
        
        PROFESSIONAL SUMMARY
        ...
        
        SKILLS
        - ...
        
        EXPERIENCE
        Company - Role (Year–Year)
        - bullet points
        
        EDUCATION
        ...
        
        FORMAT:
        - Keep formatting clean and professional
        - Uppercase each section heading
        - DO NOT use asterisks (*)
        - DO NOT use markdown (**, ###, etc.)
        - Include candidate information at top
        - Use bullet points for experience
        - Professional tone
        """
        
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You write high-quality professional resumes."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
        )
        
        resume_text = response.choices[0].message.content
        
        # Generate PDF using the AI output
        pdf_file = self.generate_pdf(resume_text)
        
        return pdf_file

    def generate_pdf(self, content):
        file_path = os.path.join(self.output_dir, "resume.pdf")
        
        try:
            doc = SimpleDocTemplate(file_path)
            styles = getSampleStyleSheet()
            elements = []
            
            name_style = ParagraphStyle(
                name="Name",
                parent=styles["Normal"],
                fontSize=14,
                fontName="Helvetica-Bold"
            )

            bullet_style = ParagraphStyle(
                name="Bullet",
                bulletIndent=10,
                leftIndent=20,
                fontSize=10,
                spaceAfter=3
            )
            
            heading_style = styles["Heading3"]
            normal_style = styles["Normal"]
            
            first_line = True

            for line in content.split("\n"):
                stripped = line.strip()
                
                # Format the name (first line)
                if first_line and stripped:
                    elements.append(Paragraph(stripped, name_style))
                    first_line = False
                    elements.append(Spacer(1, 6))
                    continue

                # Format the section headings
                if line.strip().upper() in ["PROFESSIONAL SUMMARY", "SKILLS", "EXPERIENCE", "EDUCATION"]:
                    elements.append(Spacer(1, 4))
                    elements.append(Paragraph(stripped, heading_style))
                    elements.append(Spacer(1, 3))
                # Format the bullets
                elif line.strip().startswith("-"):
                    text = line.strip().lstrip("-").strip()
                    elements.append(Paragraph(text, bullet_style, bulletText="•"))
                else:
                    elements.append(Paragraph(stripped, normal_style))
                    
                elements.append(Spacer(1, 4))
            
            doc.build(elements)
            return file_path
        except Exception as e:
            print(f"PDF Error: {e}")
            return None

# Test block
if __name__ == "__main__":
    builder = ResumeBuilder()
    print("Testing PDF generation...")
    builder.generate_pdf("Test Name\nTest Experience")
