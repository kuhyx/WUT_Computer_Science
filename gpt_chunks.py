from openai import OpenAI
import os

def sentence_loop(sentences):
  # Process each sentence
  chunked_sentences = []
  for sentence in sentences:
    chunked_sentences = process_sentence(sentence, chunked_sentences)
  return chunked_sentences


def process_sentence(sentence, chunked_sentences):
  sentence = "Divide this sentence into chunks as in iSTS, Render those chunks in a form [chunk 1] [chunk 2] ... for every sentence: " + sentence
  response = client.chat.completions.create(
      messages=[{
          "role": "user",
          "content": sentence,
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
file_path = 'STSint.testinput.answers-students.sent1.txt'
output_path = 'chunks_one.txt'
api_key = os.environ['API_KEY']
client = OpenAI(api_key=os.environ['API_KEY'])

chunk_sentences(file_path, output_path, api_key)
