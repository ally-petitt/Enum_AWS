class EnumS3:
    def __init__(self, domain: str):
        self.domain = domain

    
    def run_all_enum_checks(self):
        self.lookup_domain()
        self.check_bucket()


    def lookup_domain(self):
        import socket

        self.domain_ip = socket.gethostbyname(self.domain)
        self.reverse_domain_name = socket.gethostbyaddr(self.domain_ip)[0]

    
    def check_bucket(self):
        import re

        # s3-website-us-west-2.amazonaws.com
        pattern = r"(?!(^((2(5[0-5]|[0-4][0-9])|[01]?[0-9]{1,2})\.){3}(2(5[0-5]|[0-4][0-9])|[01]?[0-9]{1,2})$|^xn--|.+-s3alias$))^[a-z0-9][a-z0-9.-]{1,61}[a-z0-9]$"
        self.isBucket = bool(re.search(pattern, self.reverse_domain_name))


