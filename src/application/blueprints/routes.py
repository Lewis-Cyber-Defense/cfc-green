from flask import Blueprint, render_template, request, session, current_app, redirect
from application.database import login, register
from application.util import response, is_authenticated, token_verify
from datetime import datetime
import os
web = Blueprint('web', __name__)
api = Blueprint('api', __name__)

@web.route('/')
def index():
    return render_template('index.html')

@web.route('/login')
def web_login():
    return render_template('login.html')

# Begin static pages
@web.route('/contact')
def web_contact():
    return render_template('contact.html')

@web.route('/solar')
def web_solar():
    return render_template('solar.html')

@web.route('/manufacturing')
def web_manufacturing():
    return render_template('manufacturing.html')

# Authenticated stuff
@web.route('/dashboard')
@is_authenticated
def dashboard():
    def make_tree(path):
        tree = dict(name=os.path.basename(path), children=[])
        try: lst = os.listdir(path)
        except OSError:
            pass #ignore errors
        else:
            for name in lst:
                fn = os.path.join(path, name)
                if os.path.isdir(fn):
                    tree['children'].append(make_tree(fn))
                else:
                    with open(fn, 'rb') as f:
                        contents = f.read()
                    tree['children'].append(dict(name=name, contents=contents))
        return tree

    current_user = token_verify(session.get('auth'))
    if current_user.get('username') == "plank":
        try:
            with open('/app/application/emails.csv') as fd:
                emails = [x.split(',') for x in fd.readlines()]
        except Exception:
            emails = [('12-12-1337', 'Ryan An00bRektn', 'an00b@notateamserver.xyz')]   

        return render_template('dashboard.html', user=current_user.get('username'), tree=make_tree('application/static/uploads'), emails=emails)
    else:
        return render_template('dashboard-user.html', user=current_user.get('username'))

@web.route('/logout')
def logout():
    session['auth'] = None
    return redirect('/')

@api.route('/upload', methods=['POST'])
def upload():
    #myfile = request.get_json.get('body', '')
    myfile = request.files['file']
    myfile.save('/app/application/static/uploads/'+myfile.filename)
    return response('Done!'), 200

@api.route('/login', methods=['POST'])
def api_login():
    if not request.is_json:
        return response('Invalid JSON!'), 400
    
    data = request.get_json()
    username = data.get('username', '')
    password = data.get('password', '')
    
    if not username or not password:
        return response('All fields are required!'), 401
    
    user = login(username, password)
    
    if user:
        session['auth'] = user
        return response('Success'), 200
        
    return response('Invalid credentials!'), 403

@api.route('/contact', methods=['POST'])
def api_contact():
    if not request.is_json:
        return response('Invalid JSON!'), 400
    
    data = request.get_json()
    name = data.get('contactName', '').replace(',', ' ')
    email = data.get('contactEmail', '').replace(',', ' ')
    phone = data.get('contactPhone').replace(',', ' ')
    
    if not name or not email or not phone:
        return response('All fields are required!'), 401
    
    with open('/app/application/emails.csv', 'a') as fd:
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        fd.write(f"{now},{name},{email},{phone}\n")
        return response('Success'), 200
        
    return response('Success'), 200

"""
@api.route('/register', methods=['POST'])
def api_register():
    if not request.is_json:
        return response('Invalid JSON!'), 400
    
    data = request.get_json()
    username = data.get('username', '')
    password = data.get('password', '')
        
    if not username or not password:
        return response('All fields are required!'), 400
    
    user = register(username, password)
    
    if user:
        return response('User registered! Please login')
    
    return response('User exists already!'), 409
"""