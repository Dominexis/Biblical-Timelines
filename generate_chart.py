from pathlib import Path
from typing import cast
import json

PROGRAM_PATH = Path(__file__).parent
GENEALOGIES_PATH = PROGRAM_PATH / "genealogies.json"
CHART_PATH = PROGRAM_PATH / "chart.html"

# Extract genealogical data
with GENEALOGIES_PATH.open("r", encoding="utf-8") as file:
    data: dict[str, dict] = json.load(file)


# Assign sizing parameters
patriarch_height = 20
patriarch_margin = 4
patriarch_padding = 2
patriarch_container_height = patriarch_height + patriarch_margin + patriarch_padding

flood_width = 5
millennia_width = 3
century_width = 1

timeline_padding = 10
timeline_margin = 20
timeline_width = 4000 + timeline_padding*2
timeline_height = 25*patriarch_container_height
timeline_title_size = 25

background_padding = 15
background_width = timeline_width + background_padding*2


# Generate list of timelines
timelines: list[str] = []
for text in data:
    # Generate century and millennia markers
    timestamps: list[str] = []
    for i in range(41):
        timestamps.append(
f"""
                <div style="
                    position: absolute;
                    top: 0px;
                    padding-left: {i*100}px;
                ">
                    <div style="
                        background-color: {"#444444" if i%10 == 0 else "#999999"};
                        height: {timeline_height}px;
                        width: {millennia_width if i%10 == 0 else century_width}px;
                    "></div>
                </div>
""")

    # Generate patriarch entries
    patriarchs: list[str] = []
    year = 0
    patriarch_count = 0
    flood = 0
    for patriarch in cast(list[dict[str, int]], data[text]["genealogy"]):
        fade = False
        if "total" in patriarch:
            lifetime = patriarch["total"]
        elif "beget" in patriarch:
            if "after" in patriarch:
                lifetime = patriarch["beget"] + patriarch["after"]
            else:
                lifetime = patriarch["beget"] + 200
                fade = True
        else:
            lifetime = 200
            fade = True

        patriarchs.append(
f"""
                    <div style="
                        height: {patriarch_container_height}px;
                        padding-left: {year}px;
                    ">
                        <div style="
                            height: {patriarch_height}px;
                            width: {lifetime - patriarch_padding}px;
                            padding-top: {patriarch_padding}px;
                            padding-left: {patriarch_padding}px;
                            background-image: linear-gradient(to right, rgb(0, {70 + (patriarch_count%2)*40}, 0), rgba(0, 0, {120 + (patriarch_count%2)*60}, {0 if fade else 1}));
                            color: white;
                        ">
                            {patriarch["name"]}
                        </div>
                    </div>
""")
        
        if "flood" in patriarch:
            flood = year + patriarch["flood"]
        if "beget" in patriarch:
            year += patriarch["beget"]
        patriarch_count += 1

    timelines.append(
f"""
        <div style="
            margin-bottom: {timeline_margin}px;
            background-color: #dddddd;
            border-radius: 5px;
            padding: {timeline_padding}px;
            width: {timeline_width}px;
        ">
            <span style="font-size: {timeline_title_size}px;">{text}</span>
            <div style="position: relative;">
                {"\n".join(timestamps)}
                <div style="
                    padding-left: {flood}px;
                    height: {timeline_height}px;
                ">
                    <div style="
                        height: {timeline_height}px;
                        width: {flood_width}px;
                        background-color: #660000;
                        color: white;
                    ">
                    </div>
                </div>
                <div style="
                    position: absolute;
                    top: {patriarch_container_height}px;
                ">
                    {"\n".join(patriarchs)}
                </div>
            </div>
        </div>
""")



html = f"""
<!DOCTYPE html>
<html lang="en-US">
    <head>
        <title>Biblical Timelines</title>
    </head>
    <body style="
        font-family: Arial, Helvetica, sans-serif;
        padding: {background_padding}px;
        width: {background_width}px;
    ">
        {"\n".join(timelines)}
    </body>
</html>
"""



with CHART_PATH.open("w", encoding="utf-8") as file:
    file.write(html)