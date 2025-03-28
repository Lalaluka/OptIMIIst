import pandas as pd

def split_tau_loop(log: pd.DataFrame, empty_cases: int) -> tuple[pd.DataFrame, pd.DataFrame, int, int]:
    """
    Split the log assuming a tau loop
    :param log: the log to be split
    :return: the two partitions and the number of empty traces in each partition
    """
    log_partition_2 = pd.DataFrame(columns=log.columns)
    empty_cases_1 = empty_cases
    empty_cases_2 = 0

    start = log.groupby("case:concept:name").first().groupby("concept:name").size()
    end = log.groupby("case:concept:name").last().groupby("concept:name").size()

    log = log.groupby("case:concept:name", group_keys=False)[log.columns].apply(lambda x: split_case_in_tau_loop(x, start, end))

    return log, log_partition_2, empty_cases_1, empty_cases_2

def split_case_in_tau_loop(case_df, start, end):
    """
    Split the case in the tau loop
    :param trace_df: the trace to be split
    :param start: the start of the loop
    :param end: the end of the loop
    :return: the traces resulting from splitting the case
    """
    # If the trace has only one event, return it unchanged
    if case_df.shape[0] == 1: return case_df

    case_number = 0
    case_id_list = []

    for activity_index in range(0, case_df.shape[0] - 1):
        case_id_list.append(str(case_df.iloc[activity_index]["case:concept:name"]) + "🚫️SPLIT_" + str(case_number))
        # If Event is a start event and the last was a end event, increment case_number
        if str(case_df.iloc[activity_index + 1]["concept:name"]) in start and str(case_df.iloc[activity_index]["concept:name"]) in end:
            case_number += 1
    case_id_list.append(str(case_df.iloc[-1]["case:concept:name"]) + "🚫️SPLIT_" + str(case_number))
    case_df["case:concept:name"] = case_id_list
    return case_df
