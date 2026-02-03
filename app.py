import streamlit as st

# --- Page config ---
st.set_page_config(page_title="GPA & CGPA Calculator", page_icon="🎓", layout="wide")

# --- Custom CSS for attractive design ---
st.markdown("""
<style>
/* Body background */
body {
    background-color: #f0f2f6;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Headings */
h1, h2, h3 {
    color: #2c3e50;
    font-weight: 700;
}

/* Buttons */
.stButton>button {
    background: linear-gradient(90deg, #6a11cb 0%, #2575fc 100%);
    color: white;
    height: 3em;
    width: 100%;
    border-radius: 12px;
    border: none;
    font-size: 18px;
    font-weight: bold;
    transition: all 0.3s ease;
}
.stButton>button:hover {
    background: linear-gradient(90deg, #2575fc 0%, #6a11cb 100%);
}

/* Number Inputs */
.stNumberInput>div>input {
    border-radius: 12px;
    padding: 10px;
    border: 2px solid #dcdcdc;
}
.stNumberInput>div>label {
    font-weight: bold;
    color: #34495e;
}

/* Info boxes */
.stAlert {
    border-radius: 12px;
    padding: 15px;
    box-shadow: 2px 2px 12px rgba(0,0,0,0.1);
    background-color: #ffffff;
}

/* Horizontal rule */
hr {
    border: 1px solid #ddd;
    margin: 20px 0;
}
</style>
""", unsafe_allow_html=True)

# --- Title ---
st.markdown("<h1 style='text-align: center;'>🎓 GPA & CGPA Calculator</h1>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# --- Function to convert marks to grade and grade point ---
def get_grade_point(marks):
    if marks >= 85:
        return "A+", 4.0
    elif marks >= 80:
        return "A", 3.7
    elif marks >= 75:
        return "B+", 3.3
    elif marks >= 70:
        return "B", 3.0
    elif marks >= 65:
        return "C+", 2.7
    elif marks >= 60:
        return "C", 2.3
    elif marks >= 50:
        return "D", 2.0
    else:
        return "F", 0.0

# --- Input number of subjects ---
num_subjects = st.number_input("Enter the number of subjects", min_value=1, step=1)

subjects = []
if num_subjects:
    st.markdown("<h2>📘 Enter marks and credit hours for each subject</h2>", unsafe_allow_html=True)
    for i in range(num_subjects):
        col1, col2 = st.columns([2, 1])
        with col1:
            marks = st.number_input(f"Marks obtained (0–100) for Subject {i+1}", min_value=0, max_value=100, step=1, key=f"marks_{i}")
        with col2:
            credit = st.number_input(f"Credit hours for Subject {i+1}", min_value=0.1, step=0.5, key=f"credit_{i}")
        subjects.append({"marks": marks, "credit": credit})

# --- Calculate GPA & CGPA ---
if st.button("Calculate GPA & CGPA"):
    if len(subjects) != num_subjects:
        st.error("Please enter all subject details!")
    else:
        total_points = 0
        total_credits = 0
        st.markdown("<h2>📊 Grades for Each Subject:</h2>", unsafe_allow_html=True)
        for idx, subj in enumerate(subjects):
            grade, point = get_grade_point(subj["marks"])
            st.info(f"Subject {idx+1}: Marks = {subj['marks']}, Credit Hours = {subj['credit']}, Grade = {grade}, Grade Point = {point}")
            total_points += point * subj["credit"]
            total_credits += subj["credit"]

        # Calculate GPA
        gpa = total_points / total_credits if total_credits else 0
        st.markdown(f"""
        <div style='background: linear-gradient(90deg, #6a11cb 0%, #2575fc 100%); 
                    padding: 20px; border-radius: 15px; color: white; font-size: 24px; text-align: center; margin-top:20px;'>
            ✅ Semester GPA: {gpa:.2f}
        </div>
        """, unsafe_allow_html=True)

        # Previous CGPA input
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
