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
from typing import Optional, Tuple, List


class Grids:
    def __init__(self, size: int):
        self.rows = 3
        self.cols = size // self.rows
        if self.rows * self.cols != size:
            raise ValueError("Grid size must be a multiple of 3")
        self.size = size
        self.indices = [(x, y)
                        for x in range(self.rows)
                        for y in range(self.cols)]
        self.grid = dict((index, '') for index in self.indices)

    def grid_words(self,
                   word1: str,
                   word2: str,
                   word3: Optional[str] = None
                   ) -> [str]:
        """Lay out two or three words on the grid, returning the resulting grid.
        The three words are assumed to completely fill the grid, the second word
        is assumed to be the longest of the three, and if there is a third word
        it's assumed to be the same length as the second.
        Each word is laid out with its letters contiguous in reading order."""

        def possibles(r_c: Tuple[int, int], g: dict) -> List[Tuple[int, int]]:
            """Find the empty neighbors of the given cell.
            These are the spots where it's possible to put the next letter.
            """
            r, c = r_c
            empties = [(x, y)
                       for x in range(r - 1, r + 2)
                       for y in range(c - 1, c + 2)
                       if 0 <= x < self.rows and
                       0 <= y < self.cols and
                       g[(x, y)] == '']
            random.shuffle(empties)
            return empties

        def layout(w1: str, w2: str,
                   w3: Optional[str],
                   r_c1: Tuple[int, int], r_c2: Tuple[int, int],
                   r_c3: Optional[Tuple[int, int]],
                   g0: dict) -> dict:
            """Find the layout by doing a breadth-first search.
            We are given the grid so far and the most recently placed
            letter position for each word, and we try to layout the
            rest of the letters (doing one letter per word and then
            recursively laying out the rest of them).  If there are
            no letters left to lay out, we return the filled grid.
            If we fail to layout the next letter in each word, we
            return an empty grid.
            """
            if (w3 is None) != (r_c3 is None):
                raise ValueError("The number of words must match "
                                 "the number of indices.")
            if not w2:
                return g0    # success!
            possibles2 = possibles(r_c2, g0)
            if not possibles2:
                return {}
            for rc2 in possibles2:
                g2 = g0.copy()
                g2[rc2] = w2[0:1]
                if w1:
                    possibles1 = possibles(r_c1, g2)
                    if not possibles1:
                        continue  # try next possibles2
                    for rc1 in possibles1:
                        g1 = g2.copy()
                        g1[rc1] = w1[0:1]
                        if w3:
                            possibles3 = possibles(r_c3, g1)
                            if not possibles3:
                                continue    # try next possibles1
                            for rc3 in possibles3:
                                g3 = g1.copy()
                                g3[rc3] = w3[0:1]
                                g = layout(w1[1:], w2[1:], w3[1:],
                                           rc1, rc2, rc3, g3)
                                if not g:
                                    continue    # try next possibles3
                                return g    # success!
                            return {}   # failed to lay out w3
                        else:   # only laying out two words
                            g = layout(w1[1:], w2[1:], None,
                                       rc1, rc2, None, g1)
                            if not g:
                                continue    # try next possibles1
                            return g    # success!
                    return {}   # failed to lay out w1
                else:   # only laying out two words, and w1 has been completed
                    g = layout('', w2[1:], None, r_c1, rc2, None, g2)
                    if not g:
                        continue
                    return g
            return {}   # failed to lay out w2

        random_indices = random.sample(self.indices, self.size)
        for i1 in random_indices:
            grid1 = self.grid.copy()
            grid1[i1] = word1[0:1]
            for i2 in random_indices:
                if i2 == i1:
                    continue
                grid2 = grid1.copy()
                grid2[i2] = word2[0:1]
                if word3:
                    for i3 in random_indices:
                        if i3 == i1 or i3 == i2:
                            continue
                        grid3 = grid2.copy()
                        grid3[i3] = word3[0:1]
                        result = layout(word1[1:], word2[1:], word3[1:],
                                        i1, i2, i3,
                                        grid3)
                        if result:
                            return [result[index] for index in self.indices]
                else:
                    result = layout(word1[1:], word2[1:], None,
                                    i1, i2, None,
                                    grid2)
                    if result:
                        return [result[index] for index in self.indices]
        return []
