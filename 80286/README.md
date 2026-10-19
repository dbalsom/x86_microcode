# The Intel/Harris 80C286 Microcode

The 80286 microcode array contains 192x280 or 53,760 bits. This array defines 1,536 35-bit words with 8 microcode words per column.

## Previous Imaging Efforts

The Intel NMOS 80286 CPU was delayered and imaged, only to discover that the microcode array was implemented as an implant ROM and was unreadable.

That photography can be seen [here](http://infosecdj.net/map/intel/80286/infosecdj_nikpa20x/). You can select the polysilicon layer from the layer menu in the upper right; notice that no bits are visible.

In 2026, experiments with NIR photography on a CMOS 80C286 revealed that the microcode bits were theoretically readable.

<img src="cmos/images/286-rom-x21-NIR.png" alt="Intel/Harris 80C286 microcode ROM photographed in near-infrared" width="25%" />

*NIR photography of 80C286 performed by 0x31337*

Unfortunately the resolution was not sufficient for reliable bit extraction.

## New Imaging (2026)

New delayering and imaging was comissioned from [InfoSecDJ](https://siliconpr0n.org/archive/doku.php?id=infosecdj:start) on a Harris 80C286 CPU. 

## 80286 Word Format

| Field                        | Bits |
| ---------------------------- | ---: |
| Source selector              |    6 |
| Destination selector         |    6 |
| ALU source / branch offset   |    6 |
| ALU operation / branch cond. |    7 |
| Opcode                       |    3 |
| Subcode                      |    2 |
| Bus control                  |    5 |
| Total                        |   35 |

## NMOS PLA Analysis

### PLA01 - Microcode Match Decoder

#### nmos/PLA01_MatchDecoder.txt

The decoded two-stage match decoder logic of the NMOS Intel 80286

### nmos/PLA01_raw.txt

The raw extracted bits from the match decoder PLA.

### PLA02 - Decode Control PLA

#### nmos/PLA02_logic.txt

The match logic of the decode control PLA.

#### nmos/PLA02_raw.txt

The raw extracted bits from the decode control PLA.

#### nmos/PLA02_SM_01_logic.txt

The match logic of the smaller state machine AND array above PLA02 (to the right).

#### nmos/PLA02_SM_02_logic.txt

The match logic of the larger state machine AND array above PLA02 (to the left).

## NMOS Constant ROM

### nmos/CONSTANT_ROM_raw.txt

The raw extracted bits from the 80286's constant ROM.

### nmos/CONSTANT_ROM_decoded.txt

The decoded values from the constant ROM in unverified index-order.

### Shuffling

Like the 386 constant ROM's lower 16-bits, the 16-bit outputs of the 286 constant ROM are shuffled, 
but in a different pattern:

F,7,E,6,D,5,C,4,B,3,A,2,9,1,8,0

### Possible constant ROM uses

These are yet to be determined from microcode dissembly, but some plausible guesses:

| Constant | Possible use                                            | Present in 386 constant ROM      |
| -------- | ------------------------------------------------------- | -------------------------------- |
| 0000     | Zero/clear value/unused ROM entry                       | No                               |
| 0001     | Increment, shift count, bit-0 mask                      | Yes                              |
| 0002     | Word stride or decrement magnitude                      | Yes                              |
| 0004     | Descriptor offset or segment-address shift count        | Yes                              |
| 0005     | BOUND exception vector 5; small count                   | No                               |
| 0006     | Invalid-opcode vector 6; small count                    | Yes                              |
| 0007     | Coprocessor-unavailable vector 7; three-bit mask        | Yes                              |
| 0008     | Task-switched bit; double-fault vector; byte shift      | Yes                              |
| 000A     | Invalid-TSS vector 10; TSS SP2 offset                   | No                               |
| 000C     | Stack-fault vector 12; TSS SS2 offset                   | No                               |
| 000E     | TSS saved-IP offset                                     | No                               |
| 000F     | Low-nibble/MSW mask                                     | Yes                              |
| 0016     | TSS size in words (22), DX offset, or LOADALL TR offset | No                               |
| 0017     | Unknown;                                                | No                               |
| 0018     | TSS BX offset or LOADALL FLAGS offset                   | No                               |
| 001A     | TSS SP offset or LOADALL IP offset                      | No                               |
| 0028     | TSS DS offset or LOADALL SI offset                      | No                               |
| 002A     | TSS LDT offset or LOADALL BP offset                     | No                               |
| 00F8     | 286/287 command/status port                             | Same role: 800000F8              |
| 00FF     | Low-byte mask                                           | No                               |
| 0800     | LOADALL physical base; also OF mask                     | No                               |
| F000     | Reset CS value                                          | No; derived from 000F0000 on 386 |
| FDFF     | Clear descriptor TSS-busy bit                           | 16-bit equivalent of FFFFFDFF    |
| FF00     | High-byte mask                                          | No                               |
| FFF0     | Reset IP/MSW value; low-nibble-clear mask               | No                               |
| FFFC     | −4; clear selector RPL bits                             | 16-bit equivalent of FFFFFFFC    |
| FFFE     | −2; word decrement; clear bit 0                         | 16-bit equivalent of FFFFFFFE    |