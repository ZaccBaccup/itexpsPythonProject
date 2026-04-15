import pandas as pd
from datetime import datetime, timedelta

# File path
CSV_FILE = "JobApplicationsTest.csv"

# Load CSV
df = pd.read_csv(CSV_FILE)

# Ensure correct types
df['FollowedUp'] = df['FollowedUp'].astype(str).str.lower() == 'true'

# Convert date column (adjust format if needed)
df['AppDate(M-D-Y)'] = pd.to_datetime(df['AppDate(M-D-Y)'], errors='coerce')

# Calculate cutoff date
cutoff_date = datetime.now() - timedelta(days=7)

# Filter rows needing follow-up
pending = df[
    (df['FollowedUp'] == False) &
    (df['AppDate(M-D-Y)'] < cutoff_date)
]

if pending.empty:
    print("No follow-ups needed!")
else:
    print(f"{len(pending)} applications need follow-up.\n")

    for index, row in pending.iterrows():
        print("----")
        print(f"Company: {row.get('company', 'N/A')}")
        print(f"Role: {row.get('role', 'N/A')}")
        print(f"Applied Date: {row['AppDate(M-D-Y)'].date()}")

        user_input = input("Did you follow up? (y/n): ").strip().lower()

        if user_input == 'y':
            df.at[index, 'FollowedUp'] = True
            print("Marked as followed up.\n")
        else:
            print("Reminder will stay.\n")

# Save updated CSV
df['FollowedUp'] = df['FollowedUp'].astype(bool)
df.to_csv(CSV_FILE, index=False)

print("File updated successfully.")
