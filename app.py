import os
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import  StringField, IntegerField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email
from dotenv import load_dotenv
from flask_mail import Mail, Message

# Load environment variables from the .env file
load_dotenv()

app = Flask(__name__)

# Set the secret key from the environment variable
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')  # Set your Gmail email as an environment variable
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')  # Set your Gmail password (or app-specific password) as an environment variable
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

#create a form class
class NamerForm(FlaskForm):
    name = StringField("What's Your Name? for real", validators=[DataRequired()])
    submit = SubmitField("Submit")

class EmailForm(FlaskForm):
    email = StringField("Please enter your email", validators=[DataRequired()])
    submit = SubmitField("Submit")

class SessionForm(FlaskForm):
    first_name = StringField("Your First Name", validators=[DataRequired()])
    last_name = StringField("Your Last Name", validators=[DataRequired()])
    email = StringField("Your Email", validators=[DataRequired()])
    company_name = StringField("Company Name", validators=[DataRequired()])
    company_url = StringField("Company Website/URL", validators=[DataRequired()])
    company_size = IntegerField("Company Size", validators=[DataRequired()])
    comment = TextAreaField("Tell us about your Interests..", validators=[DataRequired()])

    submit = SubmitField("Submit")

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/index', methods=['GET', 'POST'])
def index():
    form = EmailForm()
    if form.validate_on_submit():
        # Email content
        subject = f"New Email from {form.email.data}"
        sender_email = form.email.data
        message_body = f"""
        Email: {form.email.data}
        """
        # Sending the email
        msg = Message(subject=subject,
                      sender=app.config['MAIL_USERNAME'],
                      recipients=[app.config['MAIL_USERNAME']])  # Send to your own business email
        msg.body = message_body
        mail.send(msg)
        flash('Welcome to our Newsletter list!', 'enjoy!')
    return render_template('index.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/team')
def team():
    return render_template('team.html')

@app.route('/session', methods=['GET', 'POST'])
def session():
    form = SessionForm()
    if form.validate_on_submit():
        # Email content
        subject = f"New Session Request from {form.first_name.data} {form.last_name.data}"
        sender_email = form.email.data
        message_body = f"""
        First Name: {form.first_name.data}
        Last Name: {form.last_name.data}
        Email: {form.email.data}
        Company Name: {form.company_name.data}
        Company URL: {form.company_url.data}
        Company Size: {form.company_size.data}
        Comments: {form.comment.data}
        """

        # Sending the email
        msg = Message(subject=subject,
                      sender=app.config['MAIL_USERNAME'],
                      recipients=[app.config['MAIL_USERNAME']])  # Send to your own business email
        msg.body = message_body

        try:
            mail.send(msg)
            flash('Your message has been sent successfully!', 'success')
        except Exception as e:
            flash(f'Failed to send message. Error: {str(e)}', 'danger')

        return redirect(url_for('session'))

    return render_template('session.html', form=form)

#invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.route('/newsletter_signup', methods=['POST'])
def newsletter_signup():
    email = request.form.get('email')

    if email:
        # Process the email for the newsletter (e.g., store it in a database or send a confirmation email)
        
        # Here you can send the email using Flask-Mail or save the email to a database
        flash('Thank you for signing up for our newsletter!', 'success')
    else:
        flash('Please enter a valid email address.', 'danger')

    return redirect(url_for('index'))  # Assuming your index page is the home page


if __name__ == '__main__':
    app.run()
