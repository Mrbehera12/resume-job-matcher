import tempfile
from pathlib import Path

import streamlit as st

from src.job_api import search_adzuna_jobs
from src.matcher import match_jobs
from src.resume_parser import extract_resume_text
from src.skill_extractor import extract_skills
from src.skill_recommender import recommend_skills


st.set_page_config(
    page_title="Resume-to-Job Matcher",
    page_icon="🎯",
    layout="wide",
)

st.title("🎯 Resume-to-Job Matcher")
st.caption("Compare your resume with job listings and discover skill gaps.")

with st.sidebar:
    st.header("Job search")
    query = st.text_input("Job title / search query", value="Python Developer")
    location = st.text_input("Location", value="Bengaluru")
    limit = st.slider("Number of jobs", min_value=1, max_value=50, value=10)

uploaded_resume = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

run_match = st.button(
    "Analyze resume and find jobs",
    type="primary",
    disabled=uploaded_resume is None or not query.strip(),
)

if run_match:
    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp:
            temp.write(uploaded_resume.getvalue())
            temp_path = Path(temp.name)

        with st.spinner("Reading resume..."):
            resume_text = extract_resume_text(str(temp_path))
            resume_skills = extract_skills(resume_text)

        if not resume_text.strip():
            st.error("No readable text was extracted. Try a text-based PDF.")
            st.stop()

        with st.spinner("Searching jobs and calculating matches..."):
            jobs = search_adzuna_jobs(
                query=query.strip(),
                location=location.strip() or None,
                results_per_page=limit,
            )

        st.subheader("Resume skills")
        if resume_skills:
            st.write(f"**{len(resume_skills)} skills detected**")
            st.write(" · ".join(resume_skills))
        else:
            st.warning("No recognized skills were detected in this resume.")

        if not jobs:
            st.warning(
                "No jobs were returned. Check your search terms and API configuration."
            )
            st.stop()

        results = match_jobs(resume_skills, jobs)
        recommendations = recommend_skills(results, top_n=10)

        st.subheader("Job match results")
        st.caption(
            "Match score = equal-weight coverage of detected job skills; "
            "it is not a hiring probability."
        )

        for index, result in enumerate(results, start=1):
            heading = (
                f"{index}. {result['title']} — {result['company']} "
                f"({result['match_score']:.2f}%)"
            )
            with st.expander(heading, expanded=(index == 1)):
                left, right = st.columns(2)
                left.metric(
                    "Detected skill coverage",
                    f"{result['match_score']:.2f}%",
                    f"{result['matched_count']}/{result['total_detected_skills']} skills",
                )

                if result["skill_data_status"] == "no_detected_skills":
                    right.warning("Insufficient detected skill data to assess this job.")
                else:
                    right.write("**Matched skills**")
                    right.write(", ".join(result["matched_skills"]) or "None")
                    right.write("**Missing skills**")
                    right.write(", ".join(result["missing_skills"]) or "None")

                if result.get("job_url"):
                    st.link_button("View job listing", result["job_url"])

        st.subheader("Skill gap recommendations")
        if recommendations:
            st.caption(
                "Prioritized by frequency among the returned jobs with detected "
                "skill data. This is not a market-wide demand estimate."
            )
            st.dataframe(
                [
                    {
                        "Skill": item["skill"],
                        "Jobs requesting": item["jobs_requesting"],
                        "Share of analyzable jobs (%)": item["job_demand_percent"],
                        "Relevant roles": ", ".join(item["job_titles"]),
                    }
                    for item in recommendations
                ],
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info("No skill gap recommendations are available for these results.")

        st.success(f"Analysis complete: {len(results)} jobs reviewed.")

    except Exception as exc: