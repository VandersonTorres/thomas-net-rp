import json
from jmespath import search as jsearch
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

import scrapy


class ThomasNetSpider(scrapy.Spider):
    name = "thomas_net"
    allowed_domains = ["www.thomasnet.com"]
    start_urls = [
        "https://www.thomasnet.com/suppliers/search?cov=NA&heading=55550206&coverage_area=NA&act=D",  # packaging
        # "https://www.thomasnet.com/suppliers/search?cov=NA&heading=41463209&searchsource=suppliers&searchterm=janitor&what=Janitorial+Equipment+&+Supplies=&coverage_area=NA&act=D",  # janitorial / sanitation
        # "https://www.thomasnet.com/suppliers/search?cov=NA&heading=70203807&searchsource=suppliers&searchterm=safety&what=Safety+Equipment+&+Supplies=&coverage_area=NA&act=D",  # safety supplies
        # "https://www.thomasnet.com/suppliers/search?cov=NA&heading=49651003&searchsource=suppliers_home&searchterm=mainten&what=Maintenance+Equipment+&+Supplies&act=D",  # maintenance supplies
    ]

    def parse(self, response):
        category = response.css("[aria-current='page'] ::text").get()
        js_script = response.css("#json-ld ::text").get()
        try:
            suppliers_data = json.loads(js_script)
        except json.JSONDecodeError:
            self.crawler.stats.inc_value(f"failed_parse_json_script/{response.url}")
            return

        parsed_url = urlparse(response.url)

        suppliers_urls_set = [
            {
                "supplier_url": f"{supplier.get('url')}?{parsed_url.query}",
                "supplier_page": jsearch("item.sameAs[0]", supplier)
            }
            for supplier in suppliers_data.get("itemListElement")
        ]
        for supplier in suppliers_urls_set:
            yield scrapy.Request(
                url=supplier.get("supplier_url"),
                callback=self.parse_supplier,
                cb_kwargs={"supplier_category": category, "supplier_page": supplier.get("supplier_page")},
            )

        # Pagination
        next_button = response.css("[aria-label='Next Results Page']")
        if next_button:
            query_params = parse_qs(parsed_url.query)
            total_pages = int(response.xpath("//button[contains(@aria-label, 'Results Page ')]//text()")[-1].get())
            for page in range(1, total_pages + 1):
                query_params["pg"] = [str(page)]
                new_query = urlencode(query_params, doseq=True)
                next_page_url = urlunparse(parsed_url._replace(query=new_query))
                yield scrapy.Request(url=next_page_url)

    def parse_supplier(self, response, supplier_category, supplier_page):
        try:
            next_data_script = json.loads(response.css("#__NEXT_DATA__ ::text").get())
        except json.JSONDecodeError:
            self.crawler.stats.inc_value(f"failed_parse_supplier_data/{response.url}")
            return

        data_json = jsearch("props.pageProps.data", next_data_script)
        supplier_url = supplier_page or jsearch("heading.url", data_json)
        supplier_description = jsearch("heading.description", data_json) or data_json.get("description")
        supplier_name = data_json.get("name")
        supplier_headcount = data_json.get("numberEmployees")
        supplier_revenue = data_json.get("annualSales")
        supplier_year_established = data_json.get("yearFounded")
        supplier_company_type = ""
        supplier_additional_activities = ""

        busines_json = jsearch("props.pageProps.businesDetailsSections", next_data_script)
        for section in busines_json.get("firstColumnSections", []):
            try:
                target_text = " ".join([element.get("text", "") for element in section.get("items", [])])
            except TypeError:
                self.logger.warning("Did not find info from firstColumnSections")
                continue

            if section.get("label") == "Primary Company Type":
                supplier_company_type = target_text
            elif section.get("label") == "Additional Activities":
                supplier_additional_activities = target_text

        if not supplier_url:
            self.crawler.stats.inc_value("missing_url/"f"{supplier_category.lower().replace(' ', '')}/")

        item = {
            "additional_activities": supplier_additional_activities,
            "category": supplier_category,
            "description": supplier_description,
            "headcount": supplier_headcount,
            "name": supplier_name,
            "primary_company_type": supplier_company_type,
            "revenue": supplier_revenue,
            "url": supplier_url,
            "year_established": supplier_year_established,
        }

        yield item
