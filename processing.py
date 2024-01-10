import pandas as pd
import numpy as np
from lxml import etree
import re


def load_sentences(senteance1_path: str, sentance2_path: str) -> pd.DataFrame:
  """
  Loads the sentences from the given paths and outputs in a 2 columns dataframe
  """
  sentance1 = pd.read_csv(senteance1_path,
                          dtype=str,
                          delimiter="}",
                          header=None)
  sentance1.columns = ["sentance1"]

  sentance2 = pd.read_csv(sentance2_path,
                          dtype=str,
                          delimiter="}",
                          header=None)
  sentance2.columns = ["sentance2"]

  sentances = pd.concat([sentance1, sentance2], axis=1)
  return sentances


def chunk2list(chunks: str) -> list:
  """
  Takes str that is all chunks from a chunked sentance and returns a list of all the chunks as seperate items 
  """
  chunks = chunks.replace('[', '')
  chunks = chunks.replace(']', '')
  chunks = chunks.replace('   ', '|')
  split = chunks.split('|')

  split = [re.sub(r'^\s+|\s+$', '', s) for s in split] # remove spaces at the beggining and end of chunks
  split = [re.sub(r'[^\w\s]', '', s) for s in split] # remove punctuation
  return split


def load_chunked(chunked_path1: str, chunked_path2: str) -> pd.DataFrame:
  """
  Loads chunked sentances in [ chunk1 ] [ chunk2 ] format into dataframe with lists of chunks
  """
  chunked_sentance1 = pd.read_csv(chunked_path1,
                                  dtype=str,
                                  delimiter="}",
                                  header=None)
  chunked_sentance1.columns = ["chunked_sentance1"]

  chunked_sentance2 = pd.read_csv(chunked_path2,
                                  dtype=str,
                                  delimiter="}",
                                  header=None)
  chunked_sentance2.columns = ["chunked_sentance2"]

  headlines_chunked = pd.concat([chunked_sentance1, chunked_sentance2], axis=1)

  # convert chunks from str to list
  headlines_chunked['chunked_sentance1'] = headlines_chunked[
      'chunked_sentance1'].apply(chunk2list)
  headlines_chunked['chunked_sentance2'] = headlines_chunked[
      'chunked_sentance2'].apply(chunk2list)

  return headlines_chunked


def return_characteers(cell: str) -> str:
  """
  converts the alignment data to restore the <==> and & tokens
  """
  cell = cell.replace('ARROWS_PLACEHOLDER', '<==>')
  cell = cell.replace('AMPERSAND_PLACEHOLDER', '&')
  return cell


def load_alignment(alignment_path: str) -> pd.DataFrame:
  """
  Loads the alignment file. Parses only the <alignment> tag and puts the data into a dataframe
  """
  with open(alignment_path, 'r') as file:
    file_content = file.read()

  # <==> and & break xml loaders so it needs to be replaces with something else
  modified_content = file_content.replace('<==>', 'ARROWS_PLACEHOLDER').replace('&', 'AMPERSAND_PLACEHOLDER')
  # it also needs a root wrapped to function properly 
  modified_content = f'<root>{modified_content}</root>'

  modified_file_path = 'temp.wa'
  with open(modified_file_path, 'w') as modified_file:
    modified_file.write(modified_content)

  # Parse the modified file using ElementTree
  tree = etree.parse(modified_file_path)
  root = tree.getroot()

  # get ansewrs
  alignments_data = []
  
  for alignment in root.xpath('//alignment'):
      # Extract relevant information from the alignment element
      data = {
          'sentence_id': alignment.xpath('ancestor::sentence/@id')[0],
          'alignment_text': alignment.text
      }
      alignments_data.append(data)

  y = pd.DataFrame(alignments_data)
  y = y.drop(columns=["sentence_id"])
  y["alignment_text"] = y["alignment_text"].apply(return_characteers)
  return y


def prettyprint(element, **kwargs):
  xml = etree.tostring(element, pretty_print=True, **kwargs)
  print(xml.decode(), end='')


def test_XML():
  # test out the format
  print(alignments_data[0]["alignment_text"])

def generate_train_test_split(xy: pd.DataFrame):
  """
  Generates a train, validate, test split of the given dataframes in a 60% 20% 20% ratio
  """
  #data = pd.merge(x, y, left_index=True, right_index=True)
  data = xy
  train, test = np.split(data.sample(frac=1, random_state=42), [int(.03*len(data))])

  return train, test

def generate_alignment_format(dataFrame:pd.DataFrame, id:int) -> str:
  output = "seq1:\n"
  chunks1 = dataFrame["chunked_sentance1"][id]
  for i, chunk in enumerate(chunks1):
    output = output + str(i+1) + ") " + str(chunk) + "\n"
  output = output + "\nseq2:\n"
  chunks2 = dataFrame["chunked_sentance2"][id]
  for i, chunk in enumerate(chunks2):
    output = output + str(i+1) + ") " + str(chunk) + "\n"
  return output

def get_chunks_as_text(data:pd.DataFrame) -> str:
  output = []
  for index, row in data.iterrows():
    chunks = ""
    for chunk in row["chunked_sentance1"]:
      chunks = chunks + "[ " + chunk  + " ] "
    chunks = chunks + "\n"
    for chunk in row["chunked_sentance2"]:
      chunks = chunks + "[ " + chunk  + " ] "
    output.append(chunks)
  return output, data.index
