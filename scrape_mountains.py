# scrape_mountains.py

from utils import *
import re
import requests
from bs4 import BeautifulSoup as bs
import datetime as dt
from time import sleep

headers_static = [
	"as_of",
	"mountain",
	"base_elevation",	 
	"peak_elevation",	
	"vertical_drop",
	"description",	
	"beginner",	
	"intermediate",
	"advanced",	
	"expert",
	"amenities",	
	"weekday_hours",
	"weekend_hours",
	"link"
]

headers_dynamic = [
	"as_of",
	"mountain",
	"trails_open",
	"lifts_open",
	"acres_open",
	"avg_base_depth",
	"24h_snow_fall",
	"link"
]

def scrape_mountains_static(mountains: list, save_path=None, sleep_seconds=2.0):
	base_url = "https://www.liftopia.com"
	mountains = clean(list(mountains), replace_char="-")

	now = dt.datetime.now()
	as_of_date_time = now.strftime(f"{DATE_FORMAT} {TIME_FORMAT}")
	save_path = save_path or "mountains.csv"

	visited = get_visited(save_path, lambda l: l.get("mountain"))

	f = open(save_path, "a") if os.path.exists(save_path) else open(save_path, "a")
	writer = csv.DictWriter(f, fieldnames=headers_static)
	writer.writeheader()

	for mountain in mountains:
		if mountain in visited:
			continue
		print(mountain)

		site = f"{base_url}/{mountain}"
		page = requests.get(site)
		soup = bs(page.content, "html.parser")


		amenities = soup.find_all("div", class_="amenities__amenity--active amenities__amenity")
		amenities = "; ".join([a.text for a in amenities])
		
		base_elevation		 = get_from_elem(soup, "span", class_="resorts-show__about-section__stat--base" )
		peak_elevation		 = get_from_elem(soup, "span", class_="resorts-show__about-section__stat--peak")
		vertical_drop		 = get_from_elem(soup, "span", class_="resorts-show__about-section__stat--drop" )
		description_hidden	 = get_from_elem(soup, "span", class_="content-revealer__text content-revealer__text--visible")		
		description_visible  = get_from_elem(soup, "span", class_="content-revealer__text content-revealer__text--hidden")
		beginner			 = get_from_elem(soup, "span", class_="trail-counts__trail-count-total trail-counts__trail-count-total--beginner")
		intermediate		 = get_from_elem(soup, "span", class_="trail-counts__trail-count-total trail-counts__trail-count-total--intermediate")
		advanced		 	 = get_from_elem(soup, "span", class_="trail-counts__trail-count-total trail-counts__trail-count-total--advanced")
		expert		 		 = get_from_elem(soup, "span", class_="trail-counts__trail-count-total trail-counts__trail-count-total--expert")
		weekday_hours		 = get_from_elem(soup, "p", class_="resort-conditions__content resort-conditions__content--small resorts-show__resort-conditions__content--operations-weekday")
		weekend_hours		 = get_from_elem(soup, "p", class_="resort-conditions__content resort-conditions__content--small resorts-show__resort-conditions__content--operations-weekend")

		amenities = amenities.replace(',', " ")
		
		description = description_visible + description_hidden
		description = description.replace(',', " ")

		out = {
			"as_of": as_of_date_time,
			"mountain": mountain,
			"base_elevation": base_elevation,
			"peak_elevation": peak_elevation,
			"vertical_drop": vertical_drop,
			"description": description,
			"beginner": beginner,
			"intermediate": intermediate,
			"advanced": advanced,
			"expert": expert,
			"amenities": amenities,
			"weekday_hours": weekday_hours,
			"weekend_hours": weekend_hours,
			"link": site
		}

		writer.writerow(out)
		visited.add(mountain)
		sleep(sleep_seconds)
	return save_path

def scrape_mountains_dynamic(mountains: list, save_path=None, sleep_seconds=2.0):
	base_url = "https://www.liftopia.com"
	mountains = clean(list(mountains), replace_char="-")

	now = dt.datetime.now()
	as_of_date_time = now.strftime(f"{DATE_FORMAT} {TIME_FORMAT}")
	as_of_date = now.strftime(f"{DATE_FORMAT}")
	save_path = save_path or f"{as_of_date}-mountains.csv"

	visited = get_visited(save_path, lambda l: f"{l.get('date')} {l.get('mountain')}")

	f = open(save_path, "a") if os.path.exists(save_path) else open(save_path, "a")
	writer = csv.DictWriter(f, fieldnames=headers_dynamic)
	writer.writeheader()

	for mountain in mountains:
		if mountain in visited:
			continue
		print(mountain)
		
		site = f"{base_url}/{mountain}"
		page = requests.get(site)
		soup = bs(page.content, "html.parser")

		trails_open		 			= get_from_elem(soup, "p", class_="resort-conditions__content resorts-show__resort-conditions__content--trails-open")
		lifts_open		 			= get_from_elem(soup, "p", class_="resort-conditions__content resorts-show__resort-conditions__content--lifts-open")
		acres_open		 			= get_from_elem(soup, "p", class_="resort-conditions__content resorts-show__resort-conditions__content--acreage" )
		avg_base_depth	 			= get_from_elem(soup, "p", class_="resort-conditions__content resorts-show__resort-conditions__content--base-depth-average")
		twenty_four_hour_snowfall   = get_from_elem(soup, "p", class_="resort-conditions__content resorts-show__resort-conditions__content--total-snowfall-24hr")

		out = {
			"as_of": as_of_date_time,
			"mountain": mountain,
			"trails_open": trails_open,
			"lifts_open": lifts_open,
			"acres_open": acres_open,
			"avg_base_depth": avg_base_depth,
			"24h_snow_fall": twenty_four_hour_snowfall,
			"link": site
		}

		writer.writerow(out)
		visited.add(mountain)
		sleep(sleep_seconds)
	return save_path

mountains = get_visited("out.csv", lambda l: l.get("mountain").lower())
# scrape_mountains_static(mountains=mountains)

scrape_mountains_dynamic(mountains=mountains)
