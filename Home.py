   import streamlit as st
   from pymongo import MongoClient

   st.set_page_config(page_title="Notes Share", page_icon="📚", layout="wide")

   @st.cache_resource
   def init_connection():
       return MongoClient(st.secrets["mongo"]["uri"])

   client = init_connection()
   db = client.notes_db

   st.title("📚 College Notes Sharing App")
   st.write("### MongoDB se powered")
   
   total_notes = db.notes.count_documents({})
   st.metric("Total Notes Uploaded", total_notes)
   
   st.info("👈 Sidebar se 'Upload Notes' ya 'View Notes' select karo")
