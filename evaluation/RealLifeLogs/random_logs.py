import pm4py
import random

seeds = [
  "440326", # Imatriculation RWTH
  "178181", # Imatriculation HfTL
  "230225", # Federal Election 2025
  "260921", # Federal Election 2021
  "240917"  # Federal Election 2017
]

# Read logs.json file
import json
with open("logs.json", "r") as f:
    logs = json.load(f)

# Create Training Logs and Test Logs directories
import os
import shutil

# Delete directories if they already exist
if os.path.exists("training_logs"):
  shutil.rmtree("training_logs")
if os.path.exists("test_logs"):
  shutil.rmtree("test_logs")

# Create directories
os.makedirs("training_logs")
os.makedirs("test_logs")

for log in logs:
  print("Log: ", log["name"])

  for seed in seeds:
    print("Seed: ", seed)

    log_df = pm4py.read_xes(log["path"])
    # Split the log into 80/20 train/test split based on the number of traces
    # Get list of trace ids
    trace_ids = log_df["case:concept:name"].unique()
    # Shuffle the list of trace ids
    random.seed(seed)
    random.shuffle(trace_ids)
    # Split the trace ids
    train_ids = trace_ids[:int(len(trace_ids) * 0.8)]

    # Create training log
    train_log = log_df[log_df["case:concept:name"].isin(train_ids)]

    # Remove any columns which are not concept:name time:timestamp case:concept:name
    train_log = train_log[["case:concept:name", "concept:name", "time:timestamp"]]

    pm4py.write_xes(train_log, f"training_logs/{log['name']}_{seed}.xes")

    # Create test log
    test_log = log_df[~log_df["case:concept:name"].isin(train_ids)]
    test_log = test_log[["case:concept:name", "concept:name", "time:timestamp"]]
    pm4py.write_xes(test_log, f"test_logs/{log['name']}_{seed}.xes")
