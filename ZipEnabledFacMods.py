import sys
import os
import json
import zipfile
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
mod_list = [mod["name"] for mod in mod_list if mod["enabled"] and mod["name"] != "base"]


# damned versioning
def parse_mod_file(file):
    split = file.split("_")
    name = "_".join(split[:-1])
    version = split[-1].split(".")[:-1]

    return {"file": file, "name": name, "version": version}


# get all zip file names, and match them with their appearance in the mod_list
mod_files = [parse_mod_file(file) for file in os.listdir(mods_folder)]


# damned mod versioning 2 electric boogaloo
def cmp_version(v_a, v_b):
    for node in [0, 1, 2]:
        if v_a[node] > v_b[node]:
            return v_a
        elif v_b[node] > v_a[node]:
            return v_b

    return v_a


latest_versions = {}
for file in mod_files:
    if file["name"] in latest_versions:
        latest_versions[file["name"]] = cmp_version(
            latest_versions[file["name"]], file["version"]
        )
    else:
        latest_versions[file["name"]] = file["version"]

# filter latest versions
mod_files = [
    file for file in mod_files if file["version"] == latest_versions[file["name"]]
]

# filter in mod list, discard unneeded info
mod_files = [file["file"] for file in mod_files if file["name"] in mod_list]

with zipfile.ZipFile("enabled_mods.zip", mode="w") as archive:
    for file in mod_files:
        path = mods_folder / file
        print(f"Zipping {path}...")
        archive.write(path, arcname=file)

    print("Archive Complete!~")
