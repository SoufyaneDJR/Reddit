"""
Through this script, we want to validate whether the video downloaded is indeed a video, 
or it is just a file with a video format 
"""
import json 
import magic
import os

def validator(post_id) : 
    """
    Validate the nature of the video downloaded
        - True Video  : The video downloaded is checked, and is of type video 
        - False Video : The video downloaded is checked, and is NOT of type video
    """
    mime_type = magic.from_file(post_id + ".mp4", mime=True)
    if mime_type.startswith('video/') : 
        print(f"[Success] Video Nature : {post_id}")
        add_nature(post_id,"nature","True Video")
    else :
        print(f"[ Error ] Video Nature : {post_id}")
        add_nature(post_id,"nature","False Video")

def add_nature(id, key, value):
    with open('examples.json', 'r+') as file:
        posts = json.load(file)
        for post in posts:
            if post['post_id'] == id:
                post[key] = value
                break
        else:
            print(f"[ Error ] Appending database : post_id not found ( id = {post['post_id']})")
            return
        file.seek(0)
        json.dump(posts, file, indent=4)
        file.truncate()
    print(f"[Success] Appending database : Value Added ( id = {post['post_id']})")


# ## Just for testing, NOT FINAL CODE 
# files = [f.split('.')[0] for f in os.listdir(os.getcwd()) if f.endswith("mp4")]

# print(len(files))
# for f_ in files : 
#     validator(f_)
