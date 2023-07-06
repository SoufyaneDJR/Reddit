import os
import shutil
import requests
from redvid import Downloader
from chelenium import scrape_links, scrape_youtube
from validation import add_nature, validator
import twitter_video_dl as tvdl

#Done
def twitter_download(twitter_url, post_id) : 
    # Download the video 
    tvdl.download_video(twitter_url, f"{post_id}.mp4")
    #Validate the download 
    validator(post_id)
    

# Done 
def source_download(source_url, post_id) : 
    """
    works on : 
    - dubz.co
    - cazn.me
    - streamff.co
    - streamable.com
    - streamin.one
    - streambug.io
    """

    urls = scrape_links(source_url)

    if urls != [] : 
        response = requests.get(urls[0], stream=True)
        response.raise_for_status()
        
        with open(f"{post_id}.mp4", 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        validator(post_id)
    else :
        ## Append the nature of the url to the Database : 
        add_nature(post_id, "nature", "Possible Dead Link")
        print("[Warning] Scrapping: Possible dead link")
    
# Done
def reddit_download(reddit_url, post_id): 

    """
    - self.soccer
    - v.redd.it
    """
    reddit = Downloader(max_q=True)
    reddit.log = False
    reddit.url = reddit_url
    reddit.file_name = post_id
    reddit.path = os.getcwd()
    try : 
        reddit.download()
    except Exception as e  : 
        print(e)

    finally :

        #Get the main path 
        main_path = os.getcwd()

        # Get the reddit download subdirectory path 
        dirs = os.listdir(main_path + "\\redvid_temp")

        # Should be empty 
        if len(dirs) == 1 : 
            # Get the first folder 
            dir_  = dirs[0] 
            # Get the mp4 type 
            file_dir = os.path.join(f"redvid_temp/{dir_}/video.mp4")
            # Copy it to the main path 
            shutil.copy(file_dir, f"{post_id}.mp4")
            # Destory the reddit download directory 
            shutil.rmtree(main_path + "/redvid_temp")
        else : 
            print("Error in Reddit Download Directory !")
            

def youtube_download(youtube_url, post_id) : 
    video_url = scrape_youtube(youtube_url)
    if video_url == None : # Means that no Youtube video is attributed to that link
        # Add the nature of the link to the database  
        add_nature(post_id, "nature", "Possible Dead Link")
    else : 
        response = requests.get(video_url, stream=True)
        print(response.status_code)
    # with open(f"{post_id}.mp4", 'wb') as file:
    #     for chunk in response.iter_content(chunk_size=8192):
    #         if chunk:
    #             file.write(chunk)


# reddit_download("https://v.redd.it/focr8la84f4b1", "142k1mu")
youtube_download("chikri", "chikri")