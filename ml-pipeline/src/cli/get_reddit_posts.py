import csv
from praw.config import sys
import yaml
from reddit import login_to_reddit, get_reddit_posts as reddit_api_get_reddit_posts
from reddit.relational import FIELD_NAMES, to_relational_table
from typing import TextIO

def get_reddit_posts(
    client_id: str,
    client_secret: str,
    password: str,
    user_agent: str,
    username: str,
    input_yaml: TextIO
):
    """
    Fetches Reddit posts based on the yaml file. Writes to stdout as a csv file.
    
    Returns:
        None
    """

    request = yaml.load(input_yaml, yaml.SafeLoader)
    # Assume the user has passed a valid RedditRequest.
    client = login_to_reddit(
        client_id,
        client_secret,
        password,
        user_agent,
        username
    )
    response = reddit_api_get_reddit_posts(client, request)
    relational_response = to_relational_table(response)

    writer = csv.DictWriter(sys.stdout, fieldnames=FIELD_NAMES)
    writer.writeheader()    
    writer.writerows(relational_response)
