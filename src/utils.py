# utils.py

import re
import datetime as dt
import csv
import os

DATE_FORMAT = "%Y-%m-%d"
TIME_FORMAT = "%H:%M:%S"

def get_as_of_date():
	now = dt.datetime.now()
	return now.strftime("{}".format(DATE_FORMAT))
	
def get_as_of_date_time():
	now = dt.datetime.now()
	return now.strftime("{} {}".format(DATE_FORMAT, TIME_FORMAT))

def get_from_elem(elem: object, tag: str, classes: list, delim=";") -> str:
	""" 
		Returns text of elements given a bs4 element, tag, and a list of classes
	"""
	if type(classes) is str:
		classes = [classes]
	results = []

	for class_ in classes:
		results += elem.find_all(tag, class_=class_)

	if results:
		result = "{} ".format(delim).join([r.text.strip() for r in results])
		result.replace(",", " ")
		return result
	return ""

def clean(strings: list, replace_char=" ") -> str:
	if type(strings) is str:
		strings = [strings]
		originally_string = True
	else:
		originally_string = False
	out = []
	regex = re.compile(r'\W+')
	for string in strings:
		clean_string = regex.sub(replace_char, string)
		out.append(clean_string)
	
	if originally_string:
		return out[0]
	return out


def daterange(start_date: str, end_date:str) -> list:
	start = dt.datetime.strptime(start_date, DATE_FORMAT)
	end = dt.datetime.strptime(end_date, DATE_FORMAT)
	for n in range(int ((end - start).days)):
		inter_date = start + dt.timedelta(n)
		yield inter_date.strftime(DATE_FORMAT)

def get_visited(path: str, key_func: object ) -> set:
	visited = set()
	if os.path.exists(path):
		with open(path, "r") as f:
			reader = csv.DictReader(f)
			for line in reader:
				key = key_func(line)
				visited.add(key)
	return visited
