import logging
import boto3
from botocore import UNSIGNED
from botocore.config import Config
from botocore.exceptions import ClientError
import re

# TODO: figure out a better way to implement logging
logging.basicConfig(encoding='utf-8', level=logging.INFO)

class EnumS3:
    '''
    Class that contains all the functions the enumerate AWS S3 Buckets

    ...

    Attributes
    ----------
    domain : str
        Initial domain name of the enumeration target
    domain_ip : str
        IP address of `domain` that was collected from a name server
    reverse_domain_name : str
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
        DNS lookup to populate the attributes domain_ip and reverse_domain_name
    get_region_name()
        Uses regex to get region name out of `reverse_domain_name` and store it
        in the region_name attribute.


    check_bucket()
        Checks if the reverse_domain_name string is consistent with the naming
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

    
    def run_all_enum_checks(self) -> None:
        """
        Runs all enumeration checks so that data can be collected as an attribute
        """

        self.lookup_domain()
        self.check_bucket()

        if self.isBucket: self.enum_bucket_permissions()


    def lookup_domain(self) -> None:
        """ 
        Look up the IP address associated with the domain name and do a reverse 
        DNS lookup to populate the attributes domain_ip and reverse_domain_name
        """

        import socket

        self.domain_ip = socket.gethostbyname(self.options["domain"])
        logging.info(f"Domain IP address is {self.domain_ip}")

        self.reverse_domain_name = socket.gethostbyaddr(self.domain_ip)[0]
        logging.info(f"Result of reverse DNS lookup is domain name {self.reverse_domain_name}")

    
    def check_bucket(self) -> None:
        """ 
        Checks if the reverse_domain_name string is consistent with the naming
        conventions of an S3 bucket
        """

        # s3-website-us-west-2.amazonaws.com
        pattern = r"s3-website-(\w+-)+\w+\.amazonaws\.com$"
        self.isBucket = bool(re.search(pattern, self.reverse_domain_name))
        self.get_region_name()

        if self.isBucket: logging.info("Domain is an S3 bucket")
        else: logging.warning("Domain is NOT an S3 bucket")


    def enum_bucket_permissions(self) -> None:
        """ 
        Checks for bucket listing, download, and upload permissions
        if permitted in user settings
        """

        if not self.region_name: return

        if self.options["list_s3_bucket"]: self.check_bucket_listing()
        if self.options["check_s3_upload"]: self.check_bucket_upload()
        if self.options["check_s3_download"]: self.check_bucket_download()
        

    
    def check_bucket_listing(self) -> None:
        """ 
        Check if permissions allow listing of bucket permissions
        """

        s3client = boto3.client('s3', region_name=self.region_name, config=Config(signature_version=UNSIGNED))
        bucket_files = s3client.list_objects(Bucket=self.options["domain"])["Contents"]

        if not bucket_files:
            logging.info("Unable to list contents of bucket")
        
        else:
            logging.info("Successfully recieved contents of bucket")
            logging.info("Filename \t Size \t Last Modified")
            for file_ in bucket_files:
                logging.info(f"{file_['Key']} \t {file_['Size']} \t {file_['LastModified']}")


    def check_bucket_download(self) -> None:
        """ 
        Check if bucket permissions allow for downloading files
        """

        s3_client = boto3.client('s3')


    def check_bucket_upload(self) -> None:
        """ 
        Check if bucket permissions allow for uploading files
        """

        s3_client = boto3.client('s3')

    
    def get_region_name(self) -> None:
        """
        Uses regex to get region name out of `reverse_domain_name` and store it
        in the region_name attribute. 
        """

        pattern = r"(\w+-)(\w+-)[0-9]"
        self.region_name = re.search(pattern, self.reverse_domain_name).group()
        
        if self.region_name: logging.info(f"Bucket region is {self.region_name}")
        else: logger.info("Unable to find bucket region. Cannot run enumeration checks")



