# importing required modules
from pypdf import PdfReader
import re  # For regular expressions

def preprocess_text(text):
    # Remove unnecessary characters and symbols
    text = re.sub(r'[^\w\s]', '', text)
    
    # Replace multiple whitespace with a single space
    text = re.sub(r'\s+', ' ', text)
    
    # Optional: Convert text to lowercase to maintain consistency
    text = text.lower()
    
    return text

# creating a pdf reader object
reader = PdfReader('test_data/IHK.pdf')  # Make sure the path is correctly formatted

# specifying the name of the text file
filename = 'extracted_text.txt'

# opening the text file in write mode
with open(filename, 'w', encoding='utf-8') as f:
    # iterating over each page in the pdf file
    for page in reader.pages:
        # extracting text from the current page
        text = page.extract_text()
        
        # Preprocess the text to clean and standardize it
        processed_text = preprocess_text(text)
        
        # writing the processed text to the file
        f.write(processed_text + '\n')  # Adding a newline for separation between pages

# printing a confirmation message
print(f"Entire PDF has been successfully converted and stored in '{filename}'.")
