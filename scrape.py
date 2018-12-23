# scrape.py

from bs4 import BeautifulSoup as bs
import requests
import csv
import re
import os

from regions import regions, valid_regions
import datetime as dt
from utils import *
from time import sleep

def scrape_deals(regions: list, start_date: str, end_date: str, save_path: str = None, sleep_seconds=2.0) -> dict:
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

	now = dt.datetime.now()
	as_of_date_time = now.strftime(f"{DATE_FORMAT} {TIME_FORMAT}")
	as_of_date = now.strftime(f"{DATE_FORMAT}")

	start_date = start_date or as_of_date
	
	invalid_regions = [region for region in regions if region not in valid_regions]
	assert len(invalid_regions) == 0, f"Invalid region(s) {invalid_regions}"

	headers = ["as_of", "date", "region", "mountain", "location", "deal_name", "num_days", "price", "savings", "rental_included", "tickets_left", "link"]
		
	save_path = save_path or f"{as_of_date}.csv"
	visited = get_visited(save_path, lambda line: f"{line.get('date') {line.get('region')}}")

	f = open(save_path, "a") if os.path.exists(save_path) else open(save_path, "a")
	writer = csv.DictWriter(f, fieldnames=headers)
	writer.writeheader()

	base_url = "https://www.liftopia.com"

	regex_price 		= re.compile(r"(?<=\$)[0-9]+\.[0-9]{2}|$")
	regex_savings 		= re.compile(r"[0-9]{1,2}%|$")
	regex_tickets_left 	= re.compile(r"[0-9]{1,}(?= ticket)|$")
	regex_num_days 		= re.compile(r"[0-9]+(?= Day)|$")
	regex_rental		= re.compile(r"\+ Rental")

	
	for region in regions:
		print(f"scraping {region}...")
		dates = daterange(start_date=start_date, end_date=end_date)
		for date in dates:
			key = f"{date} {region}"
			if key in visited:
				continue

			print(f"\r{date}", end="")
			site = f"{base_url}/find-tickets/{region}?utf8=%E2%9C%93&start_date={date}&days="
			page = requests.get(site)

			soup = bs(page.content, "html.parser")

			mountains = soup.find_all("div", class_="search-index__results-container")

			out = []

			for mountain in mountains:
				mountain_text = clean(get_from_elem(mountain, "p", class_="search-index__results-heading"))
				location_text = clean(get_from_elem(mountain, "span", class_="search-index__results-resort-info__text"))

				mountain_results = mountain.find_all("div", class_="search-result")
				
				for mountain_result in mountain_results:
					deal_text 			= get_from_elem(mountain_result,"p", class_="search-result__link-container")
					deal_price_text 	= get_from_elem(mountain_result,"span", class_="button__text")
					deal_tickets_left 	= get_from_elem(mountain_result, "p", class_="search-result__urgency-flag")
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
			sleep(sleep_seconds)
	return save_path

out = scrape_deals(regions=regions.values(), start_date=None, end_date="2019-05-01", save_path="out.csv")
