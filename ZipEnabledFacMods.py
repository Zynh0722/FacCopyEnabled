import sys
import os
import json
import re
from pathlib import Path

# fetch path from argument
try:
    mods_folder = Path(sys.argv[1])
except:
    print("Please pass the mods folder")

# fetch mod list
with open(mods_folder / "mod-list.json") as f:
    mod_list = json.load(f)["mods"]

# filter enabled mods
mod_list = [mod for mod in mod_list if mod["enabled"] and mod["name"] != "base"]

mod_files = [
    {"file": file, "name": "_".join(file.split("_")[:-1])}
    for file in os.listdir(mods_folder)
]


# mod_list = [re.compile(mod["name"] + "_\d+\.\d+\.\d+\.zip") for mod in mod_list]

for i in mod_files:
    print(i)


# print(json.load(mods_folder / "mods-list.json"))
