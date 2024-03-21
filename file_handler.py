#file_handler.py
import os
import re
from pdfminer.high_level import extract_text
import docx
import markdown
import csv



def convert_pdf_to_text(file_path):
    return extract_text(file_path)

def convert_docx_to_text(file_path):
    doc = docx.Document(file_path)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)

def convert_md_to_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    # Converting Markdown to plain text, very basic, might need improvement
    html = markdown.markdown(text)
    plain_text = re.sub('<[^<]+?>', '', html)
    return plain_text

def convert_csv_to_text(file_path):
    with open(file_path, mode='r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        csv_text = '\n'.join([' '.join(row) for row in reader])
    return csv_text

def convert_txt_to_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def convert_to_text(file_path):
    if file_path.endswith('.pdf'):
        return convert_pdf_to_text(file_path)
    elif file_path.endswith('.docx'):
        return convert_docx_to_text(file_path)
    elif file_path.endswith('.md'):
        return convert_md_to_text(file_path)
    elif file_path.endswith('.csv'):
        return convert_csv_to_text(file_path)
    elif file_path.endswith('.txt'):
        return convert_txt_to_text(file_path)
    else:
        return ""

def process_input_files(base_folder_path):
    test_phrases = {}
    
    if not os.path.exists(base_folder_path):
        print(f"Input folder '{base_folder_path}' does not exist.")
        return test_phrases
    
    for root, dirs, files in os.walk(base_folder_path):
        for file in files:
            if file.endswith(('.txt', '.pdf', '.docx', '.md', '.csv')):
                file_path = os.path.join(root, file)
                converted_text = convert_to_text(file_path)
                # Strip non-ASCII characters
                clean_text = re.sub(r'[^\x00-\x7F]+', '', converted_text).strip()
                if clean_text:  # Ensure not adding empty strings
                    relative_path = os.path.relpath(file_path, base_folder_path)
                    test_phrases[relative_path] = clean_text
                else:
                    print(f"Warning: File '{file_path}' is empty or contains only non-ASCII characters.")
    
    if not test_phrases:
        print("No valid input files found.")
    
    return test_phrases
    