import re

def remove_empty_brackets(input_string):
    pattern = r'\[\s*\]'
    cleaned_string = re.sub(pattern, '', input_string)
    cleaned_string = re.sub(r'\s{2,}', ' ', cleaned_string).strip()
    return cleaned_string

def reformat_brackets(input_string):
    formatted_string = re.sub(r'\[\s*(.*?)\s*\]', r'[ \1 ]', input_string)
    return formatted_string

def process_file(input_file_path, output_file_path):
    with open(input_file_path, 'r') as file:
        lines = file.readlines()

    # Apply both remove_empty_brackets and reformat_brackets to each line
    processed_lines = [reformat_brackets(remove_empty_brackets(line)) + '\n' for line in lines]

    with open(output_file_path, 'w') as file:
        file.writelines(processed_lines)

# Example usage
input_file_path = "output.txt"
output_file_path = "reformated.txt"
process_file(input_file_path, output_file_path)
