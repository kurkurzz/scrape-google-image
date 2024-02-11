# scraping-google-image

basically scraping the whole internet! 

we will be scraping images with the attached alt text. the images that we are interested with are the one with bahasa melayu alt text, so to start we would need a list of malaysia keywords such as "lembu" and "kereta" to be fed into the search bar. We use list of malaysian nouns from .... . bahasa melayu search keyword will ensure bahasa melayu alt text.

## Folder Structure

`scrape_thumbnail_only.py`: scraping thumbnail image on google image by scrolling through the page. pros, faster, cons, low res image (100x100)

`scrape_original.py`: scraping original image by clicking each image and traverse. pros, high res image, cons, slow
