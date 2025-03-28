import pm4py
import os
from pulp import *

def get_solver():
  solver_name = os.getenv('SOLVER', 'PULP_CBC_CMD')
  try:
    return globals()[solver_name]
  except KeyError:
    return PULP_CBC_CMD

def extract_partitions_pulp(x) -> tuple[list[str], list[str]]:
  partition_1 = []
  partition_2 = []
  for key in x:
    if x[key].varValue == 1:
      partition_1.append(key)
    else:
      partition_2.append(key)
  return partition_1, partition_2

def extract_filtered_activity_pulp(n) -> str:
  for key in n:
    if n[key].varValue == 1:
      return key
  return None

_cache = {}

def build_skip_dfg(log, activities):

  cache_key = log.to_string()
  if cache_key in _cache:
    return _cache[cache_key]

  dfg, start_activities, end_activities = pm4py.discover_dfg(log)

  one_skip_dfg = {}
  skips = {}
  start_activities_skips = {}
  end_activities_skips = {}

  for a in activities:
    start_activities_skips[a] = {key: value for key, value in start_activities.items() if key != a}
    end_activities_skips[a] = {key: value for key, value in end_activities.items() if key != a}
    for b in activities:
      one_skip_dfg[(a,b)] = 0
      for c in activities:
        skips[(a,(b,c))] = 0

  # Go through the log trace by trace
  for trace in log["case:concept:name"].unique():
    trace_df = log[log["case:concept:name"] == trace]
    tail = None

    if trace_df.shape[0] >= 2 and trace_df["concept:name"].unique().shape[0] > 1:

      if trace_df.iloc[0]["concept:name"] not in start_activities_skips:
        start_activities_skips[trace_df.iloc[0]["concept:name"]] = {}
      next_activity_index = 1
      while next_activity_index < len(trace_df) and trace_df.iloc[next_activity_index]["concept:name"] == trace_df.iloc[0]["concept:name"]:
        next_activity_index += 1
      if next_activity_index < len(trace_df):
        if trace_df.iloc[next_activity_index]["concept:name"] not in start_activities_skips[trace_df.iloc[0]["concept:name"]]:
          start_activities_skips[trace_df.iloc[0]["concept:name"]][trace_df.iloc[next_activity_index]["concept:name"]] = 0
        start_activities_skips[trace_df.iloc[0]["concept:name"]][trace_df.iloc[next_activity_index]["concept:name"]] += 1

      if trace_df.iloc[-1]["concept:name"] not in end_activities_skips:
        end_activities_skips[trace_df.iloc[-1]["concept:name"]] = {}
      next_activity_index = len(trace_df) - 2
      while next_activity_index >= 0 and trace_df.iloc[next_activity_index]["concept:name"] == trace_df.iloc[-1]["concept:name"]:
        next_activity_index -= 1
      if next_activity_index >= 0:
        if trace_df.iloc[next_activity_index]["concept:name"] not in end_activities_skips[trace_df.iloc[-1]["concept:name"]]:
          end_activities_skips[trace_df.iloc[-1]["concept:name"]][trace_df.iloc[next_activity_index]["concept:name"]] = 0
        end_activities_skips[trace_df.iloc[-1]["concept:name"]][trace_df.iloc[next_activity_index]["concept:name"]] += 1


    for i in range(len(trace_df) - 1):
      a = trace_df.iloc[i]["concept:name"]
      b = trace_df.iloc[i + 1]["concept:name"]
      one_skip_dfg[(a,b)] += 1
      if tail is not None:
        skips[(a, (tail, b))] += 1
      tail = a

  _cache[cache_key] = one_skip_dfg, skips, start_activities_skips, end_activities_skips

  return one_skip_dfg, skips, start_activities_skips, end_activities_skips
