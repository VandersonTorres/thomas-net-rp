from urllib.parse import urlparse
from scrapy.exceptions import DropItem


class ThomasNetPipeline:
    def process_item(self, item, spider):
        required_fields = ["category", "description", "name"]
        for field in required_fields:
            if not item.get(field):
                raise DropItem(f"Missing required field: {field}")

        if item.get("url"):
            parsed = urlparse(item["url"])
            if not all([parsed.scheme, parsed.netloc]):
                raise DropItem(f"Invalid URL: {item['url']}")

        return item
