#!/usr/bin/env python3
"""Regenerate CMOS/NMOS CONTROL_ROM_01 logic and decoded tables.

CTRL[1] and CTRL[3] have reversed horizontal pair order in both versions,
per the physical tracing correction supplied on 2026-10-26. The final raw
column retains the existing interpretation: present requires CTRL[4]=1.

Run with no arguments to update both versions, or --check to verify them.
"""

import argparse
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NORMAL = {"10": "0", "01": "1", "00": "?"}
REVERSED = {"10": "1", "01": "0", "00": "?"}
PAIR_MAPS = (NORMAL, REVERSED, NORMAL, REVERSED)
TITLES = {"cmos": "CMOS 80C286", "nmos": "NMOS N80286"}


def read_rows(path):
    rows = path.read_text(encoding="ascii").splitlines()
    if not rows or any(len(row) != 9 or set(row) - {"0", "1"} for row in rows):
        raise ValueError(f"Expected nine binary columns in {path}")
    return rows


def decode(rows):
    logic, matches = [], []
    for row in rows:
        term = "".join(mapping[row[2*i:2*i+2]] for i, mapping in enumerate(PAIR_MAPS))
        logic.append(term + row[8])
        matches.append(term + ("1" if row[8] == "1" else "?"))
    return logic, matches


def matches_value(pattern, value):
    return all(bit == "?" or int(bit) == ((value >> i) & 1)
               for i, bit in enumerate(pattern))


def validate(rows, logic, patterns):
    inverses = [{value: pair for pair, value in mapping.items()} for mapping in PAIR_MAPS]
    for raw, collapsed, pattern in zip(rows, logic, patterns):
        restored = "".join(inverses[i][collapsed[i]] for i in range(4)) + collapsed[4]
        assert restored == raw
        for value in range(32):
            physical = raw[8] == "0" or bool(value & 0x10)
            for i in range(4):
                first_level = int(i in (1, 3))
                bit = (value >> i) & 1
                physical &= not (raw[2*i] == "1" and bit != first_level)
                physical &= not (raw[2*i+1] == "1" and bit == first_level)
            assert matches_value(pattern, value) == physical


def observed_cmos_controls(path):
    words, controls = {}, set()
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        if len(line) > 5 and line[3:5] == "  " and all(c in "0123456789ABCDEF" for c in line[:3]):
            fields = tuple(int(token, 16) for token in line.split("|")[1].split())
            assert len(fields) == 6
            address = int(line[:3], 16)
            assert address not in words
            words[address] = fields
            if fields != (63, 63, 63, 31, 127, 31):
                controls.add(fields[3])
    assert set(words) == set(range(1536))
    return controls


def table(headers, rows):
    widths = [max(len(row[i]) for row in [headers, *rows]) for i in range(len(headers))]
    render = lambda row: " | ".join(cell.ljust(width) for cell, width in zip(row, widths)).rstrip()
    return [render(headers), "-+-".join("-" * width for width in widths),
            *(render(row) for row in rows)]


def render(version, rows, patterns, other_patterns, observed):
    other = "nmos" if version == "cmos" else "cmos"
    other_indices = {pattern[:4]: i for i, pattern in enumerate(other_patterns)}
    assert len(other_indices) == len(other_patterns) == len(patterns)
    assert {p[:4] for p in patterns} == set(other_indices)
    display_rows, differing = [], []
    for i, (raw, pattern) in enumerate(zip(rows, patterns)):
        j = other_indices[pattern[:4]]
        if pattern[4] != other_patterns[j][4]:
            differing.append(str(i + 1))
            assert {pattern[4], other_patterns[j][4]} == {"1", "?"}
            assert (pattern if version == "nmos" else other_patterns[j])[4] == "1"
        values = [f"{v:02X}" + ("*" if v not in observed else "")
                  for v in range(32) if matches_value(pattern, v)]
        display_rows.append([f"{i+1:02}", raw, pattern, f"{j+1:02}", " ".join(values)])
    lines = [f"{TITLES[version]} CONTROL_ROM_01 Decoding", "",
             "Rows are numbered 1-based, top to bottom.",
             "RAW: 1 = transistor present; 0 = absent.", "",
             "MATCH: CONTROL[0] through CONTROL[4], left to right. ? = don't care.",
             "CONTROL[0] is the least significant bit of CONTROL HEX.", "",
             "Raw pairs 1-2 / 5-6 (CONTROL[0]/[2]): 10 -> 0, 01 -> 1, 00 -> don't care.",
             "Raw pairs 3-4 / 7-8 (CONTROL[1]/[3]): 10 -> 1, 01 -> 0, 00 -> don't care.",
             "CONTROL[1] and CONTROL[3] have reversed horizontal pair order in both versions.",
             "Raw column 9 decodes as 1 -> CONTROL[4]=1, 0 -> don't care.",
             "The _logic.txt file preserves raw column 9 verbatim; MATCH expands its 0 to ?.", "",
             "CONTROL HEX lists all matching 5-bit values in ascending order.",
             "* = absent from nonempty words in ../cmos/intel286_microcode.txt.",
             "This is a CMOS microcode usage reference, not a claim about NMOS ROM usage.",
             f"{other.upper()} ROW identifies the corresponding term by its CONTROL[0..3] match.", ""]
    lines += table(["ROW", "RAW", "MATCH C0..C4", f"{other.upper()} ROW", "CONTROL HEX"], display_rows)
    lines += ["", f"All {len(rows)} CONTROL[0..3] terms match to {other.upper()} CONTROL ROM 01 after row reordering.",
              "Rows " + ", ".join(differing) + " differ in their CONTROL[4] condition.",
              "NMOS requires CONTROL[4]=1; the corresponding CMOS terms ignore that bit.", ""]
    return "\n".join(lines)


def output_bytes(path, text):
    old = path.read_bytes()
    newline = "\r\n" if b"\r\n" in old else "\n"
    if not old.endswith(b"\n"):
        text = text.rstrip("\n")
    return text.replace("\n", newline).encode("ascii")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Verify existing artifacts without writing")
    args = parser.parse_args()
    raw_paths = {v: ROOT/v/"CONTROL_ROM_01_raw.txt" for v in TITLES}
    originals = {v: path.read_bytes() for v, path in raw_paths.items()}
    rows = {v: read_rows(path) for v, path in raw_paths.items()}
    decoded = {v: decode(matrix) for v, matrix in rows.items()}
    observed = observed_cmos_controls(ROOT/"cmos/intel286_microcode.txt")
    outputs = {}
    for version in TITLES:
        logic, patterns = decoded[version]
        validate(rows[version], logic, patterns)
        other = "nmos" if version == "cmos" else "cmos"
        outputs[ROOT/version/"CONTROL_ROM_01_logic.txt"] = "\n".join(logic) + "\n"
        outputs[ROOT/version/"CONTROL_ROM_01_decoded.txt"] = render(
            version, rows[version], patterns, decoded[other][1], observed)
    prepared = {path: output_bytes(path, text) for path, text in outputs.items()}
    for version, path in raw_paths.items():
        assert path.read_bytes() == originals[version]
    for path, content in prepared.items():
        if args.check:
            if path.read_bytes() != content:
                raise SystemExit(f"Out of date: {path}")
        else:
            path.write_bytes(content)
        print(("Verified " if args.check else "Wrote ") + str(path))
    count = sum(map(len, rows.values()))
    print(f"Validated {count*9} raw bits and {count*32} term evaluations; raw files unchanged.")


if __name__ == "__main__":
    main()
