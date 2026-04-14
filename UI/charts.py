# Create charts for the dashboard
import matplotlib
from matplotlib import cm, pyplot as plt
from collections import Counter
from datetime import datetime, timedelta
from io import BytesIO

# Import the custom modules
from jobapps import JobApps

class Charts:
    def __init__(self, job_apps_data):
        self.job_apps_data = job_apps_data
    
    def generate_image_response(self, fig):
        """Helper function to generate an image response."""
        img = BytesIO()  # in-memory file to hold image data
        fig.savefig(img, format="png", bbox_inches="tight")
        img.seek(0)
        return img

    def gen_monthly_chart(self):
        # Group by month (store datetime objects)
        months = []
        for job in self.job_apps_data:
            date_str = job.get("date")
            if date_str:
                try:
                    dt = datetime.strptime(date_str, "%Y-%m-%d")
                    month_dt = datetime(dt.year, dt.month, 1)  # normalize to month
                    months.append(month_dt)
                except ValueError:
                    continue

        # Count per month
        month_counts = Counter(months)

        # Sort months
        sorted_months = sorted(month_counts.keys())
        counts = [month_counts[m] for m in sorted_months]

        # Format labels for display
        labels = [m.strftime("%b %Y") for m in sorted_months]

        # Plot
        fig, ax = plt.subplots(figsize=(7, 5))
        ax.plot(labels, counts, marker="o", linestyle="-", color="green")
        ax.set_title("Applications by Month", fontsize=16, fontweight="bold")
        ax.set_xlabel("Month")
        ax.set_ylabel("Applications")
        ax.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Use helper function to generate image response
        img = self.generate_image_response(fig)  # Call the helper method
        plt.close(fig)

        return img

    def gen_status_chart(self):
        # Extract status for each record and include it in statuses list
        statuses = [job["status"] for job in self.job_apps_data if job["status"]]
        # Count by status
        status_counts = Counter(statuses)

        # Enforce custom order
        status_order = ["Applied", "Interviewed", "Rejected"]

        labels = status_order
        values = [status_counts.get(status, 0) for status in status_order]

        # Create bar chart
        fig, ax = plt.subplots(figsize=(7, 5))
        colors = ["#4CAF50", "#FFC107", "#F44336"]  # color palettes
        bars = ax.bar(labels, values, color=colors)
        
        # Add labels
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                height + 0.1,
                str(height),
                ha="center",
                va="bottom"
                )
        
        ax.set_title("Applications by Status", fontsize=16, fontweight="bold")
        ax.set_xlabel("Status")
        ax.set_ylabel("Count")

        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(axis="y", linestyle="--", alpha=0.6)

        plt.tight_layout()

        # Use helper function to generate image response
        img = self.generate_image_response(fig)  # Call the helper method
        plt.close(fig)

        return img

    def gen_role_chart(self):
        # Extract role for each record and include it in roles list
        roles = [job.get("role") for job in self.job_apps_data if job.get("role")]
        role_counts = Counter(roles)

        # Use actual data (no hardcoding)
        labels = list(role_counts.keys())
        values = list(role_counts.values())

        # Optional: sort by most common
        labels, values = zip(*sorted(role_counts.items(), key=lambda x: x[1], reverse=True))

        fig, ax = plt.subplots(figsize=(7, 5))
        colors = cm.tab20.colors[:len(labels)] # dynamic colors
        bars = ax.barh(labels, values, color=colors)

        # Value labels
        for bar in bars:
            width = bar.get_width()
            ax.text(
                width + max(values)*0.01,
                bar.get_y() + bar.get_height() / 2,
                f"{int(width)}",
                va="center",
                ha="left"
                )

        ax.set_title("Applications by Role", fontsize=16, fontweight="bold")
        ax.set_xlabel("Role")
        ax.set_ylabel("Count")

        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(axis="y", linestyle="--", alpha=0.6)

        # Rotate labels if long (very useful for roles)
        plt.xticks(rotation=30, ha="right")

        plt.tight_layout()

        # Use helper function to generate image response
        img = self.generate_image_response(fig)  # Call the helper method
        plt.close(fig)

        return img

    def gen_followup_chart(self):
        # Count followed-up values (0 = No, 1 = Yes)
        followed = [int(job["followedup"]) for job in self.job_apps_data if job["followedup"] != ""]
        follow_counts = Counter(followed)

        # Labels and values
        labels = ["Not Followed Up", "Followed Up"]
        values = [
            follow_counts.get(0, 0),
            follow_counts.get(1, 0)
        ]

        # Create pie chart
        fig, ax = plt.subplots(figsize=(5, 5))
        colors = ["#F44336", "#4CAF50"]  # red = no, green = yes

        ax.pie(
            values,
            labels=labels,
            autopct="%1.1f%%",
            startangle=90,
            colors=colors
        )

        ax.set_title("Follow-Up Status", fontsize=16, fontweight="bold")

        plt.tight_layout()

        # Use helper function to generate image response
        img = self.generate_image_response(fig)  # Call the helper method
        plt.close(fig)

        return img
