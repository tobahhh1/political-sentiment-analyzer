from .request_types import RedditRequest
from .response_types import RedditResponse
import praw
import praw.models

_RedditClient = praw.Reddit

def login_to_reddit(
    client_id: str,
    client_secret: str,
    password: str,
    user_agent: str,
    username: str,
) -> _RedditClient:
    return praw.Reddit(
        client_id = client_id,
        client_secret = client_secret,
        password = password,
        user_agent = user_agent,
        username = username,
    )


def get_reddit_posts(client: _RedditClient, request: RedditRequest) -> RedditResponse:
    """
    Fetches posts and comments from Reddit based on the provided request using PRAW.
    Args:
        client (praw.Reddit): The PRAW Reddit client instance, returned from login_to_reddit.
        request (RedditRequest): The request object containing subreddit and post details.
    Returns:
        RedditResponse: A response object containing the fetched posts and comments.
    """

    # AI Generated, didn't read.
    # Sorry, it was so easy.

    def fetch_comments(praw_comment_forest, comment_req, depth=1, parent_upvotes=None):
        comments = []
        count = 0
        for praw_comment in praw_comment_forest:
            if hasattr(praw_comment, "body"):
                upvotes = praw_comment.score
                # Stop criteria
                if "upvotes" in comment_req["stop_at"]:
                    min_upvotes = comment_req["stop_at"]["upvotes"]
                    if min_upvotes < 1 and parent_upvotes is not None:
                        if upvotes < parent_upvotes * min_upvotes:
                            continue
                    elif upvotes < min_upvotes:
                        continue
                if "depth" in comment_req["stop_at"]:
                    if depth > comment_req["stop_at"]["depth"]:
                        continue
                if "total_comments" in comment_req["stop_at"]:
                    if count >= comment_req["stop_at"]["total_comments"]:
                        break
                comment_data = {
                    "author": str(praw_comment.author) if praw_comment.author else "",
                    "body": praw_comment.body,
                    "upvotes": upvotes,
                    "replies": [],
                }
                # Recursively fetch replies
                if comment_req.get("select_replies"):
                    for reply_req in comment_req["select_replies"]:
                        comment_data["replies"].extend(
                            fetch_comments(
                                praw_comment.replies,
                                reply_req,
                                depth=depth+1,
                                parent_upvotes=upvotes,
                            )
                        )
                comments.append(comment_data)
                count += 1
        return comments

    response = []
    for subreq in request:
        subreddit = client.subreddit(subreq["subreddit"])
        sort_by = subreq["post_sort"]["by"]
        time_filter = subreq["post_sort"].get("time_filter")
        stop_at = subreq["post_sort"].get("stop_at", {})
        limit = stop_at.get("total_posts")

        sort_method = getattr(subreddit, sort_by)
        praw_kwargs: dict[str, int | str] = {"limit": limit}
        if sort_by in {"top", "controversial"} and time_filter:
            praw_kwargs["time_filter"] = time_filter

        posts = []
        for post in sort_method(**praw_kwargs):
            post_comments = []
            for comment_req in subreq.get("select_comments", []):
                post.comment_sort = comment_req["sort"]
                post.comments.replace_more(limit=0)
                post_comments.extend(
                    fetch_comments(
                        post.comments,
                        comment_req,
                        depth=1,
                        parent_upvotes=post.score,
                    )
                )
            posts.append({
                "title": post.title,
                "author": str(post.author) if post.author else "",
                "body": post.selftext,
                "upvotes": post.score,
                "comments": post_comments,
            })

        response.append({
            "name": subreq["subreddit"],
            "posts": posts,
        })
    return response

