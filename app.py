# import streamlit as st
# import pandas as pd
# import plotly.express as px
# from utils import load_data, get_summary, get_top_n

# st.title("📊 Student Performance Dashboard")

# uploaded_file = st.file_uploader("Upload Student Marks (CSV or Excel)", type=["csv", "xlsx"])

# if uploaded_file:
#     df = load_data(uploaded_file)
#     st.success("Data Loaded Successfully!")
#     st.dataframe(df.head())

#     if st.checkbox("Show Summary by Subject"):
#         summary = get_summary(df)
#         st.dataframe(summary)

#     st.subheader("Average Marks by Subject")
#     subject_avg = df.groupby("Subject")["Marks"].mean().reset_index()
#     st.bar_chart(subject_avg.set_index("Subject"))

#     st.subheader("Top 5 Students")
#     top_students = get_top_n(df)
#     st.dataframe(top_students)

#     fig = px.bar(top_students, x='Name', y='Average Marks', title="Top Scorers", text_auto=True)
#     st.plotly_chart(fig)

#     st.subheader("Marks Distribution")
#     subject = st.selectbox("Select Subject", df['Subject'].unique())
#     subject_data = df[df['Subject'] == subject]
#     fig2 = px.box(subject_data, x='Class', y='Marks', points="all", title=f"{subject} Marks Distribution")
#     st.plotly_chart(fig2)



import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data, get_class_summary, get_student_summary, get_exam_trends, get_top_bottom_students
from utils import cluster_students, detect_declining
from utils import export_pdf


st.set_page_config(page_title="Student Performance Dashboard", layout="wide")

st.title("🎓 Student Performance Dashboard")

uploaded_file = st.file_uploader("📁 Upload Student Marks File", type=["csv", "xlsx"])

if uploaded_file:
    df = load_data(uploaded_file)
    st.success("Data Loaded Successfully!")

    # Filter sidebar
    with st.sidebar:
        st.header("🔍 Filters")
        classes = st.multiselect("Select Class", df["Class"].unique())
        students = st.multiselect("Select Student", df["Name"].unique())
        exams = st.multiselect("Select Exam", df["Exam"].unique())

    # Apply filters
    filtered_df = df.copy()
    if classes:
        filtered_df = filtered_df[filtered_df["Class"].isin(classes)]
    if students:
        filtered_df = filtered_df[filtered_df["Name"].isin(students)]
    if exams:
        filtered_df = filtered_df[filtered_df["Exam"].isin(exams)]

    st.dataframe(filtered_df)

    # Class-wise summary
    st.subheader("🏫 Class-wise Subject Averages")
    class_summary = get_class_summary(filtered_df)
    st.dataframe(class_summary)
    fig1 = px.bar(class_summary, x='Subject', y='Marks', color='Class', barmode='group',
                  title="Average Marks per Subject by Class")
    st.plotly_chart(fig1, use_container_width=True)

    # Student-wise performance
    st.subheader("👤 Individual Student Subject Averages")
    student_summary = get_student_summary(filtered_df)
    st.dataframe(student_summary)
    fig2 = px.bar(student_summary, x='Name', y='Marks', color='Subject',
                  title="Student-wise Subject Performance")
    st.plotly_chart(fig2, use_container_width=True)

    # Exam trend analysis
    st.subheader("📈 Exam-wise Performance Trends")
    exam_trends = get_exam_trends(filtered_df)
    st.dataframe(exam_trends)
    fig3 = px.line(exam_trends, x='Exam', y='Marks', color='Subject',
                   markers=True, title="Subject Trends Across Exams")
    st.plotly_chart(fig3, use_container_width=True)

    # Toppers and underperformers
    st.subheader("🏆 Top & 🚨 Underperforming Students")
    toppers, underperformers = get_top_bottom_students(filtered_df)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🏅 Top Students")
        st.dataframe(toppers)
        fig4 = px.bar(toppers, x='Name', y='Average Marks', title="Top Performers", text_auto=True)
        st.plotly_chart(fig4, use_container_width=True)

    with col2:
        st.markdown("### 😴 Underperformers")
        st.dataframe(underperformers)
        fig5 = px.bar(underperformers, x='Name', y='Average Marks', title="Students at Risk", text_auto=True)
        st.plotly_chart(fig5, use_container_width=True)

    st.subheader("🧠 Student Clusters (via ML)")
    clustered_df = cluster_students(filtered_df)
    st.dataframe(clustered_df)
    fig_cluster = px.scatter(clustered_df, x='Name', y='Marks', color='Cluster',
                            title="Student Clusters")
    st.plotly_chart(fig_cluster, use_container_width=True)

    st.subheader("📉 Students with Declining Performance")
    decline_df = detect_declining(filtered_df)
    st.dataframe(decline_df)


    # ...existing code...

    from utils import (
       load_data,
       get_class_summary,
       get_student_summary,
       get_exam_trends,
       get_top_bottom_students,
       generate_academic_suggestions  # <-- Add this import
    )

    # ...existing code...

    # AI-powered academic suggestions
    st.subheader("🤖 Personalized Academic Suggestions")
    suggestions_df = generate_academic_suggestions(filtered_df)
   

    # ...existing code...
    # ...existing code...
    for idx, row in suggestions_df.iterrows():
     if "needs at least" in row['Suggestion']:
        st.warning(f"{row['Name']} ({row['Class']}):** {row['Suggestion']}")
     else:
        st.markdown(f"{row['Name']} ({row['Class']}):** {row['Suggestion']}")
    # ...existing code...



    st.markdown("---")
    if st.button("📄 Export as PDF"):
        export_pdf(filtered_df)
        with open("student_report.pdf", "rb") as f:
            st.download_button("⬇️ Download PDF", f, file_name="student_report.pdf")

