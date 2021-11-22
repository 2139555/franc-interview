from flask import Flask, json, render_template, jsonify, Response, request
from datetime import datetime
app = Flask(__name__)
username=''
@app.route('/')
def index_view():
    return users_view()


with open('./users.json', 'r') as f:
    users = f.read()
with open('./posts.json', 'r') as f:
    posts = f.read()

@app.route('/form_login',methods=['POST','GET'])
def login():
    global username
    username=request.form['username']
    if username not in users:
	    return render_template('index.html',info='Invalid User')
    else:
        return(timeline(username,username,'Your','can'))

def timeline(username, user, otheruser,can):
    all_posts = json.loads(posts)
    all_users = json.loads(users)
    folowers = all_users[username]
    my_tweets = all_posts[username]
    my_folow_posts =[]
    for post in my_tweets:
        if(can):
            post['user'] = 'You'
        else:
            post['user'] = username
        my_folow_posts.append(post)
    for folower in folowers:
        for post in all_posts[folower]:
            post['user'] = folower
            my_folow_posts.append(post)
    sorted_posts= sorted(my_folow_posts, key=lambda x:datetime.strptime(x['time'], "%Y-%m-%dT%H:%M:%S%z"), reverse=True)
    for post in sorted_posts:
        split_string = post['time'].split("Z", 1)
        date =datetime.strptime(split_string[0], "%Y-%m-%dT%H:%M:%S")
        post['time'] = date
    return render_template('index.html', username = user, timeline_list= sorted_posts , otheruser=otheruser, can_post=can)

def users_view():
    all_users = json.loads(users)
    return render_template('index.html',users = all_users)

@app.route('/view_user',methods=['POST','GET'])
def view_user_timeline():
    username=request.form['user']
    all_posts = json.loads(posts)
    return timeline(username,'user', username+'\'s','')

@app.route('/form_tweet',methods=['POST','GET'])
def new_tweet():
    tweet=request.form['tweet']
    date = datetime.today().strftime("%Y-%m-%dT%H:%M:%S%z")+"Z"
    my_tweet = {"status": tweet, "time": date}
    #tweet_json = jsonify(my_tweet)
    global posts
    all_posts = json.loads(posts)
    all_posts[username].append(my_tweet)
    with open('./posts.json', 'w') as f:
        json.dump(all_posts,f)
    with open('./posts.json', 'r') as f:
        posts = f.read()
    return(timeline(username,username,'Your','can'))

if __name__ == '__main__':
    app.run(host='127.0.0.1')
