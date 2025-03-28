from typing import List
import pandas as pd
from pm4py.objects.process_tree.obj import Operator
from optimiist.split_log.split_base_operator import split_base_operator
from optimiist.split_log.split_loop import split_loop
from optimiist.split_log.split_tau_loop import split_tau_loop

def split_log(log: pd.DataFrame, operator: Operator, activities_partition_1: List[str], activities_partition_2: List[str], empty_cases: int, filtered_activities: List[str] = []) -> tuple[pd.DataFrame, pd.DataFrame, int, int]:
    """
    Split the log into two partitions based on the activities and the operator
    :param log: the log to be split
    :param activities_partition_1: activities to be included in the first partition
    :param activities_partition_2: activities to be included in the second partition
    :return: the two partitions and the number of empty traces in each partition
    """
    # Remove filtered activities
    log = log[~log["concept:name"].isin(filtered_activities)]
    empty_cases += log["case:concept:name"].nunique() - log[~log["concept:name"].isin(filtered_activities)]["case:concept:name"].nunique()

    # TauSkip
    if operator == Operator.XOR and activities_partition_2 == []:
        return log, pd.DataFrame(), 0, 0

    # TauLoop
    if operator == Operator.LOOP and activities_partition_2 == []:
        return split_tau_loop(log, empty_cases)

    # Loop
    if operator == Operator.LOOP and activities_partition_2 != []:
        return split_loop(log, activities_partition_1, activities_partition_2, empty_cases)
    
    # XOR, Sequence, Parallel
    log_partition_1, log_partition_2, empty_cases_1, empty_cases_2 = split_base_operator(log, activities_partition_1, activities_partition_2, empty_cases)

    # We only put the empty cases in one XOR partition in hope they are handled there
    if operator == Operator.XOR:
        empty_cases_1 = empty_cases
        empty_cases_2 = 0

    return log_partition_1, log_partition_2, empty_cases_1, empty_cases_2
