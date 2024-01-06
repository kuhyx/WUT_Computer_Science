from openai import OpenAI
import os
import re

def sentence_loop(sentences):
  # Process each sentence
  chunked_sentences = []
  for sentence in sentences:
    chunked_sentences = process_sentence(sentence, chunked_sentences)
    if chunked_sentences == False:
      return
  return chunked_sentences

def is_correct_format(s):
    # Regular expression to match sequences of '[ some words ]'
    pattern = r'^(\[\s*[^]]+\s*\]\s*)+$'

    # Check if the string matches the pattern
    return bool(re.match(pattern, s))

def check_format(input_data):
    # Check if the input is a string, and if so, process it directly
    if isinstance(input_data, str):
        return is_correct_format(input_data)
    
    # If the input is a list, process each element in the list
    elif isinstance(input_data, list):
        return [is_correct_format(string) for string in input_data]

    # Return None or raise an error if the input is neither a string nor a list
    else:
        return None

def reformat_list(strings):
    result = []

    for string in strings:
        # Remove leading numbering like '1. '
        string = re.sub(r'^\d+\.\s*', '', string)

        # Check if the string contains partially formatted brackets
        if '[' in string and ']' in string:
            # Splitting the string into parts that are enclosed in square brackets
            parts = re.findall(r'\[[^\]]*\]', string)

            # Check for trailing punctuation after the last bracket and add it to the last part
            trailing_punctuation = re.search(r'\]\s*([.!?])\s*$', string)
            if trailing_punctuation and parts:
                parts[-1] = parts[-1][:-1] + trailing_punctuation.group(1) + ']'

            result.extend(parts)

        # Handle strings without square brackets
        else:
            # Splitting based on the dashed pattern and removing the numbering
            parts = re.split(r'\s*-\s*', string)
            parts = [part.strip() for part in parts if part.strip()]

            # Enclosing each part in square brackets
            for part in parts:
                result.append(f'[ {part} ]')

    return ' '.join(result)

def reformat_square_not_full(input_string):
    # Split the string into parts that are either in brackets or not
    parts = re.split(r'(\[[^\]]*\])', input_string)

    formatted_parts = []
    for part in parts:
        if part:  # Ignore empty strings
            # For parts not in brackets, remove trailing period, trim spaces, and enclose in brackets
            if not part.startswith('['):
                part = re.sub(r'\.\s*$', '', part).strip()
                formatted_parts.append(f"[ {part} ]")
            else:
                # For parts already in brackets, add spaces inside
                formatted_parts.append(re.sub(r'\[([^]]+)\]', r'[ \1 ]', part))

    return ' '.join(formatted_parts)

def reformat_slash(input_string):
    # Split the string on slashes and strip spaces
    parts = [part.strip() for part in input_string.split('/')]
    # Enclose each part in square brackets
    formatted_parts = [f"[ {part} ]" for part in parts]
    return ' '.join(formatted_parts)

def reformat_pipe(input_string):
    # Split the string on ' | ' and strip spaces
    parts = [part.strip() for part in input_string.split('|')]
    # Enclose each part in square brackets
    formatted_parts = [f"[ {part} ]" for part in parts]
    return ' '.join(formatted_parts)

def is_pipe_format(s):
    # Regular expression to check for ' | ' pattern
    pattern = r'^(?:[^|]+\|)+[^|]+$'
    return bool(re.match(pattern, s))

def is_numbered_line_format(s):
    # Regular expression to match lines starting with 'number. word/phrase \n'
    pattern = r'^(?:\d+\.\s+.+\n?)+$'

    # Check if the input is a list of strings
    if isinstance(s, list):
        return [bool(re.match(pattern, string)) for string in s]
    
    # If the input is a single string, process it directly
    return bool(re.match(pattern, s))

def reformat_ists(input_string):
    # Use regular expression to find all occurrences of the iSTS pattern and extract the text
    parts = re.findall(r'\(iSTS \d+\)\s*([^)]+)', input_string)
    # Enclose each extracted part in square brackets
    formatted_parts = [f"[ {part.strip()} ]" for part in parts]
    return ' '.join(formatted_parts)

def is_ists_format(s):
    # Regular expression to check for the iSTS pattern
    pattern = r'^(?:\(iSTS \d+\)\s*[^)]+\s*)+$'
    return bool(re.match(pattern, s))

def reformat_with_sections(input_string):
    # Use regular expression to extract text following the section labels
    parts = re.split(r'\s*\[\s*S\d+\s*\]\s*', input_string)
    # Remove empty strings and enclose each part in square brackets
    formatted_parts = [f"[ {part.strip()} ]" for part in parts if part.strip()]
    return ' '.join(formatted_parts)

def is_section_format(s):
    # Regular expression to check for the section label pattern
    pattern = r'^(?:\s*\[\s*S\d+\s*\]\s*.+)+$'
    return bool(re.match(pattern, s))

def is_chunk_format(s):
    # Regular expression to check for both 'Chunk X: text' and '[Chunk X] text' patterns
    pattern = r'^(Chunk \d+:\s*.+?|\[\s*Chunk \d+\s*\]\s*.+?)(\s+(Chunk \d+:\s*.+?|\[\s*Chunk \d+\s*\]\s*.+?))*$'
    return bool(re.match(pattern, s))

def reformat_chunks(input_string):
    # Find all occurrences of both chunk patterns and extract the text
    parts = re.findall(r'Chunk \d+:\s*(.+?)(?=\s*Chunk \d+:|$)|\[\s*Chunk \d+\s*\]\s*(.+?)(?=\s*\[\s*Chunk \d+\s*\]|$)', input_string)
    
    # Flatten the list of tuples and remove empty strings
    flattened_parts = [item for sublist in parts for item in sublist if item]
    
    # Enclose each extracted part in square brackets
    formatted_parts = [f"[ {part.strip()} ]" for part in flattened_parts]
    return ' '.join(formatted_parts)

def reformat_ists_markers(input_string):
    # Split the string at '[ iSTS ]', remove empty strings, and enclose each part in square brackets
    parts = [part.strip() for part in re.split(r'\[\s*iSTS\s*\]', input_string) if part.strip()]
    formatted_parts = [f"[ {part} ]" for part in parts]
    return ' '.join(formatted_parts)

def is_ists_marker_format(s):
    # Regular expression to check for the pattern with '[ iSTS ]'
    pattern = r'^(?:\[\s*iSTS\s*\].+)+$'
    return bool(re.match(pattern, s))

def reformat_with_dashes(input_string):
    # Split the string on ' - ', remove empty strings, and enclose each part in square brackets
    parts = [part.strip() for part in input_string.split('-') if part.strip()]
    formatted_parts = [f"[ {part} ]" for part in parts]
    return ' '.join(formatted_parts)

def is_dash_format(s):
    # Regular expression to check for the pattern with ' - '
    pattern = r'^[^-]+(?:\s*-\s*[^-]+)+$'
    return bool(re.match(pattern, s))

def preliminary_reformat(input_string):
  input_string = input_string.strip("iSTS chunks:")
  input_string = input_string.strip("Here are the iSTS chunks for the given sentence:")
  return input_string

def reformat_brackets_and_text(input_string):
    # Remove the trailing dot if present
    input_string = re.sub(r'\.$', '', input_string)

    # Split the string into parts that are either in brackets or not
    parts = re.split(r'(\[[^\]]*\])', input_string)

    formatted_parts = []
    for part in parts:
        if part:  # Ignore empty strings
            # Remove commas and trim spaces for parts not in brackets
            if not part.startswith('['):
                part = re.sub(r',\s*', ' ', part).strip()
                # Enclose the non-bracket part in brackets
                formatted_parts.append(f"[ {part} ]")
            else:
                # Directly append the part in brackets
                formatted_parts.append(part)

    return ' '.join(formatted_parts)

def is_brackets_and_text_format(s):
    # Regular expression to check the pattern
    pattern = r'^(\[[^\]]*\]|\s*[^[\]]+\s*)(,\s*|\s+|$)+$'
    return bool(re.match(pattern, s))

def reformat(input_string):
  input_string = preliminary_reformat(input_string)
  if check_format(input_string):
    return input_string
  # Check if the string is of the first type (numbered list)
  if is_numbered_line_format(input_string):
    print("formated by reformat_list", input_string)
    return reformat_list(input_string)
  elif is_brackets_and_text_format(input_string):
    print("is_brackets_and_text_format")
    return reformat_brackets_and_text(input_string)
  # Check if the string is of the second type (already contains square brackets)
  elif '[' in input_string and ']' in input_string:
    print("formated by reformat_square_not_full")
    return reformat_square_not_full(input_string)
  # Check for the new type with slashes
  elif '/' in input_string:
    print("formated by reformat_slash")
    return reformat_slash(input_string)
  elif is_pipe_format(input_string):
    print("formated by reformat_pipe")
    return reformat_pipe(input_string)
  elif is_ists_format(input_string):
    print("formated by reformat_ists")
    return reformat_ists(input_string)
  elif is_section_format(input_string):
    print("formated by is_section_format")
    return reformat_with_sections(input_string)
  elif is_chunk_format(input_string):
    print("formated by reformat_chunks")
    return reformat_chunks(input_string)
  elif is_ists_marker_format(input_string):
    print("formated by reformat ists markers")
    return reformat_ists_markers(input_string)
  # Return the original string if it does not match either type
  elif is_dash_format(input_string):
    print("formated by reformat with dashes")
    return reformat_with_dashes(input_string)
  print("ERROR! reformat did not recognize the format of string! ", input_string)
  return False

def remove_empty_brackets(input_string):
    # Regular expression to match empty brackets (with any number of spaces)
    pattern = r'\[\s*\]'
    
    # Replace empty brackets with an empty string
    cleaned_string = re.sub(pattern, '', input_string)

    # Remove any extra spaces that might be left after removing brackets
    cleaned_string = re.sub(r'\s{2,}', ' ', cleaned_string).strip()

    return cleaned_string

def reformat_brackets(input_string):
    formatted_string = re.sub(r'\[\s*(.*?)\s*\]', r'[ \1 ]', input_string)
    return formatted_string

def process_sentence(sentence, chunked_sentences):
  # Define the instruction with line breaks to ensure each line is within 80 characters
  instruction = (
      "Please divide the following sentence into iSTS chunks. Try to return chunks as a string in format [chunk 1] [chunk 2] [chunk 3] and so on... Here is the sentence: " + sentence
  )

  # API call with the instruction variable
  response = client.chat.completions.create(
      messages=[{
          "role": "user",
          "content": instruction,
      }],
      model="gpt-3.5-turbo",
  )

  chunked_sentence = response.choices[0].message.content
  chunked_sentence = chunked_sentence.strip()
  reformated = reformat(chunked_sentence)
  if reformated == False:
    print("ERROR! failed to reformat! ", chunked_sentence, reformated)
    return False
  reformated = reformated.strip(',')
  if not is_correct_format(reformated):
    print("ERROR! wrong format ", chunked_sentence, reformated)
    return False
  print("after reformation: ", reformated)
  reformated = remove_empty_brackets(reformated)
  reformated = reformat_brackets(reformated)
  chunked_sentences.append(reformated)
  return chunked_sentences

def chunk_sentences(file_path, output_path):
  # Read the sentences from the file
  with open(file_path, 'r') as file:
    sentences = file.readlines()

  # Process each sentence
  chunk_sentences = sentence_loop(sentences)
  print(chunk_sentences)
  # Write the chunked sentences to a new file
  with open(output_path, 'w') as output_file:
    for sentence in chunk_sentences:
      output_file.write(sentence + '\n')


# Usage
file_path = 'test_goldStandard/student/STSint.testinput.answers-students.sent1.txt'
output_path = 'output.txt'
# Change me to os.environ['API_KEY']
client = OpenAI(api_key='REDACTED_OPENAI_API_KEY')

chunk_sentences(file_path, output_path)
