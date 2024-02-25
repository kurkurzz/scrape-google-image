# scraping-google-image

basically scraping the whole internet! 

we will be scraping images with the attached alt text. the images that we are interested with are the one with bahasa melayu alt text, so to start we would need a list of malaysia keywords such as "lembu" and "kereta" to be fed into the search bar. We use list of malay words from [kamus dewan](data/source/kamus-dewan.pdf). bahasa melayu search keyword will ensure bahasa melayu alt text.

### Folder Structure

[main.py](main.py): scraping thumbnail image on google image by scrolling through the page.

[main_extended.py](main_extended.py): scraping thumbnail image and additional information on google image by scrolling through the page.

[scrape.sh](scrape.sh): SH command to run multiple scraping instances parallelly.

[fail.txt](fail.txt): simple tracker file to track failed scraping index.

[tracker.txt](tracker.txt): simple tracker file to track last scraped keyword index.

[scrape_thumbnail_only.py](scrape_thumbnail_only.py): scraping thumbnail image on google image by scrolling through the page. pros, faster, cons, low res image (100x100) [FOR EXPERIMENTATION ONLY]

[scrape_fullsize_image.py](scrape_fullsize_image.py): scraping original image by clicking each image and traverse. pros, high res image, cons, slow. [FOR EXPERIMENTATION ONLY]



### To run

1. `pip install -r requirements.txt`

1. `playwright install`

1. edit the number of instance and python script in the `scrape.sh`. run `./scrape.sh`



