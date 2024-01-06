"""
Orders gpt to chunkify files from task
"""
import re
import os
from openai import OpenAI


def sentence_loop(sentences):
    """
    Processes a list of sentences, applying chunking and formatting to each.

    This function iterates through a list of sentences, processing each one
    using the `process_sentence` function. It collects the results into a list.
    If processing fails for any sentence, the function halts and returns None.

    Parameters:
    sentences (list of str): A list of sentences to be processed.

    Returns:
    list of str: A list of processed and formatted sentences, or None if processing
                 of any sentence fails.
    """
    # Process each sentence
    chunked_sentences = []
    for sentence in sentences:
        chunked_sentences = process_sentence(sentence, chunked_sentences)
        if not chunked_sentences:
            return []
    return chunked_sentences


def remove_leading_numbering(input_string):
    """
    Removes any leading numbering from the string.

    This function is designed to strip off numbering
    that typically appears at the beginning of a string,
    such as '1. ', '2. ', etc. It's useful for processing strings where such numbering is irrelevant
    or should be omitted for formatting purposes.

    Parameters:
    string (str): The string from which leading numbering should be removed.

    Returns:
    str: The string with leading numbering removed.
    """
    return re.sub(r"^\d+\.\s*", "", input_string)


def process_brackets(input_string):
    """
    Processes a string to extract and adjust parts enclosed in square brackets.

    This function identifies and extracts all segments within square brackets from the input string.
    It also adjusts the last part by handling any trailing punctuation,
    using the 'handle_trailing_punctuation' function.
    This is particularly useful for strings
    that contain multiple bracketed segments that need individual processing.

    Parameters:
    input_string (str): The string to be processed for bracketed segments.

    Returns:
    list of str: A list containing the extracted and adjusted bracketed segments from the string.
    """
    parts = re.findall(r"\[[^\]]*\]", input_string)
    if parts:
        parts[-1] = handle_trailing_punctuation(input_string, parts[-1])
    return parts


def handle_trailing_punctuation(input_string, last_part):
    """
    Handles and appends trailing punctuation to the last part of a bracketed segment.

    This function checks the given string for any punctuation (like '.', '!', or '?')
    immediately following the last bracketed segment. If found, it appends this punctuation
    to the end of the last part inside the brackets. This is used to maintain sentence
    punctuation integrity after processing bracketed segments.

    Parameters:
    input_string (str): The original string containing the bracketed segments.
    last_part (str): The last bracketed segment extracted from the string.

    Returns:
    str: The last part with any trailing punctuation correctly appended.
    """
    trailing_punctuation = re.search(r"\]\s*([.!?])\s*$", input_string)
    if trailing_punctuation:
        return last_part[:-1] + trailing_punctuation.group(1) + "]"
    return last_part


def process_non_bracketed_parts(input_string):
    """
    Split the input string by hyphens surrounded by optional whitespace and return
    a list of non-empty parts enclosed in square brackets.

    Parameters:
    input_string (str): The input string to be processed.

    Returns:
    list of str: A list of non-empty parts from the input string, enclosed in square brackets.
    """
    parts = re.split(r"\s*-\s*", input_string)
    return [f"[ {part.strip()} ]" for part in parts if part.strip()]


def reformat_list(strings):
    """
    Reformat a list of strings by processing each string element. For strings containing
    square brackets, it calls 'process_brackets' to handle the content within the brackets,
    and for other strings, it calls 'process_non_bracketed_parts' to handle them. The
    resulting parts are joined into a single string with spaces.

    Parameters:
    strings (list of str): A list of strings to be reformatted.

    Returns:
    str: A reformatted string containing the processed parts of input strings.
    """
    result = []
    for string in strings:
        string = remove_leading_numbering(string)
        if "[" in string and "]" in string:
            result.extend(process_brackets(string))
        else:
            result.extend(process_non_bracketed_parts(string))
    return " ".join(result)


def reformat_square_not_full(input_string):
    """
    Reformat the input string by splitting it into parts that are either enclosed in
    square brackets or not. For parts not in brackets, it removes trailing periods,
    trims spaces, and encloses them in square brackets. For parts already in brackets,
    it adds spaces inside the brackets. The formatted parts are then joined into a
    single string with spaces.

    Parameters:
    input_string (str): The input string to be reformatted.

    Returns:
    str: A reformatted string containing the processed parts of the input string.
    """
    # Split the string into parts that are either in brackets or not
    parts = re.split(r"(\[[^\]]*\])", input_string)

    formatted_parts = []
    for part in parts:
        if part:  # Ignore empty strings
            # For parts not in brackets,
            # remove trailing period, trim spaces, and enclose in brackets
            if not part.startswith("["):
                part = re.sub(r"\.\s*$", "", part).strip()
                formatted_parts.append(f"[ {part} ]")
            else:
                # For parts already in brackets, add spaces inside
                formatted_parts.append(re.sub(r"\[([^]]+)\]", r"[ \1 ]", part))

    return " ".join(formatted_parts)


def reformat_slash(input_string):
    """
    Reformat the input string by splitting it on slashes, trimming spaces from each
    part, and enclosing each part in square brackets. The formatted parts are then
    joined into a single string with spaces.

    Parameters:
    input_string (str): The input string to be reformatted.

    Returns:
    str: A reformatted string containing the processed parts of the input string.
    """
    # Split the string on slashes and strip spaces
    parts = [part.strip() for part in input_string.split("/")]
    # Enclose each part in square brackets
    formatted_parts = [f"[ {part} ]" for part in parts]
    return " ".join(formatted_parts)


def reformat_pipe(input_string):
    """
    Reformat the input string by splitting it on ' | ' (pipe symbol with spaces),
    trimming spaces from each part, and enclosing each part in square brackets. The
    formatted parts are then joined into a single string with spaces.

    Parameters:
    input_string (str): The input string to be reformatted.

    Returns:
    str: A reformatted string containing the processed parts of the input string.
    """
    # Split the string on ' | ' and strip spaces
    parts = [part.strip() for part in input_string.split("|")]
    # Enclose each part in square brackets
    formatted_parts = [f"[ {part} ]" for part in parts]
    return " ".join(formatted_parts)


def is_pipe_format(input_string):
    """
    Check if the input string follows the ' | ' (pipe symbol with spaces) pattern.

    Parameters:
    input_string (str): The input string to be checked.

    Returns:
    bool: True if the input string matches the pattern, otherwise False.
    """
    # Regular expression to check for ' | ' pattern
    pattern = r"^(?:[^|]+\|)+[^|]+$"
    return bool(re.match(pattern, input_string))


def is_numbered_line_format(input_string):
    """
    Check if the input string(input_string) follows the pattern of lines starting with
    'number. word/phrase \n'.

    Parameters:
    input_string (str or list of str): The input string(input_string) to be checked.
    It can be a single string or a list of strings.

    Returns:
    bool or list of bool: 
      If the input is a single string, it returns True
      if it matches the pattern, otherwise False.
      If the input is a list of strings
      it returns a list of booleans indicating if each string matches the pattern.
    """
    # Regular expression to match lines starting with 'number. word/phrase \n'
    pattern = r"^(?:\d+\.\s+.+\n?)+$"

    # Check if the input is a list of strings
    if isinstance(input_string, list):
        return [bool(re.match(pattern, string)) for string in string]

    # If the input is a single string, process it directly
    return bool(re.match(pattern, input_string))


def reformat_ists(input_string):
    """
    Reformat the input string by finding all occurrences of the (iSTS n) pattern
    (where 'n' is a number), extracting the text inside the parentheses, and
    enclosing each extracted part in square brackets. The formatted parts are
    then joined into a single string with spaces.

    Parameters:
    input_string (str): The input string to be reformatted.

    Returns:
    str: A reformatted string containing the processed parts of the input string.
    """
    # Use regular expression to find all occurrences of the iSTS pattern and
    # extract the text
    parts = re.findall(r"\(iSTS \d+\)\s*([^)]+)", input_string)
    # Enclose each extracted part in square brackets
    formatted_parts = [f"[ {part.strip()} ]" for part in parts]
    return " ".join(formatted_parts)


def is_ists_format(input_string):
    """
    Check if the input string follows the pattern of (iSTS n) followed by text, with
    multiple occurrences allowed, where 'n' is a number.

    Parameters:
    input_string (str): The input string to be checked.

    Returns:
    bool: True if the input string matches the pattern, otherwise False.
    """
    # Regular expression to check for the iSTS pattern
    pattern = r"^(?:\(iSTS \d+\)\s*[^)]+\s*)+$"
    return bool(re.match(pattern, input_string))


def reformat_with_sections(input_string):
    """
    Reformat the input string by using regular expressions to split it into parts
    following section labels (e.g., [S1], [S2], etc.), removing empty strings,
    and enclosing each part in square brackets. The formatted parts are then
    joined into a single string with spaces.

    Parameters:
    input_string (str): The input string to be reformatted.

    Returns:
    str: A reformatted string containing the processed parts of the input string.
    """
    # Use regular expression to extract text following the section labels
    parts = re.split(r"\s*\[\s*S\d+\s*\]\s*", input_string)
    # Remove empty strings and enclose each part in square brackets
    formatted_parts = [f"[ {part.strip()} ]" for part in parts if part.strip()]
    return " ".join(formatted_parts)


def is_section_format(input_string):
    """
    Check if the input string follows the pattern of section labels (e.g., [S1], [S2], etc.)
    followed by text, with multiple occurrences allowed.

    Parameters:
    input_string (str): The input string to be checked.

    Returns:
    bool: True if the input string matches the pattern, otherwise False.
    """
    # Regular expression to check for the section label pattern
    pattern = r"^(?:\s*\[\s*S\d+\s*\]\s*.+)+$"
    return bool(re.match(pattern, input_string))


def is_chunk_format(input_string):
    """
    Check if the input string follows the pattern of 'Chunk X: text' or '[Chunk X] text'
    patterns, where 'X' is a number, with multiple occurrences allowed.

    Parameters:
    input_string (str): The input string to be checked.

    Returns:
    bool: True if the input string matches the pattern, otherwise False.
    """
    # Further optimized regular expression
    pattern = r"^(Chunk \d+:|\[\s*Chunk \d+\s*\]).*?(?:\s+(?:Chunk \d+:|\[\s*Chunk \d+\s*\]).*?)*$"
    return bool(re.match(pattern, input_string))



def reformat_chunks(input_string):
    """
    Reformat the input string by finding all occurrences of both
    'Chunk X: text' and '[Chunk X] text'
    patterns, extracting the text within them, and enclosing each extracted part in square brackets.
    The formatted parts are then joined into a single string with spaces.

    Parameters:
    input_string (str): The input string to be reformatted.

    Returns:
    str: A reformatted string containing the processed parts of the input string.
    """
    # Find all occurrences of both chunk patterns and extract the text
    parts = re.findall(
        r"(?:Chunk \d+:|\[\s*Chunk \d+\s*\])\s*(.*?)(?=\s*(?:Chunk \d+:|\[\s*Chunk \d+\s*\]|$))",
        input_string,
    )

    # Flatten the list of tuples and remove empty strings
    flattened_parts = [item for sublist in parts for item in sublist if item]

    # Enclose each extracted part in square brackets
    formatted_parts = [f"[ {part.strip()} ]" for part in flattened_parts]
    return " ".join(formatted_parts)


def reformat_ists_markers(input_string):
    """
    Reformat the input string by splitting it at '[ iSTS ]' markers, removing empty strings,
    and enclosing each part in square brackets. The formatted parts are then joined into
    a single string with spaces.

    Parameters:
    input_string (str): The input string to be reformatted.

    Returns:
    str: A reformatted string containing the processed parts of the input string.
    """
    # Split the string at '[ iSTS ]', remove empty strings, and enclose each
    # part in square brackets
    parts = [
        part.strip()
        for part in re.split(r"\[\s*iSTS\s*\]", input_string)
        if part.strip()
    ]
    formatted_parts = [f"[ {part} ]" for part in parts]
    return " ".join(formatted_parts)


def is_ists_marker_format(input_string):
    """
    Check if the input string follows the pattern with '[ iSTS ]' markers followed by text,
    with multiple occurrences allowed.

    Parameters:
    input_string (str): The input string to be checked.

    Returns:
    bool: True if the input string matches the pattern, otherwise False.
    """
    # Regular expression to check for the pattern with '[ iSTS ]'
    pattern = r"^(?:\[\s*iSTS\s*\].+)+$"
    return bool(re.match(pattern, input_string))


def reformat_with_dashes(input_string):
    """
    Reformat the input string by splitting it on ' - ' (dash with spaces),
    removing empty strings, and enclosing each part in square brackets.
    The formatted parts are then joined into a single string with spaces.

    Parameters:
    input_string (str): The input string to be reformatted.

    Returns:
    str: A reformatted string containing the processed parts of the input string.
    """
    # Split the string on ' - ', remove empty strings, and enclose each part
    # in square brackets
    parts = [part.strip() for part in input_string.split("-") if part.strip()]
    formatted_parts = [f"[ {part} ]" for part in parts]
    return " ".join(formatted_parts)


def is_dash_format(input_string):
    """
    Check if the input string follows the pattern with ' - ' (dash with spaces)
    separating non-empty parts.

    Parameters:
    input_string (str): The input string to be checked.

    Returns:
    bool: True if the input string matches the pattern, otherwise False.
    """
    # Regular expression to check for the pattern with ' - '
    pattern = r"^[^-]+(?:\s*-\s*[^-]+)+$"
    return bool(re.match(pattern, input_string))


def preliminary_reformat(input_string):
    """
    Remove common prefixes like
    'iSTS chunks:'
    and
    'Here are the iSTS chunks for the given sentence:'
    from the input string.
    This function is intended as a preliminary step before further reformatting.

    Parameters:
    input_string (str): The input string to be reformatted.

    Returns:
    str: The input string with common prefixes stripped.
    """
    input_string = input_string.strip("iSTS chunks:")
    input_string = input_string.strip(
        "Here are the iSTS chunks for the given sentence:"
    )
    return input_string


def reformat_brackets_and_text(input_string):
    """
    Reformat the input string by removing trailing dots, splitting it into parts that are either
    enclosed in square brackets or not, removing commas and trimming spaces for non-bracket parts,
    and enclosing non-bracket parts in square brackets. The formatted parts are then joined into
    a single string with spaces.

    Parameters:
    input_string (str): The input string to be reformatted.

    Returns:
    str: A reformatted string containing the processed parts of the input string.
    """
    # Remove the trailing dot if present
    input_string = re.sub(r"\.$", "", input_string)

    # Split the string into parts that are either in brackets or not
    parts = re.split(r"(\[[^\]]*\])", input_string)

    formatted_parts = []
    for part in parts:
        if part:  # Ignore empty strings
            # Remove commas and trim spaces for parts not in brackets
            if not part.startswith("["):
                part = re.sub(r",\s*", " ", part).strip()
                # Enclose the non-bracket part in brackets
                formatted_parts.append(f"[ {part} ]")
            else:
                # Directly append the part in brackets
                formatted_parts.append(part)

    return " ".join(formatted_parts)


def is_brackets_and_text_format(input_string):
    """
    Check if the input string follows the pattern of parts
    that are either enclosed in square brackets
    or not, with optional commas and spaces between the parts.

    Parameters:
    input_string (str): The input string to be checked.

    Returns:
    bool: True if the input string matches the pattern, otherwise False.
    """
    # Regular expression to check the pattern
    pattern = r"^(\[[^\]]*\]|\s*[^[\]]+\s*)(,\s*|\s+|$)+$"
    return bool(re.match(pattern, input_string))


def is_correct_format(input_string):
    """
    Checks if a given string matches a specific format of sequences enclosed in square brackets.

    This function uses a regular expression to determine if the input string adheres to a format
    where sequences of text are enclosed within square brackets. Each sequence must be separated
    by spaces, and the entire string must only consist of these bracketed sequences.

    Parameters:
    input_string (str): The string to be checked against the format.

    Returns:
    bool: True if the string matches the format, False otherwise.
    """
    # Regular expression to match sequences of '[ some words ]'
    pattern = r"^(\[\s*[^]]+\s*\]\s*)+$"

    # Check if the string matches the pattern
    return bool(re.match(pattern, input_string))


def check_format(input_data):
    """
    Checks if the input data (input_data or list of strings) matches a specific format.

    This function determines if the input data,
    which can be either a single string or a list of strings,
    adheres to a predefined format where sequences of text are enclosed within square brackets.
    The format check is performed by the 'is_correct_format' function.
    For a list, the check is applied to each string in the list.

    Parameters:
    input_data (str or list of str): 
      The input data to be checked. 
      Can be a single string or a list of strings.

    Returns:
    bool or list of bool: If input_data is a string,
    returns True if it matches the format, False otherwise.
    If input_data is a list, returns a list of booleans corresponding to each string.
    Returns None if input_data is neither a string nor a list.
    """
    # Check if the input is a string, and if so, process it directly
    if isinstance(input_data, str):
        return is_correct_format(input_data)

    # If the input is a list, process each element in the list
    if isinstance(input_data, list):
        return [is_correct_format(string) for string in input_data]

    # Return None or raise an error if the input is neither a string nor a list
    return None

def check_and_reformat(input_string, check_func, format_func):
    """
    Checks what type of string got inputed and formats it accordingly
    """
    if check_func(input_string):
        print(f"formatted by {format_func.__name__}", input_string)
        return format_func(input_string)
    return None

def reformat(input_string):
    """
    Reformat the input string by applying a series of format checks and corresponding
    reformatting functions. This function attempts to identify the format of the input
    string and apply the appropriate reformatting.

    Parameters:
    input_string (str): The input string to be reformatted.

    Returns:
    str or bool: The reformatted string if a suitable format is recognized, or False if the format
                 is not recognized and cannot be reformatted.
    """
    input_string = preliminary_reformat(input_string)
    if check_format(input_string):
        return input_string

    format_checks = [
        (is_numbered_line_format, reformat_list),
        (is_brackets_and_text_format, reformat_brackets_and_text),
        (lambda s: "[" in s and "]" in s, reformat_square_not_full),
        (lambda s: "/" in s, reformat_slash),
        (is_pipe_format, reformat_pipe),
        (is_ists_format, reformat_ists),
        (is_section_format, reformat_with_sections),
        (is_chunk_format, reformat_chunks),
        (is_ists_marker_format, reformat_ists_markers),
        (is_dash_format, reformat_with_dashes),
    ]

    for check_func, format_func in format_checks:
        result = check_and_reformat(input_string, check_func, format_func)
        if result is not None:
            return result

    print("ERROR! reformat did not recognize the format of string! ", input_string)
    return False


def remove_empty_brackets(input_string):
    """
    Remove empty brackets (with or without spaces) from the input string and
    eliminate any extra spaces that might be left after removing brackets.

    Parameters:
    input_string (str): The input string from which empty brackets should be removed.

    Returns:
    str: The input string with empty brackets removed and extra spaces eliminated.
    """
    # Regular expression to match empty brackets (with any number of spaces)
    pattern = r"\[\s*\]"

    # Replace empty brackets with an empty string
    cleaned_string = re.sub(pattern, "", input_string)

    # Remove any extra spaces that might be left after removing brackets
    cleaned_string = re.sub(r"\s{2,}", " ", cleaned_string).strip()

    return cleaned_string


def reformat_brackets(input_string):
    """
    Reformat the input string by enclosing text inside square brackets.
    This function searches for text enclosed in square brackets (with or without spaces)
    and ensures that the text inside the brackets is surrounded by spaces.

    Parameters:
    input_string (str): The input string to be reformatted.

    Returns:
    str: A reformatted string with text inside square brackets and spaces around it.
    """
    formatted_string = re.sub(r"\[\s*(.*?)\s*\]", r"[ \1 ]", input_string)
    return formatted_string


def generate_instruction(sentence):
    """
    Generate an instruction for dividing a given sentence into iSTS chunks.

    Parameters:
    sentence (str): The sentence to be divided into chunks.

    Returns:
    str: A formatted instruction with the provided sentence.
    """
    return (
        "Please divide the following sentence into iSTS chunks."
        "Try to return chunks as a string in format "
        "[chunk 1] [chunk 2] [chunk 3] and so on... "
        "Here is the sentence: " + sentence
    )


def call_api(instruction):
    """
    Call the API using the provided instruction to generate a response.

    Parameters:
    client (OpenAI.Client): An OpenAI API client object.
    instruction (str): The instruction to provide to the API.

    Returns:
    dict: The response generated by the API.
    """
    return client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": instruction,
            }
        ],
        model="gpt-3.5-turbo",
    )


def process_response(response):
    """
    Process the response received from the API and extract the chunked sentence.

    Parameters:
    response (dict): The response generated by the API.

    Returns:
    str: The chunked sentence extracted from the response.
    """
    chunked_sentence = response.choices[0].message.content.strip()
    return chunked_sentence


def check_and_format_sentence(chunked_sentence):
    """
    Check and format a chunked sentence by applying a series of checks and reformatting.

    Parameters:
    chunked_sentence (str): The chunked sentence to be checked and formatted.

    Returns:
    str or bool: The formatted chunked sentence if it passes all checks,
    or False if there are errors.
    """
    reformated = reformat(chunked_sentence)
    if not reformated:
        print("ERROR! failed to reformat! ", chunked_sentence, reformated)
        return False
    reformated = reformated.strip(",")
    if not is_correct_format(reformated):
        print("ERROR! wrong format ", chunked_sentence, reformated)
        return False
    return reformated


def finalize_formatting(reformatted):
    """
    Finalize the formatting of a reformatted string by removing empty brackets and ensuring
    that text inside brackets is surrounded by spaces.

    Parameters:
    reformatted (str): The reformatted string to be finalized.

    Returns:
    str: The finalized and formatted string.
    """
    reformatted = remove_empty_brackets(reformatted)
    reformatted = reformat_brackets(reformatted)
    return reformatted


def process_sentence(sentence, chunked_sentences):
    """
    Process a sentence by generating iSTS chunks and
    adding them to the provided list of chunked sentences.

    Parameters:
    sentence (str): The input sentence to be processed.
    chunked_sentences (list): A list of previously chunked sentences to which the processed sentence
                              will be appended.
    client (OpenAI.Client): An OpenAI API client object for calling the API.

    Returns:
    list or bool: The updated list of chunked sentences if successful, or False if there are errors.
    """
    instruction = generate_instruction(sentence)
    response = call_api(instruction)
    chunked_sentence = process_response(response)
    reformatted = check_and_format_sentence(chunked_sentence)
    if not reformatted:
        return False
    reformatted = finalize_formatting(reformatted)
    chunked_sentences.append(reformatted)
    return chunked_sentences


def chunk_sentences(input_file, output):
    """
    Read sentences from a file, process each sentence to generate iSTS chunks,
    and write the chunked sentences to an output file.

    Parameters:
    file_path (str): The path to the input file containing sentences to be processed.
    output_path (str): The path to the output file where chunked sentences will be written.

    Returns:
    None
    """
    # Read the sentences from the file
    with open(input_file, "r", encoding="utf-8") as file:
        sentences = file.readlines()

    # Process each sentence
    chunked_sentences = sentence_loop(sentences)
    print(chunked_sentences)

    # Write the chunked sentences to a new file
    with open(output, "w", encoding="utf-8") as output_file:
        for sentence in chunked_sentences:
            output_file.write(sentence + "\n")


# Usage
FILE_PATH = "test_goldStandard/student/STSint.testinput.answers-students.sent1.txt"
OUTPUT_PATH = "output.txt"
# Change me to os.environ['API_KEY']
client = OpenAI(api_key=os.environ['API_KEY'])

chunk_sentences(FILE_PATH, OUTPUT_PATH)
