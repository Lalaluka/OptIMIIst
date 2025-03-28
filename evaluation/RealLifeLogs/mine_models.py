from pm4py import discover_petri_net_inductive, discover_petri_net_ilp, discover_petri_net_heuristics
import os
import pm4py
import pandas as pd
import time
from optimiist import optimiist

# ALGORITHM_NAME = "IMf"
# ALGORITHM = discover_petri_net_inductive
# ALGORITHM_PARAMS = {"noise_threshold": 0.2}

# ALGORITHM_NAME = "ILP_Miner_0"
# ALGORITHM = discover_petri_net_ilp
# ALGORITHM_PARAMS = {}

# ALGORITHM_NAME = "Heuristic_Miner"
# ALGORITHM = discover_petri_net_heuristics
# ALGORITHM_PARAMS = {}

# ALGORITHM_NAME = "OptIMIISt_filter_new"
# ALGORITHM = optimiist
# ALGORITHM_PARAMS = {}

# If the Folder models does not exist, create it
if not os.path.exists("models"):
    os.makedirs("models")

# Create a subfolder with the name of the algorithm if it does not exist
algorithm_folder = f"models/{ALGORITHM_NAME}"
if not os.path.exists(algorithm_folder):
  os.makedirs(algorithm_folder)

# Delete all files in the algorithm subfolder which start with the algorithm name
for file in os.listdir(algorithm_folder):
  if file.startswith(ALGORITHM_NAME):
    os.remove(f"{algorithm_folder}/{file}")

# Get all Training Logs
logs = []
for log in os.listdir("training_logs_123"):
  logs.append(log)

# DataFrame to store runtimes
runtimes_df = pd.DataFrame(columns=["log", "runtime"])

# Train the model on all training logs and measure runtimes
for log in logs:
  print(log)
  log_df = pm4py.read_xes(f"training_logs_123/{log}")
  start_time = time.time()
  net, im, fm = ALGORITHM(log_df, **ALGORITHM_PARAMS)
  end_time = time.time()
  runtime = end_time - start_time
  runtimes_df = pd.concat([runtimes_df, pd.DataFrame([{"log": log, "runtime": runtime}])], ignore_index=True)
  pm4py.write_pnml(net, im, fm, f"{algorithm_folder}/{ALGORITHM_NAME}_{log}")

# Save runtimes to a CSV file
runtimes_df.to_csv(f"{algorithm_folder}/runtimes.csv", index=False)
