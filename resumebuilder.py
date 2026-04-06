# create a pdf resume from user input (uploaded txt/csv or pasted content)

import io
import csv
from flask import Flask, redirect, send_file, make_response, request, render_template
from fpdf import FPDF

from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, cm

app = Flask(__name__)             # create an app instance

@app.route('/process', methods=['POST'])
def process():
    file = request.files.get('file_input')
    text_input = request.form.get('text_input')

    content = None

    # Case 1: File uploaded
    if file and file.filename != "":
        try:
            content = file.read().decode('utf-8')
        except Exception:
            return "Error: Could not read file"

    # Case 2: Text input provided
    elif text_input and text_input.strip() != "":
        content = text_input

    # Case 3: Both empty
    else:
        return "Error: No input provided"

    # Generate pdf
    c = canvas.Canvas('c:\\data\\resume.pdf')  # file to create
    # Display text
    c.drawString(100,650, content)

    # Display on page
    c.showPage()
    c.save()
    response = make_response(send_file("c:\\data\\resume.pdf"))
    return response

# Run the app on http://localhost:8085 only if this file is executed directly, not if it's imported
if __name__ == '__main__': # Without if statement, the server would start even when the file is imported
    app.run(debug=True,port=8085)
