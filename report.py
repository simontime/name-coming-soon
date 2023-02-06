import json, os

# Last build report file name
LAST_REPORT_FILE_NAME = "data/last_report.json"

last_report = None

# Checks if the report file exists
def file_exists():
    return os.path.exists(LAST_REPORT_FILE_NAME)

# Loads last report from file
def load_last_report_from_file():
    global last_report

    with open(LAST_REPORT_FILE_NAME) as file:
        last_report = json.load(file)

# Saves last report to file
def save_last_report_to_file():
    global last_report

    with open(LAST_REPORT_FILE_NAME, "w") as file:
        json.dump(last_report, file)

# Summarises differences between last and current report, overwriting it if new
def process(report):
    global last_report

    # If no last report, save and return
    if last_report is None:
        last_report = report
        save_last_report_to_file()
        return None

    # Make lists of added and removed builds
    added = []
    removed = []

    # Find added builds
    for build in report["flashstationBuild"]:
        if build not in last_report["flashstationBuild"]:
            added.append(build)

    # Find removed builds
    for build in last_report["flashstationBuild"]:
        if build not in report["flashstationBuild"]:
            removed.append(build)

    # No changes
    if added == [] or removed == []:
        return None

    # Overwrite last report
    last_report = report
    save_last_report_to_file()

    return [ added, removed ]
