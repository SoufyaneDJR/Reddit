import json 

from downloader import youtube_download, twitter_download, source_download, reddit_download

with open("posts.json", "r") as f :
    posts = json.loads(f.read())

examples = [{"domain":post["domain"], "id": post["id"], "url" : post["url"]} for post in posts ]

with open("examples.json", 'w') as f :
    f.write(json.dumps(examples))

with open("downloadMethods.json", "r") as f :
    methods = json.loads(f.read())

for post in examples : 
    # What function to use from the function existing in the downloader.py
    func_ = methods[post["domain"]]

    match func_ : 
        case "youtube_download" :
            print(f"{func_}|\t{post['id']}|\t{post['url']}")
            try :
                youtube_download(post["url"], post["id"])
                print(f"[Success] {post['id']}")
            except : 
                print(f"[ Error ] {post['id']}")
                  
        case "reddit_download" : 
            print(f"{func_}|\t{post['id']}|\t{post['url']}")
            try :
                reddit_download(post["url"], post["id"])
                print(f"[Success] {post['id']}")
            except : 
                print(f"[ Error ] {post['id']}")     
        case "source_download" : 
            print(f"{func_}|\t{post['id']}|\t{post['url']}")
            try :
                source_download(post["url"], post["id"])
                print(f"[Success] {post['id']}")
            except : 
                print(f"[ Error ] {post['id']}")     
        case "twitter_download": 
            print(f"{func_}|\t{post['id']}|\t{post['url']}")
            try :
                twitter_download(post["url"], post["id"])
                print(f"[Success] {post['id']}")
            except : 
                print(f"[ Error ] {post['id']}")     
        case _ : 
            print("Domain not recognized !",func_)
