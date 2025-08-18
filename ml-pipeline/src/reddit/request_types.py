

from typing import Literal, Optional, Sequence, TypedDict, Self

CommentSort = Literal["confidence", "controversial", "new", "old", "q&a", "top"]

class CommentStopCriteria(TypedDict):
    depth: int
    """Return no comments at a depth greater than this from the root.
    1 returns the root comment's replies, 2 returns the replies of the replies, and so on.
    """
    num_branches: int
    """At each level, return no more than this number of replies"""
    upvotes: float
    """Return comments with no fewer than this many upvotes. If < 1, will be treated as a percentage of the parent's upvotes"""
    total_comments: int
    """Return no more than this number of comments across all branchesa"""

class ReplyRequest(TypedDict):
    stop_at: CommentStopCriteria
    """Stop returning replies after any criteria in this dictionary has been met"""
    select_on_each_returned_reply: Sequence[Self]
    """Selection performed on each reply returned from this selector."""

class CommentRequest(TypedDict):
    sort: CommentSort
    """'Sort By' button on the comments section"""
    stop_at: CommentStopCriteria
    """Stop returning replies after any criteria in this dictionary has been met."""
    select_replies: Sequence[ReplyRequest]
    """Selection returned on each reply returned from this selector."""
    

class PostStopCriteria(TypedDict):
    upvotes: int
    """Return posts with no fewer than this many upvotes."""
    total_posts: int
    """Return no more than this number of posts."""

class PostSort(TypedDict):
    by: Literal[
        "controversial", 
        "gilded", 
        "hot", 
        "new", 
        "random", 
        "top"
    ]
    time_filter: Optional[Literal[
        "all", "day", "hour", "month", "week", "year" 
    ]]
    stop_at: PostStopCriteria


class SubredditRequest(TypedDict):
    subreddit: str
    """Subreddit to get posts from"""
    post_sort: PostSort
    """Sort by the number of posts"""
    """'Sort By' option on the subreddit"""
    select_comments: Sequence[CommentRequest]


RedditRequest = Sequence[SubredditRequest] 


