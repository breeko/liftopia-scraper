from scrape_mountains import scrape_mountains

def handle(event, context):
    mountains = event.get("mountains")
    return scrape_mountains(mountains)