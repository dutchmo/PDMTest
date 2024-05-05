
import os
from collections import Counter

def count_words_in_directory(directory):
    word_count = Counter()

    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)

            # Check if the file is a text file
            if file.endswith('.txt'):
                with open(file_path, 'r') as f:
                    content = f.read()
                    words = content.split()
                    word_count.update(words)

    return word_count


class Util():
    @staticmethod
    def count_words_in_directory(directory):
        word_count = Counter()