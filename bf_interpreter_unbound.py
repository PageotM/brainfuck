#scripts a tester:
init = lambda a,b : '>' + '+'*a + '>' + '+'*b + '<<'
addToNext = '[->+<]>'
addToPrevious = '[-<+>]<'
add = lambda a,b : f'{init(a,b)} {addToNext}'
#don't multiply by 0 plz
multiply = lambda a,b : f"{init(a,b)} >>- [[>]+[<]>>-] +<- [>[+>]<[<]>-] > <<->> (set neg 1) [<{addToNext}>] < <+[->{addToPrevious}<+] >{addToPrevious} "
multiplyWithNext = f">- [[>]+[<]>>-] +<- [>[+>]<[<]>-] > <<->> (set neg 1) [<{addToNext}>] < <+[->{addToPrevious}<+] >{addToPrevious} "

multiplyWithNextNoSpace = f">{addToNext}<<{addToNext} >- [[>]+[<]>>-] +<- [>[+>]<[<]>-] > <<->> (set neg 1) [<{addToNext}>] < <+[->{addToPrevious}<+] >{addToPrevious} "
multiplyWithPrevious = f"<{multiplyWithNextNoSpace}<"

exponent = lambda a,b: f"{init(a,b)} >>- [[>]+[<]>>-] +<- [>[+>]<[<]>-] + [>] <<-[+>{multiplyWithPrevious}-] >{addToPrevious*2}"

DEFAULT_SCRIPT = exponent(18,3)
print(DEFAULT_SCRIPT)

STEP_BY_STEP = False    #parametre si on veut voir toutes les etapes, appuyez enter pour passer
DISPLAY = True         #parametre pour afficher la memoire a chaque etape

def process(script, memory, writePos, readPos):
    command = script[readPos]
    
    
    if(writePos == len(memory)):
        memory.append(0)
    if(writePos < 0):
        print('writePos = ',writePos)
        raise IndexError("MEMOIRE DEPASSEE A GAUCHE")    #si on depasse la memoire a gauche

    if command in "<>+-":
        if(DISPLAY):
            displayStatus(memory, writePos, readPos)
            if(STEP_BY_STEP):
                input()

    if(command == '<'):
        return memory, (writePos-1), (readPos+1)

    elif(command == '>'):
        return memory, (writePos+1), (readPos+1)

    elif(command == '+'):
        memory[writePos] += 1
        return memory, writePos, (readPos+1)

    elif(command == '-'):
        memory[writePos] -= 1
        return memory, writePos, (readPos+1)

    elif(command == '['):
        if(memory[writePos] == 0):
            nextReadPos = matchingClosedBracket(script, readPos)
            return memory, writePos, nextReadPos
        else:
            return memory, writePos, (readPos+1)

    elif(command == ']'):
        if(memory[writePos] == 0):
            return memory, writePos, (readPos+1)
        else:
            nextReadPos = matchingOpenBracket(script, readPos) + 1
            return memory, writePos, nextReadPos
    else:   #tout autre caractere est considere comme un commentaire
        return memory, writePos, (readPos+1)

def matchingClosedBracket(script, readPos):
    count = 1
    nextPos = readPos
    while(count != 0):
        nextPos, nextType = nextBracket(script, nextPos)
        if nextType == ']':
            count -= 1
        else:   #next bracket is another [
            count += 1
    return nextPos


def matchingOpenBracket(script, readPos):
    count = 1
    lastPos = readPos
    while(count != 0):
        lastPos, lastType = lastBracket(script, lastPos)
        if lastType == '[':
            count -= 1
        else:   #next bracket is another ]
            count += 1
    return lastPos

def nextBracket(script, readPos):
    bracketPos = readPos + 1
    for char in script[(readPos+1):]:
        if char in '[]':
            return bracketPos, char
        bracketPos += 1
    raise SyntaxError


def lastBracket(script, readPos):
    bracketPos = readPos - 1
    for char in script[:readPos][::-1]:
        if char in '[]':
            return bracketPos, char
        bracketPos -= 1
    raise SyntaxError


def checkValidScript(script):
    if(script.count('[') != script.count(']')):
        raise SyntaxError("Certains crochets ne sont pas fermés")

def displayStatus(memory, writePos, readPos):
    print(f'{memory}\nwritePos = {writePos}, readPos = {readPos}')

def runScript(script = DEFAULT_SCRIPT, memory = [0]):
    
    writePos = 0
    readPos = 0
    checkValidScript(script)
    while(readPos < len(script)):
        memory, writePos, readPos = process(script, memory, writePos, readPos)
    displayStatus(memory, writePos, readPos)


def main():

    gotomin2R = "++[-->++]--"
    if_equal_0 = lambda logic: f">>+<[>-] {gotomin2R}< [-<<{logic}>>]<<"

    gotomin8R3J = "++++++++[-------->>>++++++++]--------"
    gotomin3R2J = "+++[--->>+++]---"
    jumpWriteFlag = f">{gotomin8R3J}{gotomin3R2J}"
    
    gotomin8L2J = "++++++++[--------<<++++++++]--------"
    gotomin1L3J = "+[-<<<+]-"
    jumpReadFlag = f"{gotomin8L2J}<{gotomin1L3J}"

    logic1 = f"{jumpWriteFlag} >+< {jumpReadFlag}"
    logic2 = f"{jumpWriteFlag} >-< {jumpReadFlag}"
    logic3 = f"{jumpWriteFlag} ->>+ {jumpReadFlag}"
    logic4 = f"{jumpWriteFlag} -<<+ {jumpReadFlag}"


    executeInstruction_1_4 = f">-< {if_equal_0(logic1)} >-< {if_equal_0(logic2)} >-< {if_equal_0(logic3)} >-< {if_equal_0(logic4)} >++++<"
    
    process_bf_script_1_4 = f">++++++++[-------- < + {executeInstruction_1_4} - >>>  >++++++++] --------<"
    #only processes instructions 1-4, meaning +/-/>/< respectively

    memory_test_1_4 = [-2, 1, 0, -2, 3, 0, -2, 2, 0, -2, 4, 0, -2, 1, 0, -2, -8, 0, -3, 0, -4, 0, -4, 0, -4, 0]
    print("RUNNING SCRIPT:\t",process_bf_script_1_4)
    runScript(process_bf_script_1_4, memory_test_1_4)

main()

# TODO FOR NEXT STEPS:

# * standard logic for BRACKETS []!!!
### decide on paper if using unique flag for each pair of brackets (generated when creating memory at the beginning)
### options:
#           ** unique flag for each pair of brackets... (should work BUT must be generated during compilation, not dynamic)
#           ** temporary flag with "last bracket?" (easy to implement, but how to do nested loops?)
#           ** cascade de flags? aka chaque loop dans une loop se crée un flag = flag_précedent - 1,
#                   puis on "remonte" dans les flags a chaque sortie de boucle jusqu'au flag de "pas ds une loop" or whtvr

# * decide flag conventions for read / write, script / memory... (also bracket flags conventions! ^^^) 
# 
# READ FLAG MUST BE BIGGER THAN MAX NUMBER OF INSTRUCTIONS AKA = -6?

# * finish paper documentation for final process


# * one day... if error??? (write tries to < too much, ends on -8 flag... terminate program!)



#NOTE FUNCTION PROCESS DONE!!:

# * standard logic for - / + (associated to 1 and 2, not 0...)

# * standard logic for > / < (easy if only positive numbers in memory)

# * adapt > / < logic with double jumps, and checkpoint at end-of-script-flag (-8/-5...), to have negative numbers in memory.
### AKA, do: "goto(-5 right triple jump) goto(-3 right double jump), MOVE WRITE FLAG TO RIGHT/LEFT (->>+ or -<<+) , goto(-5 left double jump) goto(-1 left triple jump)"