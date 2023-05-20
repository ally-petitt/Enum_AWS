########################################################
# 
# Description: Module containing EnumInstance class. 
#              This performs initial enumeration on a cloud instance.
# 
# Author: Ally Petitt <allypetitt@proton.me>
# Created: May 2023
# 
#########################################################

import logging
from modules import Util


util = Util()
logger = logging.getLogger(__name__)


class EnumInstance:
    """
    Class that contains functions to perform initial enumeration on a given instance

    Attributes
    ----------
    type : str
        The type of AWS instance (ec2, s3, etc.)
    domain : str
        The domain name given by the user
    reverse_domain : str
        The domain name found through reverse DNS lookup

    """
    
    def __init__(self, domain: str) -> None:
        domain_info = util.parse_domain(domain) 
        self.domain = domain_info["hostname"]
        self.protocol = domain_info["scheme"]

        # automatically perform enumerations on initialization of class
        find_instance_type()

    
    def find_instance_type(self) -> None:
        logger.info("Determining instance type...")

        domain_info = util.parse_domain(args.domain)

        self.check_aws_protocol()



    def lookup_domain(self) -> None:
        """ 
        Look up the IP address associated with the domain name and do a reverse 
        DNS lookup to populate the attributes domain_ip and reverse_domain_name
        """

        import socket

        try:
            self.domain_ip = socket.gethostbyname(self.domain)
            logger.info(f"Domain IP address is {self.domain_ip}")

            self.reverse_domain_name = socket.gethostbyaddr(self.domain_ip)[0]
            logger.info(f"Result of reverse DNS lookup is domain name {self.reverse_domain_name}")
        except Exception as e:
            logger.error(f"Domain lookup failed with error message: {e}")


    
    def check_protocol(self) -> None:
        if self.protocol == "s3":
            self.type = "s3"
