from lib2to3.pgen2.token import NEWLINE
from os import name
from flask import Flask, render_template, url_for, request, redirect
from markupsafe import escape
import csv


app = Flask(__name__)
print(__name__)


@app.route('/')
def home():
    return render_template('index.html')

# restructure code to dynamically get page data for endpoint


@app.route('/<string:page_name>')
def web_page(page_name):
    return render_template(page_name)


def write_to_file(data):
    with open('database.txt', mode='a') as database:
        email = data['email']
        subject = data['subject']
        message = data['message']
        file = database.write(f"\n{email},{subject},{message}")


def write_to_csv(data):
    with open('database.csv', mode='a', newline='') as database2:
        email = data['email']
        subject = data['subject']
        message = data['message']
        fieldnames = ['email', 'subject', 'message']
        csvwriter = csv.DictWriter(database2, fieldnames=fieldnames)
        csvwriter.writerow(
            {'email': email, 'subject': subject, 'message': message})


@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            write_to_csv(data)
            return redirect('thankyou.html')
        except NameError:
            return 'Did not save to database'
    else:
        return 'Something went wrong. Try again!'
