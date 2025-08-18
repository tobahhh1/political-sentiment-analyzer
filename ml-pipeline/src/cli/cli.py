from typing import cast
import argparse

from cli.construct_argument_parser import construct_command_args
from cli.delegate_command import delegate_command_and_execute, ParsedArgsWithCommand

def main():
    parser = argparse.ArgumentParser(
        prog="Candidate Approval Detector",
        description="""Analyze whether text approves / disapproves of a candidate."""
    )
    parser = construct_command_args(parser) 
    parsed_args = parser.parse_args()
    parsed_args = cast(ParsedArgsWithCommand, parsed_args)
    delegate_command_and_execute(parsed_args)
