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

STEP_BY_STEP = True    #parametre si on veut voir toutes les etapes, appuyez enter pour passer
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
    gotomin1L = "+[-<+]-"
    gotomin3R = "+++[--->+++]---"
    balancedLogic = f"{gotomin3R}>+<{gotomin1L}"
    ifaeq0 = f">>+<[>-] {gotomin1L} >> [-<<{balancedLogic}>>]<<"

    test_process_script = f"+++++[----- + {ifaeq0} - >>>  +++++] -----"
    memory = [-2, 1, 0, -2, 0, 0, -2, 0, 0, -5, 0, -3, 0]
    print("RUNNING SCRIPT:\t",test_process_script)
    runScript(test_process_script, memory)

main()

# NOTE FOR NEXT STEPS:
# * standard logic for - / + (associated to 1 and 2, not 0...)

# * standard logic for > / < (easy if only positive numbers in memory)

# * adapt > / < logic with double jumps, and checkpoint at end-of-script-flag (-8/-5...), to have negative numbers in memory.
### AKA, do: "goto(-5 right) goto(-3 right double jump), MOVE WRITE FLAG TO RIGHT/LEFT (->>+ or -<<+) , goto(-5 left double jump) goto(-1 left)"

# * standard logic for BRACKETS []!!!
### decide on paper if using unique flag for each pair of brackets (generated when creating memory at the beginning)
### options:
#           ** unique flag for each pair of brackets... (should work BUT must be generated during compilation, not dynamic)
#           ** temporary flag with "last bracket?" (easy to implement, but how to do nested loops?)
#           ** cascade de flags? aka chaque loop dans une loop se crée un flag = flag_précedent - 1,
#                   puis on "remonte" dans les flags a chaque sortie de boucle jusqu'au flag de "pas ds une loop" or whtvr

# * decide flag conventions for read / write, script / memory... (also bracket flags conventions! ^^^)

# * finish paper documentation for final process