import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup, SoupStrainer
import pandas as pd

import time
import logging
import os
import re

SCRAPE_OUTPUT_PATH = 'malay-words.txt'
LOG_FILE_PATH = 'scrape-malay-words.log'
HEADLESS = False
CHECKPOINT_INTERVAL = 100 # every x words, export to file

logging.basicConfig(
	level=logging.INFO,
	format='%(asctime)s [%(levelname)s] %(message)s',
	datefmt='%Y-%m-%d %H:%M:%S',
	handlers=[
		logging.FileHandler(LOG_FILE_PATH),
		logging.StreamHandler()
	]
)

def export_list_to_txt(data_list, file_path):
    try:
        with open(file_path, 'a') as file:
            for item in data_list:
                file.write(str(item) + '\n')
    except Exception as e:
        print(f"Error: {e}")

async def initiate_page(p):
	browser = await p.chromium.launch(headless=HEADLESS)
	page = await browser.new_page()
	url = f'https://www.google.com/search?q=google+translate'
	await page.goto(url)

	await page.locator('xpath=//*[@id="tw-sl"]/span[2]').click()
	await page.locator('xpath=//*[@id="sl_list-search-box"]').fill('english')
	await page.keyboard.down('Enter')

	await page.locator('xpath=//*[@id="tw-tl"]/span[2]').click()
	await page.locator('xpath=//*[@id="tl_list-search-box"]').fill('malay')
	await page.keyboard.down('Enter')

	return page

async def main():
	logging.info('Initiating converting english to malay using Google Translate...')
	text_file = open('english-words.txt', 'r')
	lines = text_file.readlines()
	logging.info(f'total english words: {len(lines)}')

	async with async_playwright() as p:
		last_index = 0
		start_from_offset = False
		while True:
			page = await initiate_page(p)
			malay_word_list = []
			for index, word in enumerate(lines):
				if start_from_offset and index < last_index:
					continue
				last_index = index
				try:
					await page.locator('xpath=//*[@id="tw-source-text-ta"]').fill(word)
					time.sleep(0.5)
					malay_word = await page.locator('xpath=//*[@id="tw-target-text"]/span[1]').text_content()
					malay_word_list.append(malay_word)
					if index > 0 and index % CHECKPOINT_INTERVAL == 0:
						export_list_to_txt(malay_word_list, SCRAPE_OUTPUT_PATH)
						logging.info(f'Appended {len(malay_word_list)} malay words to {SCRAPE_OUTPUT_PATH}')
						malay_word_list = []
				except Exception as e:
					logging.error(f'Problem converting words index {index}')
					logging.error(e)
					start_from_offset = True
					break
			if last_index == len(lines):
				logging.info('Scraping completed!')
				break

if __name__=='__main__':
	asyncio.run(main())