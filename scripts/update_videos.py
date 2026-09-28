"""Refresh the 'latest videos' block in README.md from the channel's public RSS feed."""
import html
import re
import urllib.request
import xml.etree.ElementTree as ET

CHANNEL_ID = "UCbhalUreODy-r-7fX1NoYvQ"
FEED = f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}"
NS = {"a": "http://www.w3.org/2005/Atom", "yt": "http://www.youtube.com/xml/schemas/2015"}
START, END = "<!-- VIDEOS:START -->", "<!-- VIDEOS:END -->"

with urllib.request.urlopen(FEED, timeout=20) as r:
    root = ET.fromstring(r.read())

cells = []
for e in root.findall("a:entry", NS)[:3]:
    vid = e.find("yt:videoId", NS).text
    title = html.escape(e.find("a:title", NS).text.replace(" @worth_knowing2", "").strip(), quote=True)
    if len(title) > 70:
        title = title[:67].rstrip() + "..."
    cells.append(
        f'<td width="33%" align="center"><a href="https://youtu.be/{vid}">'
        f'<img src="https://i.ytimg.com/vi/{vid}/mqdefault.jpg" width="100%" alt="{title}"/></a><br/>'
        f'<sub>{title}</sub></td>'
    )

block = f"{START}\n<table><tr>\n" + "\n".join(cells) + f"\n</tr></table>\n{END}"
readme = open("README.md", encoding="utf-8").read()
new = re.sub(re.escape(START) + r".*?" + re.escape(END), lambda m: block, readme, flags=re.S)
if new != readme:
    open("README.md", "w", encoding="utf-8", newline="\n").write(new)
    print("README updated")
else:
    print("no change")
