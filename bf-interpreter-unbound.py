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

SCRIPT = exponent(22,3)
print(SCRIPT)

STEP_BY_STEP = True    #parametre si on veut voir toutes les etapes, appuyez enter pour passer
DISPLAY = True         #parametre pour afficher la memoire a chaque etape

def process(memory, writePos, readPos):
    command = SCRIPT[readPos]
    
    
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
            nextReadPos = matchingClosedBracket(readPos)
            return memory, writePos, nextReadPos
        else:
            return memory, writePos, (readPos+1)

    elif(command == ']'):
        if(memory[writePos] == 0):
            return memory, writePos, (readPos+1)
        else:
            nextReadPos = matchingOpenBracket(readPos) + 1
            return memory, writePos, nextReadPos
    else:   #tout autre caractere est considere comme un commentaire
        return memory, writePos, (readPos+1)

def matchingClosedBracket(readPos):
    count = 1
    nextPos = readPos
    while(count != 0):
        nextPos, nextType = nextBracket(nextPos)
        if nextType == ']':
            count -= 1
        else:   #next bracket is another [
            count += 1
    return nextPos


def matchingOpenBracket(readPos):
    count = 1
    lastPos = readPos
    while(count != 0):
        lastPos, lastType = lastBracket(lastPos)
        if lastType == '[':
            count -= 1
        else:   #next bracket is another ]
            count += 1
    return lastPos

def nextBracket(readPos):
    bracketPos = readPos + 1
    for char in SCRIPT[(readPos+1):]:
        if char in '[]':
            return bracketPos, char
        bracketPos += 1
    raise SyntaxError


def lastBracket(readPos):
    bracketPos = readPos - 1
    for char in SCRIPT[:readPos][::-1]:
        if char in '[]':
            return bracketPos, char
        bracketPos -= 1
    raise SyntaxError


def checkValidScript():
    if(SCRIPT.count('[') != SCRIPT.count(']')):
        raise SyntaxError("Certains crochets ne sont pas fermés")

def displayStatus(memory, writePos, readPos):
    print(f'{memory}\nwritePos = {writePos}, readPos = {readPos}')

def main():
    memory = [0]
    writePos = 0
    readPos = 0
    checkValidScript()
    while(readPos < len(SCRIPT)):
        memory, writePos, readPos = process(memory, writePos, readPos)
    displayStatus(memory, writePos, readPos)

main()