import os, sys, re, array, enum, traceback

OPCODES = {
    'RSET': 0x000,
    # memory access functions
    'LOAD': 0x400,
    'STOR': 0x500,
     'LDI': 0x600,
     'STI': 0x700,
    # flow control functions
    'JMPZ': 0x800,
    'JMPN': 0x900,
    'JUMP': 0xA00,
      'JI': 0xB00,
    # register/ALU functions
     'ADD': 0xC00,
     'SUB': 0xC10,
     'AND': 0xC20,
      'OR': 0xC30,
     'INC': 0xC40,
     'DEC': 0xC50,
     'INV': 0xC60,
     'XOR': 0xC70,
    'SWAP': 0xCF0,
    'PUSH': 0xCC0,
     'POP': 0xCD0,
     
     'SET': 0xD00,
    'CALL': 0xF00,
     'RET': 0xF0F
}

def assemble(code):
    labels = {
        'r{}'.format(i): i
        for i in range(15)
    }
    labels['cout'] = 0xE1
    labels['dout'] = 0xE0
    
    placeholders = []
    
    last_addr = 0x0
    ip = 0x10
    memory = array.array('h', (0 for _ in range(256 - 16)))
    
    for line in code.split('\n'):
        if line == '':
            continue
        label = None
        instruction = []
        for t in line.split():
            if t[-1] == ':':
                label = t[:-1]
            elif t[0] == ';':
                break
            else:
                instruction.append(t)

        if label is not None:
            for item in placeholders:
                if item[0] == label:
                    memory[item[1]] += ip
            placeholders = [item for item in placeholders if item[0] != label]
            labels[label] = ip
        if len(instruction) == 0:
            continue
        command = instruction[0].upper()
        if len(instruction) > 1:
            operand = instruction[1]
        else:
            operand = None
    
        if command in ('DATA', 'DAT'):
            while len(instruction) > 1:
                memory[ip] = int(instruction.pop(1), 0)
                ip += 1
        elif command == 'CHAR':
            memory[ip] = ord(operand)
            ip += 1
        elif command == 'ORG':
            ip = int(operand, 0)
        elif command == 'REF':
            if operand in labels:
                memory[ip] += labels[operand]
            else:
                placeholders.append((operand, ip))
            ip += 1
        else:
            if not command in OPCODES:
                raise ValueError('Wrong operation ' + command)
            memory[ip] = OPCODES[command]
            if operand is None:
                pass
            elif operand[0] in ('+', '-'):
                memory[ip] += ip + int(operand, 0)
            elif operand.isdigit() or operand.startswith('0x'):
                value = int(operand, 0)
                memory[ip] += value
            else:
                if operand in labels:
                    memory[ip] += labels[operand]
                else:
                    placeholders.append((operand, ip))
            
            ip += 1
        last_addr = max(ip, last_addr)
    if len(placeholders) > 0:
        print('Label ' + placeholders[0][0] + ' is missing')
        raise ValueError('Label not defined')
    return memory[:last_addr + 1]

def validate_args(args):
    if len(args) < 2:
        print('Usage: asm.py <assembly file> <output file>')
        return False
    if not os.path.isfile(args[0]):
        print('Wrong assembly file')
        return False
    return True

def main(args):
    if not validate_args(args):
        return 0
    try:
        with open(args[0], 'r') as f:
            data = assemble(f.read())
        with open(args[1], 'wb') as f:
            f.write(data[0x10:].tobytes())
        return 0
    except:
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]) or 0)
