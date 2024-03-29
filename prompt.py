import json
from openai import OpenAI
from dotenv import load_dotenv
import os
from PIL import Image
import base64
import re

load_dotenv()
client=OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def image_to_text(image_path):
    with open(image_path, "rb") as image_file:
        base64_image =  base64.b64encode(image_file.read()).decode('utf-8')

    prompt = """I am going to provide you an image which might contain graphical data, textual data or tabular data.
                you have to figure out what kind of data is present in the image it could be a combination of more than one type of data, you need to extract the data
                and have to create a json MAP of the same where there could be 2 keys in the json MAP which are
                1. text: this key will contain all the textual data present in the image, do not include sub-headings in the text format. This key does not contain a json.
                2. graph: this key will contain all the data which could be tabular or graphical data, this key itself contains a json object of the data.
                
                Instructions:
                1. Scrape all the readable data on the image.
                2. NOT include any additional string apart from a valid json data, not even parameters like ```
                3. Always end your response with a comma (,) mandatorily.
                """
                
    prompt_2 = """You are a data analyst expert in analysis, proficient at analyzing images containing graphical data, textual data, or tabular data, which is the key aspect.
    
                  I will provide you an image that may include graphical data, textual data, or tabular data. Your task is to extract all the information with accurate figures and numbers in a proper meaningful textual format.
                  Instructions:

                  1. Scrape only the readable data in the image.
                  2. If the text is in German, translate it to English.
                  3. Do not summarize the text found in the image; instead, extract all the text, including every numerical figure and percentage.
                  4. If graphical or tabular data is present, convert all data to a meaningful textual format, ensuring that all numerical figures and associated information are accurately represented.
                  5. Include all analytical data found in the graphical image, if present, without omitting any numerical figures.
                  6. If no graphical data is found, include only textual data, ensuring all numerical figures and percentages are accurately translated.
                  7. Do not describe the background image.
                  8. Avoid additional dialogues.
                  
                  It is crucial to properly extract all text from the data and convert the graphical data's figures and numbers into meaningful text with brief analytical analysis. Do not miss any numerical figures or associated information, and be attentive to page numbers and headings."""
   
    response = client.chat.completions.create(
        model= "gpt-4-vision-preview",
        messages= [
            {"role": "system", "content": prompt_2},
                {
                "role": "user",
                "content": [{
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                }]
            }
        ],
        max_tokens= 4096
    ).choices[0].message.content

    # Cleaning the response
    output = response.replace("\n", " ")
    
    file_name= "Output/From_PDF/Text/gpt_image_answer.txt"
    
    # Saving the output to a file in append mode
    with open(file_name, 'a', encoding='utf-8') as file:  # 'a' is for append mode
        file.write(output + "\n\n")  # Adding a newline for separation between entries
        
    print(f'Text has been appended to {file_name}')

# def json_to_text(input_file):
#     with open(input_file, 'r', encoding='utf-8') as file:
#         json = file.read()
#     print("JSON file read successfully.")

#     prompt_xls = """I am going to provide you a json which contains the analytical data of a company.\
#                 Go through the data and convert it into a valid meaningful paragraph that includes all the data given in the json.\
#                 Instructions:
#                 1. Convert all the data from JSON to a meaningful paragraph.
#                 2. Do not include additional dialogues.
#                 Make sure to include all the data in the created paragraph.
#                 the data should be descriptive and will contain each and every small detail without skipping any point.
#                 """
#     prompt_xls_ = """I am going to provide you a json which contains the analytical data of a company.\
#                 1. Convert that data to textual readable format.
#                 2. Make sure to include all data, percentages and analyical figures.
#                 3. Do not include additional dialogues.
#                 4. Make sure that the text is readable and easy to understand
#                 5. Generate text for complete data.
#                 *the data should be descriptive and will contain each and every small detail without skipping any point.*
#                 """
    
#     print("Generating response..")

#     response = client.chat.completions.create(
#         model="gpt-4-0125-preview",
#         messages=[
#             {"role": "system", "content": prompt_xls_},
#             {"role": "user", "content": json}
#         ]
#     ).choices[0].message.content

#     output = response.replace("\n"," ")

#     file_name = "Output/From_Excel/Text/xls_text.txt"
#     with open(file_name, 'a', encoding='utf-8') as file:
#         file.write(output)

#     print(f'Text has been saved to {file_name}')

##### Main for PDF #####
def main_prompt(output_folder='Output/From_PDF/images'):
    # Regex pattern to match your file naming convention (e.g., page_1.png)
    pattern = re.compile(r'page_(\d+)\.png')

    # List all files in the output directory
    files = os.listdir(output_folder)

    for file_name in files:
        # Check if the file name matches the expected pattern
        match = pattern.match(file_name)
        if match:
            page_number = match.group(1)  # Extract the page number from the file name
            image_path = os.path.join(output_folder, file_name)

            if os.path.exists(image_path):
                image_to_text(image_path)
                print(f"Page {page_number} done")
            else:
                print(f"Page {page_number} does not exist, skipping...")


##### Main for Excel #####   
# xls_path = "Output/From_Excel/xls_to_json.txt"
# json_to_text(xls_path)

if __name__ == "__main__":
    main_prompt()