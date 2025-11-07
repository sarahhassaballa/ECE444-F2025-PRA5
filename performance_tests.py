import requests
import time
import csv
import statistics
import matplotlib.pyplot as plt

# Endpoint for deployed Flask API
ENDPOINT = "http://ece444pra5-env.eba-fx6kixxw.us-east-2.elasticbeanstalk.com/predict"

# Input samples for testing
samples = {
    "fake_1": "Scientists claim the moon is made of cheese.",
    "fake_2": "Hurricane Melissa is destroying downtown Toronto.",
    "real_1": "French is the predominant language in France.",
    "real_2": "Mark Carney is the Prime Minister of Canada.",
}

NUM_REQUESTS = 100
all_latencies = []
labels = []
averages = {}

print("=== Starting Latency Benchmark ===\n")

for label, content in samples.items():
    timings = []
    print(f"Running test for: {label}")

    for i in range(NUM_REQUESTS):
        t0 = time.time()
        res = requests.post(ENDPOINT, json={"message": content})
        t1 = time.time()
        elapsed = t1 - t0
        timings.append(elapsed)
        print(f"  Request {i+1}/{NUM_REQUESTS}: {elapsed:.4f}s (HTTP {res.status_code})")

    # Save to CSV
    csv_file = f"{label}_timing.csv"
    with open(csv_file, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["request_id", "response_time_sec"])
        for idx, duration in enumerate(timings, 1):
            writer.writerow([idx, duration])
    print(f"Saved results to {csv_file}")

    # Store for combined plot
    all_latencies.append(timings)
    labels.append(label)
    averages[label] = statistics.mean(timings)

print("\n=== Generating Combined Boxplot ===")
plt.figure(figsize=(10, 6))
plt.boxplot(all_latencies, labels=labels)
plt.ylim(0.04, 0.1)
plt.title("Latency Distribution Across Test Cases")
plt.ylabel("Latency (seconds)")
plt.xlabel("Test Case")
plt.grid(True)
plt.savefig("combined_latency_boxplot.png")
plt.close()
print("Saved combined_latency_boxplot.png")

print("\n=== Average Latency per Test Case ===")
for label in labels:
    print(f"{label}: {averages[label]:.4f} seconds")

print("\n=== Benchmark Complete ===")
