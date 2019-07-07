from instagram import Account, Media, WebAgent
import requests
from flask import Flask, render_template, url_for,request
app = Flask(__name__)
def instagram(userLogin):
    agent = WebAgent()
    d={}
    try:
        account = Account(userLogin)
        try:
            firstTenPub, pointer = agent.get_media(account)#last ten publication
            otherPubs, pointer = agent.get_media(account, pointer=pointer, count=account.media_count, delay=1)#other
            places=[]#will be next time
            tenDaysLikes=0
            tenDaysComments=0
            allLikes= 0
            allComments=0
            for i in firstTenPub:
                allLikes=allLikes+i.likes_count
                allComments = allComments+i.comments_count
                tenDaysLikes+=i.likes_count
                tenDaysComments+=i.comments_count

            for i in otherPubs:
                allLikes=allLikes+i.likes_count
                allComments = allComments+i.comments_count
                
            ln = len(otherPubs)+len(firstTenPub)
            d["Avatar: "]=account.profile_pic_url_hd
            d["Average quantity of likes from the last 10 publications: "]=str(tenDaysLikes//len(firstTenPub))
            d["Average quantity of comments from the last 10 publications: "]=str(tenDaysComments//len(firstTenPub))
            d["Average quantity of likes: "]=str(allLikes//ln)
            d["Average quantity of comments: "]=str(allComments//ln)
            d["Nickname: "]=account.username
            d["Quantity of posts: "]=str(account.media_count)
            d["Full Name: "]=account.full_name
            d["Quantity of follows: "]=str(account.follows_count)
            d["Quantity of followers: "]=str(account.followers_count)
            d["Is account private: "]=str(account.is_private)
            d["Account biography: "]=account.biography
        except:
            d["Avatar: "]=account.profile_pic_url_hd
            d["Nickname: "]=account.username
            d["Quantity of follows: "]=str(account.follows_count)
            d["Quantity of followers: "]=str(account.followers_count)
            d["Is account private: "]=str(account.is_private)
            d["Account biography: "]=account.biography

    except:
        d["Avatar: "]="https://avatars.mds.yandex.net/get-zen_doc/125920/pub_5bf184d0e9397500ab3a1aec_5bf18854297efb00aaff9147/scale_600"
        d["Error: "]="404"

    #username
    #information about user
    
    return d


def vk(inputId):
    token = '2c3233b12c3233b12c3233b1f02c59b56b22c322c3233b17112c7455c983a2581564817'
    version = 5.101
    owner_id = inputId
    first_name = ""
    last_name = ""
    dataToSend = {}
    response = requests.get('https://api.vk.com/method/wall.get',
                            params={
                                'access_token': token,
                                'v' : version,
                                'owner_id': owner_id, 
                                #'count' : 1 
                                })
    postCount = response.json()['response']['count']
    #print(postCount)
    dataToSend["Post quantity: "]=str(postCount)

    posts = response.json()['response']['items']
    #print(posts)

    commentCount = 0
    for comments in posts:
        #print(comments['comments']['count'])
        commentCount = commentCount + comments['comments']['count']
    dataToSend["Comments quantity: "]=str(commentCount)

    likeCounter = 0
    for likes in posts: 
        likeCounter=likeCounter+likes['likes']['count']
    #print(likeCounter)
    dataToSend["Likes quantity: "]=str(likeCounter)
    
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
    dataToSend['First Name: ']=first_name
    dataToSend['Last Name: ']=last_name

    response = requests.get('https://api.vk.com/method/friends.get',
                            params={
                                'access_token': token,
                                'v' : version,
                                'user_id': owner_id, 
                                
                            })
    friends = response.json()['response']['count']
    #print(friends)
    
    dataToSend["Friends: "]=str(friends)

    response = requests.get('https://api.vk.com/method/photos.get',
                            params={
                                'access_token': token,
                                'v' : version,
                                'owner_id': owner_id, 
                                'album_id': 'profile'
                                })
    photosCount = response.json()['response']['count']
    #print(photosCount)
    photos = response.json()['response']['items']
    for photo in photos:
        photo
    photoCheck =0
    #print(photo)
    #print(photo['sizes'])
    sizeCheck = 0
    for sizePhoto in photo['sizes']:
        sizePhoto
        sizeCheck+=1
        if sizeCheck ==3:
            break
    dataToSend["Avatar: "]=sizePhoto['url']
    return dataToSend


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def result():
    data =''
    if request.method == 'POST':
        if request.form['social'] == 'VK':
            userLogin=request.form['login']
            data = vk(int(userLogin))
        else:
            userLogin=request.form['login']
            data = instagram(userLogin)
    
    return render_template('results.html',userData = data)

if __name__ == '__main__':
   app.run(debug = True)