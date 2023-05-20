# Tool Overview
Enum_AWS is a tool to automate the enumeration of AWS instances to aide in cloud security assessments. In particular, enumerate public S3 buckets for the ability to list, upload,
and download files.


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

Example usage on http://flaws.cloud

```
$ python ./main.py -d flaws.cloud -a -o output/ -u upload_test.txt
2023-05-13 22:50:57,841 - Domain IP address is 52.218.233.58
2023-05-13 22:50:57,888 - Result of reverse DNS lookup is domain name s3-website-us-west-2.amazonaws.com
2023-05-13 22:50:57,888 - Bucket region is us-west-2
2023-05-13 22:50:57,888 - Domain is an S3 bucket
2023-05-13 22:50:58,249 - Unable to upload to the bucket
2023-05-13 22:50:58,552 - Successfully recieved contents of bucket
2023-05-13 22:50:58,553 - Filename       Size    Last Modified
2023-05-13 22:50:58,553 - hint1.html     2575    2017-03-14 03:00:38+00:00
2023-05-13 22:50:58,553 - hint2.html     1707    2017-03-03 04:05:17+00:00
2023-05-13 22:50:58,553 - hint3.html     1101    2017-03-03 04:05:11+00:00
2023-05-13 22:50:58,553 - index.html     3162    2020-05-22 18:16:45+00:00
2023-05-13 22:50:58,553 - logo.png       15979   2018-07-10 16:47:16+00:00
2023-05-13 22:50:58,553 - robots.txt     46      2017-02-27 01:59:28+00:00
2023-05-13 22:50:58,553 - secret-dd02c7c.html    1051    2017-02-27 01:59:30+00:00
2023-05-13 22:50:58,553 - downloading files
```

### Authenticating with AWS
As explained in the (Boto3 documentation)[https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html#configuration],
if you wish to authenticate in your AWS account, you must first configure your credential file which
is located at `~/.aws/credentials` by default. This can be done in 1 of 2 ways:

1. Using the AWS CLI
```
$ aws configure
```

2. Manually creating the credential file
```
[default]
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY
```

You can optionally add a default region to the configuration file at `~/.aws/config`
```
[default]
region=us-east-1
```

## Future Steps
* Add more enumeration methods for more cloud services
* Refactor code to make it cleaner
* Make output prettier
* Fix bugs!