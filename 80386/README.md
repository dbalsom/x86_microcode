# 80386
Microcode for the Intel 80386 CPU.

## /images

Die photos by Ken Shirriff.

## /binary

The binary information from the die photos, transcribed into 0s and 1s.

## /disassembler

A program to generate microcode_10.txt from the files in the binary directory.

## /parts.txt

Describes the size and layout of the various major ROM/PLA sections of the 386, as transcribed in the binary directory and decoded in the other files listed here.

## /microcode_10.txt

The actual microcode disassembly.

## /microcode_notes.txt

Line-by-line notes on the microcode disassembly, used in the decoding process.

## /fields.txt

Notes on the possible values of the various fields of the microinstructions and their meanings.

## /constant_rom.txt

Notes on the constant ROM including the actual values of the various constant values used by different parts of the microcode.

## /rom1_processed.txt

Processed version of the rom1 first stage decoder. This implements the state machine used to decode opcodes and effective addresses.

## /decoder23.txt

Processed version of the decoder 2/3 ROMs. These translate opcodes into microcode entry points. An instruction may need to make several trips through this decoder to determine the correct entry point (once for each prefix, once for the opcode, once for the mod r/m byte if the entry point depends on it).

## /decode2.txt

Some more notes on how the decoder 2/3 ROM generates entry points.

## pla4_expanded.txt

Expanded version of the protection test unit PLA.

## tests.txt

Notes on decoding the protection test PLA - translation from test inputs to microcode entry points.

## pla1_pla4_z386.md

nand2mario's notes on instruction decoding and the protection test unit.

## small_pla.txt

Notes on the small PLA used to dispatch the microcode to various exception handling routines.
