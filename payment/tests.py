# from django.test import TestCase

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--i",type=dict, dest="name", help="name")
args = parser.parse_args()
print(args.name,type(args.name))