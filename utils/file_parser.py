
import pdfplumber
import pandas as pd

def extract_text_from_pdf(file_path):
    """Extract raw text from PDF file."""
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def extract_table_from_pdf(file_path):
    """Extract tables from PDF file as list of DataFrames."""
    tables = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            for table in page.extract_tables():
                df = pd.DataFrame(table[1:], columns=table[0])
                tables.append(df)
    return tables

def extract_data_from_excel(file_path):
    """Extract all sheets from Excel as dictionary of DataFrames."""
    data = pd.read_excel(file_path, sheet_name=None)
    return data

# Example usage:
# pdf_text = extract_text_from_pdf('path/to/file.pdf')
# pdf_tables = extract_table_from_pdf('path/to/file.pdf')
# excel_data = extract_data_from_excel('path/to/file.xlsx')
