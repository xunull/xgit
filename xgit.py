import argparse
import sys
import xgitInit as init


parser = argparse.ArgumentParser(description='some useful git operation.')
subparsers = parser.add_subparsers(help='sub-command help')
parser_init = subparsers.add_parser('init')

parser_init.add_argument('initName')

args = parser.parse_args()

if hasattr(args, 'initName'):
    init.create(args.initName)
