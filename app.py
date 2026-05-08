# import streamlit as st
# from ocr.extract_text import extract_text
# from regex.classifier import classify_document
# from utils.extract_details import extract_details

# st.title("AI Document Classification System")

# uploaded_file = st.file_uploader(
#     "Upload Document",
#     type=["png", "jpg", "jpeg"]
# )

# if uploaded_file:

#     st.image(uploaded_file, caption="Uploaded Document")

#     # OCR Extraction
#     extracted_text = extract_text(uploaded_file)

#     # Display OCR Text
#     st.subheader("Extracted Text")
#     st.text(extracted_text)

#     # Document Classification
#     document_type = classify_document(extracted_text)

    
#     # #Paddleocr
#     # document_type, confidence = classify_document(extracted_text)
#     # st.write(f"Confidence: {confidence}%")

#     # Display Classification
#     st.subheader("Detected Document Type")
#     st.success(document_type)

#     # Extract Details using Json
#     details = extract_details(extracted_text, document_type)
#     st.subheader("Extracted Details")
#     st.json(details)
   

# Gemini LLM Extraction
import streamlit as st
from llm.gemini_extractor import extract_document_details

st.title("AI Document Intelligence System")

uploaded_file = st.file_uploader(
    "Upload Document",
    type=["png", "jpg", "jpeg"]
)

if uploaded_file:

    st.image(uploaded_file, caption="Uploaded Document")

    with st.spinner("Analyzing document..."):

        result = extract_document_details(uploaded_file)

    st.subheader("Extracted Information")

    st.json(result)