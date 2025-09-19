import streamlit as st
from utils.file_parser import extract_text_from_pdf, extract_table_from_pdf, extract_data_from_excel
from utils.ollama_client import OllamaClient

st.title("Financial Document Q&A Assistant")

ollama_client = OllamaClient(model_name="llama2")  # Update to the model you pulled

uploaded_file = st.file_uploader("Upload a PDF or Excel file", type=['pdf', 'xls', 'xlsx'])

context_text = ""  # Will hold extracted document data

if uploaded_file:
    file_details = {
        "filename": uploaded_file.name,
        "filetype": uploaded_file.type,
        "filesize": uploaded_file.size
    }
    st.write(file_details)

    if uploaded_file.name.endswith(".pdf"):
        with open("temp_uploaded.pdf", "wb") as f:
            f.write(uploaded_file.getbuffer())
        context_text = extract_text_from_pdf("temp_uploaded.pdf")
        tables = extract_table_from_pdf("temp_uploaded.pdf")
        st.header("Extracted Text (Preview)")
        st.text_area("", context_text[:1500], height=300)
        if tables:
            st.header("Extracted Tables")
            for i, table in enumerate(tables):
                st.write(f"Table {i+1}")
                st.dataframe(table)
    else:
        with open("temp_uploaded.xlsx", "wb") as f:
            f.write(uploaded_file.getbuffer())
        excel_data = extract_data_from_excel("temp_uploaded.xlsx")
        st.header("Excel Sheets")
        for sheet_name, df in excel_data.items():
            st.subheader(sheet_name)
            st.dataframe(df)
        context_text = "\n".join([df.to_string() for df in excel_data.values()])

    # Q&A chat interface
    st.header("Ask questions about the document")
    question = st.text_input("Your question:")

    if question:
        with st.spinner("Generating answer..."):
            prompt = f"Context:\n{context_text}\n\nQuestion: {question}"
            answer = ollama_client.query(prompt)
            st.markdown(f"**Answer:** {answer}")
else:
    st.info("Please upload a PDF or Excel file to get started.")
