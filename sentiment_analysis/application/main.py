from flask import Flask,request,render_template
import joblib
from functions import *
logistic_model=joblib.load('../models/logistic_model.pkl')
word2vec_model=joblib.load('../models/word2vec.model')
app = Flask(__name__)

@app.route('/' , methods=['GET', 'POST'])
def home_page():
    if request.method == 'GET':
        return render_template('index.html',text=' ',sentiment='')
    if request.method == 'POST':
        text=request.args.get('text')
        text=request.form['text']
        print(text)
        sentiment=predict_sentiment(text)
        print(sentiment)
        return render_template('index.html',text=text,sentiment=sentiment)
    

if __name__ == '__main__':
    app.run(debug=True)
