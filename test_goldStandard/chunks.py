from openai import OpenAI

def sentence_loop(sentences):
    # Process each sentence
    chunked_sentences = []
    for sentence in sentences:
        chunked_sentences = process_sentence(sentence, chunked_sentences)
    return chunked_sentences

def process_sentence(sentence, chunked_sentences):
    response = client.chat.completions.create(
        messages=[{
            "role": "user",
            "content": "Please divide the following sentence into iSTS chunks. Format the response as: [[chunk 1]] [[chunk 2]] ... Ensure each chunk is enclosed in double square brackets and separated by a space. If you cannot correctly chunkify the sentence, return an error message in the format: 'ERROR: Cannot chunkify sentence: <sentence>'. Here is the sentence: " + sentence,
        }],
        model="gpt-3.5-turbo",
    )

    chunked_sentence = response.choices[0].message.content
    print("chunked_sentence: ", chunked_sentence)
    chunked_sentences.append(chunked_sentence)
    return chunked_sentences

def chunk_sentences(file_path, output_path, api_key):
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
file_path = 'student/STSint.testinput.answers-students.sent2.txt'
output_path = 'chunks_gpt_two.txt'
# Replace me with os.environ['API_KEY']
api_key = 'REDACTED_OPENAI_API_KEY'
client = OpenAI(api_key=api_key)

chunk_sentences(file_path, output_path, api_key)
