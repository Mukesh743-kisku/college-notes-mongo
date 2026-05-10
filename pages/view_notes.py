import streamlit as st
from pymongo import MongoClient
import os

st.set_page_config(page_title="College Notes", page_icon="📚", layout="wide")

client = MongoClient(os.environ["MONGO_URI"])
db = client.notes_db

menu = st.sidebar.radio("Menu", ["📚 View Notes", "📤 Upload Notes"])

if menu == "📤 Upload Notes":
    st.title("📤 Upload College Notes")
    
    subject = st.text_input("Subject Name", placeholder="e.g. DBMS")
    semester = st.selectbox("Semester", [1,2,3,4,5,6,7,8])
    link = st.text_input("Google Drive Link", placeholder="https://drive.google.com/...")
    
    if st.button("Upload Note", type="primary"):
        if subject and link:
            db.notes.insert_one({
                "subject": subject,
                "semester": semester, 
                "link": link
            })
            st.success("✅ Note uploaded successfully!")
            st.balloons()
        else:
            st.error("⚠️ Subject aur Link dono daalo")

else:
    st.title("📚 Download College Notes")
    
    notes = list(db.notes.find())
    
    if notes:
        col1, col2 = st.columns(2)
        with col1:
            sem_filter = st.selectbox("Filter by Semester", ["All",1,2,3,4,5,6,7,8])
        with col2:
            search = st.text_input("Search Subject", placeholder="e.g. DBMS")
        
        for note in notes:
            if (sem_filter == "All" or note['semester'] == sem_filter) and search.lower() in note['subject'].lower():
                with st.container(border=True):
                    st.subheader(f"{note['subject']}")
                    st.write(f"**Semester:** {note['semester']}")
                    st.link_button("📥 Download", note['link'], use_container_width=True)
    else:
        st.warning("No notes found. Upload karo pehle!")
