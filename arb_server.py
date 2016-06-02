from flask import Flask, render_template, request, url_for, jsonify
from flask.ext.api import FlaskAPI, status, exceptions
from flask.ext.api.decorators import set_renderers
from flask.ext.api.renderers import HTMLRenderer
from flask.ext.mail import Mail, Message
import shlex
import subprocess
from werkzeug import secure_filename
from os import path
from pymongo import MongoClient
import json
from bson import json_util
from bson.objectid import ObjectId

UPLOAD_FOLDER = '/data/'
ALLOWED_EXTENSIONS = set(['csv', 'json', 'kml'])

app = FlaskAPI(__name__)
mail = Mail(app)
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

client = MongoClient('mongodb://arbapp:arb2016@ds021663.mlab.com:21663/heroku_z83skz63')
db = client.heroku_z83skz63

about_text = '''Kalamazoo College's Lillian Anderson Arboretum comprises 140 acres of marsh, meadow, pine plantation and second-growth deciduous forest in Oshtemo Township, Kalamazoo County, Michigan.\n\n
Several families worked the land between the early-19th and mid-20th centuries. Lillian Anderson, a K graduate, donated approximately 100 acres of her family's farm to the College in 1982. In 2000, thanks to the generous financial assistance of Dr. and Mrs. H. Lewis Batts, the College added 31 acres of land along the eastern boundary of the original Anderson property. The Arboretum was established in 1998 as a resource for the Kalamazoo College community, Kalamazoo-area residents, and visitors to the area.
'''

def string_rep(str):
    return {
        'url': request.host_url.rstrip('/') + url_for('about'),
        'text': str
    }

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def db_import(filename):
    args = ['mongoimport', '--db', 'arb',
            '--type', filename.rsplit('.', 1)[1],
            '--headerline', '--ignoreBlanks',
            '--file', filename]
    proc = subprocess.Popen(args)

def item_rep(item):
    print  {
        'id': str(item['_id']),
        'data': item
    }
    return {
        'id': str(item['_id']),
        'data': item
    }

def to_json(data):
    return json.dumps(data, default=json_util.default)

@app.route('/', methods=['GET', 'POST'])
@set_renderers(HTMLRenderer)
def home():
    if request.method == 'POST':
        # print 'post'
        # print request.files
        # file = request.files['file']
        # print 'checking file'
        # if file and allowed_file(file.filename):
        #     print 'file allowed'
        #     filename = secure_filename(file.filename)
        #     print filename
        #     print UPLOAD_FOLDER
        #     print os.path.abspath()
        #     file.save(os.path.join(os.path.abspath(__file__), app.config['UPLOAD_FOLDER'], filename))
        #     print 'saved'
        #     # db_import(filename)

        return redirect(url_for('main'))
    return render_template('main.jade')

@app.route('/about/', methods=['GET'])
def about():
    return string_rep(about_text)

@app.route('/mail/', methods=['POST'])
def mail():
    name = str(request.data.get('name', ''))
    email = str(request.data.get('email', ''))
    body = str(request.data.get('body', ''))

    message = Message('Message from Arb App',
                        sender=email,
                        recipient='riley.lundquist12@kzoo.edu',
                        body='Message from %s:\n\n%s' % (name, body))
    mail.send(message)

@app.route('/<string:collection>/', methods=['GET'])
def query(collection):
    cursor = db[collection].find()
    items = [to_json(item) for item in cursor]
    return items

if __name__ == '__main__':
    app.run(host='0.0.0.0')
