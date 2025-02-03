from flask import Flask,request, render_template
import os

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from functions import *
app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
@app.route('/' , methods=['GET', 'POST'])
def matchResume():
    if request.method == 'POST':
        jobDescription = request.form.get('jobtext')  # Job description from the form
        resumes = request.files.getlist('resumes')  # List of resume files uploaded
        
        # Save the uploaded resume files to the specified directory
        for file in resumes:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        
        # Extract text from the resume files
        resumes_text_dict = extract_text_from_files(resumes)
        
        # Preprocess both job description and resumes' text
        job_description = preprocess_text(jobDescription)
        resumes_text_dict = {k: preprocess_text(v) for k, v in resumes_text_dict.items()}
        

        # Initialize TfidfVectorizer
        tfidf_vectorizer = TfidfVectorizer()
        
        # Transform job description and resumes using the vectorizer
        tfidf_job_description = tfidf_vectorizer.fit_transform([job_description])  # Fit and transform job description
        tfidf_resumes = tfidf_vectorizer.transform(resumes_text_dict.values())  # Transform the resumes

        # Calculate cosine similarity between job description and each resume
        similarities = cosine_similarity(tfidf_job_description, tfidf_resumes)

        # Store the similarity scores with the corresponding resume names
        similarity_results = {}
        for idx, file_name in enumerate(resumes_text_dict.keys()):
            similarity_results[file_name] = similarities[0][idx]
        
        top_3_results = dict(sorted(similarity_results.items(), key=lambda item: item[1], reverse=True)[:3])
        print(top_3_results)

        return render_template("index.html", similarity_results=top_3_results)    
        
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)