import streamlit as st
from pymongo import MongoClient
import datetime

st.set_page_config(page_title="Upload Notes", page_icon="📤")

@st.cache_resource
def init_connection():
    return MongoClient(st.secrets["mongo"]["uri"])

client = init_connection()
db = client.notes_db
notes_collection = db.notes

st.title("📤 Upload College Notes")

with st.form("upload_form"):
    subject = st.text_input("Subject Name*", placeholder="e.g. Data Structures")
    semester = st.selectbox("Semester*", [1,2,3,4,5,6,7,8])
    uploaded_file = st.file_uploader("Upload PDF*", type=['pdf'])
    uploader_name = st.text_input("Your Name", placeholder="Optional")
    
    submitted = st.form_submit_button("Upload Note")
    
    if submitted:
        if subject and semester and uploaded_file:
            file_data = uploaded_file.read()
            
            note_doc = {
                "subject": subject,
                "semester": semester,
                "filename": uploaded_file.name,
                "file_data": file_data,
                "uploader": uploader_name if uploader_name else "Anonymous",
                "upload_date": datetime.datetime.now(),
                "downloads": 0
            }
            
            notes_collection.insert_one(note_doc)
            st.success(f"✅ {uploaded_file.name} uploaded successfully!")
            st.balloons()
        else:
            st.error("❌ Subject, Semester aur PDF file required hai")
