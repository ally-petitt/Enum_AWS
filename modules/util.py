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
    clean_domain_name(domain: str) -> dict
        Returns the domain info from a URI string as a dictionary containing the domain and protocol
    create_folders(filepath: str) -> None
        Creates necessary directories in order to write to a given filepath (avoids "folder does not
        exit error")

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

    
    def create_folders(self, filepath: str) -> None:
        """ 
        Parameters
        ----------
        filepath : str
            Path to the file to write to. 
        """

        path_list = filepath.split("/")
        directories = "/".join(path_list[0:len(path_list)-1])

        if os.path.exists(directories): return
        Path(directories).mkdir(parents=True, exist_ok=True)

        