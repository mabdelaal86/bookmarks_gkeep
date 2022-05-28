from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Tuple
import csv
import argparse
import json

InstapaperInput = Dict[str, List[Dict]]
KeepOutput = Tuple[str, Dict[str, str]]


def main():
    args = parse_args()
    path = Path(args.takeout_path)
    bookmarks = read_bookmarks(path)
    groups = group_by_labels(bookmarks)
    export_instapaper(groups)


def parse_args():
    parser = argparse.ArgumentParser(description="Convert Google Keep bookmarks into Instapaper format")
    parser.add_argument("takeout_path", help="Google Keep takeout path (.../Takeout/Keep)")
    return parser.parse_args()


def read_bookmarks(path: Path) -> Iterable[KeepOutput]:
    """
    Read bookmarks from google keep backup files.
    """
    if not path.is_dir:
        raise f"'{path}' is not a directory!"
    for file in path.iterdir():
        # Skip not json files
        if not file.name.endswith(".json"):
            continue
        item: Dict = json.loads(file.read_text())
        yield file.name, parse_item(item)


def parse_item(item: Dict) -> Dict[str, str]:
    # Skip trashed items
    if item["isTrashed"]:
        return {}
    annotations: List[Dict] = item.get("annotations", [])
    # Skip non weblink items or items with multiple links
    if len(annotations) != 1 or annotations[0]["source"] != "WEBLINK":
        return {}
    return {
        "url": annotations[0]["url"],
        "title": str(item["title"] or annotations[0]["title"]).replace("\n", " ").strip(),
        "labels": ",".join(label["name"] for label in item.get("labels", [])),
    }


def group_by_labels(data: Iterable[KeepOutput]) -> InstapaperInput:
    """
    Group bookmark items by label and log ignored items into ignore.txt file
    """
    res = {}
    cur_dt = datetime.now()

    with open("ignore.txt", mode="w") as ig_file, open("instapaper.csv", mode="w") as csv_file:
        writer = csv.writer(csv_file, delimiter=",")
        writer.writerow(["URL", "Title", "Selection", "Folder", "Timestamp"])
        for filename, item in data:
            if item:
                res.setdefault(item["labels"], []).append(item)
                writer.writerow([item["url"], item["title"], "", item["labels"], int(cur_dt.timestamp())])
            else:
                ig_file.write(f"{filename}\n")

    return res


def export_instapaper(data: InstapaperInput):
    """
    Export bookmarks into Instapaper format
    """
    with open("instapaper.html", mode="w") as html_file:
        html_file.write("""<!DOCTYPE html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<title>Instapaper: Export</title>
</head>
<body>
""")

        for labels, items in data.items():
            html_file.write(f"\n<h1>{labels}</h1>\n\n<ol>\n")
            for item in items:
                html_file.write(f'<li><a href="{item["url"]}">{item["title"]}</a>\n')
            html_file.write("</ol>\n")

        html_file.write("""
</body>
</html>
""")


if __name__ == "__main__":
    main()
