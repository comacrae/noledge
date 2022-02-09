from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField 
from wtforms.widgets.html5 import NumberInput
from wtforms.validators import DataRequired, NumberRange
from modules import get_answers, setup_pipeline, print_answers_demo

app = Flask(__name__)

# Flask-WTF requires an encryption key - the string can be anything
app.config['SECRET_KEY'] = 'XAQhvkusaB1P3cPYzqlzBoRPBrPs7p4C'

pipeline = setup_pipeline("distilbert-base-uncased-distilled-squad", "./corpus")

# Flask-Bootstrap requires this line
Bootstrap(app)

class QuestionForm(FlaskForm):
    question = StringField("Enter your question here:", 
            validators=[DataRequired()]
            )
    top_k = IntegerField("Enter number of answers to be determined (1-10):", 
            validators=[DataRequired(), NumberRange(1,10,"Must be between 1 and 10")],
            widget= NumberInput(min=1, max=10)
            )
    submit = SubmitField("Submit")

@app.route('/', methods=['GET', 'POST'])
def index():
    form = QuestionForm()
    message = ""
    answers = {}
    if form.validate_on_submit():
        question = form.question.data
        top_k = form.top_k.data
        response_dict = get_answers(question,pipeline,top_k) 
        form.top_k.data = 0
        form.question.data = ""
        return render_template('answers.html', 
                answers=response_dict['answers']['answers'],
                question=response_dict['question'])
    else:
        return render_template('index.html', form=form)

@app.route('/chrome-ex-form', methods=['GET'])
def chrome_ex_form():
    question = request.form['question']
    top_k = request.form['top_k']
    return get_answers(question,pipeline,top_k)# automatically returned in JSON format   

@app.route('/chrome-ex', methods=['GET'])
def chrome_ex():
    question = request.args.get('question')
    top_k = int(request.args.get('top_k'))
    return get_answers(question,pipeline,top_k)# automatically returned in JSON format   

@app.route('/help.html')
def help():
    return render_template('help.html')

