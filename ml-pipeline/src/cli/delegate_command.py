import sys
import typing


class ParsedArgsWithCommand:
    command: str

class ParsedArgsForGetRedditPosts(ParsedArgsWithCommand):
    client_id: str
    client_secret: str
    password: str
    user_agent: str
    username: str

def delegate_command_and_execute(parsed_args: ParsedArgsWithCommand):
    """
    From the parsed arguments, determine which command to run and run it,
    passing it the arguments appropriately.
    """
    if parsed_args.command == "get_reddit_posts":
        from cli.get_reddit_posts import get_reddit_posts
        reddit_args = typing.cast(ParsedArgsForGetRedditPosts, parsed_args)
        get_reddit_posts(
            input_yaml=sys.stdin,
            client_id=reddit_args.client_id,
            client_secret=reddit_args.client_secret,
            password=reddit_args.password,
            user_agent=reddit_args.user_agent,
            username=reddit_args.username
        )
    elif parsed_args.command == "nli_csv":
        from cli.nli_csv import nli_csv
        nli_args = typing.cast(typing.Any, parsed_args)
        nli_csv(
            nli_model_hf=nli_args.nli_model_hf,
            nli_model_type=nli_args.nli_model_type.value,
            batch_size=nli_args.batch_size,
            hypothesis_formats=nli_args.hypothesis,
            premise_format=nli_args.premise,
            input_csv=sys.stdin,
            max_tokens=nli_args.max_tokens
        )
        pass
    elif parsed_args.command == "join_parent_row":
        from cli.join_parent_row import join_parent_row
        join_parent_row(
            input_csv=sys.stdin,
        )
    else:
        raise ValueError(f"Unknown command: {parsed_args.command}")

