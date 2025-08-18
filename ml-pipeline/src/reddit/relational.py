

from typing import Iterable, Optional, TypedDict

from reddit.response_types import RedditResponse

class RedditResponseRelationalTableRow(TypedDict):
    """
    Alternate RedditResponse format where the entries
    """
    id: int
    author: str
    title: Optional[str]
    body: str 
    upvotes: int
    parent_id: Optional[int]
    subreddit_name: str

def _traverse_comments(comments, parent_id: Optional[int]):
    """
    Traverse the comments recursively and yield rows for each comment.
    """
    for comment in comments:
        yield {
            "author": comment["author"],
            "body": comment["body"],
            "upvotes": comment["upvotes"],
            "parent_id": parent_id,
        }
        # Recursively traverse replies if they exist
        if "replies" in comment and comment["replies"]:
            yield from _traverse_comments(comment["replies"], parent_id=parent_id)

def to_relational_table(response: RedditResponse) -> Iterable[RedditResponseRelationalTableRow]:
    id = 0
    for subreddit in response:
        subreddit_name = subreddit["name"]
        for post in subreddit["posts"]:
            post_author = post["author"]
            post_title = post["title"]
            post_body = post["body"]
            post_upvotes = post["upvotes"]
            post_id = id
            yield RedditResponseRelationalTableRow(
                id=post_id,
                author=post_author,
                title=post_title,
                body=post_body,
                upvotes=post_upvotes,
                parent_id=None,  # Top-level posts have no parent
                subreddit_name=subreddit_name
            )
            id += 1
            for incomplete_comment_row in _traverse_comments(post["comments"], parent_id=post_id):
                yield RedditResponseRelationalTableRow(
                    id=id,
                    author=incomplete_comment_row["author"],
                    title=None,
                    body=incomplete_comment_row["body"],
                    upvotes=incomplete_comment_row["upvotes"],
                    parent_id=incomplete_comment_row["parent_id"],
                    subreddit_name=subreddit_name
                )
                id += 1

FIELD_NAMES=['id', 'parent_id', 'subreddit_name', 'upvotes', 'body', 'author', 'title']
