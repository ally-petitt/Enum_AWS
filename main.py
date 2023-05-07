import argparse
from modules.enum_s3 import EnumS3


# collect user arguments
argParser = argparse.ArgumentParser()
argParser.add_argument("-d", "--domain", required=True,
                            help="domain name of website to enumerate")
argParser.add_argument("-u", "--check-s3-upload", required=False,
                            action="store_true", help="attempt to upload to the s3 bucket")
argParser.add_argument("-dl", "--check-s3-download", required=False,
                            action="store_true", help="attempt to download from the s3 bucket")
argParser.add_argument("-ls", "--list-s3-bucket", required=False,
                            action="store_true", help="attempt to list the contents of the s3 bucket")
argParser.add_argument("-a", "--all-checks", required=False,
                            action="store_true", help="run all enumeration checks")

args = argParser.parse_args()


enum_s3_options = {
    "domain": args.domain,
    "check_s3_upload": args.check_s3_upload or args.all_checks,
    "check_s3_download": args.check_s3_download or args.all_checks,
    "list_s3_bucket": args.list_s3_bucket or args.all_checks,
}



enum_s3 = EnumS3(enum_s3_options)
enum_s3.run_all_enum_checks()