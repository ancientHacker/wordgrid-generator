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
import sys

import click

from .grids import Grids
from .words import Words


@click.command()
@click.option('-c', '--count', default=1, show_default=True,
              help="Number of puzzles to generate")
@click.option('-s', '--size', default=12, show_default=True,
              help="Number of letters in each puzzle")
def generate(count: int, size):
    with open('Words to use.csv') as f:
        words = Words(f)
    grids = Grids(size)
    results = []
    for _ in range(count):
        word1, word2 = words.pick2(size)
        grid_strings = grids.grid_two(word1, word2)
        if not grid_strings:
            print("Failed to lay out '{}' and '{}'".format(word1, word2),
                  file=sys.stderr)
            continue
        results.append({'word1': word1, 'word2': word2, 'cells': grid_strings})
    print(json.dumps(results))


if __name__ == '__main__':
    generate()
