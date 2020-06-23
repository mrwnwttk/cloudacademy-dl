# cloudacademy-dl
Downloader for CloudAcademy courses

I wrote this within an hour or so, therefore bugs are to be expected.

## Installation
Install on Ubuntu (Example, may vary from OS to OS):
```
$ python3 -m pip install -r requirements.txt
```

## Usage
Sign up for either a demo account or a 7-day trial. Just visiting the website alone doesn't work. Log in and save the cookie from Chrome to a file called cookie.txt. The cookie looks a little like this:
```
louda-session=6fe4.............
```
The script can be run either with or without the --aria2c flag. For that to work aria2c needs to be installed and added to the respective PATH variable of your system.
Then just run it like this:
```
$ python3 cloud.py
```
or
```
$ python3 cloud.py --aria2c
```
## Example
```
$ python3 cloud.py
Using aria2c for the downloads!
Loading cookie from file cookie.txt
Cookie read!
Please enter a URL of the course you want to download: https://cloudacademy.com/course/designing-and-implementing-an-agile-work-management-approach-1017/
Downloading webpage...
Getting URLs of courses...
        https://cloudacademy.com/course/designing-and-implementing-an-agile-work-management-approach-1017/course-introduction/
        https://cloudacademy.com/course/designing-and-implementing-an-agile-work-management-approach-1017/project-metrics-and-kpis/
        https://cloudacademy.com/course/designing-and-implementing-an-agile-work-management-approach-1017/mentoring-team-members-on-agile-practices/
        https://cloudacademy.com/course/designing-and-implementing-an-agile-work-management-approach-1017/in-team-and-cross-team-collaboration/
        https://cloudacademy.com/course/designing-and-implementing-an-agile-work-management-approach-1017/tools-and-processes-for-agile-practices/
        https://cloudacademy.com/course/designing-and-implementing-an-agile-work-management-approach-1017/creating-organizational-structures-for-agile-practices/
        https://cloudacademy.com/course/designing-and-implementing-an-agile-work-management-approach-1017/course-conclusion/
Getting course title...
        Designing and Implementing an Agile Work Management Approach Course | Cloud Academy
Downloading videos...
[...]
```
