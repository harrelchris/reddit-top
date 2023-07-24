import datetime
import json
import pathlib
import sys
import urllib.error
import urllib.request

attrs = [
    "selftext",
    "title",
    "subreddit_name_prefixed",
    "upvote_ratio",
    "ups",
    "score",
    "thumbnail",
    "is_self",
    "created_utc",
    "num_comments",
    "permalink",
    "url",
    "is_video",
    "subreddit",
    "author",
]

posts = []
attempts = 0

while True:
    try:
        response = urllib.request.urlopen("https://www.reddit.com/r/all/top.json?sort=top&t=day")
    except urllib.error.HTTPError as e:
        attempts += 1
        if attempts > 3:
            sys.stderr.write(f"Failed after 3 attempts: {e}\n")
            sys.exit(1)
        continue
    else:
        response_body = response.read()
        response_json = json.loads(response_body)
        response_data = response_json["data"]
        children = response_data["children"]
        for child in children:
            data = child["data"]
            post = {attr: data[attr] for attr in attrs}
            posts.append(post)
        response.close()
        break

DATA = pathlib.Path(__file__).parent / "data"
DATE = datetime.datetime.now().strftime("%Y-%m-%d")
fp = f"{DATA / DATE}.json"

with open(fp, "w", encoding="utf-8") as f:
    json.dump(posts, f)
