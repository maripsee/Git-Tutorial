from flask import Flask, request, redirect
import random

app = Flask(__name__)

print("git-hub")

nextID = 4
topics = [
    {'id':1, 'title':'html', 'body':'html is ...'},
    {'id':2, 'title':'css', 'body':'css is ...'},
    {'id':3, 'title':'javacript', 'body':'javascript is ...'}
]

# 반복되는 표현을 함수화 
# id가 없는 기본값 None으로 줌
def template(contents, content,id=None):
    contextUI =''
    if id != None:
        contextUI = f'''
                <li><a href="/update/{id}">update</a></li>
                <li><form action="/delete/{id}" method="POST"><input type="submit" value="delete"></form></li>
        '''
    return f'''<!doctype html>
    <html>
        <body>
            <h1><a href ="/">WEB</a><h1>
            <ol>
                {contents}
            </ol>
            {content}
            <ul>
                <li><a href="/create/">create</a></li>
                {contextUI}
            </ul>
        </body>
    </html>
    '''

# 컨텐츠 가져오는 부분도 중복이므로 함수화
def getContents():
    liTags = ''
    for topic in topics:
            liTags = liTags + f'<li><a href="/read/{topic["id"]}/">{topic["title"]}</a></li>'
    return liTags
        
# f string 사용하여 html 코드를 짜기 
@app.route('/')
def index():
    return template(getContents(), '<h2>Welcome</h2>Hello, WEB')
# id읽기 

@app.route('/read/<int:id>/')
def read(id):
    title = ''
    body  = ''        
    for topic in topics:
        if id == topic['id']:
            title = topic['title']
            body = topic['body']
            break

    return template(getContents() ,f'<h2>{title}</h2>{body}', id)
    
@app.route('/create/', methods = ['GET','POST'])
def create():
    # Flask method HTTP 볼것 -> GET, POST로 지정해줘야함
    if request.method == 'GET':
        content = '''
            <form action="/create/" method="POST">
                <p><input type="text" name="title" placeholder="title"></p>
                <p><textarea name="body" placeholder="body"></textarea></p>
                <p><input type="submit" value="create"></p>
            </form>
        '''
        return template(getContents(), content)

    elif request.method =='POST':
        # 전역변수로 지정 사용하기 전에 
        global nextID 
        title = request.form['title']
        body = request.form['body']
        newTopic = {'id':nextID,'title':title,'body':body}
        topics.append(newTopic)
        url = '/read/'+str(nextID)+'/'
        nextID+=1
        # redirect를 사용하면 해당 url로 
        print(topics)
        return redirect(url)

@app.route('/update/<int:id>/', methods = ['GET','POST'])
def update(id):
    # Flask method HTTP 볼것 -> GET, POST로 지정해줘야함
    if request.method == 'GET':
        title = ''
        body  = ''        
        for topic in topics:
            if id == topic['id']:
                title = topic['title']
                body = topic['body']
                break
        content = f'''
            <form action="/update/{id}/" method="POST">
                <p><input type="text" name="title" placeholder="{title}"></p>
                <p><textarea name="body" placeholder="{body}"></textarea></p>
                <p><input type="submit" value="update"></p>
            </form>
        '''
        return template(getContents(), content)

    elif request.method =='POST':
        # 전역변수로 지정 사용하기 전에 

        title = request.form['title']
        body = request.form['body']

        for topic in topics:
            if id == topic['id']:
                topic['title'] = title
                topic['body'] = body
                break

        url = '/read/'+str(id)+'/'
        # redirect를 사용하면 해당 url로 
        return redirect(url)

@app.route('/delete/<int:id>/', methods = ['POST'])
def delete(id):
    for topic in topics:
        if id ==topic['id']:
                topics.remove(topic)
                break
    return redirect('/')
# debug는 자동으로 flask가 실행되었다가 종료됨
app.run(port=5001, debug=True)