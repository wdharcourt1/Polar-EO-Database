#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: Adrien Wehrlé, University of Zurich, Switzerland

"""

import json
import gspread
import os
import gspread_dataframe as gd

# set upload path
output_path = "./data"

# setup API account
gc = gspread.service_account("./apecs-remote-sensing-database-e3d1516b4935.json")

# Open a sheet from a spreadsheet in one go
sheet = gc.open("APECS Remote Sensing Database - AW tests").sheet1

# %% pull database (db) from Google sheets
db = gd.get_as_dataframe(sheet)

# remove unnamed rows
db_r_filtered = db[db["RS dataset name"].str.contains("Unamed") == False]

# remove unnamed columns
columns_to_keep = [c for c in db_r_filtered.columns if "unnamed" not in c.lower()]

db_rc_filtered = db_r_filtered[columns_to_keep]

# convert dataframe to dict
db_dict = db_rc_filtered.to_dict(orient="index")

# save json object in json files
for sat, content in db_dict.items():

    rs_dataset_name = content["RS dataset name"]

    # continue if empty line
    if isinstance(content["RS dataset name"], float):
        continue

    else:
        # remove bad characters for file names if appears in data set name
        # and replace them all by a dash (should be improved)
        rs_dataset_name_formatted = (
            rs_dataset_name.replace(os.sep, "-")
            .replace(" ", "-")
            .replace("(", "-")
            .replace(")", "-")
            .replace(".", "-")
        )

        with open(f"{output_path}/{rs_dataset_name_formatted}.json", "w") as outfile:
            json.dump(content, outfile, indent=4)
