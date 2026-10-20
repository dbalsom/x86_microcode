#!/usr/bin/env python3
"""Extract ASCII microcode words from the Harris 80C286 raw bit array.

Usage:
    python extract_words.py microcode_ROM_raw.txt

Input:  
    280 rows of 192 binary digits, in the original extraction orientation.
Output: 
    1,536 lines of 35 binary digits, in address order 000 through 5FF.
    Each line is printed most-significant bit first: bit 34 through bit 0.

80c286 Microcode ROM physical layout:
    The 280 rows form 35 groups of eight rows.
    Each group supplies one bit, with eight words per column.
    The top group holds bit 0; the bottom group holds bit 34.
    Starting at the right-most column, word addresses advance through the eight 
    row positions within a column then move one column left.
"""

import argparse
import sys
from pathlib import Path

WORD_BITS = 35
WORDS_PER_COLUMN = 8
COLUMNS = 192

def read_array(path: Path) -> list[str]:
    """Read the ASCII bit array"""
    return ["".join(line.split()) for line in path.read_text().splitlines() if line.strip()]

def extract_words(rows: list[str]) -> list[str]:
    """Return 35-bit strings in address order 000–5FF, MSB first."""
    words = []

    # Each column contains eight interleaved words. Start at the right edge.
    for column in range(COLUMNS - 1, -1, -1):
        for mux in range(WORDS_PER_COLUMN):
            # Read bottom to top to put bit 34 on the left of the string.
            word = "".join(
                rows[bit * WORDS_PER_COLUMN + mux][column]
                for bit in range(WORD_BITS - 1, -1, -1)
            )
            words.append(word)

    return words


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="raw ASCII bit array")
    args = parser.parse_args()

    words = extract_words(read_array(args.input))
    text = "\n".join(words) + "\n"
    sys.stdout.write(text)


if __name__ == "__main__":
    main()
