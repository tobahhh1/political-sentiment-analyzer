# Stub of a not-AI generated version of get reddit functions.
# Keeping around in case I want to use it as a prompt to clean up the implementation later.
"""
    for subreddit_request in request:
        subreddit = client.subreddit(subreddit_request["subreddit"])
        post_sort_by = subreddit_request["post_sort"]["by"]
        post_sort_time_filter = subreddit_request["post_sort"]["time_filter"]

        posts: Iterable[praw.models.Submission]

        if post_sort_by == "controversial":
            if post_sort_time_filter is None:
                post_sort_time_filter = "all"
            posts = subreddit.controversial(time_filter=post_sort_time_filter)

        elif post_sort_by == "top":
            if post_sort_time_filter is None:
                post_sort_time_filter = "all"
            posts = subreddit.top(time_filter=post_sort_time_filter)

        elif post_sort_by == "gilded":
            assert post_sort_time_filter is None, "Sort time filter not supported for option gilded"
            posts = subreddit.gilded()

        elif post_sort_by == "hot":
            assert post_sort_time_filter is None, "Sort time filter not supported for option hot"
            posts = subreddit.hot()

        elif post_sort_by == "new":
            assert post_sort_time_filter is None, "Sort time filter not supported for option new"
            posts = subreddit.new()

        elif post_sort_by == "random":
            assert post_sort_time_filter is None, "Sort time filter not supported for option random"
            posts = call_on_each_iter(lambda: get_optional(subreddit.random(), "Subreddit {} does not support random submissions".format(subreddit.display_name)))
        
        else:
            raise ValueError("Unsupported value for post sort {}".format(post_sort_by))

        for post in posts:
            for comment_request in subreddit_request["select_comments"]:
                post.comment_sort = comment_request["sort"]
                for comment in post.comments:
"""
