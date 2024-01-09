

def reformat_sentence(sentence):
    """
    Reformats a sentence by replacing slashes '/' with ' ]'.
    """
    return sentence.replace('/', ' ]')

def insert_commas(sentence, reference_sentence):
    """
    Inserts commas into 'sentence' at the same positions as they appear in 'reference_sentence'.
    """
    # Splitting the sentences into chunks
    sentence_chunks = sentence.split(' ] [ ')
    reference_chunks = reference_sentence.split(' ] [ ')

    # Insert commas into the original sentence based on the reference sentence
    for i, chunk in enumerate(reference_chunks):
        if ',' in chunk and i < len(sentence_chunks):
            sentence_chunks[i] += ','

    # Reconstruct the sentence with inserted commas
    return ' ] [ '.join(sentence_chunks)


def process_sentences(sentences1, sentences2):
    """
    Processes two lists of sentences according to the specified rules.
    """
    processed_sentences = []

    for sentence1, sentence2 in zip(sentences1, sentences2):
         # Reformat the first sentence
        reformatted_sentence1 = reformat_sentence(sentence1)
        reformatted_sentence1 = insert_commas(reformatted_sentence1, sentence2)
        # Splitting the sentences into words, ignoring the square brackets
        words1 = set(' '.join(reformatted_sentence1.strip().split('] [')).replace('[', '').replace(']', '').lower().split())
        words2 = set(' '.join(sentence2.strip().split('] [')).replace('[', '').replace(']', '').lower().split())

        # Finding differences in words
        diff = words2 - words1

        # Preparing the output sentence
        output_sentence = reformatted_sentence1.strip()
        if '[ . ]' in sentence2:
            output_sentence += ' [ . ]'

        # Adding the differences and the output sentence to the processed_sentences list
        processed_sentences.append({
            "sentence1": reformatted_sentence1.strip(),
            "sentence2": sentence2.strip(),
            "differences": diff,
            "merged_sentence": output_sentence
        })
        if diff and diff != {'.'}:
            print("Difference found!")
            print("Sentence 1:", reformatted_sentence1.strip())
            print("Sentence 2:", sentence2.strip())
            print("Differences:", diff)
            print("\n")

    return processed_sentences

# First, let's open and read the contents of both files to understand their structure and content.
file_path_1 = 'test_goldStandard/images/images-chunks-gpt-one.txt'
file_path_2 = 'test_goldStandard/images/STSint.testinput.images.sent1.chunk.txt'

# Reading the files
with open(file_path_1, 'r') as file1, open(file_path_2, 'r') as file2:
    sentences_file_1 = file1.readlines()
    sentences_file_2 = file2.readlines()

# Process the sentences
processed_sentences = process_sentences(sentences_file_1, sentences_file_2)