import csv
from JobApplicationGet import jobApplicationList
from JobApplicationClass import JobApplication
from datetime import datetime
import matplotlib.pyplot as plt

print(jobApplicationList[0].GetEverything())

# File name
csv_file = 'JobApplicationsTest.csv'

dates = []
applications = []

# Read CSV file
with open(csv_file, 'r') as file:
    reader = csv.DictReader(file)
    
    for row in reader:
        # Convert string to datetime object
        date = datetime.strptime(row['AppDate(M-D-Y)'], '%m-%d-%Y')
        dates.append(date)
        
        # Convert applications to integer
        applications.append(int(row['applications']))

# Sort data by date (important if CSV isn't ordered)
sorted_data = sorted(zip(dates, applications))
dates, applications = zip(*sorted_data)

# Create the plot
plt.figure()
plt.plot(dates, applications, marker='o')

# Labels and title
plt.xlabel('Date')
plt.ylabel('Number of Applications')
plt.title('Job Applications Over Time')

# Rotate date labels for readability
plt.xticks(rotation=45)

# Adjust layout so labels don't get cut off
plt.tight_layout()

# Show the graph
plt.show()
