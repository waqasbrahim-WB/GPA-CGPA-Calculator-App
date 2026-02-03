import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page config ---
st.set_page_config(page_title="GPA & CGPA Dashboard", page_icon="🎓", layout="wide")

# --- CSS ---
st.markdown("""
<style>
body { background-color: #f0f2f6; font-family: 'Segoe UI', sans-serif; }
h1, h2, h3 { color: #2c3e50; font-weight: 700; }
.stButton>button { 
    background: linear-gradient(90deg, #6a11cb 0%, #2575fc 100%); 
    color: white; height: 3em; width: 100%; border-radius: 12px; border: none; font-size: 18px; font-weight: bold;
    transition: all 0.3s ease;
}
.stButton>button:hover { background: linear-gradient(90deg, #2575fc 0%, #6a11cb 100%); }
.stNumberInput>div>input { border-radius: 12px; padding: 10px; border: 2px solid #dcdcdc; }
.stNumberInput>div>label { font-weight: bold; color: #34495e; }
.stAlert { border-radius: 12px; padding: 15px; box-shadow: 2px 2px 12px rgba(0,0,0,0.1); background-color: #ffffff; }
</style>
""", unsafe_allow_html=True)

# --- Title ---
st.markdown("<h1 style='text-align: center;'>🎓 GPA & CGPA Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# --- Functions ---
def get_grade_point(marks):
    if marks >= 85: return "A+", 4.0
    elif marks >= 80: return "A", 3.7
    elif marks >= 75: return "B+", 3.3
    elif marks >= 70: return "B", 3.0
    elif marks >= 65: return "C+", 2.7
    elif marks >= 60: return "C", 2.3
    elif marks >= 50: return "D", 2.0
    else: return "F", 0.0

# --- Input number of subjects ---
num_subjects = st.number_input("Enter the number of subjects", min_value=1, step=1)
subjects = []

if num_subjects:
    st.markdown("<h2>📘 Enter marks and credit hours for each subject</h2>", unsafe_allow_html=True)
    for i in range(num_subjects):
        col1, col2 = st.columns([2, 1])
        with col1:
            marks = st.number_input(f"Marks (0–100) for Subject {i+1}", min_value=0, max_value=100, step=1, key=f"marks_{i}")
        with col2:
            credit = st.number_input(f"Credit Hours for Subject {i+1}", min_value=0.1, step=0.5, key=f"credit_{i}")
        subjects.append({"marks": marks, "credit": credit})

# --- Calculate GPA & CGPA ---
if st.button("Calculate GPA & CGPA"):

    if len(subjects) != num_subjects:
        st.error("Please enter all subject details!")
    else:
        total_points = 0
        total_credits = 0
        grades = []
        marks_list = []

        st.markdown("<h2>📊 Grades for Each Subject</h2>", unsafe_allow_html=True)
        for idx, subj in enumerate(subjects):
            grade, point = get_grade_point(subj["marks"])
            grades.append(grade)
            marks_list.append(subj["marks"])
            st.info(f"Subject {idx+1}: Marks = {subj['marks']}, Credit Hours = {subj['credit']}, Grade = {grade}, Grade Point = {point}")
            total_points += point * subj["credit"]
            total_credits += subj["credit"]

        # --- GPA ---
        gpa = total_points / total_credits if total_credits else 0
        st.markdown(f"""
        <div style='background: linear-gradient(90deg, #6a11cb 0%, #2575fc 100%);
                    padding: 20px; border-radius: 15px; color: white; font-size: 24px; text-align: center; margin-top:20px;'>
            ✅ Semester GPA: {gpa:.2f}
        </div>
        """, unsafe_allow_html=True)

        # --- Previous CGPA ---
        st.markdown("<h2>📝 Previous CGPA Details (Optional)</h2>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            prev_cgpa = st.number_input("Previous CGPA", min_value=0.0, max_value=4.0, step=0.01)
        with col2:
            prev_credits = st.number_input("Previous Total Credit Hours", min_value=0.0, step=0.1)

        if prev_credits or prev_cgpa:
            updated_cgpa = (prev_cgpa * prev_credits + gpa * total_credits) / (prev_credits + total_credits) if (prev_credits + total_credits) else 0
            st.markdown(f"""
            <div style='background: linear-gradient(90deg, #ff416c 0%, #ff4b2b 100%);
                        padding: 20px; border-radius: 15px; color: white; font-size: 24px; text-align: center; margin-top:20px;'>
                🎯 Updated CGPA: {updated_cgpa:.2f}
            </div>
            """, unsafe_allow_html=True)

        # --- Prepare DataFrame ---
        df = pd.DataFrame({
            "Subject": [f"Subject {i+1}" for i in range(num_subjects)],
            "Marks": marks_list,
            "Grades": grades
        })

        # --- Area Chart for Marks ---
        st.markdown("<h2>📈 Marks Area Chart</h2>", unsafe_allow_html=True)
        fig_area = px.area(df, x="Subject", y="Marks", text="Marks", markers=True,
                           color_discrete_sequence=px.colors.qualitative.Pastel)
        fig_area.update_layout(yaxis=dict(range=[0, 100]))
        st.plotly_chart(fig_area, use_container_width=True)

        # --- Pie Chart for Grade Distribution ---
        st.markdown("<h2>🥧 Grade Distribution Pie Chart</h2>", unsafe_allow_html=True)
        grade_counts = df['Grades'].value_counts().reset_index()
        grade_counts.columns = ['Grade', 'Count']
        fig_pie = px.pie(
            grade_counts,
            names='Grade',
            values='Count',
            color='Grade',
            color_discrete_sequence=px.colors.qualitative.Pastel  # ✅ fixed!
        )
        st.plotly_chart(fig_pie, use_container_width=True)
