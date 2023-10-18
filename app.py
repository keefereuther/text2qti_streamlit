import streamlit as st
import subprocess
import os

def convert_txt_to_qti(file_path):
    # Use subprocess to run the text2qti command
    output_file = file_path.replace('.txt', '.zip')
    subprocess.run(["text2qti", file_path])
    return output_file

def main():
    st.title("text2qti Converter")
    
    uploaded_file = st.file_uploader("Upload a .txt file", type=["txt"])

    if uploaded_file:
        # Extract the filename without the extension
        file_name = os.path.splitext(uploaded_file.name)[0]

        # Save the uploaded file to a location with the same name
        temp_file_path = f"{file_name}.txt"
        with open(temp_file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.write("File uploaded successfully!")

        # Button to initiate the conversion
        if st.button('Convert to QTI'):
            qti_zip_file = convert_txt_to_qti(temp_file_path)
            if os.path.exists(qti_zip_file):
                with open(qti_zip_file, "rb") as f:
                    zip_data = f.read()
                st.download_button(f'Download {file_name}.zip', zip_data, file_name=f'{file_name}.zip', mime='application/zip')

    # Footer
    st.markdown("---")
    st.markdown("""
        The text2qti python library is Copyright (c) 2020 by Geoffrey M. Poore. 
        It can be found at [https://github.com/gpoore/text2qti](https://github.com/gpoore/text2qti) 
        and is distributed under the BSD 3-Clause License.
    """)
    st.markdown("""
        This app is managed by Keefe Reuther - [https://reutherlab.biosci.ucsd.edu/](https://reutherlab.biosci.ucsd.edu/)
    """)

if __name__ == "__main__":
    main()
