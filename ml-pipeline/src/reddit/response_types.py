
from typing import Self, Sequence, TypedDict

class CommentResponse(TypedDict):
    author: str
    body: str
    upvotes: int
    replies: Sequence[Self]

class PostResponse(TypedDict):
    title: str
    author: str
    body: str
    upvotes: int
    comments: Sequence[CommentResponse]


class SubredditResponse(TypedDict):
    name: str
    posts: Sequence[PostResponse]

RedditResponse = Sequence[SubredditResponse]
