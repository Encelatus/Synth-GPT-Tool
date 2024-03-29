import json
import os

def data_prepare(file_path, output_folder):
    try:
        # Ensure the output folder exists
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Read the content of the file
        with open(file_path, 'r') as file:
            st = file.read()

        # Correct the JSON format if necessary
        ar = '[' + st + ']'
        data = json.loads(ar)
        
        # Debug print
        print(data[:100])  # Print the first 100 characters of the loaded data

        # Initialize variables to hold the text and graph data
        text = []
        text_graph_dict = {}
        k = 1

        # Process each item in the JSON data
        for dic in data:
            
            if len(dic.get("graph", {})) == 0:  # Use .get() with a default empty dict
                print(f"Adding text: {dic.get('text')}")  # Debug print
                text.append(str(dic.get("text")))
            else:
                text_graph_dict[k] = dic
                k += 1

        # Join all text items into a single string
        text_str = " ".join(text)
        if text_str:  # Check if the string is non-empty
            with open(file_name_t, 'w') as file:
                file.write(text_str)
            print("Text file saved successfully.")
        else:
            print("No text data to save.")
        
        # Define the output file path and save the text data
        file_name_t = os.path.join(output_folder, "pdf_text.txt")
        with open(file_name_t, 'w') as file:  # Use 'w' mode to overwrite existing content
            file.write(text_str)

        print("Text file saved successfully.")
        return text_graph_dict

    except Exception as e:
        print(f"error: {e}")
        return "No Data"

# Set your input and output directories
input_folder = "Output/From_PDF/Json"
output_folder = "Output/From_PDF/Json_post_prep"

# Process each JSON file in the input directory
for file_name in os.listdir(input_folder):
    if file_name.endswith('.json'):  # Make sure to process only JSON files
        file_path = os.path.join(input_folder, file_name)
        data_prepare(file_path, output_folder)
