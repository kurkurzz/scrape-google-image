# scraping-google-image

basically scraping the whole internet! 

we will be scraping images with the attached alt text. the images that we are interested with are the one with bahasa melayu alt text, so to start we would need a list of malaysia keywords such as "lembu" and "kereta" to be fed into the search bar. We use list of malaysian nouns from .... . bahasa melayu search keyword will ensure bahasa melayu alt text.

### Folder Structure

`scrape_thumbnail_only.py`: scraping thumbnail image on google image by scrolling through the page. pros, faster, cons, low res image (100x100)

`scrape_fullsize_image.py`: scraping original image by clicking each image and traverse. pros, high res image, cons, slow. [NOT READY FOR PRODUCTION]

`tracker.txt`: simple tracker file to track last scraped keyword index.

### To run

1. `pip install -r requirements.txt`

1. Set your initial keyword index in the `tracker.txt`.

	```txt
	100
	```

	Example above will make the script to start scraping from index 100

1. run `python scrape_thumbnail_only.py`

### Further work

specify end index


