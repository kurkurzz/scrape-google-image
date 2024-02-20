# scraping-google-image

basically scraping the whole internet! 

we will be scraping images with the attached alt text. the images that we are interested with are the one with bahasa melayu alt text, so to start we would need a list of malaysia keywords such as "lembu" and "kereta" to be fed into the search bar. We use list of malay words from [kamus dewan](data/source/kamus-dewan.pdf). bahasa melayu search keyword will ensure bahasa melayu alt text.

### Folder Structure

[scrape_thumbnail_only.py](scrape_thumbnail_only.py): scraping thumbnail image on google image by scrolling through the page. pros, faster, cons, low res image (100x100)

[scrape_fullsize_image.py](scrape_fullsize_image.py): scraping original image by clicking each image and traverse. pros, high res image, cons, slow. [NOT READY FOR PRODUCTION]

[tracker.txt](tracker.txt): simple tracker file to track last scraped keyword index.

### To run

1. `pip install -r requirements.txt`

1. `playwright install`

1. there is 77000+ keywords. to scrape on chunk of it, run `python main.py --start 0 --end 100`
	this wil scrape the first 100 keywords. it also keep tracks on the last scraped index so in the event of the script is interrupted, it can resume from the last checkpoint. all you need to do is run the same command.



