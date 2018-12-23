import csv
import re
import requests
from bs4 import BeautifulSoup as bs
import datetime as dt
from time import sleep
from collections import namedtuple
import random
import os

from utils import *

Parse = namedtuple("Parse", "tag classes")

dynamic_fields = {
    "suffix": "dynamic",
    "fields":
        {
            "trails_open":                  Parse(tag="p", classes="resort-conditions__content resorts-show__resort-conditions__content--trails-open"),
            "lifts_open":                   Parse(tag="p", classes="resort-conditions__content resorts-show__resort-conditions__content--lifts-open"),
            "acres_open":                   Parse(tag="p", classes="resort-conditions__content resorts-show__resort-conditions__content--acreage" ),
            "avg_base_depth":               Parse(tag="p", classes="resort-conditions__content resorts-show__resort-conditions__content--base-depth-average"),
            "twenty_four_hour_snowfall":    Parse(tag="p", classes="resort-conditions__content resorts-show__resort-conditions__content--total-snowfall-24hr")
		}
}

static_fields = {
	"suffix": "static",
	"fields":
	{
		"base_elevation":		Parse(tag="span", classes="resorts-show__about-section__stat--base"),
		"peak_elevation":		Parse(tag="span", classes="resorts-show__about-section__stat--peak"),
		"vertical_drop":		Parse(tag="span", classes="resorts-show__about-section__stat--drop"),
		"description":			Parse(tag="span", classes=["content-revealer__text content-revealer__text--visible", "content-revealer__text content-revealer__text--hidden"]),
		"beginner": 			Parse(tag="span", classes="trail-counts__trail-count-total trail-counts__trail-count-total--beginner"),
		"intermediate": 		Parse(tag="span", classes="trail-counts__trail-count-total trail-counts__trail-count-total--intermediate"),
		"advanced":				Parse(tag="span", classes="trail-counts__trail-count-total trail-counts__trail-count-total--advanced"),
		"expert":				Parse(tag="span", classes="trail-counts__trail-count-total trail-counts__trail-count-total--expert"),
		"weekday_hours":		Parse(tag="p", classes="resort-conditions__content resort-conditions__content--small resorts-show__resort-conditions__content--operations-weekday"),
		"weekend_hours":		Parse(tag="p", classes="resort-conditions__content resort-conditions__content--small resorts-show__resort-conditions__content--operations-weekend"),
		"amenities":			Parse(tag="div", classes="amenities__amenity--active amenities__amenity")
	}
}

def scrape_mountains(scrape_fields: dict, mountains: list, save_path=None, sleep_seconds=1.0):
	assert len(dynamic_fields.get("fields", [])) + len(dynamic_fields.get("joined", [])) > 0, "nothing to scrape"
	if type(mountains) is str:
		mountains = [mountains]

	base_url = "https://www.liftopia.com"
	mountains = sorted(clean(list(mountains), replace_char="-"))

	as_of_date = get_as_of_date()
	save_path = save_path or "{}_{}.csv".format(as_of_date, scrape_fields.get("suffix"))
	
	visited = get_visited(save_path, lambda l: l.get("mountain"))
	write_header = not os.path.exists(save_path)

	with open(save_path, "a") as f: # if os.path.exists(save_path) else open(save_path, "a")

		fields = scrape_fields.get("fields")
		
		headers = list(fields.keys()) + ["as_of", "mountain", "link"]
		writer = csv.DictWriter(f, fieldnames=headers)
		if write_header:
			writer.writeheader()

		num_mountains = len(mountains)
		for idx, mountain in enumerate(mountains):
			if mountain in visited:
				continue
			print("\r{} / {}".format(idx, num_mountains), end="")

			site = "{}/{}".format(base_url, mountain)
			page = requests.get(site)

			as_of_date_time = get_as_of_date_time()

			soup = bs(page.content, "html.parser")
			out = {"as_of": as_of_date_time, "mountain": mountain, "link": site}
			for field, parse in fields.items():
				out[field] = get_from_elem(elem=soup, tag=parse.tag, classes=parse.classes)

			writer.writerow(out)
			visited.add(mountain)
			sleep(max(0,sleep_seconds + random.random() - 0.5))
	print()
	return save_path

def scrape_mountains_dynamic(mountains: str, save_path: str = None):
	return scrape_mountains(scrape_fields=dynamic_fields, mountains=mountains,save_path=save_path)

def scrape_mountains_static(mountains: str, save_path: str = None):
	return scrape_mountains(scrape_fields=static_fields,mountains=mountains,save_path=save_path)
