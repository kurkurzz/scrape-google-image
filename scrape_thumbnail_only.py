import playwright
import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup, SoupStrainer
import pandas as pd

import time
import logging
import os

SCRAPE_OUTPUT_PATH = 'data_v2.json'
LOG_FILE_PATH = 'scraping.log'
HEADLESS = False

logging.basicConfig(
	level=logging.INFO,
	format='%(asctime)s [%(levelname)s] %(message)s',
	datefmt='%Y-%m-%d %H:%M:%S',
	handlers=[
		logging.FileHandler(LOG_FILE_PATH),
		logging.StreamHandler()
	]
)

async def scroll_and_extract(page):
	'''
	scroll through the page and extract image with alt text
	'''
	try:
		for _ in range(6):
			time.sleep(1)
			await page.keyboard.down('End')
		await page.locator('xpath=//*[@id="islmp"]/div/div/div/div/div[1]/div[2]/div[2]/input').click(timeout=3000)
		for _ in range(10):
			time.sleep(1)
			await page.keyboard.down('End')
	except:
		pass

	html = await page.content()
	image_segment = SoupStrainer('div',{'role': 'list'})
	soup = BeautifulSoup(html,'html.parser', parse_only=image_segment)
	image_list = []
	for image in soup.find_all('img'):
		try:
			if image.attrs['alt'] != '':
				image_metadata = {
					'alt_text':  image.attrs['alt'], 
				}
				if image.attrs['src'].startswith('data:image'):
					image_metadata['image_base64'] = image.attrs['src']
				else:
					image_metadata['image_url'] = image.attrs['src']

				image_list.append(image_metadata)
		except:
			pass
	
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
			image_list = await scroll_and_extract(page)
			df = pd.DataFrame(image_list)
			df.to_json(SCRAPE_OUTPUT_PATH, orient='records', mode='a', lines=True)
			logging.info(f'Completed!')

			for alt_type in alternate_type_list:
				logging.info(f'[{keyword}] Scraping "{alt_type}" subkeyword...')
				url = f'https://www.google.com/search?q={keyword}&tbm=isch&chips=q:{keyword},g_1:{alt_type}'
				await page.goto(url)
				image_list = await scroll_and_extract(page)
				df = pd.DataFrame(image_list)
				df.to_json(SCRAPE_OUTPUT_PATH, orient='records', mode='a', lines=True)
				logging.info(f'[{keyword}] Completed!')
		logging.info(f'Completed scraping keyword: "{keyword}"!')

if __name__=='__main__':
	keyword_list = ['lembu', 'kereta']
	asyncio.run(main(keyword_list))