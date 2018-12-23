# utils.py

import bs4
import re
import datetime as dt
import csv
import os

DATE_FORMAT = "%Y-%m-%d"
TIME_FORMAT = "%H:%M:%S"

def get_from_elem(elem: bs4.element.Tag, tag: str, class_: str) -> str:
	result = elem.find(tag, class_=class_)
	if result:
		return result.text.strip()
	return ""

def clean(strings: list, replace_char=" ") -> str:
	if type(strings) is str:
		strings = [strings]
	out = []
	regex = re.compile(r'\W+')
	for string in strings:
		clean_string = regex.sub(replace_char, string)
		out.append(clean_string)
	
	if len(out) == 1:
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
