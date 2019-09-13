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
import json
import random
import sys

import click

from .grids import Grids
from .words import Words


@click.command()
@click.option('-c', '--count', default=1, show_default=True,
              help="Number of puzzles to generate")
@click.option('-s', '--size', default=12, show_default=True,
              help="Number of letters in each puzzle")
@click.option('-r', '--ratio', default=0.33, show_default=True,
              help="Fraction of 12x12 grids to fill with three 4-letter words")
def generate(count: int, size, ratio):
    if size not in [9, 12]:
        raise ValueError(f"Grid size ({size}) must be 9 or 12")
    if size == 12 and not 0 <= ratio <= 1:
        raise ValueError(f"Ratio ({ratio}) must be between 0 and 1 (inclusive)")
    with open('Words to use.csv') as f:
        words = Words(f)
    grids = Grids(size)
    results = []
    for _ in range(count):
        if size == 9:
            word1, word2 = words.pick2for9()
            word3 = None
        else:
            if random.random() <= ratio:
                word1, word2 = words.pick2for12()
                word3 = None
            else:
                word1, word2, word3 = words.pick3for12()
        grid_strings = grids.grid_words(word1, word2, word3)
        if not grid_strings:
            print(f"Failed to lay out '{word1}', '{word2}', '{word3}'",
                  file=sys.stderr)
            continue
        results.append({'word1': word1, 'word2': word2, 'word3': word3 or '',
                        'cells': grid_strings})
    print(json.dumps(results))


if __name__ == '__main__':
    generate()
