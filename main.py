import argparse
from modules.enum_s3 import EnumS3

argParser = argparse.ArgumentParser()

argParser.add_argument("-d", "--domain", help="domain name of website to enumerate")

args = argParser.parse_args()

DOMAIN = args.domain


enum_s3 = EnumS3(DOMAIN)
enum_s3.test()
