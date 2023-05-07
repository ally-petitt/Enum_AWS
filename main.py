import argparse
from modules.enum_s3 import EnumS3

argParser = argparse.ArgumentParser()

argParser.add_argument("-d", "--domain", required=True,
                            help="domain name of website to enumerate")

args = argParser.parse_args()

DOMAIN = args.domain


enum_s3 = EnumS3(DOMAIN)
enum_s3.run_all_enum_checks()
print(enum_s3.reverse_domain_name)
