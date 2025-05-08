import streamlit as st
import os
import tempfile
import shutil
from ranker import rank_resumes
from main import jd_text 

st.set_page_config(page_title="Resume Ranker", layout="wide")
st.title("📄 AI Resume Ranker")
st.markdown("Upload a job description and resumes to get an AI-powered ranking.")

st.subheader("Job Description")
with st.expander("View Job Description"):
    st.code(jd_text.strip(), language='markdown')


skills_input = st.text_input("Curated Skills (comma-separated)", value="Python, Flask, AWS, System Design, Deployment, Databases")


uploaded_files = st.file_uploader("Upload Resumes (PDF only)", type=["pdf"], accept_multiple_files=True)

if st.button("🔍 Rank Resumes"):
    if not jd_text or not uploaded_files:
        st.warning("Please upload both a job description and at least one resume.")
    else:
        with st.spinner("Processing..."):
            with tempfile.TemporaryDirectory() as tmpdir:
                resume_paths = []
                for file in uploaded_files:
                    path = os.path.join(tmpdir, file.name)
                    with open(path, "wb") as f:
                        f.write(file.read())
                    resume_paths.append(path)

                skills_list = [s.strip() for s in skills_input.split(",") if s.strip()]

                df = rank_resumes(resume_paths, jd_text, skills_list)

                st.success("✅ Ranking Complete!")
                st.dataframe(df, use_container_width=True)
                
                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button("📥 Download Results as CSV", data=csv, file_name="ranked_resumes.csv", mime="text/csv")
