import glob
import json
import re
from datetime import datetime
import matplotlib.pyplot as plt

# Match your files
files = glob.glob("Phase2Timing_resources_NGT_CMSSW_16_0_X_*.json")

# Extract date + time from filename
date_pattern = re.compile(r"_(\d{4}-\d{2}-\d{2})-(\d{4})\.json$")

results = []

for f in sorted(files):
    m = date_pattern.search(f)
    if not m:
        print(f"Filename does not match date format: {f}")
        continue

    date_str = m.group(1)
    time_str = m.group(2)

    timestamp = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H%M")

    with open(f) as jf:
        data = json.load(jf)

    # Get total values
    total_time_real = data["total"]["time_real"]   # ms
    total_events = data["total"]["events"]

    # Compute per-event time (in ms)
    per_event_time_ms = total_time_real / total_events

    results.append((timestamp, per_event_time_ms))

# Sort results chronologically
results.sort(key=lambda x: x[0])

# Unpack
dates = [r[0] for r in results]
values = [r[1] for r in results]

# Plot
plt.figure(figsize=(10,5))
plt.plot(dates, values, marker="o")
plt.xlabel("Date")
plt.ylabel("Per-event real time (ms)")
plt.title("Trend of per-event time_real from Phase2Timing JSON")
plt.grid(True)
plt.tight_layout()
plt.show()
