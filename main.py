from flask import Flask, request, jsonify, render_template
from flask_mail import Mail, Message
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

app = Flask(__name__)

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'test.testington.788@gmail.com'
app.config['MAIL_PASSWORD'] = 'TestingtonPassword123'
mail = Mail(app)

# Scheduler
scheduler = BackgroundScheduler()
scheduler.start()
atexit.register(lambda: scheduler.shutdown())

@app.route('/')
def index():
    return render_template("test.html")

@app.route('/send_email',methods=['POST'])
# def send_email(to, subject, body):
def send_email():
    subject="tesT"
    to="test.testington.788@gmail.com"
    body="testing email generation"
    msg = Message(subject, recipients=[to], body=body)
    mail.send(msg)

@app.route('/schedule_email', methods=['POST'])
def schedule_email():
    data = request.json
    to = data['to']
    subject = data['subject']
    body = data['body']
    send_time = data['send_time']  # Expected format: 'YYYY-MM-DD HH:MM:SS'

    scheduler.add_job(func=send_email, trigger='date', run_date=send_time, args=[to, subject, body])
    return jsonify({"message": "Email scheduled successfully!"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
