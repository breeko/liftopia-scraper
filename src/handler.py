from scrape_mountains import scrape_mountains_dynamic

def handle(event, context):
    mountains = event.get("mountains") or event["multiValueQueryStringParameters"]["mountains"]
    dynamic = scrape_mountains_dynamic(mountains)
    return {
        "isBase64Encoded": False,
        "statusCode": 200,
        "headers": { },
        "body": str(dynamic)
    }
