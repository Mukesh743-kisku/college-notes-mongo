import streamlit as st
from pymongo import MongoClient
import os

st.set_page_config(page_title="View Notes", page_icon="📚")

@st.cache_resource
def init_connection():
    return MongoClient(os.environ["MONGO_URI"])

client = init_connection()
db = client.notes_db
notes_collection = db.notes

st.title("📚 Download College Notes")

# Filter
col1, col2 = st.columns(2)
with col1:
    sem_filter = st.selectbox("Filter by Semester", ["All",1,2,3,4,5,6,7,8])
with col2:
    search = st.text_input("Search Subject", placeholder="e.g. DBMS")

# Query banao
query = {}
if sem_filter != "All":
    query["semester"] = sem_filter
if search:
    query["subject"] = {"$regex": search, "$options": "i"}

notes = list(notes_collection.find(query).sort("upload_date", -1))

if not notes:
    st.warning("No notes found. Upload karo pehle!")
else:
    st.write(f"**Found {len(notes)} notes**")
    
    for note in notes:
        with st.expander(f"📄 {note['subject']} - Sem {note['semester']}"):
            st.write(f"**File:** {note['filename']}")
            st.write(f"**Uploaded by:** {note['uploader']}")
            st.write(f"**Date:** {note['upload_date'].strftime('%d-%m-%Y %H:%M')}")
            st.write(f"**Downloads:** {note['downloads']}")
            
            # Download button
            st.download_button(
                label="⬇️ Download PDF",
                data=note['file_data'],
                file_name=note['filename'],
                mime="application/pdf",
                key=str(note['_id']),
                on_click=lambda id=note['_id']: notes_collection.update_one(
                    {"_id": id}, {"$inc": {"downloads": 1}}
                )
            )
