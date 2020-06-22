# cloudacademy-dl
Downloader for CloudAcademy courses

I wrote this within an hour or so, therefore bugs are to be expected.

## Installation
Install on Ubuntu (Example, may vary from OS to OS):
```
$ python3 -m pip install -r requirements.txt
```

## Usage
Save cookie from Chrome to a file called cookie.txt. The cookie looks a little like this:
```
louda-session=6fe4.............
```
Then just run it like this:
```
$ python3 cloud.py
Please enter a URL of the course you want to download: https://cloudacademy.com/course/amazon-dynamodb-high-availability/course-introduction/
Loading cookie from file cookie.txt
Cookie read!
Downloading webpage...
Getting URLs of courses...
        https://cloudacademy.com/course/amazon-dynamodb-high-availability/course-introduction/
        https://cloudacademy.com/course/amazon-dynamodb-high-availability/aws-dynamodb-ha-options/
        https://cloudacademy.com/course/amazon-dynamodb-high-availability/aws-dynamodb-ha-options-demo/
        https://cloudacademy.com/course/amazon-dynamodb-high-availability/on-demand-backup-and-restore/
        https://cloudacademy.com/course/amazon-dynamodb-high-availability/point-in-time-recovery/
        https://cloudacademy.com/course/amazon-dynamodb-high-availability/point-in-time-recovery-demo/
        https://cloudacademy.com/course/amazon-dynamodb-high-availability/course-summary/
Getting course title...
        Amazon DynamoDB High Availability Course | Cloud Academy
Creating folder for videos...
Downloading videos...
[...]
```
