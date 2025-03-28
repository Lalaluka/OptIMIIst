import pandas as pd

from pm4py.util.compression import util as comut
from pm4py.algo.discovery.inductive.dtypes.im_ds import IMDataStructureUVCL
from pm4py.algo.discovery.inductive.cuts.factory import CutFactory
from pm4py.algo.discovery.inductive.variants.instances import IMInstance

def get_inductive_miner_cuts(log: pd.DataFrame) -> tuple[str, list[str], list[str]]:
    """
    Get the cuts of the inductive miner
    :param log: the log to be split
    :return: the operator and the activities of the two partitions
    """
    uvcl = comut.get_variants(
        comut.project_univariate(log))
    cut = CutFactory.find_cut(IMDataStructureUVCL(uvcl), IMInstance.IM, parameters={})
    if not cut: return None
    operator = cut[0].operator
    partition_1 = list(cut[1][0].dfg.end_activities.keys()) + list(cut[1][0].dfg.start_activities.keys())
    partition_1 += sum([[a, b] for a, b in list(cut[1][0].dfg.graph.keys())], [])
    partition_2 = []
    for i in range(1, len(cut[1])):
        partition_2 += list(cut[1][i].dfg.end_activities.keys()) + list(cut[1][i].dfg.start_activities.keys())
        partition_2 += sum([[a, b] for a, b in list(cut[1][i].dfg.graph.keys())], [])
    return operator, list(set(partition_1)), list(set(partition_2))
