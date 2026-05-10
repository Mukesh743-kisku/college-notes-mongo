import streamlit as st
from pymongo import MongoClient
import os

st.set_page_config(page_title="College Notes", page_icon="📚", layout="wide")

# MongoDB Connection
client = MongoClient(os.environ["MONGO_URI"])
db = client.notes_db

# ADMIN PASSWORD - isko change kar de apne hisaab se
ADMIN_PASS = "admin123"

# Session state for login
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Sidebar Menu
if st.session_state.logged_in:
    menu = st.sidebar.radio("Menu", ["📚 View Notes", "📤 Upload Notes", "🚪 Logout"])
else:
    menu = st.sidebar.radio("Menu", ["📚 View Notes", "🔐 Admin Login"])

# ADMIN LOGIN PAGE
if menu == "🔐 Admin Login":
    st.title("🔐 Admin Login")
    password = st.text_input("Enter Admin Password", type="password")
    if st.button("Login"):
        if password == ADMIN_PASS:
            st.session_state.logged_in = True
            st.success("✅ Logged in successfully!")
            st.rerun()
        else:
            st.error("❌ Wrong password")

# LOGOUT
elif menu == "🚪 Logout":
    st.session_state.logged_in = False
    st.success("Logged out!")
    st.rerun()

# UPLOAD NOTES - Sirf Admin ke liye
elif menu == "📤 Upload Notes":
    if not st.session_state.logged_in:
        st.error("⚠️ Login karo pehle")
        st.stop()
    
    st.title("📤 Upload College Notes")
    
    subject = st.text_input("Subject Name", placeholder="e.g. DBMS")
    semester = st.selectbox("Semester", [1,2,3,4,5,6,7,8])
    link = st.text_input("Note Link", placeholder="Google Drive / Direct PDF Link")
    
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

# VIEW NOTES - Sabke liye
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
                    col1, col2 = st.columns([3,1])
                    with col1:
                        st.subheader(f"{note['subject']}")
                        st.write(f"**Semester:** {note['semester']}")
                        st.link_button("📥 Download", note['link'], use_container_width=True)
                    
                    # DELETE BUTTON - Sirf Admin dikhega
                    with col2:
                        if st.session_state.logged_in:
                            if st.button("🗑️ Delete", key=str(note['_id']), use_container_width=True):
                                db.notes.delete_one({"_id": note['_id']})
                                st.success("Deleted!")
                                st.rerun()
    else:
        st.warning("No notes found. Admin login karke upload karo!")
