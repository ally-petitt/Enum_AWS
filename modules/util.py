########################################################
# 
# Description: Module containing helper methods
# 
# Author: Ally Petitt <allypetitt@proton.me>
# Created: May 2023
# 
#########################################################

import re, os, logging
from urllib.parse import urlparse
from pathlib import Path

logger = logging.getLogger(__name__)

class Util:
    '''
    Class that contains helper functions that can be utilized accross multiple classes

    ...
    Methods
    -------
    parse_domain(domain: str) -> dict
        Returns the domain info from a URI string as a dictionary containing the domain and protocol
    create_folders(filepath: str) -> None
        Creates necessary directories in order to write to a given filepath (avoids "folder does not
        exit error")

    '''

    def __init__(self): 
        pass

    
    def parse_domain(self, domain: str) -> dict:
        """
        Returns the domain info from a URI string as a dictionary containing the domain and protocol

        Parameters
        ----------
        domain : str
            Function to extract domain from a URI
        """

        if self.check_valid_domain(domain):
            return { 
                "domain": domain,
                "protocol": ""
            }

        parsed = urlparse(domain)
        return {
            "domain": parsed.netloc,
            "protocol": parsed.scheme
        }

    
    def check_valid_domain(self, domain: str) -> bool:
        """
        Function to check whether a string is a valid domain

        Paramters
        ---------
        domain : str
            Domain to check 
        """

        try:
            pattern = r"^(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9]$"
            isDomain = bool(re.search(pattern, domain).group())

            return isDomain 
        except:
            return False
            

    
    def create_folders(self, filepath: str) -> None:
        """ 
        Creates necessary directories in order to write to a given filepath

        Parameters
        ----------
        filepath : str
            Path to the file to write to. 
        """

        path_list = filepath.split("/")
        directories = "/".join(path_list[0:len(path_list)-1])

        if os.path.exists(directories): return
        Path(directories).mkdir(parents=True, exist_ok=True)

        