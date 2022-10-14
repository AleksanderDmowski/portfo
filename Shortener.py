from flask import Flask, render_template, url_for, request, redirect
import random
app = Flask(__name__)


@app.route('/')
def my_home():
    return render_template('index.html')


@app.route('/MyWork/Project/submit_link_shorter', methods=['POST', 'GET'])
def submit_form2():
    if request.method == 'POST':
        link = request.form.get('subject')
        return render_template('/MyWork/Project/linkShorter.html', end_link=(f'Its yout link: {str(shorter(link))}'))
    else:
        return 'something wrong'


def shorter(link):
    auto_grow = True
    txt_dict = {}
    id_start = 10000
    id_end = 10999
    with open('links_database.txt', mode='r+') as database:
        for line in database:
            (k, v) = line.split()
            txt_dict.update({k: v})

        if auto_grow:
            if len(dict(txt_dict)) >= id_end-id_start:
                while id_end-id_start < len(dict(txt_dict)):
                    id_end += 1000

        if link in txt_dict:
            return str(dict(txt_dict).get(link))
        else:
            id_ = random.randint(id_start, id_end)
            x = (f'http://127.0.0.1:5000/linkShorter/{id_}')
            while x in txt_dict.values():
                id_ = random.randint(id_start, id_end)
                x = (f'http://127.0.0.1:5000/linkShorter/{id_}')
            database.write(
                f'{link} {x}\n')
            txt_dict.update({link: x})
            return (dict(txt_dict).get(link))
