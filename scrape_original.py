import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup, SoupStrainer
import pandas as pd

import time
import logging
import os

SCRAPE_OUTPUT_PATH = 'data_original2.jsonl'
LOG_FILE_PATH = 'scraping.log'
HEADLESS = True
MAX_EXTRACTION_ERROR = 5 # if error more than x times, break and scraping new page


logging.basicConfig(
	level=logging.INFO,
	format='%(asctime)s [%(levelname)s] %(message)s',
	datefmt='%Y-%m-%d %H:%M:%S',
	handlers=[
		logging.FileHandler(LOG_FILE_PATH),
		logging.StreamHandler()
	]
)

async def iterate_extract_image(page):
	await page.locator('xpath=//*[@id="islrg"]/div[1]/div[1]/a[1]/div[1]').click()
	image_list = []
	last_url = None
	error_counter = 0
	while True:
		try:
			time.sleep(0.2)
			last_url = page.url
			html = await page.content()
			image_segment = SoupStrainer('a',{'class': 'jlTjKd'})
			soup = BeautifulSoup(html, 'html.parser', parse_only=image_segment)
			img = soup.find('img')
			image_metadata = {
				'alt_text':  img.attrs['alt'], 
			}
			if img.attrs['src'].startswith('data:image'):
				image_metadata['image_base64'] = img.attrs['src']
			else:
				image_metadata['image_url'] = img.attrs['src']
			image_list.append(image_metadata)

		except:
			# capture general error, such as image does not have alt text
			# will just ignore and click next button below
			pass
		try:
			next_button = page.locator('xpath=//*[@id="Sva75c"]/div[2]/div[2]/div[2]/div[2]/c-wiz/div/div/div/div/div[1]/div/div[2]/button[2]')
			if await next_button.get_attribute('aria-disabled', timeout=3000)=='true':
				break
			await next_button.click()
		except:
			error_counter += 1
			if error_counter > MAX_EXTRACTION_ERROR:
				break
			await page.goto(last_url)
	return image_list

async def main(keyword_list):
	for keyword in keyword_list:
		logging.info(f'Scraping keyword: "{keyword}"')
		
		alternate_type_list = []
		async with async_playwright() as p:
			browser = await p.chromium.launch(headless=HEADLESS)
			page = await browser.new_page()
			url = f'https://www.google.com/search?q={keyword}&tbm=isch'
			await page.goto(url)
			# get list of alternate images type
			html = await page.content()
			image_segment = SoupStrainer('span',{'role': 'list'})
			soup = BeautifulSoup(html,'html.parser', parse_only=image_segment)
			for index, span in enumerate(soup.find_all('span')):
				if index == 0:
					continue
				alternate_type_list.append(span.get_text())
			logging.info(f'[{keyword}] alternate subkeyword {alternate_type_list}')
			logging.info(f'[{keyword}] Scraping base keyword...')
			image_list = await iterate_extract_image(page)
			df = pd.DataFrame(image_list)
			df.to_json(SCRAPE_OUTPUT_PATH, orient='records', mode='a', lines=True)
			for alt_type in alternate_type_list:
				logging.info(f'[{keyword}] Scraping "{alt_type}" subkeyword...')
				url = f'https://www.google.com/search?q={keyword}&tbm=isch&chips=q:{keyword},g_1:{alt_type}'
				await page.goto(url)
				image_list = await iterate_extract_image(page)
				df = pd.DataFrame(image_list)
				df.to_json(SCRAPE_OUTPUT_PATH, orient='records', mode='a', lines=True)
				logging.info(f'[{keyword}] Completed!')
			
		logging.info(f'Completed scraping keyword: "{keyword}"!')

if __name__=='__main__':
	keyword_list = ['lembu']
	asyncio.run(main(keyword_list))