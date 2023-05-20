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
import socket

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
    reverse_domain_name : str
        The domain name found through reverse DNS lookup

    """

    def __init__(self, domain: str) -> None:
        domain_info = util.parse_domain(domain) 
        self.domain = domain_info["domain"]
        self.protocol = domain_info["protocol"]

        # automatically perform enumerations on initialization of class
        self.find_instance_type()

    
    def find_instance_type(self) -> None:
        logger.info("Determining instance type...")

        domain_info = util.parse_domain(self.domain)

        if self.check_protocol() and self.type \
            or self.lookup_domain() and self.type:
            logger.info(f"Instance was found to be of type {self.type}")
        
        else:
            logger.info("Instance could not be identified. Exiting...")
            exit()




    def lookup_domain(self) -> None:
        """ 
        Look up the IP address associated with the domain name and do a reverse 
        DNS lookup to populate the attributes domain_ip and reverse_domain_name
        """

        try:
            domain_ip = socket.gethostbyname(self.domain)
            logger.info(f"Domain IP address is {domain_ip}")

            self.reverse_domain_name = socket.gethostbyaddr(domain_ip)[0]
            logger.info(f"Result of reverse DNS lookup is domain name {self.reverse_domain_name}")
        except Exception as e:
            logger.error(f"Domain lookup failed with error message: {e}")


    
    def check_protocol(self) -> None:
        if self.protocol == "s3":
            self.type = "s3"
            return True 
        
        else:
            return False


    def check_bucket(self) -> None:
        """ 
        Iterates through potential instance types and populates value of self.type
        if a type is found to be valid
        """
        ## TODO: improve regex
        # s3-website-us-west-2.amazonaws.com
        pattern = r"^{}-.*?\.amazonaws\.com$"
        types = ["s3", "ec2"]

        for instance_type in types:
            isType = bool(re.search(pattern.format(instance_type), self.domain))

            if isType: 
                logger.info(f"Instance was found to be of type {self.type}")
                self.get_region_name()
                return True

        return False
