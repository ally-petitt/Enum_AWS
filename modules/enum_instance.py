########################################################
# 
# Description: Module containing EnumInstance class. 
#              This performs initial enumeration on a cloud instance.
# 
# Author: Ally Petitt <allypetitt@proton.me>
# Created: May 2023
# 
#########################################################

import logging, socket, re

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
    region_name : str
        Name of the region that the instance is located in

    Methods
    -------
    enumerate_instance() -> None
        Method to carry out the steps of enumerating the instance
    find_instance_type() -> None
        Method to determine the instance type (s3, ec2, etc)
    lookup_domain -> None
        Look up the IP address associated with the domain name and do a reverse 
        DNS lookup to populate the attributes domain_ip and reverse_domain_name

    """

    def __init__(self, domain: str) -> None:
        domain_info = util.parse_domain(domain) 
        self.domain = domain_info["domain"]
        self.protocol = domain_info["protocol"]

        # automatically perform enumerations on initialization of class
        self.enumerate_instance()


    def enumerate_instance(self) -> None:
        '''Method to carry out the steps of enumerating the instance'''

        self.find_instance_type()
        self.get_region_name()

    
    def find_instance_type(self) -> None:
        '''Method to determine the instance type (s3, ec2, etc)'''

        logger.info("Determining instance type...")

        protocol_type = self.check_protocol()
        domain_type = self.find_instance_type()

        if domain_type == "":
            raise Exception("Instance could not be identified. Exiting...")
        
        elif (protocol_type != domain_type):
            raise Exception("Instance protocol does not match instance type. Exiting...")
        
        self.type = domain_type

        logger.info(f"Instance was found to be of type {self.type}")

            




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


    
    def check_protocol(self) -> str:
        """
        Check the protocol if included on the user's URI string to determine instance type
        """

        type_ = ""

        if self.protocol == "s3":
            type_ = "s3"
        
        return type_


    def find_instance_type(self) -> str:
        """ 
        Iterates through potential instance types and populates value of self.type
        if a type is found to be valid
        """

        self.lookup_domain()

        pattern = r"^{}-.*?\.amazonaws\.com$"
        types = ["s3", "ec2"]
        type_ = ""

        for instance_type in types:
            isType = bool(re.search(pattern.format(instance_type), self.reverse_domain_name))

            if isType: 
                type_ = instance_type
                break
        
        return type_



    def get_region_name(self) -> None:
        """
        Uses regex to get region name out of self.reverse_domain_name and store it
        in the region_name attribute. 
        """

        try: 
            pattern = r"\w+-\w+-[0-9]"
            self.region_name = re.search(pattern, self.reverse_domain_name).group()
            
            logger.info(f"Instance region is {self.region_name}")

        except:
            logger.info("Unable to find instance region. Cannot run enumeration checks. Exiting...")
            exit()
