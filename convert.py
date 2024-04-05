import fitz 
from pptx import Presentation
from docx import Document
from spire.presentation.common import *
from spire.presentation import *
from PIL import Image , ImageDraw, ImageFont
import pandas as pd
import os
import json

class Conversion:
    @classmethod
    def pdf_to_images(cls, pdf_folder, output_folder, dpi):
        try:
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
            print("Output folder created successfully.")

            

            for filename in os.listdir(pdf_folder):
                if filename.endswith('.pdf'):
                    pdf_path = os.path.join(pdf_folder, filename)
                    pdf_document = fitz.open(pdf_path)
                    
                    print(f"Total number of pages in {pdf_path}: {pdf_document.page_count}")

                    # Use the dpi and zoom_factor to calculate the matrix
                    # mat = fitz.Matrix(dpi/100, dpi/100)

                    # for page_number in range(pdf_document.page_count - 60):
                    for page_number in range(pdf_document.page_count):
                        print(f"Processing page {page_number + 1} of {pdf_path}...")
                        page = pdf_document[page_number]
                        image = page.get_pixmap(matrix=fitz.Matrix(dpi/100.0, dpi/100.0))
                        rgb_image = Image.frombytes("RGB", [image.width, image.height], image.samples)
                        image_filename = f"{filename}_page_{page_number + 1}.png"
                        image_path = os.path.join(output_folder, image_filename)
                        rgb_image.save(image_path)
                        print(f"Page {page_number + 1} saved as {image_path}")

                    pdf_document.close()
            print("PDF conversion to images completed successfully.")
        except Exception as e:
            print(f"Error: {e}")

    # @classmethod        
    # def excel_to_json(cls, input_excel_file):
    #     try:
    #         # Read Excel file into DataFrame
    #         df = pd.read_excel(input_excel_file, engine='openpyxl', skiprows=0)
    #         # print("DataFrame head for inspection:", df.head())  # Debugging line

    #         # Convert the DataFrame to a dictionary
    #         records = df.to_dict(orient='records')
            
    #         # Convert dictionary to JSON string
    #         json_data = json.dumps(records, ensure_ascii=False, indent=4).replace('\/', '/').replace('\\n', ' ')

    #         # Print the JSON data for inspection
    #         # print(json_data)
            
    #         # Specify output file path
    #         output_json_file = "Output/From_Excel/xls_to_json.txt"
            
    #         # Write JSON string to file
    #         with open(output_json_file, 'w', encoding='utf-8') as json_file:
    #             json_file.write(json_data)
                
    #         print(f"JSON data saved to {output_json_file}")
    #     except Exception as e:
    #         print(f"Error: {e}")



def main_convert():
    pdf_input_folder = 'test_data/'
    pdf_output_folder = 'Output/From_PDF/images'
    dpi=300
    Conversion.pdf_to_images(pdf_input_folder, pdf_output_folder, dpi)
    
    # xlsx_input_folder = 'test_data/'
    # xlsx_output_folder = 'Output/From_Excel'
    
    # # Iterate over Excel files in the input folder and convert each to JSON
    # for filename in os.listdir(xlsx_input_folder):
    #     if filename.endswith('.xlsx'):
    #         excel_file_path = os.path.join(xlsx_input_folder, filename)
    #         Conversion.excel_to_json(excel_file_path)  # Call the method with a single Excel file path

if __name__ == "__main__":
    main_convert()
