import os
import traceback
import time
import threading
from pathlib import Path
from datetime import datetime
import bcrypt
import streamlit as st
from process_csv import process

PASSWORD = b'$2b$12$8u0eB3hNQid98UA.O.c6y.jG/mrcmv/EenM8vrcrh6GoVbw02ywyS'
FILES_DIR = "files"
Path(FILES_DIR).mkdir(parents=True, exist_ok=True)


def delete_with_delay(files):
    if 'upload_file' in st.session_state:
        del st.session_state['upload_file']
    
    def delete_files(files):
        """Delete the file from the server after process is completed."""
        time.sleep(10)
        for file_path in files:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"File deleted successfully: {file_path}")
            else:
                print(f"File not found: {file_path}")

    threading.Thread(target=delete_files, args=(files,)).start()

def file_upload_and_download_form(st):
    # App header
    st.markdown("<h2 style='font-size:24px;'>Please upload (.csv) file.</h2>", unsafe_allow_html=True)
    
    # File uploader
    uploaded_file = st.file_uploader("Choose a file", type=['csv'])
    if uploaded_file:
        print("Uploading file: ", uploaded_file)
    
    if uploaded_file is not None:
        # Display the uploaded file name
        # st.write("Uploading file please wait...", uploaded_file.name)
        uploaded_file.flush()
        input_file_path = os.path.join(FILES_DIR, f"{int(datetime.now().timestamp())}_{uploaded_file.name}")
        output_file_path = os.path.join(FILES_DIR, f"{int(datetime.now().timestamp())}_weekly_{uploaded_file.name}")
        
        # Save the uploaded file
        with open(input_file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
            try:
                process(input_file_path, output_file_path)
                st.success("File ready to download \"{}\"".format(os.path.basename(output_file_path)))

            except:
                print(traceback.format_exc())
                st.error("Error: Invalid file format. Please check your file and try again.")
        
        
        
        # Create a link to download the uploaded file
        with open(output_file_path, "rb") as f:
            btn = st.download_button(
                label="Download File",
                data=f,
                file_name=os.path.basename(output_file_path),
                mime=uploaded_file.type,
                on_click=lambda: delete_with_delay([input_file_path, output_file_path])
            )



def main():
    print("Main method called")
   
    # Password page
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False

    if not st.session_state['authenticated']:
        
        # Ask for password
        with st.form("password_form"):
            # password = st.text_input("Enter Password", type="password")
            print("Hello")    
            password = st.text_input("Enter Password", type="password")
            submit_button = st.form_submit_button("Submit")
            
        if submit_button:
            if bcrypt.checkpw(password.encode(), PASSWORD):
                st.session_state['authenticated'] = True
                st.success("Password correct! You can now upload a file.")
                st.experimental_rerun()

            else:
                st.error("Incorrect password. Please try again.")
    else:
       file_upload_and_download_form(st)
    


    for i in range(0, 10):
        st.write("")  # Blank line for spacing

    # Create two columns
    col1, col2 = st.columns(2)

    # Display the images in separate columns
    with col1:
        st.image("./images/halo_logo.png", caption="Created by Halo.", width=200)
    with col2:
        st.image("./images/irs_logo.jpeg", caption="Powered by IRS.", width=350)
            

if __name__ == "__main__":
    main()