import pm4py
import os
import math

ALGORITHM = ""

# Check if results folder exists
if not os.path.exists("results"):
  os.makedirs("results")

# Check if in the results folder there is a folder with the name of the algorithm
if not os.path.exists("results" + "/" + ALGORITHM):
  os.makedirs("results" + "/" + ALGORITHM)
else:
  # Delete all files in the algorithm subfolder which start with the algorithm name
  for file in os.listdir("results" + "/" + ALGORITHM):
    os.remove(f"results/{ALGORITHM}/{file}")

# Check if in the models folder there is a folder with the name of the algorithm
if not os.path.exists("models"):
  raise Exception("The models folder does not exist")

# Get a list of all the models for the algorithm
models = []
for model in os.listdir("models" + "/" + ALGORITHM):
  if model.startswith(ALGORITHM):
    models.append(model)

# Write the header to the results csv file
with open("results" + "/" + ALGORITHM + "/" + "results.csv", "w") as f:
  f.write("model,size,activities,is_sound,alignments_fitness,alignments_precision\n")

import concurrent.futures

def process_model(model):
  # Load the model
  net, im, fm = pm4py.read_pnml(os.path.join("models", ALGORITHM, model))

  # The log name is in the name between the _ after the algorithm name and the .pnml
  log_name = model[len(ALGORITHM) + 1:].rsplit(".", 1)[0].rsplit(".xes", 1)[0]
  
  # Load test log from the test_logs folder
  log_test = pm4py.read_xes(os.path.join("test_logs", log_name + ".xes"))
  # Load the log from the logs folder
  log_name = log_name[:-7]  # Remove the seed which is at the end of the log_name with 6 characters and a leading _
  print(os.path.join("logs", log_name + ".xes.gz"))
  log = pm4py.read_xes(os.path.join("logs", log_name + ".xes.gz"))

  size = len(net.transitions) + len(net.places) + len(net.arcs)
  activities = len([t for t in net.transitions if t.label is not None and t.label != ""])
  is_sound = pm4py.analysis.check_soundness(net, im, fm)[0]
  alignments_fitness = {
    'log_fitness': math.nan,
  }
  alignments_precision = math.nan

  # Write the result as append to a results csv file
  with open("results" + "/" + ALGORITHM + "/" + "results.csv", "a") as f:
    f.write(f"{model},{size},{activities},{is_sound},{alignments_fitness['log_fitness']},{alignments_precision}\n")

for model in models:
  process_model(model)

# with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
#   executor.map(process_model, models)
