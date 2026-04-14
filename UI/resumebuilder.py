# Create a pdf resume from user input (uploaded txt/csv or pasted content)
import os
from fpdf import FPDF
from reportlab.pdfgen import canvas
from config import OUTPUT_DIR # config.py has the directory where csv files are stored

class ResumeBuilder:
    def __init__(self, output_dir=OUTPUT_DIR):
        self.output_dir = output_dir
        # Ensure the directory exists
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def generate_pdf(self, content):
        """Processes text content and saves it as a PDF."""
        file_path = os.path.join(self.output_dir, "resume.pdf")
        
        try:
            c = canvas.Canvas(file_path)
            # Simple text drawing logic
            c.setFont("Helvetica-Bold", 16)
#            c.drawString(100, 750, "Generated Resume")
            c.setFont("Helvetica", 12)
            
            # Basic support for multi-line text
            y_position = 700
            for line in content.split("\n"):
                c.drawString(100, y_position, line)
                y_position -= 20
                
            c.showPage()
            c.save()
            return file_path
        except Exception as e:
            print(f"PDF Error: {e}")
            return None

# Test block
if __name__ == "__main__":
    builder = ResumeBuilder()
    print("Testing PDF generation...")
    builder.generate_pdf("Test Name\nTest Experience")
