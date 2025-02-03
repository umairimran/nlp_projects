import pdfplumber
import docx
import re



def extract_text_from_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text()
    return text

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    text = ''
    for para in doc.paragraphs:
        text += para.text
    return text

def extract_text_from_txt(txt_path):
    with open(txt_path,'r',encoding='utf-8') as file:
        return file.read()
    

def extract_text_from_files(resumes):
    resumes_text_dict={}
    for resume in resumes:
        if resume.filename.endswith('.pdf'):
            text=extract_text_from_pdf(resume)
        elif resume.filename.endswith('.docx'):
            text=extract_text_from_docx(resume)
        elif resume.filename.endswith('.txt'):
            text=extract_text_from_txt(resume)
        else:
            text='Invalid file format'
        resumes_text_dict[resume.filename]=text
    return resumes_text_dict


def get_similarity_index(job_description_text,resume_text):
    job_description_text


def preprocess_text(text):
    # 1. Lowercasing
    text = text.lower()
    
    # 2. Remove URLs (web addresses)
    text = re.sub(r'http\S+|www\S+|https\S+', '', text)
    
    # 3. Remove newlines, tabs, and multiple spaces
    text = re.sub(r'\s+', ' ', text.replace('\n', ' ').replace('\t', ' ').replace('\r', ' '))
    
    # 4. Remove numbers
    text = re.sub(r'\d+', '', text)
    
    # 5. Remove special characters (keeping only alphabets and spaces)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
        
    # 8. Remove dates (simple date formats like dd-mm-yyyy, mm/dd/yyyy)
    text = re.sub(r'\b(?:\d{1,2}[-/]\d{1,2}[-/]\d{2,4}|\w+\s\d{1,2},\s\d{4})\b', '', text)
    
    # 9. Expand contractions (e.g., don't -> do not)
    text = re.sub(r"i'm", "i am", text)
    text = re.sub(r"i've", "i have", text)
    text = re.sub(r"you've", "you have", text)
    text = re.sub(r"he's", "he is", text)
    text = re.sub(r"she's", "she is", text)
    text = re.sub(r"it's", "it is", text)
    text = re.sub(r"don't", "do not", text)
    text = re.sub(r"can't", "cannot", text)
    text = re.sub(r"won't", "will not", text)
    text = re.sub(r"ain't", "is not", text)

    # 10. Remove leading and trailing spaces
    text = text.strip()
    
    return text
