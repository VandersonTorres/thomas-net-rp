import scrapy
from itemloaders.processors import TakeFirst


class ThomasNetItem(scrapy.Item):
    additional_activities = scrapy.Field(
        input_processor=TakeFirst(),
        output_processor=TakeFirst(),
        required=False,
    )
    category = scrapy.Field(
        input_processor=TakeFirst(),
        output_processor=TakeFirst(),
        required=True,
    )
    description = scrapy.Field(
        input_processor=TakeFirst(),
        output_processor=TakeFirst(),
        required=True,
    )
    headcount = scrapy.Field(
        input_processor=TakeFirst(),
        output_processor=TakeFirst(),
        required=False,
    )
    name = scrapy.Field(
        input_processor=TakeFirst(),
        output_processor=TakeFirst(),
        required=True,
    )
    primary_company_type = scrapy.Field(
        input_processor=TakeFirst(),
        output_processor=TakeFirst(),
        required=False,
    )
    revenue = scrapy.Field(
        input_processor=TakeFirst(),
        output_processor=TakeFirst(),
        required=False,
    )
    url = scrapy.Field(
        input_processor=TakeFirst(),
        output_processor=TakeFirst(),
        required=False,
    )
    year_established = scrapy.Field(
        input_processor=TakeFirst(),
        output_processor=TakeFirst(),
        required=False,
    )
