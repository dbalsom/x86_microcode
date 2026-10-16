# x86_microcode

Microcode resources for various x86 CPUs.

## Microcode ROM size:

| Processor | Microcode word size |  Words | Total bits |
| --------- | ------------------: | -----: | ---------: |
| 8088/8086 |             21 bits |    512 |     10,752 |
| 80186     |             21 bits |    576 |     12,096 |
| V20/V30   |             29 bits | 1,032* |     29,928 |
| 80286     |             35 bits |  1,536 |     53,760 |
| 80386DX   |             37 bits |  2,560 |     94,720 |
| 80486DX   |             47 bits |  5,760 |    270,720 |

 * Active word count 1024, selected by metal mask.

## /8088

Microcode for the Intel 8088 and 8086 CPUs.

## /v20

Microcode for the NEC V20 and V30 CPUs.

## /8087

Microcode for the Intel 8087 FPU.

## /80286

Microcode for the Intel 80286 CPU.

## /80386

Microcode for the Intel 80386 CPU.
