from flask import Flask, request, jsonify,render_template
import spacy 
from spacy import displacy
nlp=spacy.load('en_core_web_sm')

app = Flask(__name__)

@app.route('/' , methods=['POST','GET'])
def entity():
    if request.method=='POST':
        text = request.form.get('text')
        if text:
            doc=nlp(text)
            html=displacy.render(doc,style='ent',jupyter=False)
            return render_template('index.html',html=html,text=text)
            
    if request.method=='GET':  
        return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)