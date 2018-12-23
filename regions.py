# regions.py


# regions: {name: path}
# e.g. full path: https://www.liftopia.com/region/new-england
regions = {
	"New England": "new-england",
	"Colorado": "colorado",
	"Utah": "utah",
	"NY, NJ and PA": "ny-nj-and-pa",
	"California: Central & Southern": "california-central-and-southern",
	"California: Lake Tahoe & Northern": "california-lake-tahoe-and-northern",
	"Northern Rockies": "northern-rockies",
	"Pacific Northwest": "pacific-northwest",
	"Midwest": "midewest",
	"Mid-Atlantic": "mid-atlantic",
	"Southwest": "southwest",
	"Southeast": "southeast",
	"Alaska": "alaska",
	"Eastern Canada": "eastern-canada",
	"Central Canada": "central-canada",
	"Western Canada": "western-canada",
	"Chile": "chile",
	"New Zealand": "new-zealand",
	"Switzerland": "switzerland",
	"Japan": "japan"
}

valid_regions = set(list(regions.values()) + list(regions.keys()))