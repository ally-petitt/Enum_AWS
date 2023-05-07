# Tool Overview
Enum_AWS is a tool to automate the enumeration of AWS instances to aide in cloud security assessments.


## Usage

```
$ python3.11 ./main.py -h
usage: main.py [-h] -d DOMAIN [-u] [-dl] [-ls] [-a]

options:
  -h, --help            show this help message and exit
  -d DOMAIN, --domain DOMAIN
                        domain name of website to enumerate
  -u, --check-s3-upload
                        attempt to upload to the s3 bucket
  -dl, --check-s3-download
                        attempt to download from the s3 bucket
  -ls, --list-s3-bucket
                        attempt to list the contents of the s3 bucket
  -a, --all-checks      run all enumeration checks
```

## Future Steps

* Add ability to check S3 bucket permissions