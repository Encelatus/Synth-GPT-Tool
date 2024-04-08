from flask import Flask, request, redirect, flash, render_template, url_for, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
from main import main_convert, main_prompt, main_store
from pdf_to_txt import main_pdf_to_txt
from response import Response_class
import delete_data_pinecone
import logging
logging.basicConfig(level=logging.DEBUG)


obj=Response_class()
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'test_data'
print("UPLOAD_FOLDER: ", app.config['UPLOAD_FOLDER'])
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB upload limit
app.secret_key = 'your_secret_key'

ALLOWED_EXTENSIONS = set(['pdf'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/clear-database', methods=['POST'])
def clear_database():
    print("Received request to clear the database")  # Confirms the route is accessed.
    # Assuming you have a method to clear the database
    try:
        delete_data_pinecone.delete_data_pinecone()
        print("Database cleared successfully")  # Indicates the operation was successful.
        return jsonify({"success": True, "message": "Database cleared successfully"})
    except Exception as e:
        print(f"Failed to clear the database: {e}")  # Logs the exception if the operation fails.
        return jsonify({"success": False, "message": "Could not clear the database"}), 500


@app.route('/upload', methods=['POST'])
def upload_file():
    print("Uploading file...")
    if 'document' not in request.files:
        flash('No file part')
        return redirect(url_for('index'))
    file = request.files['document']
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('index'))
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        print(f"Saving file to {file_path}...")
        file.save(file_path)
        flash('File successfully uploaded')
        return redirect(url_for('index'))
    else:
        flash('Allowed file types are pdf')
        return redirect(request.url)
    
@app.route('/files', methods=['GET'])
def list_files():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    files = [f for f in files if os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], f))]
    return jsonify(files)

@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "error": "File not found"}), 404
    
@app.route('/process/<filename>', methods=['POST'])
def process_file(filename):
    print(f"Processing file: {filename}")
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    print(f"File path: {file_path}")
    if not os.path.exists(file_path):
        print("File does not exist.")
        return jsonify({"success": False, "error": "File not found"}), 404
    try:
        print("Calling main_pdf_to_txt...")
        main_pdf_to_txt()
        print("Calling main_store...")
        main_store()
        print("File processed successfully.")
        return jsonify({"success": True, "message": "File processed successfully"})
    except Exception as e:
        print(f"Error during file processing: {e}")
        return jsonify({"success": False, "error": str(e)}), 500
    
@app.route('/chat', methods=['POST'])
def get_response():
    try:
        user_info = request.json
        query = user_info.get("query")
        key = ["PDF"]

        if not query:
            raise ValueError("No query provided.")
        
        # Assuming your obj has been initialized somewhere above as an instance of Response_class
        match = obj.find_match(query, key)
        print("**********************MATCH**********************" + match)
        chain = obj.query_refiner()
        # print("**********************QUERY REFINER - WITHOUT TEXT & QUERY**********************" + chain)
        res = chain.run(text=match, query=query)
        print("**********************QUERY REFINER - WITH TEXT & QUERY**********************" + res)

        # Depending on what run() returns, you might need to extract the actual response string
        # response_text = res['output'] if isinstance(res, dict) else res
        
        return jsonify({"response": res})
    except Exception as e:
        app.logger.error(f"Error in get_response: {e}")  # Detailed error log
        return jsonify({"error": str(e)}), 400

@app.route('/')
def index():
    # Get a list of file names in the upload directory
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    files = [file for file in files if file.endswith('.pdf')]  # Filter for PDF files if necessary
    return render_template('test.html', uploaded_files=files)

@app.route('/pdf/<filename>')
def serve_pdf(filename):
    # Ensure the filename is secure to prevent directory traversal vulnerabilities.
    safe_filename = secure_filename(filename)
    # Serve the PDF file from the upload folder.
    return send_from_directory(app.config['UPLOAD_FOLDER'], safe_filename)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
