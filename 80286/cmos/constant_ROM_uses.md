| Constant | Confirmed use                                                                                                            | Count | Present in 386 constant ROM           |
| -------- | ------------------------------------------------------------------------------------------------------------------------ | ----: | ------------------------------------- |
| `0000`   | Unused, ZERO source makes it redundant                                                                                   |     0 | No                                    |
| `0001`   | REP count adjustments; increments when constructing exception vectors and error codes                                    |    12 | Yes                                   |
| `0002`   | Word-sized stack/address increments; doubled single-step vector; HLT address                                             |    32 | Yes                                   |
| `0004`   | Doubled NMI vector; LGDT/SGDT address stepping; coprocessor address/vector adjustments                                   |     5 | Yes                                   |
| `0005`   | Unused(??)                                                                                                               |     0 | No                                    |
| `0006`   | Byte-IDIV count seed; PUSHA index seed; IRET stack adjustment; doubled INT3 vector; bits 1–2 mask                        |     6 | Yes                                   |
| `0007`   | Byte MUL/DIV and AAM/AAD iteration-count seed; POPA index seed                                                           |     7 | Yes                                   |
| `0008`   | Doubled INTO vector; double-fault vector; coprocessor-error vector construction                                          |     4 | Yes                                   |
| `000A`   | Doubled BOUND vector; invalid-TSS vector; construction of segment-not-present vector; task-save count/index seed         |     6 | No                                    |
| `000C`   | Doubled invalid-opcode vector; stack-fault vector; construction of general-protection vector; task-load count/index seed |     7 | No                                    |
| `000E`   | Word-IDIV count seed; POPA stack offset; coprocessor exception-vector construction                                       |     5 | No                                    |
| `000F`   | Word MUL/DIV and immediate-IMUL iteration-count seed                                                                     |     6 | Yes                                   |
| `0016`   | Unused(??)                                                                                                               |     0 | No                                    |
| `0017`   | LOADALL descriptor-cache count/index seed                                                                                |     1 | No                                    |
| `0018`   | STOREALL descriptor-cache count/index seed                                                                               |     1 | No                                    |
| `001A`   | RESET count/index initialization; ICEBP, STOREALL and LOADALL register-area traversal seed                               |     4 | No                                    |
| `0028`   | TSS offset of the saved DS selector                                                                                      |     2 | No                                    |
| `002A`   | RESET initialization of X2; TSS offset of the LDTR selector                                                              |     3 | No                                    |
| `00F8`   | 287 FPU addressing                                                                                                       |     6 | Related: `800000F8`                   |
| `00FF`   | Extracts the eight-bit interrupt vector from INTA                                                                        |     1 | No                                    |
| `0800`   | LOADALL/STOREALL image base address                                                                                      |     2 | No                                    |
| `F000`   | RESET CS selector                                                                                                        |     1 | Related: `000F0000`                   |
| `FDFF`   | Clear the outgoing TSS descriptor’s busy bit                                                                             |     1 | 16-bit equivalent of `FFFFFDFF`       |
| `FF00`   | Retain descriptor access-rights bits for LAR                                                                             |     1 | No                                    |
| `FFF0`   | RESET IP; PUSHA stack allocation of 16 bytes                                                                             |     2 | No                                    |
| `FFFC`   | Protected-call stack adjustment of −4; clear selector RPL bits when constructing error codes                             |     5 | Yes; 16-bit equivalent of `FFFFFFFC`  |
| `FFFE`   | Stack decrements and backward address stepping by two bytes                                                              |    38 | Yes; 16-bit equivalent of `FFFFFFFE`  |
| `FFFF`   | Decrement CX in LOOP-family instructions*                                                                                |     2 | Yes; also `FFFFFFFF` for −1           |

*Note `FFFF` was not present in the N80286 constant ROM, indicating at least one microcode revision