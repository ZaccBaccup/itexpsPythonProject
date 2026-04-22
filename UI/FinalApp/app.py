# Flask app for Group 1 Python project
from flask import Flask, request, render_template, send_file, url_for, redirect, Response, flash, session
from datetime import datetime, timedelta
from werkzeug.security import check_password_hash
from datetime import datetime
import matplotlib
matplotlib.use("Agg")  # non-GUI backend - renders images in memory (no GUI thread issues, no reload crashes)

# Import the custom modules
from jobapps import JobApps
from resumebuilder import ResumeBuilder
from careerprep import CareerPrep
from userinfo import UserInfo

app = Flask(__name__)

job_apps = JobApps() # Create a single JobApps instance used by the methods below
career_prep = CareerPrep()
user_info = UserInfo()
# app.secret_key = os.urandom(24) # required for sessions
# sign the cookie so it can’t be tampered with, and verify it hasn’t been changed when it comes back
app.secret_key = "careerflow-dev-key" 

@app.route("/")
def landing():
    return render_template("landing.html")

# =============================================================================
# Login
# =============================================================================

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        # Load all users from CSV
        users = user_info.read_user_csv()

        # Find user
        user = next((u for u in users if u["username"] == username), None)

        # Validate credentials and store user info in session
        if user and check_password_hash(user["password"], password):
            session["username"] = user["username"]
            session["firstname"] = user["firstname"]
            session["lastname"] = user["lastname"]
            session["phone"] = user["phone"]
            session["email"] = user["email"]

            return redirect(url_for("home"))

        else:
            flash("Invalid username or password", "danger")
            return redirect(url_for("login"))

    return render_template("landing.html")  # home page

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# =============================================================================
# Home
# =============================================================================

@app.route("/home")
def home():
    job_apps_data = job_apps.read_csv("jobapps.csv")
    active_statuses = ["Applied", "Interviewed", "Interview Scheduled", "Offer Received"]
    
    active_apps = sum(
        1 for job in job_apps_data
        if job.get("status") in active_statuses
    )

    interviews_sched = sum(
        1 for job in job_apps_data
        if job.get("status") == "Interview Scheduled"
    )

    offers = sum(
        1 for job in job_apps_data
        if job.get("status") == "Offer Received"
    )
    
    user_data = user_info.read_user_csv()
    for user in user_data:
        user_name=user["firstname"] + " " + user["lastname"]

    return render_template(
        'home.html',
        user_name=user_name,
        active_apps=active_apps,
        interviews_sched=interviews_sched,
        offers=offers
    )

# =============================================================================
# Dashboard
# =============================================================================

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

# =============================================================================
# Resume Builder
# =============================================================================

@app.route("/resume", methods=["GET", "POST"])
def resume():
    if request.method == "POST":
        # Handle the request data - skills and experiences
        exp_file = request.files.get("exp_file")
        exp_text = request.form.get("exp_text")
        exp_content = ""

        # Handle the request data - job description
        jd_file = request.files.get("jd_file")
        jd_text = request.form.get("jd_text")
        jd_content = ""

        if exp_file and exp_file.filename != "":
            exp_content = exp_file.read().decode("utf-8")
        elif exp_text:
            exp_content = exp_text
        else:
            return "Error: No input provided", 400

        if jd_file and jd_file.filename != "":
            jd_content = jd_file.read().decode("utf-8")
        elif jd_text:
            jd_content = jd_text
        else:
            return "Error: No input provided", 400

        candidate_info = {
            "name": f"{session.get('firstname','')} {session.get('lastname','')}",
            "email": session.get("email", ""),
            "phone": session.get("phone", "")
        }

        # Use the ResumeBuilder() class from the resumebuilder.py module
        builder = ResumeBuilder()
        pdf_file = builder.generate_resume(exp_content, jd_content, candidate_info)

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
# Career Prep
# =============================================================================

@app.route("/careerprep", methods=["GET", "POST"])
def careerprep():
    questions = None
    cover_letter = None
    
    print("Firstname:", session.get("firstname"))
    print("Lastname:", session.get("lastname"))
    print("Email:", session.get("email"))
    print("Phone:", session.get("phone"))
    print("SESSION IN CAREERPREP:", dict(session))

    if request.method == "POST":
        action = request.form.get("action")
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
        else:
            career_prep = CareerPrep() # create instance

        if jd_text and action == "interview_questions":
            questions = career_prep.generate_questions(jd_text)

        elif jd_text and action == "cover_letter":
            # Create candidate_info from session
            candidate_info = {
                "name": f"{session.get('firstname','')} {session.get('lastname','')}",
                "email": session.get("email", ""),
                "phone": session.get("phone", "")
            }
            
            today = datetime.now().strftime("%B %d, %Y")

            cover_letter = career_prep.generate_cover_letter(jd_text, candidate_info, today)
            
    return render_template("careerprep.html", questions=questions, cover_letter=cover_letter)

# Run the app on http://localhost:8085 only if this file is executed directly, not if it's imported
if __name__ == "__main__": # Without if statement, the server would start even when the file is imported
    app.run(debug=True,port=8085)
