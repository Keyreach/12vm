import sys, re, array, enum

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
     
     'SET': 0xD00
}

def assemble(code):
    labels = {
        'r{}'.format(i): i
        for i in range(15)
    }
    labels['cout'] = 0xE1
    labels['dout'] = 0xE0
    
    placeholders = []
    
    ip = 0x10
    memory = array.array('h', (0 for _ in range(256 - 16)))
    
    # rgx = r'(?:([A-z0-9]+):\s+)*([A-z0-9]+)(?:[ \t]+([A-z0-9]+))*(\n|$)'
    
    ops = []
    
    #for m in re.finditer(rgx, code):
    #    label = m.group(1)
    #    command = m.group(2).upper()
    #    operand = m.group(3)
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
        try:
            operand = instruction[1]
        except:
            pass
    
        if command in ('DATA', 'DAT'):
            value = int(operand, 0)
            memory[ip] = value
            ip += 1
        elif command == 'ORG':
            value = int(operand, 0)
            ip = value
        elif command == 'REF':
            if operand in labels:
                memory[ip] += labels[operand]
            else:
                placeholders.append((operand, ip))
            ip += 1
        # elif command == 'SET':
        #    value = int(operand, 0)
        #    memory[ip] = OPCODES['JUMP'] + (ip + 2)
        #    memory[ip + 1] = value
        #    memory[ip + 2] = OPCODES['LOAD'] + (ip + 1)
        #    ip += 3
        else:
            if not command in OPCODES:
                raise ValueError('Wrong operation ' + command)
            memory[ip] = OPCODES[command]
            if operand is None:
                pass
            elif not operand.isdigit():
                if operand in labels:
                    memory[ip] += labels[operand]
                else:
                    placeholders.append((operand, ip))
            else:
                value = int(operand, 0)
                memory[ip] += value
            ip += 1
    if len(placeholders) > 0:
        print('Label ' + placeholders[0][0] + 'missing')
        raise ValueError('Label not defined')
    return memory

def main(args):
    with open(args[0], 'r') as f:
        data = assemble(f.read())
    with open(args[1], 'wb') as f:
        f.write(data[0x10:].tobytes())
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]) or 0)
