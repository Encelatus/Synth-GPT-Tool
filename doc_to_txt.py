import os
from openai import OpenAI
import docx2txt
from dotenv import load_dotenv

load_dotenv()

# Set up OpenAI API credentials
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Specify the path to the folder containing the .doc files
folder_path = "test_data"

# Define the system prompt for formatting instructions
system_prompt = """
    You are an AI assistant that helps format text extracted from .doc files. Your primary goal is to make minimal adjustments to the text to optimize it for storing in a vector database and querying later, without altering its content, meaning, or language.

    Please adhere to the following guidelines:

    1. **Preserve Original Content and Language:** Do not summarize, paraphrase, rewrite, or translate the text. It is crucial that you retain all original words, sentences, and paragraphs exactly as they appear in the input text, in their original language. Do not omit any part of the content.
    2. **Grammar and Punctuation:** Ensure correct grammar, punctuation, and sentence structure to enhance readability, while maintaining the original language.
    3. **References:** If the text contains references, citations, or bibliographic information, gather them into a dedicated "References" section at the end of the document and give them numbers like this "[1], [2], etc".
    4. **Key Terms:** Identify and extract important keywords, phrases, or entities that represent the main topics of the document. Create a separate "Key Terms" section at the end and list these terms in their original language.
    5. **Tables and Figures:** If tables, figures, or images are present, provide concise descriptions or captions for each in the original language. Include these descriptions in a "Tables and Figures" section at the end.
    6. **Code Formatting:** Format any code snippets or examples using appropriate techniques like code blocks or syntax highlighting for better readability.

    Remember, your role is to make minimal formatting adjustments to optimize the text for storage in a vector database while ensuring the complete preservation of the original content and language. The pre-formatted and post-formatted texts should be nearly identical, with only minor formatting changes. Do not remove, modify, or translate any part of the original text.

    Here is the text to be formatted:
"""

# Define the maximum number of tokens per chunk
max_tokens_per_chunk = 15000  # Adjust as needed

# Define the delimiter for separating documents in the pre-formatted text file
delimiter = "##################NEW DOCUMENT##################"

# Open the pre-formatted text file in append mode
pre_formatted_file = "pre_formatted_doc_text.txt"
pre_formatted_path = os.path.join(folder_path, pre_formatted_file)
with open(pre_formatted_path, "a", encoding="utf-8") as pre_formatted_file:
    # Iterate over all the files in the folder
    for filename in os.listdir(folder_path):
        # Check if the file has a .doc or .docx extension
        if filename.endswith(".doc") or filename.endswith(".docx"):
            print(f"Processing file: {filename}")
            
            # Construct the full path to the .doc file
            doc_path = os.path.join(folder_path, filename)

            # Extract the text from the .doc file using docx2txt
            text = docx2txt.process(doc_path)

            # Remove excessive empty lines from the text
            lines = text.split("\n")
            cleaned_lines = []
            empty_line_count = 0
            for line in lines:
                if line.strip():
                    cleaned_lines.append(line)
                    empty_line_count = 0
                else:
                    empty_line_count += 1
                    if empty_line_count <= 2:
                        cleaned_lines.append(line)
            cleaned_text = "\n".join(cleaned_lines)

            # Append the pre-formatted text to the file, separated by the delimiter
            pre_formatted_file.write(delimiter + "\n")
            pre_formatted_file.write(cleaned_text + "\n")

            # Split the cleaned text into chunks
            text_chunks = [cleaned_text[i:i + max_tokens_per_chunk] for i in range(0, len(cleaned_text), max_tokens_per_chunk)]
            print(f"Text split into {len(text_chunks)} chunks.")

            # Construct the output .txt file name by replacing the extension
            txt_file = os.path.splitext(filename)[0] + ".txt"

            # Construct the full path to the output .txt file
            txt_path = os.path.join(folder_path, txt_file)

            # Open the output .txt file in write mode
            with open(txt_path, "w", encoding="utf-8") as file:
                # Process each chunk individually
                for i, chunk in enumerate(text_chunks, start=1):
                    print(f"Sending chunk {i} to the API for formatting...")
                    
                    # Send the prompt to the GPT-3.5 Turbo API for formatting
                    response = client.chat.completions.create(
                        model="gpt-4-0125-preview",
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

                    # Write the formatted chunk to the output .txt file
                    file.write(formatted_text_chunk + "\n\n")
                    print(f"Chunk {i} written to {txt_file}")

            print(f"Text extracted from {filename} has been formatted and saved to {txt_file}")
            print("---")

print("All documents processed. Pre-formatted text appended to pre_formatted_doc_text.txt")