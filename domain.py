import json 

with open("posts.json", "r") as f : 
    posts = json.loads(f.read())


domains_ = set([post['domain'] for post in posts])
examples_ = []
for domain in domains_ : 
    for post in posts : 
        if post["domain"] == domain : 
            examples_.append({domain: post["url"] })
            break


print(examples_)
with open("examples.json", "w") as f :
    f.write(json.dumps(examples_))