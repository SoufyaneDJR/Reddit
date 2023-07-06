import praw
import json
import re 


import urllib.request
# Create a Reddit instance by providing your API credentials
reddit = praw.Reddit(
    client_id='HMw-z-4JuYG4ogGVl0mLmw',
    client_secret='-LoRaRHoOdYh_L6-i_cr33cdPlsqpQ',
    user_agent='TestFootball'
)

# Specify the subreddit you want to fetch data from
subreddit_name = 'soccer'

# Get the soccer subreddit
subreddit = reddit.subreddit(subreddit_name)

posts = subreddit.search(query = "goal", sort = "top", time_filter = "month", limit = 200)

# Print the title and score of each post
posts_json = []
for post in posts:

    #Check if post does contains a media 
    if "Media" not in post.link_flair_text : 
        continue

    # Check if there is a goal pattern in the title 
    # example : MCO [1] - 0 UTS, Ali thiam (Great fucking goal !) 
    if not re.findall("[\[][0-9][\]]", post.title) :
        continue

    dict_ = {
        "id" : post.id,
        "title" : post.title,
        "text_html" : post.selftext_html,
        "flair" : post.link_flair_text,
        "is_video" : post.secure_media["reddit_video"]["fallback_url"] if post.is_video else None,
        "domain" : post.domain,
        "url" : post.url,
        "media_embedded" : post.secure_media_embed["media_domain_url"] if post.secure_media_embed != {} else None
    }

    posts_json.append(dict_)


with open("posts.json" , "w") as f : 
    f.write(json.dumps(posts_json))

print(len(posts_json))