import os
#import fitz  # PyMuPDF for PDF
from transformers import pipeline

Load the summarization pipeline
summarizer = pipeline("summarization",model="Falconsai/text_summarization")

# Function to extract text from a .txt file
def extract_text_from_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Function to extract text from a .pdf file
#def extract_text_from_pdf(file_path):
    text = ""
    with fitz.open(file_path) as pdf_document:
        for page_number in range(pdf_document.page_count):
            page = pdf_document[page_number]
            text += page.get_text()
    return text

# Function to generate a summary using the summarization pipeline
def generate_summary(input_text):
    # Generate a summary
    summary = summarizer(input_text, max_length=150, min_length=50, length_penalty=2.0, num_beams=4)[0]['summary_text']
    return summary

# Main function
def main():
    # Read input from a file or take user input
    input_choice = input("Enter 'file' to input a file path or 'text' for direct input: ").lower()

    if input_choice == 'file':
        input_file_path = input("Enter the file path (supporting .txt and .pdf): ")

        try:
            _, file_extension = os.path.splitext(input_file_path.lower())

            if file_extension == '.txt':
                input_text = extract_text_from_txt(input_file_path)
            elif file_extension == '.pdf':
                input_text = extract_text_from_pdf(input_file_path)
            else:
                print("Unsupported file type. Only .txt and .pdf are supported.")
                return

            # Generate summary
            summary = generate_summary(input_text)

            # Print the generated summary
            print("Generated Summary:")
            print(summary)

        except FileNotFoundError:
            print(f"File not found: {input_file_path}")
        except Exception as e:
            print(f"An error occurred: {e}")

    elif input_choice == 'text':
        input_text = input("Enter the text to summarize: ")

        # Generate summary
        summary = generate_summary(input_text)

        # Print the generated summary
        print("Generated Summary:")
        print(summary)

    else:
        print("Invalid input choice. Please enter 'file' or 'text'.")

# Call the main function directly
main()