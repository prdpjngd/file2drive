import requests
import ast
import urllib.parse
import base64
import os
from flask import Flask, render_template, request, redirect, make_response
app = Flask(__name__)


#sensetive data os.environ['S3_KEY']
client_id=os.environ['c_i']
client_secret=os.environ['c_s']
redirect_uri=''
mya=os.environ['mya']




#global inicialization block
access_token=''
refresh_token=''
login_url='https://accounts.google.com/o/oauth2/v2/auth?scope=https%3A//www.googleapis.com/auth/drive+https://www.googleapis.com/auth/userinfo.profile&access_type=offline&include_granted_scopes=true&redirect_uri='+redirect_uri+'&response_type=code&client_id='+client_id+'&prompt=consent'




#Routing is here (URLs - used for there respective jobs)
@app.route('/',methods = ['GET'])
def home():
    d_btn=1#download button  variable : 1 - yes & 0 - no
    welcome=0 # welcome message variable : 0 - no & 1 - yes
    u_name='USER-733657s'
    u_pic_url='https://cdn2.iconfinder.com/data/icons/user-management/512/temporary-512.png'
    file_id = request.args.get('file')
    if file_id:
        if len(file_id)%4==0:
            file_id=str(base64.b64decode(bytes(file_id, 'utf-8'))).split("'")[1]
            #check - file ID is givan to page
        metadata=requests.get('https://www.googleapis.com/drive/v3/files/'+file_id+'?key='+mya+'&fields=*').text
        #if file ID is wrong
        if 'error' in metadata:
            f_name='File Not Found !'
            f_type='File might be deleted from Google Drive by Owner.'
            f_size='ERROR(0KB)'
            d_btn=0
        # File ID is correct
        else:
            f_name=str(metadata).split('"name": "')[1].split('"')[0]
            f_type=str(metadata).split('"mimeType": "')[1].split('"')[0]
            f_size=str(int(int(str(metadata).split('"size": "')[1].split('"')[0])/1000000))+'MB'
            welcome=0
    # case when file is not given
    else:
        f_name=''
        f_type=''
        f_size=''
        welcome=1
    #access_token and refresh_token check up in the cookies
    if 'a_t' and 'r_t' in request.cookies:
        access_token = request.cookies.get("a_t")
        refresh_token = request.cookies.get("r_t")
        url='https://www.googleapis.com/oauth2/v1/userinfo?alt=json&access_token='+access_token
        html_op = requests.get(url).text
        if "error" in html_op:
            data = {
                'client_id': client_id,
                'client_secret': client_secret,
                'grant_type': 'refresh_token',
                'refresh_token': refresh_token
                }
            response = requests.post('https://www.googleapis.com/oauth2/v4/token', data=data)
            response=ast.literal_eval(response.text.replace('\n','').replace(' "','"').replace('false','"false"'))
            if 'error' in response:
                return redirect(login_url, code=302)
            else:
                access_token=response['access_token']
                url='https://www.googleapis.com/oauth2/v1/userinfo?alt=json&access_token='+access_token
                html_op = requests.get(url).text
                if 'error' in html_op:
                    u_name='Failed to load [ But login Sucess ]'
                    u_pic_url='https://cdn2.iconfinder.com/data/icons/user-management/512/temporary-512.png'
                else:
                    u_name=str(html_op).split('"name": "')[1].split('"')[0]
                    u_pic_url=str(html_op).split('"picture": "')[1].split('"')[0]
                resp=make_response(render_template('index.html',log_q=1,name=u_name,pic_url=u_pic_url,f_name=f_name,f_type=f_type,f_size=f_size,welcome=welcome,d_btn=d_btn))
                resp.set_cookie('a_t', access_token)
                return resp
        else:
            u_name=str(html_op).split('"name": "')[1].split('"')[0]
            u_pic_url=str(html_op).split('"picture": "')[1].split('"')[0]
            return render_template('index.html',log_q=1,name=u_name,pic_url=u_pic_url,f_name=f_name,f_type=f_type,f_size=f_size,welcome=welcome,d_btn=d_btn)
    else:
        return render_template('index.html',log_q=0,f_name=f_name,f_type=f_type,f_size=f_size,welcome=welcome,d_btn=d_btn)

@app.route('/login')
def login():
    uri=str(request.url)
    redirect_uri=uri.split('/')[0]+'//'+uri.split('/')[2]+'/auth'
    return redirect(login_url, code=302)

@app.route('/auth',methods = ['GET'])
def auth():
    code = request.args.get('code')
    code= urllib.parse.unquote(code)
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'authorization_code',
        'redirect_uri': redirect_uri,
        'code': code
    }
    response = requests.post('https://oauth2.googleapis.com/token', data=data)
    response=ast.literal_eval(response.text.replace('\n','').replace(' "','"').replace('false','"false"'))
    access_token=response['access_token']
    refresh_token=response['refresh_token']
    resp = make_response(render_template('login.html'))
    resp.set_cookie('a_t', access_token)
    resp.set_cookie('r_t', refresh_token)
    return resp

@app.route('/open',methods = ['GET'])
def open():
    file_id = request.args.get('file')
    if len(file_id)%4==0:
        file_id=str(base64.b64decode(bytes(file_id, 'utf-8'))).split("'")[1]
    if file_id:
        access_token='Bearer '+ request.cookies.get("a_t")
        headers = {
            'Authorization': access_token,
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        params = (
            ('key', mya),
        )
        data = '{}'
        response = requests.post('https://www.googleapis.com/drive/v3/files/'+file_id+'/copy', headers=headers, params=params, data=data)
        response=ast.literal_eval(response.text.replace('\n','').replace(' "','"').replace('false','"false"'))
        if 'error' in response:
            warning=1
            return render_template('gdrive.html',warning=1)
        else:
            n_file_id=str(response).split("'id': '")[1].split("'")[0]
            return render_template('gdrive.html',n_file_id=n_file_id)

@app.route('/upload',methods = ['GET'])
def upload():
    file_id = request.args.get('file')
    if file_id:
        if 'https://drive.google.com/file/d/' in file_id:
            file_id=file_id.split('/')[5]
        elif 'https://drive.google.com/open?id=' in file_id:
            file_id=file_id.split('/')[3].split('=')[1]
        n_file_id=base64.b64encode(bytes(file_id, 'utf-8'))
        n_file_id=redirect_uri.split('/')[0]+'//'+redirect_uri.split('/')[2]+'/?file='+str(n_file_id).split("'")[1]
        return render_template('upload.html',n_file_id=n_file_id)
    else:
        return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
