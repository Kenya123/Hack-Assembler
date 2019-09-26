import sys
import re
#file is open
file = sys.argv[1]

read = open(file, 'r')
#convert to 16-bit binary(A-instr)
def toBinary(num):
    binary = bin(num)
    binary_update = binary[2:]
    while len(binary_update) < 16:
        binary_update = '0' + binary_update
    return binary_update

#the @ is removed and number converted
def a_instruction(instruction):
    addr = int(instruction[1:])
    converted = toBinary(addr)
    return converted

#for  c-instruction

def c_instruction(instruction):
    #splitted = re.split('[= ;]', instruction)
    starter = '111'
    if '=' in instruction and ';' not in instruction:
        loc = instruction.find('=')
        loc1 = instruction.find(' ')
        c = instruction[loc+1:]
        d = instruction[:loc]
        return starter + compute[c] + dest[d] + jump['null']
    elif ';' in instruction and '=' not in instruction:
        loc = instruction.find(';')
        c = instruction[:loc]
        j = instruction[loc+1:]
        return starter + compute[c] + dest['null'] + jump[j]         

compute = {'0':'0101010',
           '1':'0111111',
           '-1':'0111010',
           'D':'0001100',
           'A':'0110000',
           '!D':'0001101',
           '!A':'0110001',
           '-D':'0001111',
           '-A':'0110011',
           'D+1':'0011111',
           'A+1':'0110111',
           'D-1':'0001110',
           'A-1':'0110010',
           'D+A':'0000010',
           'D-A':'0010011',
           'A-D':'0000111',
           'D&A':'0000000',
           'D|A':'0010101',
           'M':'1110000',
           '!M':'1110001',
           '-M':'1110011',
           'M+1':'1110111',
           'M-1':'1110010',
           'D+M':'1000010',
           'D-M':'1010011',
           'M-D':'1000111',
           'D&M':'1000000',
           'D|M':'1010101'}

dest = {'null':'000',
        'M':'001',
        'D':'010',
        'MD':'011',
        'A':'100',
        'AM':'101',
        'AD':'110',
        'AMD':'111'}

jump = {'null':'000',
        'JGT':'001',
        'JEQ':'010',
        'JGE':'011',
        'JLT':'100',
        'JNE':'101',
        'JLE':'110',
        'JMP':'111'}



sym_table = {'SP': toBinary(0),
             'LCL': toBinary(1),
             'ARG': toBinary(2),
             'THIS': toBinary(3),
             'THAT': toBinary(4),
             'R0': toBinary(0),
             'R1': toBinary(1),
             'R2': toBinary(2),
             'R3': toBinary(3),
             'R4': toBinary(4),
             'R5': toBinary(5),
             'R6': toBinary(6),
             'R7': toBinary(7),
             'R8': toBinary(8),
             'R9': toBinary(9),
             'R10': toBinary(10),
             'R11': toBinary(11),
             'R12': toBinary(12),
             'R13': toBinary(13),
             'R14': toBinary(14),
             'R15': toBinary(15),
             'SCREEN': toBinary(16384),
             'KBD': toBinary(24576)}
                    

#print(sym_table['LCL'])
counter1 = 0
for line in read:
    line = line.rstrip("\n")
    line = line.lstrip()
    if line.startswith('//'):
        continue
    elif len(line.strip()) == 0:
        continue
    elif line.startswith('('):
        firstbr = line.find('(')
        lastbr = line.find(')')
        inside = line[firstbr+1:lastbr]
        sym_table[inside] = toBinary(counter1)
    else:
        counter1 = counter1 + 1
read.close()
 

fp = open(file, 'r')

#print(c_instruction('D=M'))

name= sys.argv[1]
ext = name.find('.')
nameMod = name[:ext] 
newExt = ".hack"
fullName = nameMod + newExt

newFile = open(fullName, "a+")
counter = 0
register = 16
for line in fp:
    line = line.rstrip("\n")
    line = line.lstrip()
    if line.startswith('//'):
       continue
    elif len(line.strip()) == 0:
       continue
    elif re.search('^@+[0-9]', line):
       code = a_instruction(line)
       newFile.write(str(code))
       newFile.write("\n")
       counter = counter + 1
    elif line.startswith('('):
       first = line.find('(')
       second = line.find(')')
       inside = line[first+1:second]
       sym_table[inside] = toBinary(counter)
    elif re.search('^@+[^0-9]', line):
       loc = line.find('@')
       code = line[loc+1:]
       if code in sym_table:
           newFile.write(str(sym_table[code]))
           newFile.write("\n")
       elif code not in sym_table:
           sym_table[code] = toBinary(register)
           register = register + 1
           newFile.write(sym_table[code])
           newFile.write("\n")
       counter = counter + 1
    else:
       code = c_instruction(line)
       newFile.write(str(code))
       newFile.write("\n")
       counter = counter + 1 
       


