from flask import request, url_for
from flask.ext.api import FlaskAPI, status, exceptions

app = FlaskAPI(__name__)

about_text = '''Kalamazoo College's Lillian Anderson Arboretum comprises 140 acres of marsh, meadow, pine plantation and second-growth deciduous forest in Oshtemo Township, Kalamazoo County, Michigan.\n\n
Several families worked the land between the early-19th and mid-20th centuries. Lillian Anderson, a K graduate, donated approximately 100 acres of her family's farm to the College in 1982. In 2000, thanks to the generous financial assistance of Dr. and Mrs. H. Lewis Batts, the College added 31 acres of land along the eastern boundary of the original Anderson property. The Arboretum was established in 1998 as a resource for the Kalamazoo College community, Kalamazoo-area residents, and visitors to the area.
'''

def string_rep(str):
    return {
        'url': request.host_url.rstrip('/') + url_for('about'),
        'text': str
    }

@app.route('/', methods=['GET'])
def home():
    return string_rep('connected to arb server')

@app.route('/about/', methods=['GET'])
def about():
    return string_rep(about_text)

if __name__ == '__main__':
    app.run()
