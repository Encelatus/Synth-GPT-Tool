import json
from openai import OpenAI
from dotenv import load_dotenv
import os
from PIL import Image
import base64

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
                
    prompt_2 = """You are a data analyst expert in analysis. You are good at analysing images having textual information 
                  and graphical/textual/tabular data which is the Key aspect.
                  
                  I am going to provide you an image which might contain graphical data, textual data or tabular data.\
                  You have to extract all the information with accurate figures and numbers in a proper meaningful textual format.\
                  
                  Instructions:
                  1. Scrape only the readable data in the image.
                  2. If graphical or tabular data is present, convert all data found to a proper meaningful textual format.
                  3. Mandatorily include all the analytical data found on the graphical image, if found.
                  4. If no graphical data is found, include only textual data.
                  5. DONT describe the background image.
                  6. Do not include additional dialogues.
                  
                  Make sure to properly extract all of text from the data and store the graphical\
                  data's figures and numbers in a proper meaningful text with additional brief analytical analysis.
                  Dont miss any numerical figures by any chance and associated info with it.
                  Also, take care the page numbers and Headings. 
                """
   
    response = client.chat.completions.create(
        model= "gpt-4-vision-preview",
        messages= [
            {"role": "system", "content": prompt_2},
                {
                "role": "user",
                "content": [{
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}",
                        "detail":"high"
                    }
                }]
            }
        ],
        max_tokens= 4096
    ).choices[0].message.content

    # Cleaning the response
    output = response.replace("\n", " ")
    
    file_name= "Output/From_PDF/Text/image_text.txt"
    
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
def main_prompt():
    for i in range(1):
        image_path = f'Output/From_PDF/images/page_{i+1}.png'
        if os.path.exists(image_path):
            image_to_text(image_path)
            print(f"Page {i+1} done")
        else:
            print(f"Page {i+1} does not exist, skipping...")

##### Main for Excel #####   
# xls_path = "Output/From_Excel/xls_to_json.txt"
# json_to_text(xls_path)

if __name__ == "__main__":
    main_prompt()