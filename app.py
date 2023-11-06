import streamlit as st
import text2qti
import traceback
import subprocess
import os

def convert_txt_to_qti(file_path):
    # Use subprocess to run the text2qti command
    output_file = file_path.replace('.txt', '.zip')
    try:
        subprocess.run(["text2qti", file_path], check=True, capture_output=True, text=True)
        return output_file, None
    except subprocess.CalledProcessError as e:
        # Capture the stderr output
        error_message = e.stderr.strip() if e.stderr else "An error occurred without any specific error message."
        return None, error_message

def main():
    st.title("text2qti Converter")

    st.markdown("""
        For help or more information about how to generate/format .txt files for conversion and upload to Canvas, please visit the [following walk-through guide.](https://reutherlab.biosci.ucsd.edu/)
    """)
    
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
            try:  
                qti_zip_file, error = convert_txt_to_qti(temp_file_path)
                if qti_zip_file and os.path.exists(qti_zip_file):
                    with open(qti_zip_file, "rb") as f:
                        zip_data = f.read()
                    st.download_button(f'Download {file_name}.zip', zip_data, file_name=f'{file_name}.zip', mime='application/zip')
                else:
                    # If the conversion failed, display the error message
                    error_message = (f"""Failed to convert the file. You will see a long, confusing error. **Focus on the part that provides a line number and text from the quiz itself. it will often be near the end of the error message.**  
                                     ---  
                                     **Here is an made-up example of what you should look for:**  
                                     In test_quiz_error.txt on line 23: Syntax error; unexpected text, or incorrect indentation for a wrapped paragraph: #a) Polar heads face outward, nonpolar tails face inward  
                                     This would indicate that there is an error on line 23 of the quiz. You need to change #a) to \*a) to fix the error.     
                                     Please visit the walkthrough linked above for more information.  
                                     ---  
                    **Your error:**  
                                     {error}") 
                    """)
                    st.markdown(error_message)
            except Exception as e:
                # Catch any other exception that might occur and display it using traceback
                error_traceback = traceback.format_exc()
                st.error(f"An unexpected error occurred: {error_traceback}") 


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
