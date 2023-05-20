########################################################
# 
# Description: AWS Enumeration Tool in Python
# 
# Author: Ally Petitt <allypetitt@proton.me>
# Created: May 2023
# 
#########################################################

import argparse, logging
from modules import EnumS3, Util, EnumInstance


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)



# collect user arguments
argParser = argparse.ArgumentParser()
argParser.add_argument("-d", "--domain", required=True,
                            help="domain name of website to enumerate")
argParser.add_argument("-ul", "--attempt-s3-upload", required=False,
                            help="attempt to upload a file to the s3 bucket")
argParser.add_argument("-dl", "--attempt-s3-download", required=False,
                            action="store_true", help="attempt to download the listed \
                            files from the s3 bucket in the inputted directory")
argParser.add_argument("-ls", "--list-s3-bucket", required=False,
                            action="store_true", help="attempt to list the contents of the s3 bucket")
argParser.add_argument("-a", "--all-checks", required=False,
                            action="store_true", help="run all enumeration checks")
argParser.add_argument("-o", "--output-dir", required=False, help="Directory to output \
                            downloaded and log files into (default: enum_aws_output/)")


def handle_user_input():
    args = argParser.parse_args()
    util = Util()

    # domain_info = util.parse_domain(args.domain)
    instance = EnumInstance(args.domain)

    options = {
        "domain": instance.domain,
        "region_name": instance.region_name,
        "output_dir": args.output_dir,
    }


    
    if instance.type == "s3":

        options["attempt_s3_upload"] = args.attempt_s3_upload,
        options["attempt_s3_download"] = args.attempt_s3_download or args.all_checks,
        options["list_s3_bucket"] = args.list_s3_bucket or args.all_checks,

        print(options)

        enum_s3 = EnumS3(options)
        enum_s3.run_all_enum_checks()
    
    



def main():
    handle_user_input()



if __name__ == "__main__":
    main()