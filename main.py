from google.oauth2 import service_account
from flask import Flask, render_template, url_for, request, redirect
from google.cloud import storage
import os
import random
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = ('porfoad-2611d2f26375.json')
app = Flask(__name__)

# credentials = service_account.Credentials.from_service_account_file("your-json-path-with-filename.json")
# # client = language.LanguageServiceClient(credentials=credentials)
storage_client = storage.Client()
# my_bucket = storage_client.get_bucket('porfoad.appspot.com')
server = 'http://127.0.0.1:5000'

project_id = "porfoad"
test_mode = True
flask_run = True


def authenticate_implicit_with_adc(project_id):
    storage_client = storage.Client(project=project_id)
    buckets = storage_client.list_buckets()
    print("Buckets:")
    for bucket in buckets:
        print(bucket.name)
    print("Listed all storage buckets.")


# authenticate_implicit_with_adc(project_id)


@app.route('/')
def my_home():
    return render_template('index.html')


@app.route('/<path:url>')
def page(url):
    return render_template('/'+url)


@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        data = request.form.to_dict()
        write_to_file(data)
        return render_template('contact.html')
    else:
        return 'somethig wrong'


def write_to_file(data):
    with open('database.txt', mode='a') as database:
        email = data['email']
        subject = data['subject']
        message = data['message']
        file = database.write(
            f'\nFrom: {email}\nTopic: {subject}\n{message}\n')

# ///////////////////////////////////////////////////////////


@app.route('/MyWork/Project/submit_link_shorter', methods=['POST', 'GET'])
def submit_form2():
    if test_mode:
        print('Test mode submit_form2')
    if request.method == 'POST':
        link = request.form.get('subject')
        return render_template('/MyWork/Project/linkShorter.html', end_link=(f'Its yout link: {str(shorter(link))}'))
    else:
        return 'something wrong'


# def shorter(link):
#     auto_grow = True
#     txt_dict = {}
#     id_start = 10000
#     id_end = 10999
#     with open('links_database.txt', mode='r+') as database:
#         for line in database:
#             (k, v) = line.split()
#             txt_dict.update({k: v})

#         if auto_grow:
#             if len(dict(txt_dict)) >= id_end-id_start:
#                 while id_end-id_start < len(dict(txt_dict)):
#                     id_end += 1000

#         if link in txt_dict:
#             return str(dict(txt_dict).get(link))
#         else:
#             id_ = random.randint(id_start, id_end)
#             x = (f'https://www.aleksanderdmowski.com/linkShorter/{id_}')
#             while x in txt_dict.values():
#                 id_ = random.randint(id_start, id_end)
#                 x = (f'https://www.aleksanderdmowski.com/linkShorter/{id_}')
#             database.write(
#                 f'{link} {x}\n')
#             txt_dict.update({link: x})
#             return (dict(txt_dict).get(link))


# @app.route('/linkShorter/<id_db>')
# def go_to(id_db):
#     with open('links_database.txt', mode='r') as database:
#         for line in database:
#             (k, v) = line.split()

#             if ('https://www.aleksanderdmowski.com/linkShorter/'+id_db) == v:
#                 return redirect(k)
#     return 'something wrong'

# # /////////////////////////////////////


@app.route('/MyWork/Project/todo', methods=['POST', 'GET'])
def submit_link_shorter():
    if request.method == 'POST':
        link = request.form.get('subject')
        return render_template('/MyWork/Project/linkShorter.html', end_link=(f'Its yout code for share: {str(shorter(link))}'))
    else:
        return 'something wrong'

# /////
# /////
# /////


def shorter(link, project_id=project_id, bucket_name='porfoad.appspot.com', blob_name='links_database.txt'):
    if test_mode:
        print('test mode start shorter function')
    storage_client = storage.Client(project=project_id)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    auto_grow = True
    txt_dict = {}
    id_start = 10000
    id_end = 10999
    # with open('links_database.txt', mode='r+') as database:
    # update(bucket_name='porfoad.appspot.com', blob_name='links_database.txt') as database:
    with blob.open("r") as database:
        print(txt_dict)
        for line in database:
            (k, v) = line.split()
            txt_dict.update({k: v})

        if auto_grow:
            if len(dict(txt_dict)) >= id_end-id_start:
                while id_end-id_start < len(dict(txt_dict)):
                    id_end += 1000

        if link in txt_dict:
            if test_mode:
                print(str(dict(txt_dict).get(link)))
            return str(dict(txt_dict).get(link))
        else:
            if test_mode:
                print('dodawanie nowego linku')
            id_ = random.randint(id_start, id_end)
            x = (f'https://www.aleksanderdmowski.com/linkShorter/{id_}')
            while x in txt_dict.values():
                id_ = random.randint(id_start, id_end)
                x = (f'https://www.aleksanderdmowski.com/linkShorter/{id_}')

            txt_dict.update({link: x})
            y = ''
            print(txt_dict)
            for k in txt_dict:
                y += (f'{k} {txt_dict[k]}\n')
            print(y)
            blob.upload_from_string(y)

            if test_mode:
                print(
                    f"{blob_name} with contents {link} as {x} uploaded to {bucket_name}.")
            return str(dict(txt_dict).get(link))


@app.route('/linkShorter/<id_db>')
def go_to(id_db, bucket_name='porfoad.appspot.com', blob_name='links_database.txt'):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    with blob.open("r") as database:
        for line in database:
            (k, v) = line.split()

            if ('https://www.aleksanderdmowski.com/linkShorter/'+id_db) == v:
                return redirect(k)
    return 'something wrong'

# /////////////////////////////////////


def clear(project_id, bucket_name='porfoad.appspot.com', blob_name='links_database.txt'):
    storage_client = storage.Client(project=project_id)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_string('')
    print('clear')


# shorter('https://www.google.com/search?q=git+force+pull&oq=git+force+pu&aqs=chrome.1.0i512l2j69i57j0i512l6j69i64.5064j0j7&sourceid=chrome&ie=UTF-8')
