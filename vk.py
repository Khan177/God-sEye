import requests
from flask import Flask, render_template, url_for,request
app = Flask(__name__)

token = '2c3233b12c3233b12c3233b1f02c59b56b22c322c3233b17112c7455c983a2581564817'
version = 5.101
def take_posts(inputId):
    owner_id = inputId
    first_name = ""
    last_name = ""
    dataToSend = []
    response = requests.get('https://api.vk.com/method/wall.get',
                            params={
                                'access_token': token,
                                'v' : version,
                                'owner_id': owner_id, 
                                #'count' : 1 
                                })
    postCount = response.json()['response']['count']
    #print(postCount)
    dataToSend.append(postCount)

    posts = response.json()['response']['items']
    #print(posts)

    commentCount = 0
    for comments in posts:
        commentCount = commentCount + comments['comments']['count']
    #print(commentCount)
    dataToSend.append(commentCount)

    likeCounter = 0
    for likes in posts: 
        likeCounter=likeCounter+likes['likes']['count']
    #print(int(likeCounter/postCount))
    dataToSend.append(likeCounter)
    
    response = requests.get('https://api.vk.com/method/users.get',
                            params={
                                'access_token': token,
                                'v' : version,
                                'user_ids': owner_id, 
                                
                            })
    data = response.json()['response']
    for info in data:
        #print(len(info))
        first_name = info['first_name']
        last_name = info['last_name']
    dataToSend.append(first_name)
    dataToSend.append(last_name)

    response = requests.get('https://api.vk.com/method/friends.get',
                            params={
                                'access_token': token,
                                'v' : version,
                                'user_id': owner_id, 
                                
                            })
    friends = response.json()['response']['count']
    #print(friends)
    dataToSend.append(friends)
    return dataToSend


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def result():
    if request.method == 'POST':
        if request.form['social'] == 'VK':
            userLogin=request.form['login']
            data = take_posts(int(userLogin))
        else:
            data = 'Huis'
    
    return render_template('results.html',userData = data)

if __name__ == '__main__':
   app.run(debug = True)