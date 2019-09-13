# MIT License
#
# Copyright (c) 2019 Daniel Brotsky
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import csv
import random
from typing import IO, List
import logging


class Words:
    """Make high-frequency words available for the grid."""
    def __init__(self, in_csv: IO):
        """Load the words from the given CSV stream."""
        self.three2eight: List[List[str]] = [[], [], [], [], [], []]
        read_rows, used_rows = 0, 0
        for row in csv.DictReader(in_csv):
            read_rows += 1
            word = row.get('Word', '').upper()
            if word:
                word_length = int(row.get('Word length', '0'))
                offset = word_length - 3
                if 0 <= offset <= 5:
                    used_rows += 1
                    self.three2eight[offset].append(row['Word'])
        if used_rows < read_rows:
            logging.log(logging.ERROR,
                        "Read %d rows but only used %d." %
                        (read_rows, used_rows))
        for words in self.three2eight:
            random.shuffle(words)
        self.next_index = {length: 0 for length in range(3, 9)}

    def pick2for9(self) -> (str, str):
        """Pick two words whose lengths are 3 and 6 or 4 and 5."""
        len1 = random.randint(3, 4)
        len2 = 9 - len1
        word1 = self.next_word(len1)
        word2 = self.next_word(len2)
        return word1.upper(), word2.upper()

    def pick2for12(self) -> (str, str):
        """Pick two words whose lengths are 5 and 7 or 6 and 6."""
        len1 = random.randint(5, 6)
        len2 = 12 - len1
        word1 = self.next_word(len1)
        word2 = self.next_word(len2)
        return word1.upper(), word2.upper()

    def pick3for12(self) -> (str, str, str):
        """Pick three four-letter words."""
        word1 = self.next_word(4)
        word2 = self.next_word(4)
        word3 = self.next_word(4)
        return word1.upper(), word2.upper(), word3.upper()

    def next_word(self, length: int) -> str:
        words = self.three2eight[length - 3]
        index = self.next_index[length]
        word = words[index]
        self.next_index[length] = next_index = (index + 1) % len(words)
        if next_index == 0:
            random.shuffle(words)
        return word
