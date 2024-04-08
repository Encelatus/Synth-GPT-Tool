# import os
# from pypdf import PdfReader
# import re
# from openai import OpenAI
# from dotenv import load_dotenv

# load_dotenv()

# # Set up OpenAI API credentials
# client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# def preprocess_text(text):
#     # Remove unnecessary characters and symbols
#     text = re.sub(r'[^\w\s]', '', text)
    
#     # Replace multiple whitespace with a single space
#     text = re.sub(r'\s+', ' ', text)
    
#     # Optional: Convert text to lowercase to maintain consistency
#     text = text.lower()
    
#     return text

# # Specify the folder path containing the PDF files
# folder_path = 'test_data/'  # Make sure to include the trailing slash

# # Specify the output directory for the post-formatted text file
# output_dir = 'Output/From_PDF/Text/'

# # Create the output directory if it doesn't exist
# os.makedirs(output_dir, exist_ok=True)

# # Specify the output text file name within the designated output directory
# post_formatted_file = os.path.join(output_dir, 'post_formatted_text.txt')
# pre_formatted_file = os.path.join(output_dir, 'pre_formatted_text.txt')

# # Define the system prompt for formatting instructions (minimizing changes)
# system_prompt = """
#     You are an AI assistant that helps clean and combine text extracted from PDF files. Your primary goal is to make minimal adjustments to the text to improve readability and ensure sentences are properly joined, without altering the content, meaning, or language. Do not add any new information or create headings. 

#     Please adhere to the following guidelines:

#     1. **Preserve Original Content and Language:** Do not summarize, paraphrase, rewrite, or translate the text. Retain all original words, sentences, and paragraphs exactly as they appear in the input text, in their original language. Do not omit any part of the content.
#     2. **Sentence Combining:** Identify instances where sentences might have been incorrectly separated during text extraction and combine them to form complete and coherent sentences.
#     3. **No Additional Content:** Do not add any new information, headings, or formatting elements. The output should be as similar as possible to the input, with only necessary sentence combining.

#     Here is the text to be cleaned and combined:
# """

# # Define the maximum number of tokens per chunk
# max_tokens_per_chunk = 15000  # Adjust as needed

# # Open the pre-formatted text file in append mode
# with open(pre_formatted_file, 'a', encoding='utf-8') as f_pre:
#     # Open the post-formatted text file in append mode
#     with open(post_formatted_file, 'a', encoding='utf-8') as f_post:
#         # Iterate over each file in the folder
#         for filename in os.listdir(folder_path):
#             if filename.endswith('.pdf'):
#                 # Create a PDF reader object for the current file
#                 reader = PdfReader(os.path.join(folder_path, filename))

#                 # Write the file name as a separator in both files
#                 f_pre.write(f"\n\n===== {filename} =====\n\n")
#                 f_post.write(f"\n\n===== {filename} =====\n\n")

#                 # Iterate over each page in the PDF file
#                 for page in reader.pages:
#                     # Extract text from the current page
#                     text = page.extract_text()

#                     # Preprocess the text to clean and standardize it
#                     processed_text = preprocess_text(text)

#                     # Write the pre-formatted text to the file
#                     f_pre.write(processed_text + '\n')

#                     # Split the processed text into chunks
#                     text_chunks = [processed_text[i:i + max_tokens_per_chunk] for i in range(0, len(processed_text), max_tokens_per_chunk)]
#                     print(f"Text split into {len(text_chunks)} chunks.")

#                     # Process each chunk individually
#                     for i, chunk in enumerate(text_chunks, start=1):
#                         print(f"Sending chunk {i} to the API for formatting...")

#                         # Send the prompt to the GPT-3.5 Turbo API for formatting
#                         response = client.chat.completions.create(
#                             model="gpt-3.5-turbo-0125",
#                             messages=[
#                                 {"role": "system", "content": system_prompt},
#                                 {"role": "user", "content": chunk}
#                             ],
#                             max_tokens=4096,  # Adjust as needed
#                             temperature=0.1,
#                         )

#                         # Get the formatted text from the API response
#                         formatted_text_chunk = response.choices[0].message.content.strip()
#                         print(f"Received formatted text for chunk {i}.")

#                         # Write the formatted chunk to the post-formatted file
#                         f_post.write(formatted_text_chunk + "\n\n")
#                         print(f"Chunk {i} written to {post_formatted_file}")

#                 print(f"Extracted text from '{filename}' has been saved in '{pre_formatted_file}' and '{post_formatted_file}'.")

# print(f"All PDF files have been processed. Pre-formatted text saved in '{pre_formatted_file}' and post-formatted text saved in '{post_formatted_file}'.")

import os
from pypdf import PdfReader
import re
from openai import OpenAI
from dotenv import load_dotenv

def main_pdf_to_txt():
    def preprocess_text(text):
        # Remove unnecessary characters and symbols
        text = re.sub(r'[^\w\s]', '', text)
        # Replace multiple whitespace with a single space
        text = re.sub(r'\s+', ' ', text)
        # Optional: Convert text to lowercase to maintain consistency
        text = text.lower()
        return text

    load_dotenv()

    # Set up OpenAI API credentials
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    # Specify the folder path containing the PDF files
    folder_path = 'test_data/'  # Make sure to include the trailing slash

    # Specify the output directory for the text files
    output_dir = 'Output/From_PDF/Text/'

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Specify the output text file names within the designated output directory
    pre_formatted_file = 'pre_formatted_text.txt'
    post_formatted_file = os.path.join(output_dir, 'post_formatted_text.txt')

    # Define the system prompt for formatting instructions (minimizing changes)
    system_prompt = """
        You are an AI assistant that helps clean and combine text extracted from PDF files. Your primary goal is to make minimal adjustments to the text to improve readability and ensure sentences are properly joined, without altering the content, meaning, or language. Do not add any new information or create headings.

        Please adhere to the following guidelines:

        1. **Preserve Original Content and Language:** Do not summarize, paraphrase, rewrite, or translate the text. Retain all original words, sentences, and paragraphs exactly as they appear in the input text, in their original language. Do not omit any part of the content.
        2. **Sentence Combining:** Identify instances where sentences might have been incorrectly separated during text extraction and combine them to form complete and coherent sentences.
        3. **No Additional Content:** Do not add any new information, headings, or formatting elements. The output should be as similar as possible to the input, with only necessary sentence combining.
        
        Here is the text to be cleaned and combined:
    """

    # Open both the pre-formatted and post-formatted text files in append mode
    with open(pre_formatted_file, 'a', encoding='utf-8') as f_pre, open(post_formatted_file, 'a', encoding='utf-8') as f_post:
        # Iterate over each file in the folder
        for filename in os.listdir(folder_path):
            if filename.endswith('.pdf'):
                # Create a PDF reader object for the current file
                reader = PdfReader(os.path.join(folder_path, filename))

                # Write the file name as a separator in both files
                f_pre.write(f"\n\n===== {filename} =====\n\n")
                f_post.write(f"\n\n===== {filename} =====\n\n")

                # Iterate over each page in the PDF file
                for page in reader.pages:
                    # Extract text from the current page
                    text = page.extract_text()

                    # Preprocess the text to clean and standardize it
                    processed_text = preprocess_text(text)

                    # Write the pre-formatted text to the pre-formatted file
                    f_pre.write(processed_text + '\n')

                    # Split the processed text into chunks (if necessary)
                    text_chunks = [processed_text[i:i + 4096] for i in range(0, len(processed_text), 4096)]
                    print(f"Text split into {len(text_chunks)} chunks.")

                    # Process each chunk individually
                    for i, chunk in enumerate(text_chunks, start=1):
                        print(f"Sending chunk {i} to the API for formatting...")

                        # Send the prompt to the GPT-3.5 Turbo API for formatting
                        response = client.chat.completions.create(
                            model="gpt-3.5-turbo-0125",
                            messages=[
                                {"role": "system", "content": system_prompt},
                                {"role": "user", "content": chunk}
                            ],
                            max_tokens=4096,  # Adjust as needed
                            temperature=0.1,
                        )

                        # Get the formatted text from the API response
                        formatted_text_chunk = response.choices[0].message.content.strip()
                        print(f"Received formatted text for chunk {i}.")

                        # Write the formatted chunk to the post-formatted file
                        f_post.write(formatted_text_chunk + "\n\n")
                        print(f"Chunk {i} written to {post_formatted_file}")

                print(f"Extracted text from '{filename}' has been saved in '{pre_formatted_file}' and '{post_formatted_file}'.")

    print(f"All PDF files have been processed. Pre-formatted text saved in '{pre_formatted_file}' and post-formatted text saved in '{post_formatted_file}'.")

if __name__ == "__main__":
    main_pdf_to_txt()
