import httpx
import parsel
import asyncio
from db_utils.db_settings import Database

MAIN_URL = 'https://www.house.kg'
db = Database()

async def get_html(url):
    async with httpx.AsyncClient() as client:
        data = await client.get(url)
        return data.text

async def clean_text(response: list):
    cleaned_data = [item.strip().replace('\n', '') for item in response]
    return [i for i in cleaned_data if i]

async def insert_in_table(data: list, type_: str):
    n = 0
    for item in data:
        if n < 10:
            n += 1
            await db.insert_value_in_houses(type_, item, n)

async def parsing_html():
    for page in range(1, 10):
        data = await get_html(MAIN_URL + f'/snyat?page={page}')
        selector = parsel.Selector(text=data)
        parsing_title = selector.xpath('//div[@class="left-side"]/p[@class="title"]/a/text()').getall()
        cleaned_title = await clean_text(parsing_title)
        await insert_in_table(cleaned_title, 'title')

        parsing_location = selector.xpath('//div[@class="left-side"]/div[@class="address"]/text()').getall()
        cleaned_location = await clean_text(parsing_location)
        await insert_in_table(cleaned_location, 'location')

        parsing_price = selector.xpath('//div[@class="sep main"]/div[@class="price"]/text()').getall()
        cleaned_price = await clean_text(parsing_price)
        await insert_in_table(cleaned_price, 'price')

        parsing_url = selector.xpath('//div[@class="left-image"]/a/@href').getall()
        cleaned_url = await clean_text(parsing_url)
        await insert_in_table(cleaned_url, 'url')


async def start_parser():
    await db.drop_table_house()
    await db.create_table()
    await parsing_html()


if __name__ == '__main__':
    asyncio.run(start_parser())