import os
import traceback
import time
import threading
from pathlib import Path
from datetime import datetime

import streamlit as st

from process_csv import process

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

def main():
    # App header
    st.header("Please upload (.csv) file.")
    
    # File uploader
    uploaded_file = st.file_uploader("Choose a file", type=['csv'])
    print("Event happened: ", uploaded_file)
    
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
            

if __name__ == "__main__":
    main()