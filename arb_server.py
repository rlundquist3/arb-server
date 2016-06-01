from flask import Flask, render_template, request, url_for
from flask.ext.api import FlaskAPI, status, exceptions
from flask.ext.mail import Mail, Message
import shlex
import subprocess
from werkzeug import secure_filename

UPLOAD_FOLDER = '/data/'
ALLOWED_EXTENSIONS = set(['csv', 'json', 'kml'])

app = FlaskAPI(__name__)
mail = Mail(app)
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            db_import(filename)

            return redirect(url_for('index'))
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



if __name__ == '__main__':
    app.run(host='0.0.0.0')
