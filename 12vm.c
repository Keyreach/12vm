#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
/*
* opcode mapping
* 
* ..0 ..1 ..2 ..3
* INT -   -   -    +0
* LD  ST  LDI STI  +4
* JZR JNG JMP JI   +8
* ALU SET -   -    +C
*/
enum {
    OP_INT,
    OP_LD = 4,
    OP_ST,
    OP_LDI,
    OP_STI,
    OP_JZR,
    OP_JNG,
    OP_JMP,
    OP_JI,
    OP_ALU,
    OP_SET
};
/*
* alu subcode mapping
* 
* .C0 .C1 .C2 .C3
* ADD SUB AND OR   +0
* INC DEC INV XOR  +4
* -   -   -   -    +8
* PSH POP -   XCH  +C
*/
enum {
    ALU_ADD,
    ALU_SUB,
    ALU_AND,
    ALU_OR,
    ALU_INC,
    ALU_DEC,
    ALU_INV,
    ALU_XOR,
    ALU_PSH = 0xC,
    ALU_POP,
    ALU_XCH = 0xF
};
// designated registers
enum {
    REG_SP = 0xE, // stack pointer
    REG_RA = 0xF // return address
};
// i/o
enum {
    MMIO_DIGIT_OUT = 0xE0,
    MMIO_CHAR_OUT = 0xE1,
    MMIO_RND_IN = 0xE2
};

#define RESERVED_OFFSET 0x10
#define LOW_NIBBLE(x) (unsigned short)x & 0xF
#define LOW_BYTE(x) (unsigned short)x & 0xFF


static short vmem[0x100] = {
    0x000, 0x000, 0x000, 0x000,
    0x000, 0x000, 0x000, 0x000,
    0x000, 0x000, 0x000, 0x000,
    0x000, 0x000, 0x0DF, 0x000
};

short vm_mem_read(unsigned short addr) {
    if(addr == MMIO_RND_IN) {
        return rand() & 0xFFFF;
    }
    return vmem[addr];
}

void vm_mem_write(unsigned short addr, short value) {
    if(addr == MMIO_DIGIT_OUT) {
        printf("%hd\n", value);
    } else if(addr == MMIO_CHAR_OUT) {
        putchar((unsigned char)(value & 0xFF));
    } else {
        vmem[addr] = value;
    }
}

void runvm() {
    unsigned long counter = 0;
    unsigned short ip = RESERVED_OFFSET, op, addr, tmp;
    signed short acc = 0;
    char prefix;
    
    srand(time(NULL));
    
    while(ip < 0x100) {
        counter++;
        op = vmem[ip];
        ip++;
        prefix = (op >> 8);
        //printf("%02hx: %03hx\n", ip, op);
        switch(prefix) {
        case OP_INT:
            ip = 1000;
            break;
        case OP_JMP:
            vmem[REG_RA] = ip;
            ip = (LOW_BYTE(op));
            break;
        case OP_JZR:
            if(acc == 0)
                ip = LOW_BYTE(op);
            break;
        case OP_JNG:
            if(acc < 0)
                ip = LOW_BYTE(op);
            break;
        case OP_JI:
            ip = vmem[LOW_BYTE(op)];
            break;
        case OP_LD:
            acc = vm_mem_read(LOW_BYTE(op));
            break;
        case OP_LDI:
            acc = vm_mem_read(vm_mem_read(LOW_BYTE(op)));
            break;
        case OP_ST:
            addr = LOW_BYTE(op);
            vm_mem_write(addr, acc);
            break;
        case OP_STI:
            addr = vm_mem_read(LOW_BYTE(op));
            vm_mem_write(addr, acc);
            break;
        case OP_SET:
            acc = LOW_BYTE(op);
            break;
        case OP_ALU:
            switch((op >> 4) & 0xF) {
            case ALU_ADD:
                acc += vmem[LOW_NIBBLE(op)];
                break;
            case ALU_SUB:
                acc -= vmem[LOW_NIBBLE(op)];
                break;
            case ALU_AND:
                acc &= vmem[LOW_NIBBLE(op)];
                break;
            case ALU_OR:
                acc |= vmem[LOW_NIBBLE(op)];
                break;
            case ALU_XOR:
                acc ^= vmem[LOW_NIBBLE(op)];
                break;
            case ALU_INV:
                vmem[LOW_NIBBLE(op)] = ~vmem[LOW_NIBBLE(op)];
                break;
            case ALU_INC:
                vmem[LOW_NIBBLE(op)]++;
                break;
            case ALU_DEC:
                vmem[LOW_NIBBLE(op)]--;
                break;
            case ALU_PSH:
                vm_mem_write(vmem[REG_SP], vmem[LOW_NIBBLE(op)]);
                vmem[REG_SP]--;
                break;
            case ALU_POP:
                vmem[REG_SP]++;
                vmem[LOW_NIBBLE(op)] = vm_mem_read(vmem[REG_SP]);
                break;
            case ALU_XCH:
                tmp = vmem[LOW_NIBBLE(op)];
                vmem[LOW_NIBBLE(op)] = acc;
                acc = tmp;
                break;
            }
            break;
        default:
            printf("Invalid instruction\n- %04hx\n", op);
            return;
            break;
        }
    }
    printf("\nOperations: %ld\n", counter);
}

int main(int argc, char **argv) {
    FILE *f;
    unsigned short *buf;
    size_t fs, fr;
    if(argc < 2) {
        puts("Argument required");
        return 1;
    }
    f = fopen(argv[1], "rb");
    fseek(f, 0, SEEK_END);
    fs = ftell(f);
    buf = (unsigned short *)calloc(fs / sizeof(unsigned short), sizeof(unsigned short));
    fseek(f, 0, SEEK_SET);
    fr = fread(buf, sizeof(unsigned short), fs / sizeof(unsigned short), f);
    if(fr * sizeof(short) < fs) {
        printf("Error while reading file, %ld of %ld read (%d)\n", fr, fs, ferror(f));
        fclose(f);
        return 1;
    }
    fclose(f);
    

    if(fs > 245 * 2) return 1;
    memcpy((char *)(&vmem[RESERVED_OFFSET]), buf, fs);
    
    runvm();
    return 0;
}
