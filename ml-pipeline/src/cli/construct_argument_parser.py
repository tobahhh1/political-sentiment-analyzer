import argparse
from model.nli.model_types import NliModelType

def construct_command_args(parser: argparse.ArgumentParser) -> argparse.ArgumentParser: 
    """Constructs the command line argument parser for the CLI."""
    subparsers = parser.add_subparsers(dest="command", help="Command to run", required=True)

    parser_get_reddit_posts = subparsers.add_parser(
        "get_reddit_posts",
        help="Get Reddit posts based on a YAML file read from stdin",
    )
    parser_get_reddit_posts.add_argument("--client_id", type=str, help="Reddit client ID", required=True)
    parser_get_reddit_posts.add_argument("--client_secret", type=str, help="Reddit client secret", required=True)
    parser_get_reddit_posts.add_argument("--password", type=str, help="Reddit password", required=True)
    parser_get_reddit_posts.add_argument("--user_agent", type=str, help="Reddit user agent", required=True)
    parser_get_reddit_posts.add_argument("--username", type=str, help="Reddit username", required=True)

    parser_nli_csv = subparsers.add_parser(
        "nli_csv",
        help="Run NLI a CSV file read from stdin, passing columns in a format string",
    )
    parser_nli_csv.add_argument("--nli_model_hf", type=str, help="Name of HuggingFace NLI model to use", required=True)
    parser_nli_csv.add_argument("--nli_model_type", type=NliModelType, default=NliModelType.DEBERTA_V2, help="Type of NLI model to use", choices=list(NliModelType), required=False)
    parser_nli_csv.add_argument("--batch_size", type=int, default=1, help="Batch size for NLI model inference")
    parser_nli_csv.add_argument("--hypothesis", type=str, nargs="+", help="Format string to use in hypothesis for NLI. Using {{column}} syntax in the format string like --hypothesis \"value of col1: {{col1}}\" allows substitution of column values for the given row. Passing multiple space-separated strings allows for multiple premises per hypothesis.", required=True)
    parser_nli_csv.add_argument("--premise", type=str, help="Format string to use in premise for NLI. Using {{column}} syntax in the format string like --hypothesis \"value of col1: {{col1}}\" allows substitution of column values for the given row", required=True)

    subparsers.add_parser(
        "join_parent_row",
        help="If the CSV has a parent_id column, join the parent row with the child row, prepending each parent column with parent_. Useful for performing NLI models on Reddit comments with thieir parents"
    )
    # No additional arguments needed for join_parent_row

    return parser



