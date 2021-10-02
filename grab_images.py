import re
import requests
from os import path, makedirs
from urllib.parse import urlparse

with open("Twinetroid.html", "r", encoding="utf-8") as twinetroidfile:
    lines = twinetroidfile.readlines()

REGEX_LINE = r"&quot;(https?://www\.metroid-database\.com/.+?jpg)&quot;"
regex = re.compile(REGEX_LINE)
local_list = []
links = []
idx = 1
for _, line in enumerate(lines):
    if matches := regex.findall(line):
        matches_done = 0
        hold_line = None
        for m in matches:
            parsed_result = urlparse(m)
            filename = path.basename(parsed_result.path)
            links.append([m, filename])
            idx += 1
            res = re.subn(REGEX_LINE, f"./images/{path.basename(parsed_result.path)}", line)
            if res[1] == 1:
                new_line = res[0]
            else:
                if hold_line:
                    new_line = re.sub(REGEX_LINE, f"./images/{path.basename(parsed_result.path)}", hold_line, 1)
                else:
                    hold_line = re.sub(REGEX_LINE, f"./images/{path.basename(parsed_result.path)}", line, 1)
        local_list.append(new_line)
    else:
        local_list.append(line)

makedirs("images", exist_ok=True)
for link in links:
    r = requests.get(link[0])
    with open(f"images/{link[1]}", "wb") as f:
        f.write(r.content)

out = "\n".join(local_list)
with open(f"Twinetroid_local.html", "w", encoding="utf-8") as f:
    f.write(out)
with open(f"index.html", "w", encoding="utf-8") as f:
    f.write(out)
