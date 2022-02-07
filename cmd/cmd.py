import argparse

from command import init

parser = argparse.ArgumentParser()
init(parser.add_subparsers())

if __name__ == '__main__':
    args = parser.parse_args()
    args.func(args)
    exit(0)
