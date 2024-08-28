import argparse
import sys

def main():
    args = sys.argv[1:]

    parser = argparse.ArgumentParser(
        description="A very simplified version of git, implemented in Python."
    )

    subparsers = parser.add_subparsers(title="Commands", dest="command")
    subparsers.required = True

    parsed_args = parser.parse_args(args)
    match parsed_args.command:
        case _:
            print("Unknown command")
            sys.exit(1)

