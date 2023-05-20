########################################################
# 
# Description: Module containing helper methods
# 
# Author: Ally Petitt <allypetitt@proton.me>
# Created: May 2023
# 
#########################################################
import re
import logging
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

class Util:
    '''
    Class that contains helper functions that can be utilized accross multiple classes

    ...
    Methods
    -------
    clean_domain_name(domain: str) -> dict
        Returns the domain info from a URI string as a dictionary containing the domain and protocol

    '''

    def __init__(self): 
        pass

    
    def parse_domain(self, domain: str) -> dict:
        """
        Parameters
        ----------
        domain : str
            URI to extract the domain name from
        """

        parsed = urlparse(domain)

        return {
            "domain": parsed.hostname,
            "protocol": parsed.scheme
        }
        