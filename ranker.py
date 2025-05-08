import os
import PyPDF2
import pandas as pd
from difflib import SequenceMatcher
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def extract_text(file_path):
    if file_path.lower().endswith(".pdf"):
        text = ""
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() or ""
        return text
    elif file_path.lower().endswith(".docx"):
        import docx
        doc = docx.Document(file_path)
        return '\n'.join([p.text for p in doc.paragraphs])
    else:
        return ""

def get_similarity(text1, text2):
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf = vectorizer.fit_transform([text1, text2])
    return cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]

def find_matched_skills(resume_text, skills_list):
    resume_text_lower = resume_text.lower()
    matched_skills = [skill for skill in skills_list if skill.lower() in resume_text_lower]
    return matched_skills

def score_resume(resume_text, jd_text, skills_list):
    similarity = get_similarity(resume_text, jd_text)
    matched_skills = find_matched_skills(resume_text, skills_list)
    skill_score = len(matched_skills)

    hybrid_score = (similarity * 5 + skill_score) / 2 

    if similarity < 0.3 and skill_score < 3:
        feedback = "Resume poorly matches JD and lacks key skills."
    elif similarity < 0.5:
        feedback = "Resume content is not well-aligned with JD. Good skill overlap."
    else:
        feedback = "Strong alignment with JD and skill set."

    return {
        "Similarity": round(similarity, 3),
        "Skill Match": skill_score,
        "Hybrid Score": round(hybrid_score, 3),
        "Skills Found": ", ".join(matched_skills),
        "Feedback": feedback
    }

def rank_resumes(resume_files, jd_text, skills_list):
    results = []

    for file in resume_files:
        resume_text = extract_text(file)
        score_data = score_resume(resume_text, jd_text, skills_list)
        result = {
            "Resume File": os.path.basename(file),
            **score_data
        }
        results.append(result)

    df = pd.DataFrame(results)
    df.sort_values(by="Hybrid Score", ascending=False, inplace=True)
    return df
