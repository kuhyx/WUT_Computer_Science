#!/usr/bin/env python3
"""Load the SemEval corpus: sentences, chunkings and gold alignments."""

import sys
import logging
import re
from pathlib import Path

import numpy as np
import pandas as pd
from lxml import etree

logger = logging.getLogger(__name__)
logging.basicConfig(format="%(message)s", level=logging.INFO)


def load_sentences(senteance1_path: str, sentance2_path: str) -> pd.DataFrame:
    """Load the sentences from the given paths and outputs in a 2 columns dataframe."""
    sentance1 = pd.read_csv(senteance1_path, dtype=str, delimiter="}", header=None)
    sentance1.columns = ["sentance1"]

    sentance2 = pd.read_csv(sentance2_path, dtype=str, delimiter="}", header=None)
    sentance2.columns = ["sentance2"]

    return pd.concat([sentance1, sentance2], axis=1)


def chunk2list(chunks: str) -> list:
    """Split one chunked sentence into its chunks."""
    chunks = chunks.replace("[", "")
    chunks = chunks.replace("]", "")
    chunks = chunks.replace("   ", "|")
    split = chunks.split("|")

    split = [
        re.sub(r"^\s+|\s+$", "", s) for s in split
    ]  # remove spaces at the beggining and end of chunks
    return [re.sub(r"[^\w\s]", "", s) for s in split]  # remove punctuation


def load_chunked(chunked_path1: str, chunked_path2: str) -> pd.DataFrame:
    """Load two chunk files into a dataframe of chunk lists.

    The on-disk format is ``[ chunk1 ] [ chunk2 ] ...`` per line.
    """
    chunked_sentance1 = pd.read_csv(
        chunked_path1, dtype=str, delimiter="}", header=None
    )
    chunked_sentance1.columns = ["chunked_sentance1"]

    chunked_sentance2 = pd.read_csv(
        chunked_path2, dtype=str, delimiter="}", header=None
    )
    chunked_sentance2.columns = ["chunked_sentance2"]

    headlines_chunked = pd.concat([chunked_sentance1, chunked_sentance2], axis=1)

    # convert chunks from str to list
    headlines_chunked["chunked_sentance1"] = headlines_chunked[
        "chunked_sentance1"
    ].apply(chunk2list)
    headlines_chunked["chunked_sentance2"] = headlines_chunked[
        "chunked_sentance2"
    ].apply(chunk2list)

    return headlines_chunked


def return_characteers(cell: str) -> str:
    """Convert the alignment data to restore the <==> and & tokens."""
    cell = cell.replace("ARROWS_PLACEHOLDER", "<==>")
    return cell.replace("AMPERSAND_PLACEHOLDER", "&")


def load_alignment(alignment_path: str) -> pd.DataFrame:
    """Load the gold alignment file into a dataframe.

    Only the ``<alignment>`` tag is parsed; the rest of the .wa XML is
    metadata this project does not use.
    """
    with Path(alignment_path).open() as file:
        file_content = file.read()

    # <==> and & break xml loaders so it needs to be replaces with something else
    modified_content = file_content.replace("<==>", "ARROWS_PLACEHOLDER").replace(
        "&", "AMPERSAND_PLACEHOLDER"
    )
    # it also needs a root wrapped to function properly
    modified_content = f"<root>{modified_content}</root>"

    modified_file_path = "temp.wa"
    with Path(modified_file_path).open("w") as modified_file:
        modified_file.write(modified_content)

    # Parse the modified file using ElementTree
    tree = etree.parse(modified_file_path)
    root = tree.getroot()

    # get ansewrs
    alignments_data = []

    for alignment in root.xpath("//alignment"):
        # Extract relevant information from the alignment element
        data = {
            "sentence_id": alignment.xpath("ancestor::sentence/@id")[0],
            "alignment_text": alignment.text,
        }
        alignments_data.append(data)

    y = pd.DataFrame(alignments_data)
    y = y.drop(columns=["sentence_id"])
    y["alignment_text"] = y["alignment_text"].apply(return_characteers)
    return y


def prettyprint(element: etree._Element, **kwargs: object) -> None:
    """Log an XML element with lxml's pretty printer."""
    xml = etree.tostring(element, pretty_print=True, **kwargs)
    sys.stdout.write(xml.decode())


def log_first_alignment(alignments_data: list[dict[str, str]]) -> None:
    """Log the first parsed alignment, to eyeball the .wa parsing.

    This was `test_XML()` and read a module-level `alignments_data` that does
    not exist at module scope -- it only ever worked when pasted into a
    session where load_alignment had already run. It takes the data as an
    argument now, and is no longer named test_* so pytest does not collect it.
    """
    logger.info("%s", alignments_data[0]["alignment_text"])


def generate_train_test_split(xy: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Split the dataframe into a train and a test half.

    The docstring said 60/20/20 when it was written; the code splits at 3%,
    which is what the experiments actually used.
    """
    data = xy
    train, test = np.split(
        data.sample(frac=1, random_state=42), [int(0.03 * len(data))]
    )

    return train, test


def generate_alignment_format(data_frame: pd.DataFrame, row_id: int) -> str:
    """Render one row's two chunkings as the numbered text GPT is shown."""
    output = "seq1:\n"
    chunks1 = data_frame["chunked_sentance1"][row_id]
    for i, chunk in enumerate(chunks1):
        output = output + str(i + 1) + ") " + str(chunk) + "\n"
    output = output + "\nseq2:\n"
    chunks2 = data_frame["chunked_sentance2"][row_id]
    for i, chunk in enumerate(chunks2):
        output = output + str(i + 1) + ") " + str(chunk) + "\n"
    return output


def get_chunks_as_text(data: pd.DataFrame) -> tuple[list[str], pd.Index]:
    """Render every row's chunk pair as bracketed text, with its index."""
    output = []
    for _index, row in data.iterrows():
        chunks = ""
        for chunk in row["chunked_sentance1"]:
            chunks = chunks + "[ " + chunk + " ] "
        chunks = chunks + "\n"
        for chunk in row["chunked_sentance2"]:
            chunks = chunks + "[ " + chunk + " ] "
        output.append(chunks)
    return output, data.index
