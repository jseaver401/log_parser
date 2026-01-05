
#!/usr/bin/env python3
import re
import csv
import operator

# Regular expression to capture INFO/ERROR, the message, and the username
pattern = re.search(r'(INFO|ERROR)\s+(.*?)\s+\(([^)]+)\)')

# Initialize dictionaries
error_counts = {}   # key: error message, value: count
per_user = {}       # key: username, value: {"INFO": n, "ERROR": m}

# Open and read the log file
with open("syslog.log", "r") as logfile:
    for line in logfile:
        match = pattern.search(line)
        if match:
            level = match.group(1)          # INFO or ERROR
            message = match.group(2).strip()
            user = match.group(3).strip()

            # Update per_user counts
            if user not in per_user:
                per_user[user] = {"INFO": 0, "ERROR": 0}
            per_user[user][level] += 1

            # Update error_counts only if it's an ERROR
            if level == "ERROR":
                error_counts[message] = error_counts.get(message, 0) + 1

# Sort results
errors_sorted = sorted(error_counts.items(), key=operator.itemgetter(1), reverse=True)
users_sorted = sorted(per_user.items(), key=operator.itemgetter(0))

# Prepare CSV rows
errors_csv = [("Error", "Count")] + [(msg, count) for msg, count in errors_sorted]
users_csv = [("Username", "INFO", "ERROR")] + [
    (user, counts["INFO"], counts["ERROR"]) for user, counts in users_sorted
]

# Write error_message.csv
with open("error_message.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(errors_csv)

# Write user_statistics.csv
with open("user_statistics.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(users_csv)

print("Reports generated: error_message.csv and user_statistics.csv")





