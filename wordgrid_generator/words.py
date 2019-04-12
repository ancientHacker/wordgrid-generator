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

    def pick2(self, total: int) -> (str, str):
        """Pick two words whose lengths add to the given total length,
        which must be in the range 9-12.  The shorter of the two
        words is never more than two shorter than half the total.
        The first word is always the shorter of the two."""
        len1 = random.randrange(max(3, total // 2 - 2), total // 2 + 1)
        words1 = self.three2eight[len1 - 3]
        len2 = total - len1
        words2 = self.three2eight[len2 - 3]
        # note that we may have len1 == len2 and thus words1 is words2
        index_1 = self.next_index[len1]
        self.next_index[len1] = next_index_1 = (index_1 + 1) % len(words1)
        index_2 = self.next_index[len2]
        self.next_index[len2] = next_index_2 = (index_2 + 1) % len(words2)
        word1 = words1[index_1]
        word2 = words2[index_2]
        if next_index_1 == 0:
            random.shuffle(words1)
        if next_index_2 == 0:
            random.shuffle(words2)
        return word1.upper(), word2.upper()
