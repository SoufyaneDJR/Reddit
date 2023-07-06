# GOLD SHIT 
# Gives you all the attributes of a given "element"
# attrs = driver.execute_script('var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;', element)
#________________________________________________________________

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
def scrape_links(url):
    # Set up headless Selenium options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('log-level=3')
    chrome_options.add_argument("--no-sandbox")

    # Set user-agent string
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    chrome_options.add_argument(f"user-agent={user_agent}")
    # Set up the Selenium webdriver with the specified path
    driver = webdriver.Chrome(options=chrome_options)

    # this try except close is written for some cases where the driver.get(url) doesn't stop from running. 
    # Some cases : 
    #       - streamin.me
    #       - streamin.one
    try:
        # Set the page load timeout
        driver.set_page_load_timeout(5)
        # Load the URL
        driver.get(url)
        # If the page loads successfully within the timeout, continue with further actions
    except :
        print("[Exception] Selenium : Page load timed out. Skipping further actions.\n[Suggestion]\t   >>> Check driver.get(url) command")
    
    #Waiting for the first div 
    try :
        WebDriverWait(driver = driver,timeout=5).until(EC.presence_of_element_located((By.TAG_NAME, "div")))
    except :
        print("[Exception] Selenium : 'Div' cannot be rendered before Timeout ")

    # Waiting for a Video     
    try :
        WebDriverWait(driver = driver, timeout= 5).until(EC.presence_of_element_located((By.TAG_NAME, "video")))
    except :
        print("[Exception] Selenium : 'Video' cannot be rendered before Timeout ")
        print("                     : 'Video' isn't used the url ")


    driver.implicitly_wait(5) # seconds


    print("Scrapping ...")
    divElement_url = ""
    sourceElement_url = ""
    videoElement_url = ""
    
    # <div src = "...">
    try : 
        # - dubz.
        divElement = driver.find_element(By.CLASS_NAME, "my-video")
        divElement_url = divElement.get_attribute("src")
    except : 
        print("\tNo url found in the boilerplate <div src = '...' >")

    # <video src = "..."> 
    try : 
        # - Streamff
        # - dubz.live
        # - streamin.me
        # - streamin.one  
        videoElement = driver.find_element(By.TAG_NAME, "video")
        videoElement_url = videoElement.get_attribute("src")
    except : 
        print("\tNo url found in the boilerplate <video src = '...'>")

    # <video ...><source src = "..." ></video> 
    try : 
        # - streambug.io
        sourceElement = videoElement.find_element(By.TAG_NAME, "source")
        sourceElement_url = sourceElement.get_attribute("src")
    except :
        print("\tNo url found in the boilerplate <video><source src = '...'>")
    
    print("Scraping done .")

    
    urls = []
    if divElement_url != None : 
        urls.append(divElement_url) 
    if videoElement_url != None : 
        urls.append(videoElement_url) 
    if sourceElement_url != None : 
        urls.append(sourceElement_url) 
    driver.quit()

    video_formats = ["mp4", ".mkv", ".avi"]
    checked = []
    for format in video_formats : 
        checked_videos = [url for url in urls if format in url]
        checked.extend(checked_videos)

    "list of urls that are videos"
    return list(set(checked))

def scrape_youtube(url) : 
    # Set up headless Selenium options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('log-level=3')
    chrome_options.add_argument("--no-sandbox")

    # Set user-agent string
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

    # Set up the Selenium webdriver with the specified path
    driver = webdriver.Chrome(options=chrome_options)
    driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": user_agent})

    driver.get("https://fr.savefrom.net/")

    # Complete the form : 
    form_element = WebDriverWait(driver=driver, timeout= 3).until(EC.presence_of_element_located((By.ID, "sf_form")))

    # Find the input field and enter the URL
    url_input = form_element.find_element(By.ID, "sf_url")
    url_input.send_keys(url)

    # Find the submit button and click it
    submit_button = form_element.find_element(By.ID, "sf_submit")
    submit_button.click()

    
    # get result component 
    result = WebDriverWait(driver=driver, timeout= 100).until(EC.presence_of_element_located((By.ID, "sf_result")))
    driver.implicitly_wait(10)
    elements = result.find_elements(By.TAG_NAME, "a")

    if len(elements) >= 2:
        second_element = elements[1]
        download_url = second_element.get_attribute("href")
        driver.quit()
        return download_url
    else:
        driver.quit()
        print("[Error] Selenium Youtube : Video not found (Probably)")
        return None
