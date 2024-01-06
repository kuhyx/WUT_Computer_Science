import re

def read_file(file_path): 
    lines = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return lines

def brackets(lines):
    reformatted_lines = []
    for line in lines:
        # Split the line into segments of bracketed and non-bracketed parts
        segments = re.split(r'(\[.*?\])', line)
        reformatted_line = ""

        for segment in segments:
            # If the segment is already in brackets, keep as is
            if segment.startswith('[') and segment.endswith(']'):
                reformatted_line += segment
            # Else, enclose the segment in brackets if it's not empty or just whitespace
            elif segment.strip():
                reformatted_line += f"[{segment.strip()}]"

        reformatted_lines.append(reformatted_line)

    # Join the reformatted lines into a single string
    return reformatted_lines

def reformat_chunk_number(lines):
    reformatted_lines = []
    current_chunk = []
    last_chunk_number = 0

    for line in lines:
        # Check if the line starts with a chunk pattern (case-insensitive)
        if re.match(r'\[chunk \d+\]', line, re.IGNORECASE):
            # Extract the chunk number
            chunk_number = int(re.search(r'\d+', line).group())

            # If the chunk number is sequential, add the sentence to the current_chunk
            if chunk_number == last_chunk_number + 1:
                sentence = line.split(']', 1)[1].strip()
                current_chunk.append(f"[{sentence}]")
                last_chunk_number = chunk_number
            else:
                # Append the current_chunk to reformatted_lines and start a new chunk
                if current_chunk:
                    reformatted_lines.append(' '.join(current_chunk))
                    current_chunk = []

                # Start the new chunk
                sentence = line.split(']', 1)[1].strip()
                current_chunk = [f"[{sentence}]"]
                last_chunk_number = chunk_number
        else:
            # If the line is not a chunk, add current_chunk to reformatted_lines and reset
            if current_chunk:
                reformatted_lines.append(' '.join(current_chunk))
                current_chunk = []
                last_chunk_number = 0

            # Add the non-chunk line to reformatted_lines
            reformatted_lines.append(line.strip())

    # Add any remaining chunks
    if current_chunk:
        reformatted_lines.append(' '.join(current_chunk))

    return reformatted_lines

def reformat_slash_separated_sentences(lines):
    reformatted_lines = []

    for line in lines:
        # Check if the line contains a slash "/", indicating a split sentence
        if '/' in line:
            # Split the sentence at each slash and enclose each segment in brackets
            segments = [f"[{segment.strip()}]" for segment in line.split('/')]
            reformatted_line = ' '.join(segments)
            reformatted_lines.append(reformatted_line)
        else:
            # For lines without slashes, add them as they are
            reformatted_lines.append(line.strip())

    return reformatted_lines

# File path
file_path = 'test_goldStandard/student/chunks_gpt_student_one.txt'
# Reformat the file content
lines = read_file(file_path)
reformated_text = reformat_chunk_number(lines)
reformated_text = reformat_slash_separated_sentences(reformated_text)
reformated_text = brackets(reformated_text)
print(reformated_text)
output_path = 'chunks_gpt_student_two_reformated.txt'
with open(output_path, 'w') as output_file:
    for sentence in reformated_text:
        output_file.write(sentence + '\n')