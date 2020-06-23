import re
import os
import requests
import json
import urllib
import sys

aria2cflag = 0
parallel_connections_aria2 = 16

for arg in sys.argv:
	if arg == "--aria2c":
		aria2cflag = 1

if aria2cflag != 0:
	print("Using aria2c for the downloads!")

print("Loading cookie from file cookie.txt")
cookie = ""
try:
	with open("cookie.txt") as f:
		cookie = (f.read()).rstrip()
except:
	print("Could not read cookie! Exiting...")
	exit()
print("Cookie read!")
headers = {
	'cookie': cookie
    }


def fix_string_filename(string):
	forbidden = ["?", "|", ":", "<", ">", "\"", "*"]
	for char in forbidden:
		if char in string:
			string = string.replace(char, "-")
	return string

def get_course_title(url):
	global cookie
	global headers
	r = str(requests.get(url, headers=headers).content)
	print("\t" + (r.split("<title data-react-helmet=\"true\">")[1]).split("</title>")[0])
	string = ((r.split("<title data-react-helmet=\"true\">")[1]).split("</title>")[0]).replace("|", "-")
	return fix_string_filename(string)

def get_course_mp4_url_and_title(url):
	global cookie
	global headers
	r = requests.get(url, headers=headers).text
	content = (r.split("window.__INITIAL_STATE__ = ")[1]).split(";</script>")[0]
	j = json.loads(content)
	video_mp4_urls = []
	video_titles = []
	for value in j["course"]["stepMap"].keys():
		v = value
	for i in range(len(j["course"]["stepMap"][str(v)]["data"]["player"]["sources"])):
		video_titles.append(j["course"]["stepMap"][str(v)]["data"]["title"])
		if '1080' in j["course"]["stepMap"][str(v)]["data"]["player"]["sources"][i]["src"]:
			video_mp4_urls.append(j["course"]["stepMap"][str(v)]["data"]["player"]["sources"][i]["src"])
	return video_mp4_urls[0], video_titles[0]

def get_all_courses(url):
	global cookie
	global headers
	course_list = []
	print("Going through the pages...")
	for i in range(1, 30):
		current_page_url = url + "?page={}".format(i)
		print("\t" + current_page_url)
		r = requests.get(current_page_url, headers=headers).text
		if "Can&#x27;t find what you&#x27;re looking for?" in r:
			return course_list
		r = r.split("<div name=\"libraryContent\">")[1]

		regex_courses = re.findall(r"/course/[a-zA-Z0-9\-]{1,}/", r)
		len_results = 0
		for x in range(len(regex_courses)):
			len_results += 1
		if len(regex_courses) == 0:
			return course_list
		for x in regex_courses:
			course_list.append("https://cloudacademy.com" + x)
		len_results = 0

def download_single_course(url):
	global aria2cflag
	global cookie
	global headers
	global parallel_connections_aria2
	print("Downloading webpage...")

	r = requests.get(url, headers=headers)
	r_text = r.text
	content = (r_text.split("window.__INITIAL_STATE__ = ")[1]).split(";</script>")[0]
	j = json.loads(content)
	
	print("Getting URLs of courses...")
	course_urls = []
	courses_regex = re.findall(r"<a palette=\"lecture\" [a-zA-Z0-9=\"\- \/]{1,}", r_text)
	course_urls.append(r.url)
	for u in courses_regex:
		course_urls.append("https://cloudacademy.com" + (u.split("href=\"")[1]).split("\"")[0])

	for course in course_urls:
		print("\t{}".format(course))

	print("Getting course title...")
	title = get_course_title(url)
	if not os.path.isdir(fix_string_filename(title)):
		print("Creating folder for videos...")
		os.mkdir(fix_string_filename(title))

	for value in j["course"]["stepMap"].keys():
		v = value

	print("Downloading videos...")
	for u in range(len(course_urls)):
		video_url, video_title = get_course_mp4_url_and_title(course_urls[u])
		print("{} - {}".format(video_title, video_url))
		extension = ""
		if ".webm" in video_url:
			extension = ".webm"
		if ".mp4" in video_url:
			extension = ".mp4"
		if aria2cflag == 1:
			os.system("aria2c -x {} -o \"{}/{}{}\" \"{}\"".format(parallel_connections_aria2, fix_string_filename(title), fix_string_filename(video_title), extension, video_url))
		else:
			urllib.request.urlretrieve(video_url, "{}/{}{}".format(fix_string_filename(title), fix_string_filename(video_title), extension))	

def download_learning_path(url):
	global cookie
	global headers
	r = requests.get(url, headers=headers)
	r_text = r.text
	learning_path_courses = [] 
	regex_courses = re.findall(r"https://cloudacademy.com/course/[a-zA-Z0-9\-]{1,}/", r_text)
	for x in regex_courses:
		learning_path_courses.append(x)

	print("Number of courses: {}".format(len(learning_path_courses)))
	for course in range(len(learning_path_courses)):
		print("Downloading course [{} / {}]".format(course + 1, len(learning_path_courses)))
		download_single_course(learning_path_courses[course])

url = input("Please enter a URL of the course you want to download: ")

if '/library/' in url:
	if '/courses/' in url:
		all_the_courses = get_all_courses(url)
		print("Number of courses: {}".format(len(all_the_courses)))
		for course in all_the_courses:
			download_single_course(course)

if "/course/" in url:
	download_single_course(url)
elif "/learning-paths/" in url:
	download_learning_path(url)