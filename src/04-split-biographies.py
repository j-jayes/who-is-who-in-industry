import os
import re
import yaml
import logging
import string 

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


def read_and_split_biographies(file_name, letter):
    """
    Reads a text file containing biographies and splits them based on the provided letter.
    
    Args:
    file_name (str): The path of the file to read.
    letter (str): The letter used to split the biographies.
    
    Returns:
    list: A list containing the split biographies.
    
    Example:
    >>> read_and_split_biographies('data/joined/vemindu/vemindu_A-names.txt', 'A')
    """
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            text = file.read()
        
        # Replace multiple spaces with a single space
        text = re.sub(' +', ' ', text)
        
        # Use string.punctuation for matching punctuation characters
        punctuation = re.escape(string.punctuation)
        pattern = fr'^[\s{punctuation}\d]*({letter}[A-ZÅÄÖ{punctuation}]+),'
        if letter == 'V':
            pattern = fr'^[\s{punctuation}\d]*(?:[VW][A-ZÅÄÖ{punctuation}]+),'

        split_text = re.split(pattern, text, flags=re.MULTILINE)
        biographies = [f"{surname}, {bio}" for surname, bio in zip(split_text[1::2], split_text[2::2])]
        
        return biographies
    except Exception as e:
        logging.error(f"Error occurred while reading and splitting biographies from {file_name}: {e}")
        return []


def clean_biography(biography):
    """Cleans a biography by removing line breaks and trimming whitespace."""
    return ' '.join(biography.split()).strip()


def save_biography(biography, file_path):
    """Saves a cleaned biography to a specified file path."""
    try:
        with open(file_path, 'w', encoding='utf-8') as output_file:
            output_file.write(biography)
    except Exception as e:
        logging.error(f"Error occurred while saving biography to {file_path}: {e}")


def save_biographies(biographies, letter):
    """
    Saves each biography in the list of biographies to a separate file.
    
    Args:
    biographies (list): A list of biographies to save.
    letter (str): The letter used as a part of the output file name.
    
    Example:
    >>> save_biographies(['Anderson, John...'], 'A')
    """
    output_directory = 'data/biographies'
    os.makedirs(output_directory, exist_ok=True)

    for index, biography in enumerate(biographies):
        cleaned_biography = clean_biography(biography)
        output_file_name = f'vemindu_{letter}_biography_{index + 1}.txt'
        output_file_path = os.path.join(output_directory, output_file_name)
        
        save_biography(cleaned_biography, output_file_path)


def main():
    """
    Executes the main script functions.
    
    Reads the YAML file containing the table of contents (Expected YAML structure: {letter: title}),
    loops through the letters, reads, splits, and saves the biographies for each corresponding letter.
    """
    with open('data/vemindu_toc.yaml', 'r', encoding='utf-8') as yaml_file:
        toc = yaml.safe_load(yaml_file)

    letters = list(toc.keys())
    for letter in letters:
        input_file_name = f'vemindu_{letter}-names.txt'
        input_file_path = os.path.join('data', 'joined', "vemindu", input_file_name)

        if os.path.isfile(input_file_path):
            biographies = read_and_split_biographies(input_file_path, letter)
            save_biographies(biographies, letter)
        else:
            logging.warning(f"File not found: {input_file_path}")


if __name__ == '__main__':
    main()
