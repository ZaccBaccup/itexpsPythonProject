# Read/write job applications from/to csv
import os
import csv
from config import OUTPUT_DIR # config.py has the directory where csv files are stored

class UserInfo:
    def __init__(self, output_dir=OUTPUT_DIR):
        self.output_dir = output_dir
        
        # Ensure the directory exists
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        # Full path to CSV
        self.csv_file = os.path.join(self.output_dir,"users.csv")

    def read_user_csv(self):
        """Read csv file"""
        file_path = os.path.join(self.output_dir, "users.csv")
        
        users = []
        
        with open(file_path, mode="r", newline="") as file:
            csv_reader = csv.reader(file)
            
            header = next(csv_reader)  # Skip header row

            # Convert each row into a dictionary
            for col in csv_reader:
                user = {
                    "id": col[0],
                    "username": col[1],
                    "password": col[2],
                    "firstname": col[3],
                    "lastname": col[4],
                    "phone": col[5],
                    "email": col[6]
                }
                users.append(user)

        return users # Return a list
