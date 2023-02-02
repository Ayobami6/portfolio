import os
from flask import Flask, render_template, url_for, request, redirect
from flask_mail import Mail, Message
import csv

app = Flask(__name__)
print(__name__)

# Configuring Flask mail
app.config["MAIL_DEFAULT_SENDER"] = os.environ["MAIL_SENDER"]
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config["MAIL_USERNAME"] = os.environ["MAIL_USERNAME"]
app.config["MAIL_PASSWORD"] = os.environ["MAIL_PASSWORD"]
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)


@app.route('/')
def home():
    return render_template('index.html')

# restructure code to dynamically get page data for endpoint


@app.route('/<string:page_name>')
def web_page(page_name):
    return render_template(page_name)


def send_mail(data):
    email = data["email"]
    name = data["name"]
    msg = Message(subject="Thanks For Reaching Out",
                  recipients=[email],
                  body=f"Hi, {name} \nThanks for reaching out, will get back shortly")
    mail.send(msg)


def write_to_csv(data):
    with open('database.csv', mode='a', newline='') as database2:
        email = data['email']
        name = data['name']
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
            send_mail(data)
            return redirect('thankyou.html')
        except NameError:
            return 'Did not save to database'
    else:
        return 'Something went wrong. Try again!'
