from scrape_deals import scrape_deals
from scrape_mountains import scrape_mountains_dynamic, scrape_mountains_static
from regions import regions
from utils import get_visited

# scrape all deals
deals = scrape_deals(regions=regions, start_date=None, end_date="2019-05-01")

# get all mountains
mountains = get_visited("mountains.csv", lambda l: l.get("mountain").lower())

# scrape all mountain data
static = scrape_mountains_static(mountains=mountains)
dynamic = scrape_mountains_dynamic(mountains=mountains)
