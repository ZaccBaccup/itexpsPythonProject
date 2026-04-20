import pandas as pd
from datetime import datetime, timedelta

# File path
CSV_FILE = "JobApplicationsTest.csv"

# Load CSV
df = pd.read_csv(CSV_FILE)

# Convert date column (adjust format if needed)
df['AppDate(M-D-Y)'] = pd.to_datetime(df['AppDate(M-D-Y)'], errors='coerce')

# Calculate cutoff date
cutoff_date = datetime.now() - timedelta(days=7)

# Filter rows needing follow-up
pending = df[
    (df['FollowedUp'] == 0) &
    (df['AppDate(M-D-Y)'] < cutoff_date)
]

# print(pending)

if pending.empty:
    print("No follow-ups needed!")
else:
    print(f"{len(pending)} applications need follow-up.\n")

    for index, row in pending.iterrows():
        print("----")
        print(f"Company: {row.get('CompanyName', 'N/A')}")
        print(f"Role: {row.get('JobTitle', 'N/A')}")
        print(f"Applied Date: {row.get('AppDate(M-D-Y)', 'N/A').strftime("%m-%d-%Y")}")

        user_input = input("Did you follow up? (y/n): ").strip().lower()

        if user_input == 'y':
            df.at[index, 'FollowedUp'] = 1
            print("Marked as followed up.\n")
        else:
            print("Reminder will stay.\n")
        

# Save updated CSV
df['FollowedUp'] = df['FollowedUp'].astype(int)  #convert to int

df['AppDate(M-D-Y)'] = df['AppDate(M-D-Y)'].dt.strftime("%m-%d-%Y")

df.to_csv(CSV_FILE, index=False)

# print("File updated successfully.")
