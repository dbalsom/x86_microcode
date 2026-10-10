> [!NOTE]  
> If you would like to assist with the decoding effort, there is a thread on the [VCF forums](https://forum.vcfed.org/index.php?threads/the-nec-v20-microcode-rom.1254770/) where the most recent updates occur.



# The NEC V20 & V30 Microcode

A decoding of the NEC V20/V30 microcode was recently made possible via the imaging work of [InfoSecDJ](https://infosec.exchange/@infosecdj):
<img width="800" height="697" alt="The NEC V20 Die" src="images/v20_die_shot_01.jpg" />

See the full die shot mosaic on [siliconprawn](https://siliconprawn.org/archive/doku.php?id=infosecdj:sharp:lh70108).

NEC used unified microcode for both the NEC V20 and V30, which differ only in their metal layer interconnects.

The only difference between the microcode for either version of CPU is in the microcode routine that handles hardware
interrupts. Like the 8088, the V20 needs a special routine to only issue one INTA request to the 8259 as otherwise its
BIU logic will split two INTA cycles into four. 

## Word Format

There are some differences between the actual microcode word format the published legend, which has its origin in 
court documents from the NEC vs Intel lawsuit. The microcode is logically split into two parts, 17 bits that encode
source and destination operands, and 12 bits that encode executive instructions.

The source/destination field has two formats, one that encodes two source/destination pairs, and one that encodes an
immediate constant value. 

![word_format](./images/v20_word_format.png)

## Files

#### vx0_microcode.xlsx

A working decode spreadsheet of the V20/V30 microcode.

#### v20_microcode_01.txt

The extracted bits from the V20's microcode ROM in ASCII format, an array of 258x116 bits. 

Note that there are two more columns than you may expect. Column 128 (exactly halfway through the ROM) does not appear
to be decoded. Columns 119 & 120 contain the hardware interrupt routine for the V20 and V30, respectively. 

The column not used by the specific CPU is disabled by a cut in the metal layer on top of the ROM.

These bits are also available as a PNG and PBM image, as follows:

![microcode_bits](./images/microcode_rom.png)

#### /images/microcode_rom.png
#### /images/microcode_rom.pbm

#### /images/microcode_crop_01.jpg

This is a half-resolution crop of the microcode ROM region. This image file was used with MaskRomTool to define the ROM
bit positions.

#### /images/microcode_crop_01.jpg.json

MaskRomTool's saved project file for the image above. If you load the image with this JSON in the same directory in
MaskRomTool the project should be restored and you could attempt your own extraction.

#### /images/microcode_bit_check.jpg

This is a grid-aligned image of the microcode ROM bits showing the logical bit extraction overlayed - a 1 bit being a 
bright square and a 0 being a dark square.  This image was used for manual verification of the extraction accuracy.

Spot any errors? Please open an issue if you do!

#### /images/activation_pla_01.jpg

This is a half-resolution crop of the microcode activation PLA, or what Intel calls a matching decoder PLA. 

#### /images/activation_pla_01.jpg.json

MaskRomTool's saved project file for the image above. If you load the image with this JSON in the same directory in
MaskRomTool the project should be restored and you could attempt your own extraction.

### v20_activation_pla.txt

The extracted gates from the V20's microcode activation PLA in ASCII format, an array of 257x26 bits. 
The PLA encodes logic, not just bits - the way to interpret this image is as pairs of two pixels, vertically, that 
encode the following logic.

|     |     | Meaning    |
| --- | --- | ---------- |
| 0   | 0   | Don't Care |
| 1   | 0   | Match 1    |
| 0   | 1   | Match 0    |
| 1   | 1   | Impossible |

Lines 

The extracted bits from the activation PLA are also encoded as two image files, as specfied below.

![activation_pla_bits](./images/activation_pla_01.png)

#### /images/activation_pla_01.png
#### /images/activation_pla_01.pbm


### /scripts/bit_classifier.py 

A python script that uses the PyTorch framework to either train or run a convolutional neural network (CNN) to classify
input images as either 1's or 0's. The CNN trained by this script was used to extract the bits from the die photos.

The versions of pytorch used with this script were:
| package     | version      |
| ----------- | ------------ |
| Python      | 3.10.5       |
| torch       | 2.8.0+cu126  |
| torchvision | 0.23.0+cu126 |

### /models/microcode/model.pt

The trained PyTorch model used to extract the microcode bits. It was trained on an input size of 42x42.

### /models/activation_pla/model.pt

The trained PyTorch model used to extract the activation PLA bits. It was trained on an input size of 64x64.

### /scripts/extract_bits.py

This script takes the JSON file output by MaskRomTool and extracts square PNG files representing the area around each
indicated bit position, and will save the resulting images into a ZIP file to avoid thrashing your filesystem.

The resulting ZIP can be fed to the model via bit_classifier.py to reproduce the classification process, if you wish.

## Additional PLAS

Zoomed in views of the indicated PLAs:

![pla_locations](./images/pla_locations.jpg)

### /images/pla_1.jpg
### /images/pla_2.jpg
### /images/pla_3.jpg
### /images/pla_4.jpg
### /images/pla_5.jpg


### /v20_pla2.txt

PLA2 is the V20's conditional match decoder. It has 12 inputs and 26 outputs. It takes the CPU flags
and opcode bits as inputs and produces a condition code. This PLA implements the `OPC` jump condition 
code, as referenced in jump conditions below.

All inputs are inverted.

| m   | OF  | CF  | ZF  | SF  | PF  | 80  | 86   | Mnemonic |
| --- | --- | --- | --- | --- | --- | --- | ---- | -------- |
| 0   | 0   | ?   | ?   | ?   | ?   |     | 1111 | JO       |
| 0   | 1   | ?   | ?   | ?   | ?   |     | 1110 | JNO      |
| 0   | ?   | 0   | ?   | ?   | ?   |     | 1?01 | JB/JBE   |
| 0   | ?   | 1   | ?   | ?   | ?   |     | 1100 | JAE      |
| 0   | ?   | ?   | 0   | ?   | ?   |     | 10?1 | JZ/JBE   |
| 0   | ?   | ?   | 1   | ?   | ?   |     | 1010 | JNZ      |
| 0   | ?   | 1   | 1   | ?   | ?   |     | 1000 | JA       |
| 0   | ?   | ?   | ?   | 0   | ?   |     | 0111 | JS       |
| 0   | ?   | ?   | ?   | 1   | ?   |     | 0110 | JNS      |
| 0   | ?   | ?   | ?   | ?   | 0   |     | 0101 | JP       |
| 0   | ?   | ?   | ?   | ?   | 1   |     | 0100 | JNP      |
| 0   | 1   | ?   | ?   | 0   | ?   |     | 00?1 | JL/JLE   |
| 0   | 0   | ?   | ?   | 1   | ?   |     | 00?1 | JL/JLE   |
| 0   | ?   | ?   | 0   | ?   | ?   |     | 0001 | JLE      |
| 0   | 1   | ?   | ?   | 1   | ?   |     | 0010 | JGE      |
| 0   | 0   | ?   | ?   | 0   | ?   |     | 0010 | JGE      |
| 0   | 1   | ?   | 1   | 1   | ?   |     | 0000 | JG       |
| 0   | 0   | ?   | 1   | 0   | ?   |     | 0000 | JG       |
| 1   | ?   | ?   | 1   | ?   | ?   | 111 |      | JNZ      |
| 1   | ?   | ?   | 0   | ?   | ?   | 110 |      | JZ       |
| 1   | ?   | 1   | ?   | ?   | ?   | 101 |      | JNC      |
| 1   | ?   | 0   | ?   | ?   | ?   | 100 |      | JC       |
| 1   | ?   | ?   | ?   | ?   | 1   | 011 |      | JPO      |
| 1   | ?   | ?   | ?   | ?   | 0   | 010 |      | JPE      |
| 1   | ?   | ?   | ?   | 1   | ?   | 001 |      | JP       |
| 1   | ?   | ?   | ?   | 0   | ?   | 000 |      | JM       |

| Input bits | Function                              |
| ---------- | ------------------------------------- |
| 11         | Inverted Mode flag                    |
| 10         | Inverted OF                           |
| 9          | Inverted CF                           |
| 8          | Inverted ZF                           |
| 7          | Inverted SF                           |
| 6          | Inverted PF                           |
| 5:3        | Inverted 8080 condition-code bits     |
| 3:0        | Inverted 8086 Jcc condition-code bits |

### /v20_pla3.txt

The decoded PLA3 which is the V20's equivalent of the 8088's "Group Decode ROM".

It has 10 inputs and 14 outputs.

The first two input bits are a sort of opcode class field:

| Value | Input bits | Meaning                     |
| ----- | ---------- | --------------------------- |
| `0`   | `00`       | 8080 emulation instructions |
| `1`   | `01`       | Native instructions         |
| `2`   | `10`       | Unrepresented               |
| `3`   | `11`       | NEC extended instructions   |

The last 8 inputs are the instruction opcode.

### Output signals

| Output | Meaning                                                                   |
| ------ | ------------------------------------------------------------------------- |
| 0      | Force byte operand                                                        |
| 1      | W bit is valid                                                            |
| 2      | Miscellaneous logic: one-byte non-microcoded instruction or prefix        |
| 3      | AX or AL register operand                                                 |
| 4      | Segment register operand                                                  |
| 5      | Has modrm - this appears to only be valid for the 8088/80186 instructions |
| 6      | Doesn't read EA operand                                                   |
| 7      | D bit is valid                                                            |
| 8      | Opcode high bit: set for all opcodes > 7F                                 |
| 9      | Upper bit for XI calculation                                              |
| 10     | M1 if bit 2,                                                              |
| 11     | M2 if bit 2,                                                              |
| 12     | M3 if bit 2,                                                              |
| 13     | M4 if bit 2,                                                              |

When output 2 is active, the final four output bits select an operation implemented in miscellaneous logic (non-microcoded).

### Miscellaneous-logic selector

| Value | Bits 11:14 | Operation        | Meaning                                                       | 8080 | Native                 | Status    |
| ----- | ---------- | ---------------- | ------------------------------------------------------------- | ---- | ---------------------- | --------- |
| `0`   | `0000`     | Segment override | Select the segment used by the following instruction.         | —    | `26`, `2E`, `36`, `3E` | Known     |
| `1`   | `0001`     | 0F               | Extended-opcode prefix: 0F in native mode, ED in 8080 mode.   | `ED` | `0F`                   | Known     |
| `2`   | `0010`     | STD              | Set the direction flag.                                       | —    | `FD`                   | Known     |
| `3`   | `0011`     | CLD              | Clear the direction flag.                                     | —    | `FC`                   | Known     |
| `4`   | `0100`     | STI / EI         | Enable interrupts.                                            | `FB` | `FB`                   | Known     |
| `5`   | `0101`     | CLI / DI         | Disable interrupts.                                           | `F3` | `FA`                   | Known     |
| `6`   | `0110`     | STC              | Set the carry flag.                                           | `37` | `F9`                   | Known     |
| `7`   | `0111`     | CLC              | Clear the carry flag.                                         | —    | `F8`                   | Known     |
| `8`   | `1000`     | REPC             | Repeat prefix conditioned on carry set.                       | —    | `65`                   | Known     |
| `9`   | `1001`     | REPNC            | Repeat prefix conditioned on carry clear.                     | —    | `64`                   | Known     |
| `A`   | `1010`     | CMC              | Complement the carry flag.                                    | `3F` | `F5`                   | Known     |
| `B`   | `1011`     | HLT              | Halt instruction execution.                                   | `76` | `F4`                   | Known     |
| `C`   | `1100`     | REPZ             | Repeat prefix; zero-set condition where applicable.           | —    | `F3`                   | Known     |
| `D`   | `1101`     | REPNZ            | Repeat prefix; zero-clear condition where applicable.         | —    | `F2`                   | Known     |
| `E`   | `1110`     | F1 LOCK ALIAS(?) | Possible F1 alias of the LOCK prefix; tentative.              | —    | `F1`                   | Tentative |
| `F`   | `1111`     | LOCK             | Request a locked bus operation for the following instruction. | —    | `F0`                   | Known     |

### Microcode Disassemblies

#### v20_disassembly.txt 

Microcode disassembly for the logical V20 metal layer column-selection.

#### v30_disassembly.txt

Microcode disassembly for the logical V30 metal layer column-selection.

## Microcode Fields

### Source1

Bits **1:5**, complemented. Selects the source of Assignment1. `17` selects the five-bit immediate form instead of a register source.

| Value | Raw bits | Name     | Meaning                                                                | Uses | Status  |
| ----- | -------- | -------- | ---------------------------------------------------------------------- | ---- | ------- |
| `00`  | `11111`  | `ES`     | Extra segment register.                                                | 0    | Known   |
| `01`  | `11110`  | `CS`     | Code segment register.                                                 | 3    | Known   |
| `02`  | `11101`  | `SS`     | Stack segment register.                                                | 0    | Known   |
| `03`  | `11100`  | `DS`     | Data segment register.                                                 | 0    | Known   |
| `04`  | `11011`  | `PC`     | Instruction pointer.                                                   | 25   | Known   |
| `05`  | `11010`  | `Unused` | Not used.                                                              | 0    | Unused  |
| `06`  | `11001`  | `OPR`    | Memory operand latch.                                                  | 66   | Known   |
| `07`  | `11000`  | `Q`      | Instruction prefetch queue data.                                       | 71   | Known   |
| `08`  | `10111`  | `DIRSZ`  | Address step selected by direction and operand size.                   | 13   | Known   |
| `09`  | `10110`  | `ZERO`   | Constant zero.                                                         | 21   | Known   |
| `0A`  | `10101`  | `PFXCNT` | Instruction prefix count.                                              | 1    | Known   |
| `0B`  | `10100`  | `Unused` | Not used.                                                              | 0    | Unused  |
| `0C`  | `10011`  | `tmpA`   | Internal temporary A.                                                  | 49   | Known   |
| `0D`  | `10010`  | `tmpB`   | Internal temporary B.                                                  | 32   | Known   |
| `0E`  | `10001`  | `tmpC`   | Internal temporary C.                                                  | 10   | Known   |
| `0F`  | `10000`  | `FLAGS`  | Flags register.                                                        | 8    | Known   |
| `10`  | `01111`  | `AL:AH`  | Accumulator with its bytes exchanged: AL in bits 15:8, AH in bits 7:0. | 13   | Known   |
| `11`  | `01110`  | `LC`     | Internal loop counter.                                                 | 11   | Known   |
| `12`  | `01101`  | `OP2`    | Decoded instruction operand 2.                                         | 15   | Known   |
| `13`  | `01100`  | `OP1`    | Decoded instruction operand 1.                                         | 48   | Known   |
| `14`  | `01011`  | `SIGMA`  | ALU result.                                                            | 212  | Known   |
| `15`  | `01010`  | `K`      | Internal constant/mask bus: contents vary by operation                 | 18   | Partial |
| `16`  | `01001`  | `OPC38`  | Opcode bits selected by mask 0x38.                                     | 1    | Known   |
| `17`  | `01000`  | `CONST`  | Five-bit immediate; replaces the second transfer.                      | 25   | Known   |
| `18`  | `00111`  | `A`      | Accumulator register.                                                  | 20   | Known   |
| `19`  | `00110`  | `C`      | Count register.                                                        | 14   | Known   |
| `1A`  | `00101`  | `D`      | Data register.                                                         | 10   | Known   |
| `1B`  | `00100`  | `B`      | Base register.                                                         | 10   | Known   |
| `1C`  | `00011`  | `SP`     | Stack pointer.                                                         | 23   | Known   |
| `1D`  | `00010`  | `BP`     | Base pointer.                                                          | 15   | Known   |
| `1E`  | `00001`  | `SI`     | Source index.                                                          | 12   | Known   |
| `1F`  | `00000`  | `DI`     | Destination index.                                                     | 20   | Known   |

### Destination1

Bits **6:10**, complemented. Selects the destination of Assignment1.

| Value | Raw bits | Name     | Meaning                                                       | Uses | Status |
| ----- | -------- | -------- | ------------------------------------------------------------- | ---- | ------ |
| `00`  | `11111`  | `ES`     | Extra segment register.                                       | 2    | Known  |
| `01`  | `11110`  | `CS`     | Code segment register.                                        | 7    | Known  |
| `02`  | `11101`  | `SS`     | Stack segment register.                                       | 1    | Known  |
| `03`  | `11100`  | `DS`     | Data segment register.                                        | 2    | Known  |
| `04`  | `11011`  | `PC`     | Instruction pointer.                                          | 26   | Known  |
| `05`  | `11010`  | `DP`     | Data pointer / address latch.                                 | 77   | Known  |
| `06`  | `11001`  | `OPR`    | Memory operand latch.                                         | 47   | Known  |
| `07`  | `11000`  | `NULL`   | Discard the transfer result.                                  | 39   | Known  |
| `08`  | `10111`  | `AL`     | Low accumulator byte.                                         | 16   | Known  |
| `09`  | `10110`  | `Unused` | Not used.                                                     | 0    | Unused |
| `0A`  | `10101`  | `Unused` | Not used.                                                     | 0    | Unused |
| `0B`  | `10100`  | `Unused` | Not used.                                                     | 0    | Unused |
| `0C`  | `10011`  | `tmpA`   | Internal temporary A.                                         | 64   | Known  |
| `0D`  | `10010`  | `tmpB`   | Internal temporary B.                                         | 132  | Known  |
| `0E`  | `10001`  | `tmpC`   | Internal temporary C.                                         | 40   | Known  |
| `0F`  | `10000`  | `FLAGS`  | Flags register.                                               | 7    | Known  |
| `10`  | `01111`  | `AH`     | High accumulator byte.                                        | 8    | Known  |
| `11`  | `01110`  | `LC`     | Internal loop counter.                                        | 38   | Known  |
| `12`  | `01101`  | `OP2`    | Decoded instruction operand 2.                                | 15   | Known  |
| `13`  | `01100`  | `OP1`    | Decoded instruction operand 1.                                | 31   | Known  |
| `14`  | `01011`  | `tmpAL`  | Write the low byte of temporary A and zero-extend to 16 bits. | 40   | Known  |
| `15`  | `01010`  | `tmpBL`  | Write the low byte of temporary B and sign-extend to 16 bits. | 33   | Known  |
| `16`  | `01001`  | `tmpAH`  | Write bits 15:8 of temporary A, preserving bits 7:0.          | 20   | Known  |
| `17`  | `01000`  | `tmpBH`  | Write bits 15:8 of temporary B, preserving bits 7:0.          | 16   | Known  |
| `18`  | `00111`  | `A`      | Accumulator register.                                         | 16   | Known  |
| `19`  | `00110`  | `C`      | Count register.                                               | 10   | Known  |
| `1A`  | `00101`  | `D`      | Data register.                                                | 8    | Known  |
| `1B`  | `00100`  | `B`      | Base register.                                                | 5    | Known  |
| `1C`  | `00011`  | `SP`     | Stack pointer.                                                | 25   | Known  |
| `1D`  | `00010`  | `BP`     | Base pointer.                                                 | 16   | Known  |
| `1E`  | `00001`  | `SI`     | Source index.                                                 | 12   | Known  |
| `1F`  | `00000`  | `DI`     | Destination index.                                            | 13   | Known  |

For tmpAL/tmpBL, the incoming low byte is either zero-extended or sign-extended, respectively. 
For tmpAH/tmpBH, incoming bits 15:8 replace the high byte and the old low byte is retained. 
Queue bytes are explicitly routed into the high byte for these destinations.

## Source2

Bits **11:14**, complemented. Selects the source of Assignment2. The entire assignment is inactive with CONST-type words.

| Value | Raw bits | Name     | Meaning                             | Uses | Status |
| ----- | -------- | -------- | ----------------------------------- | ---- | ------ |
| `00`  | `1111`   | `ONES`   | Constant with all sixteen bits set. | 1    | Known  |
| `01`  | `1110`   | `Unused` | Not used.                           | 0    | Unused |
| `02`  | `1101`   | `Unused` | Not used.                           | 0    | Unused |
| `03`  | `1100`   | `Unused` | Not used.                           | 0    | Unused |
| `04`  | `1011`   | `SIGMA`  | ALU result.                         | 94   | Known  |
| `05`  | `1010`   | `Q`      | Instruction prefetch queue data.    | 8    | Known  |
| `06`  | `1001`   | `ZERO`   | Constant zero.                      | 4    | Known  |
| `07`  | `1000`   | `OP2`    | Decoded instruction operand 2.      | 4    | Known  |
| `08`  | `0111`   | `A`      | Accumulator register.               | 11   | Known  |
| `09`  | `0110`   | `C`      | Count register.                     | 12   | Known  |
| `0A`  | `0101`   | `D`      | Data register.                      | 0    | Known  |
| `0B`  | `0100`   | `B`      | Base register.                      | 3    | Known  |
| `0C`  | `0011`   | `SP`     | Stack pointer.                      | 14   | Known  |
| `0D`  | `0010`   | `BP`     | Base pointer.                       | 8    | Known  |
| `0E`  | `0001`   | `SI`     | Source index.                       | 10   | Known  |
| `0F`  | `0000`   | `DI`     | Destination index.                  | 10   | Known  |

## Destination2

Bits **15:16**, complemented. Selects the destination of Assignment2.

| Value | Raw bits | Name   | Meaning                      | Uses | Status |
| ----- | -------- | ------ | ---------------------------- | ---- | ------ |
| `00`  | `11`     | `tmpA` | Internal temporary A.        | 39   | Known  |
| `01`  | `10`     | `tmpB` | Internal temporary B.        | 74   | Known  |
| `02`  | `01`     | `IND`  | Memory address/index latch.  | 45   | Known  |
| `03`  | `00`     | `NULL` | Discard the transfer result. | 21   | Known  |

## F, W, E

F/W/E are present in every word

| Field | Bit | Raw bit | Meaning                                                                      | Uses |
| ----- | --- | ------- | ---------------------------------------------------------------------------- | ---- |
| F     | 17  | 1       | FETCH: Latch the completed bus operand before transfers proceed              | 81   |
| W     | 18  | 1       | Commit ALU flag results to FLAGS; applies during repeated ALU execution too. | 47   |
| E     | 19  | 1       | Request instruction completion; similar to 8088's RNI                        | 146  |

## Constant

Bits **17:13**, complemented, active only when Source1 is `17` (CONST).
The decoded value is a five-bit unsigned source value; destination byte routing
and extension still apply normally. There is no Assignment2 in this format.

| Value | Decimal | Stored bits | Uses |
| ----- | ------- | ----------- | ---- |
| `00`  | 0       | `11111`     | 0    |
| `01`  | 1       | `11110`     | 5    |
| `02`  | 2       | `11101`     | 2    |
| `03`  | 3       | `11100`     | 1    |
| `04`  | 4       | `11011`     | 2    |
| `05`  | 5       | `11010`     | 1    |
| `06`  | 6       | `11001`     | 0    |
| `07`  | 7       | `11000`     | 0    |
| `08`  | 8       | `10111`     | 6    |
| `09`  | 9       | `10110`     | 0    |
| `0A`  | 10      | `10101`     | 0    |
| `0B`  | 11      | `10100`     | 0    |
| `0C`  | 12      | `10011`     | 0    |
| `0D`  | 13      | `10010`     | 0    |
| `0E`  | 14      | `10001`     | 0    |
| `0F`  | 15      | `10000`     | 3    |
| `10`  | 16      | `01111`     | 5    |
| `11`  | 17      | `01110`     | 0    |
| `12`  | 18      | `01101`     | 0    |
| `13`  | 19      | `01100`     | 0    |
| `14`  | 20      | `01011`     | 0    |
| `15`  | 21      | `01010`     | 0    |
| `16`  | 22      | `01001`     | 0    |
| `17`  | 23      | `01000`     | 0    |
| `18`  | 24      | `00111`     | 0    |
| `19`  | 25      | `00110`     | 0    |
| `1A`  | 26      | `00101`     | 0    |
| `1B`  | 27      | `00100`     | 0    |
| `1C`  | 28      | `00011`     | 0    |
| `1D`  | 29      | `00010`     | 0    |
| `1E`  | 30      | `00001`     | 0    |
| `1F`  | 31      | `00000`     | 0    |

Bit 11 is outside the immediate field and is always 1.

## ALUop

Bits **22:26**, complemented, in ALU-type format. Selects the ALU operation used by the datapath; executing `SIGMA` evaluates its result.

| Value | Raw bits | Name     | Meaning                                                          | Uses | Status |
| ----- | -------- | -------- | ---------------------------------------------------------------- | ---- | ------ |
| `00`  | `11111`  | `ADD`    | Addition.                                                        | 36   | Known  |
| `01`  | `11110`  | `OR`     | Bitwise OR.                                                      | 2    | Known  |
| `02`  | `11101`  | `ADC`    | Addition with carry.                                             | 2    | Known  |
| `03`  | `11100`  | `SBB`    | Subtraction with borrow.                                         | 2    | Known  |
| `04`  | `11011`  | `AND`    | Bitwise AND.                                                     | 9    | Known  |
| `05`  | `11010`  | `SUB`    | Subtraction.                                                     | 21   | Known  |
| `06`  | `11001`  | `XOR`    | Bitwise exclusive OR.                                            | 2    | Known  |
| `07`  | `11000`  | `CMP`    | Subtraction for comparison.                                      | 0    | Known  |
| `08`  | `10111`  | `ROL`    | Rotate left.                                                     | 0    | Known  |
| `09`  | `10110`  | `ROR`    | Rotate right.                                                    | 0    | Known  |
| `0A`  | `10101`  | `RCL`    | Rotate left through carry.                                       | 0    | Known  |
| `0B`  | `10100`  | `RCR`    | Rotate right through carry.                                      | 0    | Known  |
| `0C`  | `10011`  | `SHL`    | Logical shift left.                                              | 0    | Known  |
| `0D`  | `10010`  | `SHR`    | Logical shift right.                                             | 3    | Known  |
| `0E`  | `10001`  | `Unused` | Not used.                                                        | 0    | Unused |
| `0F`  | `10000`  | `SAR`    | Arithmetic shift right.                                          | 0    | Known  |
| `10`  | `01111`  | `ROL12`  | Rotate-left operation used by digit rotates.                     | 2    | Known  |
| `11`  | `01110`  | `Unused` | Not used.                                                        | 0    | Unused |
| `12`  | `01101`  | `DIV`    | Division step with a left shift of temporary B:A*                | 7    | Known  |
| `13`  | `01100`  | `MUL`    | Multiplication step.*                                            | 8    | Known  |
| `14`  | `01011`  | `ADJD`   | Decimal-adjust operation.                                        | 6    | Known  |
| `15`  | `01010`  | `ADJA`   | ASCII-adjust control.*                                           | 3    | Known  |
| `16`  | `01001`  | `XI`     | Instruction-selected ALU operation.                              | 12   | Known  |
| `17`  | `01000`  | `BITM`   | Bit-mask generation.                                             | 8    | Known  |
| `18`  | `00111`  | `INC`    | Increment by one.                                                | 10   | Known  |
| `19`  | `00110`  | `DEC`    | Decrement by one.                                                | 8    | Known  |
| `1A`  | `00101`  | `NOT`    | Bitwise complement.                                              | 5    | Known  |
| `1B`  | `00100`  | `NEG`    | Arithmetic negation.                                             | 6    | Known  |
| `1C`  | `00011`  | `INC2`   | Increment by two.                                                | 22   | Known  |
| `1D`  | `00010`  | `DEC2`   | Decrement by two.                                                | 20   | Known  |
| `1E`  | `00001`  | `MULDIV` | Take the selected temporary's absolute value and save its sign.* | 3    | Known  |
| `1F`  | `00000`  | `PASS`   | Pass the selected operand through the ALU.                       | 48   | Known  |

 - **12**: An unrepeated final step corrects the remainder and quotient. This operation is also used for bit-field shifts.
 - **13**: Conditionally accepts the partial sum, then shifts temporary B:A right. A zero multiplicand gives a two-register shift.
 - **15**: Supplies an adjustment mask through K; evaluating SIGMA also masks the selected temporary to its low nibble.
 - **1E**: Used for signed multiply/divide correction. Undetermined how the sign is actually stored.

## Tmp

Bits **27:28**, complemented, in ALU format. Selects the temporary used by the ALU operation.

| Value | Raw bits | Name     | Meaning               | Uses | Status |
| ----- | -------- | -------- | --------------------- | ---- | ------ |
| `00`  | `11`     | `tmpA`   | Internal temporary A. | 94   | Known  |
| `01`  | `10`     | `tmpB`   | Internal temporary B. | 103  | Known  |
| `02`  | `01`     | `tmpC`   | Internal temporary C. | 48   | Known  |
| `03`  | `00`     | `Unused` | Not used.             | 0    | Unused |

## Jcond

Bits **22:25**, complemented, in Jump format. If the condition is true, replace the four-bit sequence index with JmpT.

| Value | Raw bits | Name        | Meaning                                                                                    | Uses | Status  |
| ----- | -------- | ----------- | ------------------------------------------------------------------------------------------ | ---- | ------- |
| `00`  | `1111`   | `JC`        | Carry-set condition from FLAGS.                                                            | 2    | Known   |
| `01`  | `1110`   | `JNC`       | ALU carry clear condition.                                                                 | 7    | Known   |
| `02`  | `1101`   | `JZ`        | ALU zero condition.                                                                        | 16   | Known   |
| `03`  | `1100`   | `JNZ`       | ALU nonzero condition.                                                                     | 2    | Known   |
| `04`  | `1011`   | `JNWO`      | Jump if not word operand.*                                                                 | 1    | Known   |
| `05`  | `1010`   | `JLCNZ`     | Decrement LC and branch if the result is nonzero.                                          | 3    | Known   |
| `06`  | `1001`   | `JL`        | Signed-less ALU result (SF XOR OF)                                                         | 3    | Known   |
| `07`  | `1000`   | `JNW`       | Byte operand or sign-extended byte immediate; skips the second immediate byte.             | 14   | Known   |
| `08`  | `0111`   | `UNC`       | Unconditional transfer.                                                                    | 4    | Known   |
| `09`  | `0110`   | `JPOS/NZ4S` | Overloaded(?): nonnegative signed product/quotient, or a nonzero packed-BCD string result. | 3    | Partial |
| `0A`  | `0101`   | `JO`        | Overflow condition.                                                                        | 1    | Known   |
| `0B`  | `0100`   | `JNS`       | Temporary B's sign is clear, according to operand size.                                    | 3    | Known   |
| `0C`  | `0011`   | `REP`       | Decrement LC and test for another iteration.*                                              | 8    | Partial |
| `0D`  | `0010`   | `BUSY`      | Condition polling the BUSY input.                                                          | 1    | Known   |
| `0E`  | `0001`   | `INT`       | Condition polling the INTR input.                                                          | 2    | Known   |
| `0F`  | `0000`   | `OPC`       | Opcode-dependent condition from PLA2                                                       | 4    | Known   |

- **04**: Unlike `JNW`, a sign-extended byte immediate does not select this branch when the operand is a word.
- **06**: Value is independent of any simultaneous FLAGS transfer.
- **0C**: CMPS/SCAS also test ZF or CF according to the repeat prefix; LOOPZ/LOOPNZ test ZF.

## JmpT

Bits **26:29**, complemented, in Jump format. All 16 targets are local offsets.

```text
target = (microaddress & 0x7FF0) | JmpT
```

| Value | Sequence index (decimal) | Raw bits | Uses |
| ----- | ------------------------ | -------- | ---- |
| `0`   | 0                        | `1111`   | 1    |
| `1`   | 1                        | `1110`   | 1    |
| `2`   | 2                        | `1101`   | 9    |
| `3`   | 3                        | `1100`   | 15   |
| `4`   | 4                        | `1011`   | 6    |
| `5`   | 5                        | `1010`   | 12   |
| `6`   | 6                        | `1001`   | 4    |
| `7`   | 7                        | `1000`   | 5    |
| `8`   | 8                        | `0111`   | 2    |
| `9`   | 9                        | `0110`   | 1    |
| `A`   | 10                       | `0101`   | 1    |
| `B`   | 11                       | `0100`   | 5    |
| `C`   | 12                       | `0011`   | 3    |
| `D`   | 13                       | `0010`   | 1    |
| `E`   | 14                       | `0001`   | 6    |
| `F`   | 15                       | `0000`   | 2    |

## IC: internal control

Bits **21:24**, complemented, in Control format. IC includes bit 21, which overlaps the low `Type` bit. IC `0E` changes bits **25:29** into a **CallT** target.

| Value | Raw bits | Name           | Meaning                                                                      | Uses | Status    |
| ----- | -------- | -------------- | ---------------------------------------------------------------------------- | ---- | --------- |
| `00`  | `1111`   | `Unidentified` | Unidentified control at listing line 3FD, in RETEM.*                         | 1    | Unknown   |
| `01`  | `1110`   | `CIFTF`        | Interrupt-entry control: clears the interrupt-enable and trap flags.         | 1    | Tentative |
| `02`  | `1101`   | `SETEM`        | Emulation-mode entry control.                                                | 1    | Known     |
| `03`  | `1100`   | `MFS`          | Set the native-mode flag.                                                    | 3    | Known     |
| `04`  | `1011`   | `BCD_INIT`     | Clear carry and initialize the cumulative-zero state for packed-BCD strings. | 1    | Known     |
| `05`  | `1010`   | `Unused`       | Not used.                                                                    | 0    | Unused    |
| `06`  | `1001`   | `CCOF`         | Clear carry and overflow.                                                    | 1    | Known     |
| `07`  | `1000`   | `SCOF`         | Set carry and overflow.                                                      | 2    | Known     |
| `08`  | `0111`   | `SUSP`         | Instruction prefetch suspension control.                                     | 27   | Known     |
| `09`  | `0110`   | `FLUSH`        | Flush the instruction prefetch queue.                                        | 26   | Known     |
| `0A`  | `0101`   | `WAIT`         | WAIT processing.*                                                            | 1    | Tentative |
| `0B`  | `0100`   | `Unused`       | Not used.                                                                    | 0    | Unused    |
| `0C`  | `0011`   | `SIGN`         | Capture the XOR of the signs of the saved operand and tmpB.*                 | 2    | Known     |
| `0D`  | `0010`   | `BCD_ZERO`     | Accumulate whether all packed-BCD results so far are zero.                   | 1    | Known     |
| `0E`  | `0001`   | `CALL`         | Transfer to the five-bit CallT target.                                       | 40   | Known     |
| `0F`  | `0000`   | `--`           | No internal-control action.                                                  | 598  | Known     |

- *00*: Likely some internal detail related to emulation mode processing. There is no equivalent in `BRKEM`.
- *0A*: `WAIT` Likely defers interrupt recognition until after the following instruction; affected interrupt sources and exact behavior remain unverified.
- *0C*: Used for signed multiply/divide correction.

## EC: external control

Bits **25:27**, complemented, in non-`CALL` Control format. These bits are part of `CallT` when `IC` is `0E`.

| Value | Raw bits | Name     | Meaning                                                                            | Uses | Status  |
| ----- | -------- | -------- | ---------------------------------------------------------------------------------- | ---- | ------- |
| `00`  | `111`    | `Unused` | Not used.                                                                          | 0    | Unused  |
| `01`  | `110`    | `MR`     | Memory read request.                                                               | 62   | Known   |
| `02`  | `101`    | `MW`     | Memory write request.                                                              | 51   | Known   |
| `03`  | `100`    | `INTV`   | Select segment-zero memory reads for interrupt vectors.                            | 1    | Partial |
| `04`  | `011`    | `Unused` | Not used.                                                                          | 0    | Unused  |
| `05`  | `010`    | `INTA`   | Word-sized interrupt-acknowledge request..                                         | 1    | Known   |
| `06`  | `001`    | `COMMIT` | Request memory-operand writeback when the instruction writes a memory destination. | 23   | Known   |
| `07`  | `000`    | `--`     | No external-control action.                                                        | 527  | Known   |

- *05*: The V20 splits one request into two byte bus cycles and takes the vector from the high byte. V30 issues two requests and takes the second response.

## SR: segment/access selection

Bits **28:29**, complemented, in non-CALL Control format. SR selects the segment or unsegmented path; EC still determines the bus operation.

| Value | Raw bits | Name   | Meaning                                                                           | Uses | Status |
| ----- | -------- | ------ | --------------------------------------------------------------------------------- | ---- | ------ |
| `00`  | `11`     | `ES`   | Select the extra segment.                                                         | 16   | Known  |
| `01`  | `10`     | `None` | Unsegmented access: I/O, or interrupt-vector memory when INTV is selected.        | 14   | Known  |
| `02`  | `01`     | `SS`   | Select the stack segment.                                                         | 47   | Known  |
| `03`  | `00`     | `--`   | Default data segment, including effective-address and segment-override selection. | 588  | Known  |

## CallT: far microcode target

Bits **25:29**, complemented, when IC is `0E` (CALL). EC and SR are inactive overlapping views in this format. 
The name `CALL` denotes a far microcode transfer.

| Value | Raw bits | Name    | Microaddress | ROM line | Meaning                                              | Uses | Status |
| ----- | -------- | ------- | ------------ | -------- | ---------------------------------------------------- | ---- | ------ |
| `00`  | `11111`  | Unused  | `7000`       | `1D8`    | Not used.                                            | 0    | Unused |
| `01`  | `11110`  | IRET    | `7080`       | `1E4`    | Interrupt-return routine.                            | 2    | Known  |
| `02`  | `11101`  | INT     | `7100`       | `1EC`    | Native interrupt-entry routine.                      | 9    | Known  |
| `03`  | `11100`  | EM_INT  | `7180`       | `1EC`    | Emulation/native transition interrupt-entry routine. | 2    | Known  |
| `04`  | `11011`  | MUL     | `7200`       | `204`    | Unsigned multiplication entry.                       | 3    | Known  |
| `05`  | `11010`  | MUL2    | `7280`       | `208`    | Unsigned multiplication continuation.                | 3    | Known  |
| `06`  | `11001`  | IMUL    | `7300`       | `20C`    | Signed multiplication entry.                         | 1    | Known  |
| `07`  | `11000`  | IMUL2   | `7380`       | `20C`    | Signed multiplication alternate entry/continuation.  | 1    | Known  |
| `08`  | `10111`  | REP     | `7400`       | `220`    | Repeated-instruction helper.                         | 7    | Known  |
| `09`  | `10110`  | ROT     | `7480`       | `228`    | Shift/rotate helper.                                 | 2    | Known  |
| `0A`  | `10101`  | ENTER   | `7500`       | `264`    | Stack-frame construction routine.                    | 1    | Known  |
| `0B`  | `10100`  | PUSHA   | `7580`       | `23C`    | Push general registers.                              | 1    | Known  |
| `0C`  | `10011`  | POPA    | `7600`       | `250`    | Pop general registers.                               | 1    | Known  |
| `0D`  | `10010`  | FARCALL | `7680`       | `22C`    | Far-call helper.                                     | 2    | Known  |
| `0E`  | `10001`  | EXT     | `7700`       | `328`    | Bit-field extraction helper.                         | 1    | Known  |
| `0F`  | `10000`  | IDIV    | `7780`       | `1A0`    | Signed division entry: normalize the dividend        | 1    | Known  |
| `10`  | `01111`  | FARRET  | `7800`       | `234`    | Far-return helper.                                   | 2    | Known  |
| `11`  | `01110`  | Unused  | `7880`       | Unmapped | Not used.                                            | 0    | Unused |
| `12`  | `01101`  | IDIV2   | `7900`       | `1A8`    | Signed division continuation.                        | 1    | Known  |
| `13`  | `01100`  | Unused  | `7980`       | Unmapped | Not used.                                            | 0    | Unused |
| `14`  | `01011`  | Unused  | `7A00`       | Unmapped | Not used.                                            | 0    | Unused |
| `15`  | `01010`  | Unused  | `7A80`       | Unmapped | Not used.                                            | 0    | Unused |
| `16`  | `01001`  | Unused  | `7B00`       | Unmapped | Not used.                                            | 0    | Unused |
| `17`  | `01000`  | Unused  | `7B80`       | Unmapped | Not used.                                            | 0    | Unused |
| `18`  | `00111`  | Unused  | `7C00`       | Unmapped | Not used.                                            | 0    | Unused |
| `19`  | `00110`  | Unused  | `7C80`       | Unmapped | Not used.                                            | 0    | Unused |
| `1A`  | `00101`  | Unused  | `7D00`       | Unmapped | Not used.                                            | 0    | Unused |
| `1B`  | `00100`  | Unused  | `7D80`       | Unmapped | Not used.                                            | 0    | Unused |
| `1C`  | `00011`  | Unused  | `7E00`       | Unmapped | Not used.                                            | 0    | Unused |
| `1D`  | `00010`  | Unused  | `7E80`       | Unmapped | Not used.                                            | 0    | Unused |
| `1E`  | `00001`  | Unused  | `7F00`       | Unmapped | Not used.                                            | 0    | Unused |
| `1F`  | `00000`  | Unused  | `7F80`       | Unmapped | Not used.                                            | 0    | Unused |