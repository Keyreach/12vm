# 12vm architecture

## Memory

### Total address space

256 x 16 bytes

### Zero page/Memory-mapped registers

16 x 16 bytes (starting from 0x00)

### Memory-mapped IO area

32 x 16 bytes (from 0xE0)

## Instruction types

### IM instruction

<table>
<tr><td>15</td><td>14</td><td>13</td><td>12</td><td>11</td><td>10</td><td>9</td><td>8</td><td>7</td><td>6</td><td>5</td><td>4</td><td>3</td><td>2</td><td>1</td><td>0</td></tr>
<tr><td colspan='4'>0000 (unused)</td><td colspan='4'>OpCode</td><td colspan='8'>Address / Immediate</td></tr>
</table>


### ISR instruction

<table>
<tr><td>15</td><td>14</td><td>13</td><td>12</td><td>11</td><td>10</td><td>9</td><td>8</td><td>7</td><td>6</td><td>5</td><td>4</td><td>3</td><td>2</td><td>1</td><td>0</td></tr>
<tr><td colspan='4'>0000 (unused)</td><td colspan='4'>OpGroup</td><td colspan='4'>SubOpCode</td><td colspan='4'>Address</td></tr>
</table>


## Instruction set

### Memory access instructions

Mnemonic | Opcode | Type | Description
---------|--------|------|-------------
LOAD     | 0100   | IM   | Loads value from specified location to accumulator register
STOR     | 0101   | IM   | Stores value from accumulator register to specified location
LDI      | 0110   | IM   | Load value from location stored in specified address
STI      | 0111   | IM   | Stores value from accumulator register in address stored in specified location

### Flow control instructions

Mnemonic | Opcode | Type | Description
---------|--------|------|-------------
JMPZ     | 1000   | IM   | Jumps to address if accumulator is 0
JMPN     | 1001   | IM   | Jumps to address if accumulator is less than 0
JUMP     | 1010   | IM   | Jumps to address, stores IP at address 0x0F
JI       | 1011   | IM   | Jumps to address, stored in specified location

### ALU instructions

Mnemonic | Opcode    | Type | Description
---------|-----------|------|-------------
ADD      | 1100 0000 | ISR  | Adds value at ZP address to accumulator
SUB      | 1100 0001 | ISR  | Subtracts value at ZP address from accumuator
AND      | 1100 0010 | ISR  |
OR       | 1100 0011 | ISR  |
INC      | 1100 0100 | ISR  |
DEC      | 1100 0101 | ISR  |
INV      | 1100 0110 | ISR  |
XOR      | 1100 0111 | ISR  |
SWAP     | 1100 1111 | ISR  | Swaps accumulator and ZP address value

### Misc

Mnemonic | Opcode | Type | Description
---------|--------|------|-------------
SET      | 1101   | IM   | Set accumulator with immediate
INT      | 0000   | IM   | Call interrupt
