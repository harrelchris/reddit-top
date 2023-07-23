import datetime
import json
import pathlib
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

with urllib.request.urlopen("https://www.reddit.com/r/all/top.json?sort=top&t=day") as response:
    response_body = response.read()
    response_json = json.loads(response_body)
    response_data = response_json["data"]
    children = response_data["children"]
    for child in children:
        data = child["data"]
        post = {attr: data[attr] for attr in attrs}
        posts.append(post)

DATA = pathlib.Path(__file__).parent / "data"
DATE = datetime.datetime.now().strftime("%Y-%m-%d")
fp = f"{DATA / DATE}.json"

with open(fp, "w", encoding="utf-8") as f:
    json.dump(post, f)
