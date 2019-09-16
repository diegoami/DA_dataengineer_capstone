import csv
import json
import os
import traceback


def export_to_csv(exp_data, exp_output, map_query_columns):
    with open(exp_output, 'w', encoding="utf-8") as ehandle:
        print("Writing to {}".format(exp_output))

        f = csv.writer(ehandle)

        f.writerow(map_query_columns.values())
        for item in exp_data:
            f.writerow(item.values())


def try_read_data_from_json_file(file_output):
    rel_data = None
    if os.path.isfile(file_output):
        print("Reading data from file {}".format(file_output))
        with open(file_output, 'r', encoding="utf-8") as fhandle:
            try:
                rel_data = json.load(fhandle)
            except ValueError as ve:
                print("Could not read data from file {}".format(file_output))
                traceback.print_exc(ve)
    return rel_data