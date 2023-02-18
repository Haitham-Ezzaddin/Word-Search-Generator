import os
import sys
import random
from copy import deepcopy

#  This algorithm was used from https://scipython.com/blog/making-a-word-search-puzzle-in-python/
#  The author of this algorithm is Christian Hill
#  I have emailed him asking him for permission of use and questions about some functions in the algorithm
#  Contact : https://scipython.com/contact/

RowColMAX = 16  # This is the maximum number of Rows and Columns permitted

alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'  # a string containing all the letters in the alphabet


def make_grid():
    # Make the grid by creating a list of lists, defined by the rows and columns, containing an empty string
    grid = [[' '] * n_of_cols for r in range(n_of_rows)]
    return grid


def _make_wordsearch(nrows, ncols, wordlist, allow_backwards_words=True,
                     mask=None):
    """Attempt to make a word search with the given parameters."""

    grid = make_grid()

    def fill_grid_randomly(grid):
        """Fill up the empty, unmasked positions with random letters."""
        for irow in range(nrows):
            for icol in range(ncols):
                if grid[irow][icol] == ' ':
                    grid[irow][icol] = random.choice(alphabet)

    def remove_mask(grid):
        """Remove the mask, for text output, by replacing with whitespace."""
        for irow in range(nrows):
            for icol in range(ncols):
                if grid[irow][icol] == '*':
                    grid[irow][icol] = ' '

    def test_candidate(irow, icol, dx, dy, word):
        """Test the candidate location (icol, irow) for word in orientation
           dx, dy)."""
        for j in range(len(word)):
            if grid[irow][icol] not in (' ', word[j]):
                return False
            irow += dy
            icol += dx
        return True

    def place_word(word):
        """Place word randomly in the grid and return True, if possible."""

        # Left, down, and the diagonals.
        layout_choices = [(0,1), (1,0), (1,1), (1,-1)]
        random.shuffle(layout_choices)
        for (dx, dy) in layout_choices:
            if allow_backwards_words and random.choice([True, False]):
                # If backwards words are allowed, simply reverse word.
                word = word[::-1]
            # Work out the minimum and maximum column and row indexes, given
            # the word length.
            word_length = len(word)
            min_col = 0
            max_col = ncols - word_length if dx else ncols - 1
            min_row = 0 if dy >= 0 else word_length - 1
            max_row = nrows - word_length if dy >= 0 else nrows - 1
            if max_col - min_col < 0 or max_row - min_row < 0:
                # No possible place for the word in this orientation.
                continue
            # Build a list of candidate locations for the word.
            candidates = []
            for irow in range(min_row, max_row+1):
                for icol in range(min_col, max_col+1):
                    if test_candidate(irow, icol, dx, dy, word):
                        candidates.append((irow, icol))
            # If we don't have any candidates, try the next orientation.
            if not candidates:
                continue
            # Pick a random candidate location and place the word in this
            # orientation.
            loc = irow, icol = random.choice(candidates)
            for j in range(word_length):
                grid[irow][icol] = word[j]
                irow += dy
                icol += dx
            # We're done: no need to try any more orientations.
            break
        else:
            # If we're here, it's because we tried all orientations but
            # couldn't find anywhere to place the word. Oh dear.
            return False
        print(word, loc, (dx, dy))
        return True

    # Iterate over the word list and try to place each word (without spaces).
    for word in wordlist:
        word = word.replace(' ', '')
        if not place_word(word):
            # We failed to place word, so bail.
            return None, None

    # grid is a list of lists, so we need to deepcopy here for an independent
    # copy to keep as the solution (without random letters in unfilled spots).
    solution = deepcopy(grid)
    fill_grid_randomly(grid)
    remove_mask(grid)
    remove_mask(solution)

    return grid, solution


def make_wordsearch(*args, **kwargs):
    """Make a word search, attempting to fit words into the specified grid."""

    # We try NATTEMPTS times (with random orientations) before giving up.
    NATTEMPTS = 10
    for i in range(NATTEMPTS):
        grid, solution = _make_wordsearch(*args, **kwargs)
        if grid:
            print('Fitted the words in {} attempt(s)'.format(i+1))
            return grid, solution
    raise SystemError


def show_grid_text(grid):
    """Output a text version of the filled grid wordsearch."""
    for irow in range(n_of_rows):
        print(' '.join(grid[irow]))

def show_wordlist_text(wordlist):
    """Output a text version of the list of the words to find."""
    for word in wordlist:
        print(word)

def show_wordsearch_text(grid, wordlist):
    """Output the wordsearch grid and list of words to find."""
    show_grid_text(grid)
    print()
    show_wordlist_text(wordlist)


def svg_preamble(fo, width, height):
    """Output the SVG preamble, with styles, to open file object fo."""

    print("""<?xml version="1.0" encoding="utf-8"?>
    <svg xmlns="http://www.w3.org/2000/svg"
         xmlns:xlink="http://www.w3.org/1999/xlink" width="{}" height="{}" >
    <defs>
    <style type="text/css"><![CDATA[
    line, path {{
      stroke: Black;
      stroke-width: 9;
      stroke-linecap: square;
    }}
    path {{
      fill: none;http://www.w3.org/2000/svg
    }}

    text {{
      font: bold 24px Verdana, Helvetica, Arial, sans-serif; fill: rgb(67, 85, 141);
    }}

    ]]>
    </style>
    </defs>
    """.format(width, height), file=fo)

def grid_as_svg(grid, width, height):
    """Return the wordsearch grid as a sequence of SVG <text> elements."""

    # A bit of padding at the top.
    YPAD = 20
    # There is some (not much) wiggle room to squeeze in wider grids by
    # reducing the letter spacing.
    letter_width = min(32, width / n_of_cols)
    grid_width = letter_width * n_of_cols
    # The grid is centred; this is the padding either side of it.
    XPAD = (width - grid_width) / 2
    letter_height = letter_width
    grid_height = letter_height * n_of_rows
    s = []

    # Output the grid, one letter at a time, keeping track of the y-coord.
    y = YPAD + letter_height / 2
    for irow in range(n_of_rows):
        x = XPAD + letter_width / 2
        for icol in range(n_of_cols):
            letter = grid[irow][icol]
            if letter != ' ':
                s.append('<text x="{}" y="{}" text-anchor="middle">{}</text>'
                         .format(x, y, letter))
            x += letter_width
        y += letter_height

    # We return the last y-coord used, to decide where to put the word list.
    return y, '\n'.join(s)


def wordlist_svg(wordlist, width, height, y0):
    """Return a list of the words to find as a sequence of <text> elements."""

    # Use two columns of words to save (some) space.
    n = len(wordlist)
    col1, col2 = wordlist[:n//2], wordlist[n//2:]

    def word_at(x, y, word):
        """The SVG element for word centred at (x, y)."""
        return ( '<text x="{}" y="{}" text-anchor="middle" class="wordlist">'
                 '{}</text>'.format(x, y, word))

    s = []
    x = width * 0.25
    # Build the list of <text> elements for each column of words.
    y0 += 25
    for i, word in enumerate(col1):
        s.append(word_at(x, y0 + 25*i, word))
    x = width * 0.75
    for i, word in enumerate(col2):
        s.append(word_at(x, y0 + 25*i, word))
    return '\n'.join(s)


def write_wordsearch_svg(filename, grid, wordlist):
    """Save the wordsearch grid as an SVG file to filename."""

    width, height = 816, 1056
    with open(filename, 'w') as fo:
        svg_preamble(fo, width, height)
        y0, svg_grid = grid_as_svg(grid, width, height)
        print(svg_grid, file=fo)
        # If there's room print the word list.
        if y0 + 25 * len(wordlist) // 2 < height:
            print(wordlist_svg(wordlist, width, height, y0), file=fo)
        print('</svg>', file=fo)
        return fo


class EmptyWordlist(Exception):
    pass


def get_wordlist(wordlist_filename):
    """Read in the word list from wordlist_filename."""
    wordlist = []
    with open(wordlist_filename) as fi:
        for line in fi:
            # The word is upper-cased and comments and blank lines are ignored.
            line = line.strip().upper()
            if not line or line.startswith('#'):
                continue
            wordlist.append(line)
    if len(wordlist) == 0:
        raise EmptyWordlist
    return wordlist


# n_of_rows, n_of_cols = 11, 11 #default


def start_game(file_path, rows=11, columns=11):
    global n_of_rows, n_of_cols

    wordlist_filename = file_path
    n_of_rows, n_of_cols = rows, columns
    mask = None

    if n_of_rows > RowColMAX or n_of_cols > RowColMAX:
        sys.exit('Maximum number of rows and columns is {}'.format(RowColMAX))
    wordlist = sorted(get_wordlist(wordlist_filename), key=lambda w: len(w),
                      reverse=True)
    # Obviously, no word can be longer than the maximum dimension.
    max_word_len = max(n_of_rows, n_of_cols)
    if max(len(word) for word in wordlist) > max_word_len:
        raise ValueError('Word list contains a word with too many letters.'
                         'The maximum is {}'.format(max(n_of_rows, n_of_cols)))

    # This flag determines whether words can be fitted backwards into the grid
    # (which makes the puzzle a bit harder).
    allow_backwards_words = False
    # If using a mask, specify it by a key to the apply_mask dictionary.
    grid, solution = make_wordsearch(n_of_rows, n_of_cols, wordlist, allow_backwards_words,
                                     mask)

    # If we fitted the words to the grid, show it in text format and save SVG files
    # of the grid and its solution.
    if grid:
        show_wordsearch_text(grid, wordlist)
        filename = os.path.splitext(wordlist_filename)[0] + '.svg'
        write_wordsearch_svg(filename, grid, wordlist)
        filename = os.path.splitext(wordlist_filename)[0] + '-solution.svg'
        write_wordsearch_svg(filename, solution, [])





