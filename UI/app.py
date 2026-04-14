# Flask app for Group 1 Python project
from flask import Flask, request, render_template, send_file, url_for, redirect, Response, flash, jsonify
from datetime import datetime, timedelta
import matplotlib
matplotlib.use("Agg")  # non-GUI backend - renders images in memory (no GUI thread issues, no reload crashes)

# Import the custom modules
from jobapps import JobApps
from resumebuilder import ResumeBuilder
from charts import Charts
from interviewprep import InterviewPrep

app = Flask(__name__)

job_apps = JobApps() # Create a single JobApps instance used by the methods below
int_prep = InterviewPrep()

# =============================================================================
# Dashboard
# =============================================================================

@app.route("/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/monthly_apps.png")
def monthly_apps():
    # Read data
    job_apps_data = job_apps.read_csv("jobapps.csv")  # returns list
    
    # Instantiate the Charts class and generate the monthly apps chart
    chart = Charts(job_apps_data)  # Pass job apps data to Charts class
    img = chart.gen_monthly_chart()  # Generate the chart
    return Response(img.getvalue(), mimetype="image/png")
 
@app.route("/status_chart.png")
def status_chart():
    # Read data
    job_apps_data = job_apps.read_csv("jobapps.csv")

    # Instantiate the Charts class and generate the monthly apps chart
    chart = Charts(job_apps_data)  # Pass job apps data to Charts class
    img = chart.gen_status_chart()  # Generate the chart
    return Response(img.getvalue(), mimetype="image/png")

@app.route("/role_chart.png")
def role_chart():
    job_apps_data = job_apps.read_csv("jobapps.csv")

    # Instantiate the Charts class and generate the monthly apps chart
    chart = Charts(job_apps_data)  # Pass job apps data to Charts class
    img = chart.gen_role_chart()  # Generate the chart
    return Response(img.getvalue(), mimetype="image/png")

@app.route("/followup_chart.png")
def followup_chart():
    # Read data
    job_apps_data = job_apps.read_csv("jobapps.csv")

    # Instantiate the Charts class and generate the monthly apps chart
    chart = Charts(job_apps_data)  # Pass job apps data to Charts class
    img = chart.gen_followup_chart()  # Generate the chart
    return Response(img.getvalue(), mimetype="image/png")

# =============================================================================
# Resume Builder
# =============================================================================

@app.route("/resume", methods=["GET", "POST"])
def resume():
    if request.method == "POST":
        # Handle the request data
        file = request.files.get("file_input")
        text_input = request.form.get("text_input")
        content = ""

        if file and file.filename != "":
            content = file.read().decode("utf-8")
        elif text_input:
            content = text_input
        else:
            return "Error: No input provided", 400

        # Use the ResumeBuilder() class from the resumebuilder.py module
        builder = ResumeBuilder()
        pdf_file = builder.generate_pdf(content)

        if pdf_file:
            return send_file(pdf_file)
        else:
            return "Error generating PDF", 500

    return render_template("resumebuilder.html")

# =============================================================================
# Job Tracker
# =============================================================================

@app.route("/jobtracker")
def jobtracker():
    # Use the JobApps() class from the jobapps.py module to read all jobs
    job_apps_data = job_apps.read_csv("jobapps.csv")
    
    # Check if job application needs follow up
    today = datetime.today()
    for job in job_apps_data:
        try:
            job_date = datetime.strptime(job["date"], "%Y-%m-%d")
            days_old = (today - job_date).days

            job["needs_followup"] = (
                days_old > 7 and str(job["followedup"]) == "0"
            )
        except:
            job["needs_followup"] = False  # fallback if date is bad

    # Get search query from URL (?q=...)
    query = request.args.get("q", "").strip().lower()

    # Filter results if query exists
    if query:
        job_apps_data = [
            job for job in job_apps_data
            if any(query in str(value).lower() for value in job.values())
            ]

    # Sort after filtering
    job_apps_data.sort(key=lambda x: x["date"], reverse=True)

    return render_template(
        "jobtracker.html",
        jobs=job_apps_data,
        query=query  # send back to template
    )

@app.route("/jobappadd", methods=["GET", "POST"])
def jobappadd():
    if request.method == "POST":
        # Get form values from jobappadd.html
        company = request.form.get("app_company")
        role = request.form.get("app_role")
        date = request.form.get("app_date")
        cname = request.form.get("app_cname")
        cemail = request.form.get("app_cemail")
        status = request.form.get("app_status")
        joblink = request.form.get("app_joblink")
        followedup = 0

        # Add to CSV
        job_apps.add_job_app(company, role, date, cname, cemail, status, joblink, followedup)

        # Redirect to the job tracker list after submission
        return redirect(url_for("jobtracker"))

    # GET request - just render the form
    return render_template("jobappadd.html")

@app.route("/jobappedit/<int:job_id>", methods=["GET", "POST"])
def jobappedit(job_id):
    job_apps_data = job_apps.read_csv("jobapps.csv")
    
    job = next((j for j in job_apps_data if int(j["id"]) == job_id), None)

    if request.method == "POST":
        job["company"] = request.form["company"]
        job["role"] = request.form["role"]
        job["date"] = request.form["date"]
        job["cname"] = request.form["cname"]
        job["cemail"] = request.form["cemail"]
        job["status"] = request.form["status"]
        job["joblink"] = request.form["joblink"]
        job["followedup"] = request.form["followedup"]

        job_apps.upd_job_app(job_apps_data)
        return redirect("/jobtracker")

    return render_template("jobappedit.html", job=job)

# =============================================================================
# Interview Prep
# =============================================================================

@app.route("/interviewprep", methods=["GET", "POST"])
def interviewprep():
    questions = None

    if request.method == "POST":
        jd_text = ""

        file = request.files.get("jd_file_input")
        if file and file.filename.endswith(".txt"):
            content = file.read()
            try:
                jd_text = content.decode("utf-8")
            except UnicodeDecodeError:
                jd_text = content.decode("cp1252")

        if not jd_text:
            jd_text = request.form.get("jd_text_input", "").strip()
            return "Error: No input provided", 400

        if jd_text:
            generator = InterviewPrep()
            questions = generator.generate_questions(jd_text)

    return render_template("interviewprep.html", questions=questions)

# Run the app on http://localhost:8085 only if this file is executed directly, not if it's imported
if __name__ == "__main__": # Without if statement, the server would start even when the file is imported
    app.run(debug=True,port=8085)
