# sample_data/generate_sample_data.py
import csv
import random
from datetime import datetime, timedelta
import os

os.makedirs('sample_data', exist_ok=True)

modules = ["Auth", "Payment", "UI", "Reporting", "Search", "Notification"]
severities = ["Low", "Medium", "High", "Critical"]
error_types = ["NullPointer", "IndexError", "Timeout", "WrongCalculation", "UI-Bug", "Security"]

templates = [
    "Null pointer when token is expired in {module}",
    "Timeout calling external API from {module} during high load",
    "Off-by-one error causing incorrect totals in {module}",
    "UI overflow when displaying long usernames in {module}",
    "Race condition when concurrent requests hit {module}",
    "Missing permission check in {module} leading to security lapse",
    "Incorrect date parsing in {module} leading to wrong report"
]

def generate_row(i):
    module = random.choice(modules)
    severity = random.choices(severities, weights=[0.4,0.3,0.2,0.1])[0]
    et = random.choice(error_types)
    desc = random.choice(templates).format(module=module)
    if random.random() < 0.3:
        desc += " — happens intermittently after specific user workflows"
    date = (datetime.now() - timedelta(days=random.randint(0,365))).strftime("%Y-%m-%d")
    return [i, module, severity, et, desc, date]

def main():
    with open("qa_tool/static/sample_defects.csv", "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id","module","severity","error_type","description","occurrence_date"])
        for i in range(1,501):
            writer.writerow(generate_row(i))
    print("qa_tool/static/sample_defects.csv generated (500 rows)")

if __name__ == "__main__":
    main()
