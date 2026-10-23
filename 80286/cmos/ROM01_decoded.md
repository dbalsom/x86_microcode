| Row | Address | Entrypoint name  | Guessed purpose                        |
| --: | ------- | ---------------- | -------------------------------------- |
|   1 | `237`   | `INTR_ACK`       | External hardware interrupt            |
|   2 | `2DC`   | `NPX_OVERRUN`    | Coprocessor segment overrun (vector 9) |
|   3 | `24F`   | `NMI`            | NMI (vector 2)                         |
|   4 | `40F`   | `ICEBP`          | Hardware ICE breakpoint                |
|   5 | `245`   | `SINGLE_STEP`    | Single-step/trap (vector 1)            |
|   6 | `3E5`   | `IP_NEXT`        | ?                                      |
|   7 | `24A`   | `DIV_ERROR`      | Divide error (vector 0)                |
|   8 | `5C6`   | `GP_FAULT`       | General protection fault (vector 13)   |
|   9 | `5B9`   | `FAULT_DISPATCH` | Protection-fault dispatch(?)           |
|  10 | `5AB`   | `DOUBLE_FAULT`   | Double fault (vector 8)                |
|  11 | `5B4`   | `SHUTDOWN`       | Processor shutdown                     |