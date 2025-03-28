import pm4py
from pm4py import discover_eventually_follows_graph

def get_log_statistics(log):
  if len(log) == 0:
    return {
      "dfg": {},
      "efg": {},
      "start_activities": {},
      "end_activities": {},
      "activities": []
    }

  dfg, start_activities, end_activities = pm4py.discover_dfg(log)

  activities = log["concept:name"].unique()

  # Fill non existing relationships in dfg with 0
  for a in activities:
    for b in activities:
      if (a,b) not in dfg: dfg[(a,b)] = 0

  class LazyEFG:
    def __init__(self, log):
      self.log = log
      self._efg = None

    def __getitem__(self, key):
      if self._efg is None:
        self._efg = discover_eventually_follows_graph(self.log)
      return self._efg.get(key, 0)

    def __contains__(self, key):
      if self._efg is None:
        self._efg = discover_eventually_follows_graph(self.log)
      return key in self._efg

  efg = LazyEFG(log)

  return {
    "dfg": dfg,
    "efg": efg,
    "start_activities": start_activities,
    "end_activities": end_activities,
    "activities": activities
  }
