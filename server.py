from flask import Flask, render_template, url_for, request
app = Flask(__name__)

@app.route('/')
def my_home():
    return render_template('index.html')

@app.route('/MyWork/<path:page_name>')
def page2(page_name):
    return render_template('/MyWork/'+page_name)

@app.route('/MyWork/FakeYouTube/<path:page_name>')
def project3(page_name):
    return render_template('/MyWork/FakeYouTube/'+page_name)

@app.route('/<string:page_name>')
def page(page_name):
    return render_template(page_name)


@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        data = request.form.to_dict()
        write_to_file(data)
        return 'horaaay'
    else:
        return 'somethig wrong'

def write_to_file(data):
    with open('database.txt', mode='a') as database:
        email = data['email']
        subject = data['subject']
        message = data['message']
        file = database.write(f'\nFrom: {email}\nTopic: {subject}\n{message}\n')

@app.route('/generate')
def generate():
   print('Hello World!')