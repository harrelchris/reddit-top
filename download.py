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
    request = urllib.request.Request("https://www.reddit.com/r/all/top.json?sort=top&t=day")
    request.add_header("Accept", "image/avif,image/webp,*/*")
    request.add_header("Accept-Language", "en-US,en;q=0.9")
    request.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    request.add_header("Accept-Encoding", "gzip, deflate, br")
    request.add_header("Cache-Control", "no-cache")
    request.add_header("Dnt", "1")
    request.add_header("Pragma", "no-cache")
    request.add_header("Sec-Ch-Ua", '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"')
    request.add_header("Sec-Ch-Ua-Mobile", "?0")
    request.add_header("Sec-Ch-Ua-Platform", '"Windows"')
    request.add_header("Sec-Fetch-Dest", "document")
    request.add_header("Sec-Fetch-Mode", "navigate")
    request.add_header("Sec-Fetch-Site", "none")
    request.add_header("Sec-Fetch-User", "?1")
    request.add_header("Sec-Gpc", "1")
    request.add_header("Upgrade-Insecure-Requests", "1")

    try:
        response = urllib.request.urlopen(request)
    except urllib.error.HTTPError as e:
        sys.stderr.write(f"{e}\n")
        attempts += 1
        if attempts > 2:
            sys.stderr.write("Failed after 3 attempts\n")
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
