import os
import time
import requests
from selenium import webdriver
from logger_class import getlog

logger = getlog("Imagescrapper.py")

sleep_time = 1


def extract_image_urls(query, max_links_required, browser, sleep_time):
    # building a google query for search

    search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"

    # loading th web page
    browser.get(search_url.format(q=query))

    image_urls = set()
    image_count = 0
    results_start = 0

    while image_count <= max_links_required:

        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(sleep_time)

        thumbnails_results = browser.find_elements_by_css_selector("img.Q4LuWd")
        numbers_results = len(thumbnails_results)

        logger.info(f"Found: {numbers_results} search results Extraction links from {results_start}:{numbers_results}")

        for img in thumbnails_results[results_start:numbers_results]:

            try:
                img.click()
                time.sleep(sleep_time)
            except Exception:
                continue

            actual_image = browser.find_elements_by_css_selector("img.n3VNCb")
            for actual_image in actual_image:
                if actual_image.get_attribute("src") and "http" in actual_image.get_attribute("src"):
                    image_urls.add(actual_image.get_attribute("src"))
                    # print(image_urls)

            image_count = len(image_urls)

            if len(image_urls) >= max_links_required:
                logger.info(f"found {len(image_urls)} image links, Done!!")
                break
            else:
                logger.info(f"found: {len(image_urls)}, image link  and fetching more wait.....")
                time.sleep(sleep_time)
                load_more_button = browser.find_element_by_css_selector(".mye4qd")
                if load_more_button:
                    browser.execute_script("document.querySelector('.mye4qd').click();")

            results_start = len(thumbnails_results)

        return image_urls


def save_image(folder_path, url, counter):
    try:
        image_content = requests.get(url).content
    except Exception as e:
        logger.info(f"ERROR - Couldn't download{url}-{e}")

    try:
        f = open(os.path.join(folder_path, "jpg" + "_" + str(counter) + ".jpg"), "wb")
        f.write(image_content)
        f.close()
        logger.info(f"SUCCESSFULLY saved {url} - as {folder_path}")
    except Exception as e:
        logger.info(f"Error - could not save {url} - {e}")


def search_and_download(search_term, DRIVER_PATH='./chromedriver', target_path="./images", number_images=int()):
    target_path = os.path.join(target_path, "_".join(search_term.lower().split(" ")))

    if not os.path.exists(target_path):
        os.makedirs(target_path)

    with webdriver.Chrome(DRIVER_PATH) as wd:
        res = extract_image_urls(search_term, number_images, browser=webdriver.Chrome(DRIVER_PATH),
                                 sleep_time=sleep_time)

    counter = 0

    for elem in res:
        save_image(target_path, elem, counter)
        counter += 1
