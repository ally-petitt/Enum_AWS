########################################################
# 
# Description: Module containing EnumS3 class
# 
# Author: Ally Petitt <allypetitt@proton.me>
# Created: May 2023
# 
#########################################################


from botocore import UNSIGNED
from botocore.config import Config
from botocore.exceptions import ClientError
import re, os, boto3

from tqdm import tqdm
import logging

from modules.util import Util

logger = logging.getLogger(__name__)
util = Util()

class EnumS3:
    '''
    Class that contains all the functions the enumerate AWS S3 Buckets

    ...

    Attributes
    ----------
    options["domain"] : str
        The domain name that was returned from a reverse DNS lookup of the IP address
    region_name : str
        The name of the AWS region that the bucket is located in
    options : dict
        The options that were selected by the user (see `enum_s3_options` variable
        in ../main.py)


    Methods
    -------
    run_all_enum_checks()
        Runs all enumeration checks so that data can be collected as an attribute
    lookup_domain()
        Look up the IP address associated with the domain name and do a reverse 
        DNS lookup to populate the attributes domain_ip and options["domain"]
    get_region_name()
        Uses regex to get region name out of `options["domain"]` and store it
        in the region_name attribute.

    check_bucket()
        Checks if the options["domain"] string is consistent with the naming
        conventions of an S3 bucket
    check_bucket_listing()
        Check if permissions allow listing of bucket permissions
    check_bucket_upload()
        Check if bucket permissions allow for downloading files
    check_bucket_download()
        Check if bucket permissions allow for downloading files
    enum_bucket_permissions()
        Check for directory listing, download, and download permissions

    '''


    def __init__(self, options: dict) -> None:
        """
        Parameters
        ----------
        options : dict
            The configuration options for enumerating S3 buckets
        """

        self.options = options
        

        # set defaults if they were not selected by user
        if not self.options["output_dir"]: self.options["output_dir"] = "enum_aws_output"
    

    def run_all_enum_checks(self) -> None:
        """
        Runs all enumeration checks so that data can be collected as an attribute
        """

        self.lookup_domain()
        self.check_bucket()

        if self.isBucket: self.enum_bucket_permissions()


    
    def check_bucket(self) -> None:
        """ 
        Checks if the options["domain"] string is consistent with the naming
        conventions of an S3 bucket
        """
        ## TODO: improve regex
        # s3-website-us-west-2.amazonaws.com
        pattern = r"^s3-.*?\.amazonaws\.com$"
        self.isBucket = bool(re.search(pattern, self.options["domain"]))

        if self.isBucket: 
            logger.info("Domain is an S3 bucket")
            self.get_region_name()
        else: 
            logger.warning("Domain is NOT an S3 bucket")


    def enum_bucket_permissions(self) -> None:
        """ 
        Checks for bucket listing, download, and upload permissions
        if permitted in user settings
        """

        if not self.region_name: return
        s3_client = boto3.client('s3', region_name=self.region_name, config=Config(signature_version=UNSIGNED))

        if self.options["attempt_s3_upload"]: self.check_bucket_upload(s3_client)
        if self.options["attempt_s3_download"]: 
            filenames = self.check_bucket_listing(s3_client)
            self.check_bucket_download(s3_client, filenames)
        elif self.options["list_s3_bucket"]: self.check_bucket_listing(s3_client)
        

    
    def check_bucket_listing(self, s3: object) -> None:
        """ 
        Check if permissions allow listing of bucket permissions

        Parameters
        ----------
        s3 : object 
            the s3 client used to interact with the bucket
        """

        # s3client = boto3.client('s3', region_name=self.region_name, config=Config(signature_version=UNSIGNED))
        bucket_files = s3.list_objects(Bucket=self.options["domain"])["Contents"]

        if not bucket_files:
            logger.info("Unable to list contents of bucket")
        
        else:
            logger.info("Successfully recieved contents of bucket")
            logger.info("Filename \t Size \t Last Modified")

            filenames = []
            for file_ in bucket_files:
                filenames += [file_['Key']]
                logger.info(f"{file_['Key']} \t {file_['Size']} \t {file_['LastModified']}")
            
            return filenames


    def check_bucket_download(self, s3: object, filenames: list) -> None:
        """ 
        Check if bucket permissions allow for downloading files

        Parameters
        ----------
        s3 : object 
            the s3 client used to interact with the bucket
        filenames : list
            list of filenames returned from self.check_bucket_listing()
        """

        logger.info("downloading files")
        for filename in tqdm(filenames):
            filepath = f'{self.options["output_dir"]}/s3_download/{filename}'
            util.create_folders(filepath)

            s3.download_file(
                self.options["domain"], 
                filename, 
                filepath
            )


    def check_bucket_upload(self, s3: object) -> None:
        """ 
        Check if bucket permissions allow for uploading files

        Parameters
        ----------
        s3 : object 
            the s3 client used to interact with the bucket
        """

        filename = self.options["attempt_s3_upload"]

        try:
            s3.upload_file(filename, self.options["domain"], filename)
            logger.info(f"Successfully uploaded {filename} to the bucket")
        except:
            logger.warn("Unable to upload to the bucket")
    

    def get_region_name(self) -> None:
        """
        Uses regex to get region name out of `options["domain"]` and store it
        in the region_name attribute. 
        """

        pattern = r"\w+-\w+-[0-9]"
        self.region_name = re.search(pattern, options["domain"]self.).group()
        
        if self.region_name: logger.info(f"Bucket region is {self.region_name}")
        else: logger.info("Unable to find bucket region. Cannot run enumeration checks")



