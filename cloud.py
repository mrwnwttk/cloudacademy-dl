import re
import os
import requests
import json
import urllib

def get_course_title(url):
	global cookie
	global headers
	r = str(requests.get(url, headers=headers).content)
	print("\t" + (r.split("<title data-react-helmet=\"true\">")[1]).split("</title>")[0])
	string = ((r.split("<title data-react-helmet=\"true\">")[1]).split("</title>")[0]).replace("|", "-")
	forbidden = ["?", "|", ":", "<", ">", "\"", "*"]
	for char in forbidden:
		if char in string:
			string = string.replace(char, "-")
	return string

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
		if '.mp4' in j["course"]["stepMap"][str(v)]["data"]["player"]["sources"][i]["src"] and '1080' in j["course"]["stepMap"][str(v)]["data"]["player"]["sources"][i]["src"]:
			video_mp4_urls.append(j["course"]["stepMap"][str(v)]["data"]["player"]["sources"][i]["src"])
	return video_mp4_urls[0], video_titles[0]

url = input("Please enter a URL of the course you want to download: ")

print("Loading cookie from file cookie.txt")
cookie = ""
try:
	with open("cookie.txt") as f:
		cookie = f.read()
except:
	print("Could not read cookie! Exiting...")
	exit()
print("Cookie read!")

print("Downloading webpage...")

headers = {
	'cookie': cookie
}
r = requests.get(url, headers=headers).text
content = (r.split("window.__INITIAL_STATE__ = ")[1]).split(";</script>")[0]
j = json.loads(content)

print("Getting URLs of courses...")

course_urls = []
courses_regex = re.findall(r"<a palette=\"lecture\" [a-zA-Z0-9=\"\- \/]{1,}", r)
course_urls.append(url)
for u in courses_regex:
	course_urls.append("https://cloudacademy.com" + (u.split("href=\"")[1]).split("\"")[0])

for course in course_urls:
	print("\t{}".format(course))


print("Getting course title...")
title = get_course_title(url)
if not os.path.isdir(title):
	print("Creating folder for videos...")
	os.mkdir(title)

for value in j["course"]["stepMap"].keys():
	v = value

print("Downloading videos...")
for u in range(len(course_urls)):
	video_url, video_title = get_course_mp4_url_and_title(course_urls[u])
	print("{} - {}".format(video_title, video_url))
	urllib.request.urlretrieve(video_url, "{}/{}.mp4".format(title, video_title))
