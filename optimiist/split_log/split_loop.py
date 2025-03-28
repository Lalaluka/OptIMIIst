import pandas as pd
from typing import List
from .split_tau_loop import split_tau_loop

def split_loop(log: pd.DataFrame, activities_partition_1: List[str], activities_partition_2: List[str], empty_cases) -> tuple[pd.DataFrame, pd.DataFrame, int, int]:
    """
    Split the log into two partitions based on the activities and the operator
    :param log: the log to be split
    :param activities_partition_1: activities to be included in the first partition
    :param activities_partition_2: activities to be included in the second partition
    :return: the two partitions and the number of empty traces in each partition
    """
    # Tau Loops are handeled seperatly
    if activities_partition_2 == []:
        return split_tau_loop(log, empty_cases)
    
    empty_cases_a = [empty_cases]
    
    def wrapper(case_df):
        df, count = split_case_in_loop(case_df, activities_partition_1, activities_partition_2)
        empty_cases_a[0] += count
        return df
    log = log.groupby("case:concept:name", group_keys=False)[log.columns].apply(lambda x: wrapper(x))

    empty_cases = empty_cases_a[0]

    log_partition_1 = log[log["concept:name"].isin(activities_partition_1)]
    log_partition_2 = log[log["concept:name"].isin(activities_partition_2)]
    empty_cases_1 = empty_cases
    empty_cases_2 = 0
    return log_partition_1, log_partition_2, empty_cases_1, empty_cases_2

def split_case_in_loop(case_df, activities_partition_1, activities_partition_2) -> tuple[pd.DataFrame, int]:
    """
    Split the case in the loop
    :param trace_df: the trace to be split
    :param activities_partition_1: activities to be included in the first partition
    :param activities_partition_2: activities to be included in the second partition
    :return: the traces resulting from splitting the case
    """
    case_number = 0
    case_id_list = []
    empty_cases = 0
    partition1_activity = False
    
    # If the first activity is in partition 2 increment empty_cases
    if case_df.iloc[0]["concept:name"] in activities_partition_2:
        empty_cases += 1
    # If the last activity is in partition 2 increment empty_cases
    if case_df.iloc[-1]["concept:name"] in activities_partition_2:
        empty_cases += 1

    for activity_index in range(0, case_df.shape[0]):
        case_id_list.append(str(case_df.iloc[activity_index]["case:concept:name"]) + "🚫️SPLIT_" + str(case_number))
        if case_df.iloc[activity_index]["concept:name"] not in activities_partition_1 != case_df.iloc[activity_index - 1]["concept:name"] in activities_partition_1:
            case_number += 1
        if case_df.iloc[activity_index]["concept:name"] in activities_partition_1:
            partition1_activity = True

    # If there are no activities from partition 1 one empty case is sufficient
    if not partition1_activity:
        empty_cases = 2

    case_df["case:concept:name"] = case_id_list
    return case_df, empty_cases