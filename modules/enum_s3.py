import logging

# TODO: figure out a better way to implement logging
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

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


    Methods
    -------
    lookup_domain()
        Look up the IP address associated with the domain name and do a reverse 
        DNS lookup to populate the attributes domain_ip and reverse_domain_name
    check_bucket()
        Checks if the reverse_domain_name string is consistent with the naming
        conventions of an S3 bucket
    run_all_enum_checks()
        Runs all enumeration checks so that data can be collected as an attribute

    '''


    def __init__(self, domain: str) -> None:
        """
        Parameters
        ----------
        domain : str
            The domain name of the target to enumeration (required)
        """

        self.domain = domain

    
    def run_all_enum_checks(self) -> None:
        """
        Runs all enumeration checks so that data can be collected as an attribute
        """


        self.lookup_domain()
        self.check_bucket()


    def lookup_domain(self) -> None:
        """ 
        Look up the IP address associated with the domain name and do a reverse 
        DNS lookup to populate the attributes domain_ip and reverse_domain_name
        """

        import socket

        self.domain_ip = socket.gethostbyname(self.domain)
        logging.info(f"Domain IP address is {self.domain_ip}")

        self.reverse_domain_name = socket.gethostbyaddr(self.domain_ip)[0]
        logging.info(f"Result of reverse DNS lookup is domain name {self.reverse_domain_name}")

    
    def check_bucket(self) -> None:
        """ 
        Checks if the reverse_domain_name string is consistent with the naming
        conventions of an S3 bucket
        """

        import re

        # s3-website-us-west-2.amazonaws.com
        pattern = r"s3-website-(\w+-)+\w+\.amazonaws\.com$"
        self.isBucket = bool(re.search(pattern, self.reverse_domain_name))

        if self.isBucket: logging.info("Domain is an S3 bucket")
        else: logging.warning("Domain is NOT an S3 bucket")


