import os
from flask import Flask, request, jsonify
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
import nltk

nltk.download('punkt')
nltk.download('stopwords')

app = Flask(__name__)
CORS(app)

def preprocess_text(text):
    tokens = word_tokenize(text)
    tokens = [word.lower() for word in tokens if word.isalpha()]
    tokens = [word for word in tokens if word not in stopwords.words('english')]
    return tokens

def calculate_match_percentage(cv_tokens, job_tokens):
    cv_word_count = Counter(cv_tokens)
    job_word_count = Counter(job_tokens)

    total_keywords = len(job_word_count)
    
    if total_keywords == 0:
        return 0  # Avoid division by zero

    matching_keywords = sum(min(cv_word_count[key], job_word_count[key]) for key in job_word_count.keys())

    match_percentage = (matching_keywords / total_keywords) * 100

    return match_percentage

@app.route('/', methods=['POST'])
def calculate_matches():
    try:
        data = request.get_json()
        cvs = data['cvs']
        job_description = data['Oportunidad_Laboral']
        
        results = []
        
        job_tokens = preprocess_text(job_description)
        
        for cv in cvs:
            cv_text = cv['CV']
            cv_tokens = preprocess_text(cv_text)
            match_percentage = calculate_match_percentage(cv_tokens, job_tokens)
            results.append({
                'id_candidato': cv['id_candidato'],
                'match_percentage': match_percentage
            })
        
        return jsonify(results)
    except KeyError:
        return jsonify({'error': 'Invalid JSON data'}), 400

if __name__ == '__main__':
    app.run(debug=False)
