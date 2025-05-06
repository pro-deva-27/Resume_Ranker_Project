import os
from ranker import rank_resumes

# ✅ Make JD globally accessible for import
jd_text = """
We are hiring a Python Developer with a strong background in backend development, RESTful APIs, and Flask.
Experience in deploying applications, software testing, databases, and cloud environments like AWS or Azure is highly preferred.
Candidates with knowledge of system design, scalable software architectures, and performance optimization will be prioritized.
"""

# Optional: curated skills list (can also be reused elsewhere)
skills_list = [
    "Python", "Flask", "RESTful APIs", "AWS", "Azure",
    "System Design", "Software Testing", "Deployment",
    "Scalable Architecture", "Databases", "Backend Development"
]

def main():
    print("🔍 Scanning 'resumes/' folder for resumes...")

    resume_folder = "resumes"
    resume_files = [os.path.join(resume_folder, f)
                    for f in os.listdir(resume_folder)
                    if f.lower().endswith(('.pdf', '.docx'))]

    if not resume_files:
        print("❌ No resumes found in 'resumes/' folder.")
        return

    df = rank_resumes(resume_files, jd_text, skills_list)

    print("\n🏆 Resume Ranking Result:\n")
    print(df.to_string(index=False))
    df.to_csv("ranked_results.csv", index=False)
    print("\n✅ Results saved to 'ranked_results.csv'.")

if __name__ == "__main__":
    main()

