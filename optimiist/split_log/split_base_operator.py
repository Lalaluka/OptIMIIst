from typing import List
import pandas as pd

def split_base_operator(log: pd.DataFrame, activities_partition_1: List[str], activities_partition_2: List[str], empty_cases) -> tuple[pd.DataFrame, pd.DataFrame, int, int]:
    """
    Split the log into two partitions based on the activities works for Sequence, XOR and Parallel splits
    :param log: the log to be split
    :param activities_partition_1: activities to be included in the first partition
    :param activities_partition_2: activities to be included in the second partition
    :return: the two partitions and the number of empty traces in each partition
    """
    log_partition_1 = log[log["concept:name"].isin(activities_partition_1)]
    log_partition_2 = log[log["concept:name"].isin(activities_partition_2)]
    empty_cases_1 = log["case:concept:name"].nunique() - log_partition_1["case:concept:name"].nunique()
    empty_cases_2 = log["case:concept:name"].nunique() - log_partition_2["case:concept:name"].nunique()
    return log_partition_1, log_partition_2, empty_cases_1 + empty_cases, empty_cases_2 + empty_cases