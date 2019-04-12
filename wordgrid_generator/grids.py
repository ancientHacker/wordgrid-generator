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
import random


class Grids:
    def __init__(self, size: int):
        self.rows = 3
        self.cols = size // self.rows
        if self.rows * self.cols != size:
            raise ValueError("Grid size must be a multiple of 3")
        self.indices = [(x, y)
                        for x in range(self.rows) for y in range(self.cols)]

    def grid_two(self, word1: str, word2: str) -> [str]:
        """Lay out two words on the grid, returning the resulting grid.
        The two words are assumed to completely fill the grid, and
        the second is assumed to be at least as long as the first word.
        Each word is laid out with its letters contiguous."""

        def possibles(r_c: (int, int), grid: dict) -> (int, int):
            """Find the empty neighbors of the given cell.
            These are the spots where it's possible to put the next letter.
            """
            r, c = r_c
            empties = [(x, y)
                       for x in range(r - 1, r + 2)
                       for y in range(c - 1, c + 2)
                       if 0 <= x < self.rows and
                          0 <= y < self.cols and
                          grid[(x, y)] == '']
            random.shuffle(empties)
            return empties

        def layout(w1: str, w2: str,
                   r_c1: (int, int), r_c2: (int, int),
                   grid: dict) -> dict:
            """Find the layout by doing a breadth-first search.
            We are given the grid so far and the most recently placed
            letter position for each word, and we try to layout the
            rest of the letters (alternating between the two words).
            """
            if not w2:
                return grid
            possibles2 = possibles(r_c2, grid)
            if not possibles2:
                return {}
            for rc2 in possibles2:
                g2 = grid.copy()
                g2[rc2] = w2[0:1]
                if w1:
                    possibles1 = possibles(r_c1, g2)
                    if not possibles1:
                        continue  # try next possibles2
                    for rc1 in possibles1:
                        g1 = g2.copy()
                        g1[rc1] = w1[0:1]
                        g = layout(w1[1:], w2[1:], rc1, rc2, g1)
                        if not g:
                            continue
                        return g
                else:
                    g = layout('', w2[1:], r_c1, rc2, g2)
                    if not g:
                        continue
                    return g
            return {}

        grid = dict(((index, '') for index in self.indices))
        i1, i2 = random.sample(self.indices, 2)
        grid[i2] = word2[0:1]
        grid[i1] = word1[0:1]
        result = layout(word1[1:], word2[1:], i1, i2, grid)
        if result:
            return [result[index] for index in self.indices]
        else:
            return []

