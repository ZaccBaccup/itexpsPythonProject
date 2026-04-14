# Read/write job applications from/to csv
import os
import csv
from config import OUTPUT_DIR # config.py has the directory where csv files are stored

class JobApps:
    def __init__(self, output_dir=OUTPUT_DIR):
        self.output_dir = output_dir
        
        # Ensure the directory exists
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        # Full path to CSV
        self.csv_file = os.path.join(self.output_dir,"jobapps.csv")

    def read_csv(self, file_path):
        """Read csv file"""
        file_path = os.path.join(self.output_dir, "jobapps.csv")
        
        job_apps = []
        
        with open(file_path, mode="r", newline="") as file:
            csv_reader = csv.reader(file)
            
            header = next(csv_reader)  # Skip header row

            # Convert each row into a dictionary
            for col in csv_reader:
                job_app = {
                    "id": col[0],
                    "company": col[1],
                    "role": col[2],
                    "date": col[3],
                    "cname": col[4],
                    "cemail": col[5],
                    "status": col[6],
                    "joblink": col[7],
                    "followedup": col[8]
                }
                job_apps.append(job_app)

        return job_apps # Return a list
    
    def upd_job_app(self, job_apps):
        """Overwrite CSV with updated job applications"""
        with open(self.csv_file, mode="w", newline="") as file:
            writer = csv.writer(file)
            
            # Write header
            writer.writerow([
                "id", "company", "role", "date", "cname",
                "cemail", "status", "joblink", "followedup"
                ])
            
            # Write rows
            for job in job_apps:
                writer.writerow([
                    job["id"],
                    job["company"],
                    job["role"],
                    job["date"],
                    job["cname"],
                    job["cemail"],
                    job["status"],
                    job["joblink"],
                    job["followedup"]
                    ])
            
    def add_job_app(self, company, role, date, cname, cemail, status, joblink, followedup):
        job_apps = self.read_csv(self.csv_file)

        # Generate new ID
        new_id = 1
        if job_apps:
            new_id = max(int(job["id"]) for job in job_apps) + 1

        with open(self.csv_file, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                new_id, company, role, date, cname,
                cemail, status, joblink, followedup
            ])

# Test block
if __name__ == "__main__":
    job_apps = JobApps() # Create instance of JobApps
    print("Testing csv reader...")
    job_apps_data = job_apps.read_csv("jobapps.csv") # Store results in job_apps_data variable
    for job_app in job_apps_data:
        print(job_app) # Print each job application dictionary
