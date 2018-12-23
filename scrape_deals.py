# scrape.py

from bs4 import BeautifulSoup as bs
import requests
import csv
import re
import os

from regions import regions
import datetime as dt
from utils import *
from time import sleep
import random

def scrape_deals(regions: list, start_date: str, end_date: str, save_path: str = None, sleep_seconds=1.0) -> dict:
	"""
		Retuns a dictionary of all deal information given a region and date
		inputs:
			region (list or str):				regions from liftopia
			start_day (str - yyyy-mm-dd):		first day to search
			end_day (str - yyyy-mm-dd):			last day to search
			save_path (str):					csv path to save to
			sleep_seconds (float):				how many seconds to sleep in between regions
		outputs:
			out (dict): {
				as_of, 			# date which the quest was run
				region, 		# region provided
				mountain, 		# name of mountain
				location, 		# location of mountain
				date, 			# date which was provided
				num_days, 		# num
				price, 
				savings, 
				tickets_left, 
				link}

	"""
	if type(regions) is str:
		regions = [regions]

	base_url = "https://www.liftopia.com"
	as_of_date = get_as_of_date()

	start_date = start_date or as_of_date
	
	invalid_regions = [region for region in regions if region not in regions]
	assert len(invalid_regions) == 0, "Invalid region(s) {}".format(invalid_regions)

	headers = ["as_of", "date", "region", "mountain", "location", "deal_name", "num_days", "price", "savings", "rental_included", "tickets_left", "link"]
		
	save_path = save_path or "{}_deals.csv".format(as_of_date)
	visited = get_visited(save_path, lambda line: "{} {}".format(line.get('date'), line.get('region')))
	
	write_header = not os.path.exists(save_path)
	with open(save_path, "a") as f:
		writer = csv.DictWriter(f, fieldnames=headers)
		if write_header:
			writer.writeheader()

		regex_price 		= re.compile(r"(?<=\$)[0-9]+\.[0-9]{2}|$")
		regex_savings 		= re.compile(r"[0-9]{1,2}%|$")
		regex_tickets_left 	= re.compile(r"[0-9]{1,}(?= ticket)|$")
		regex_num_days 		= re.compile(r"[0-9]+(?= Day)|$")
		regex_rental		= re.compile(r"\+ Rental")

		for region in regions:
			print("\nscraping {}...".format(region))
			dates = daterange(start_date=start_date, end_date=end_date)
			for date in dates:
				key = "{} {}".format(date,region)
				if key in visited:
					continue

				print("\r{}".format(date), end="")
				site = """{}/find-tickets/{}?utf8=%E2%9C%93&start_date={}&days=""".format(base_url, region,date)
				page = requests.get(site)
				
				as_of_date_time = get_as_of_date_time()

				soup = bs(page.content, "html.parser")

				mountains = soup.find_all("div", class_="search-index__results-container")

				out = []

				for mountain in mountains:
					mountain_text = clean(get_from_elem(mountain, "p", classes="search-index__results-heading"))
					location_text = clean(get_from_elem(mountain, "span", classes="search-index__results-resort-info__text"))

					mountain_results = mountain.find_all("div", class_="search-result")
					
					for mountain_result in mountain_results:
						deal_text 			= get_from_elem(mountain_result,"p", classes="search-result__link-container")
						deal_price_text 	= get_from_elem(mountain_result,"span", classes="button__text")
						deal_tickets_left 	= get_from_elem(mountain_result, "p", classes="search-result__urgency-flag")
						deal_link 			= mountain_result.find("a", class_="button--icon-right")

						deal_text_clean = clean(deal_text)
						
						price_text 			= re.search(regex_price, deal_price_text).group()
						savings_text 		= re.search(regex_savings, deal_price_text).group()
						tickets_left_text 	= clean(re.search(regex_tickets_left, deal_tickets_left).group())
						num_days   			= clean(re.search(regex_num_days, deal_text).group().strip())
						rental_included		= re.search(regex_rental, deal_text) is not None

						link_text 			= deal_link.get("href", "")

						result = {	
									"as_of": 			as_of_date_time,
									"date": 			date,
									"region": 			region,
									"mountain": 		mountain_text,
									"location": 		location_text,
									"deal_name": 		deal_text_clean,
									"num_days": 		num_days,
									"price": 			price_text,
									"savings":  		savings_text,
									"rental_included": 	rental_included,
									"tickets_left": 	tickets_left_text,
									"link": 			link_text
						}
						out.append(result)
				writer.writerows(out)
				visited.add(key)
				sleep(max(0,sleep_seconds + random.random() - 0.5))
	return save_path
