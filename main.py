script = "puissance:(+++)>base:(++++) setup:(>>>+<<<<>-<)[->[->+>+<<]>[-<+>]>[->[->+>+<<]>[-b<+>]<<]>>>[-<<+>>]<<<<<<]"
valueList = [0, 0, 0]
lecteurPos = 0
writerPos = 0


def scriptIter(writerPos, valueList, lecteurPos, script):
    if lecteurPos >= len(script):
        return ("script fini!")
    I = script[lecteurPos]
    if I == ">":
        writerPos += 1
        if writerPos >= len(valueList):
            valueList.append(0)
    elif I == "<":
        writerPos -= 1
        if writerPos == -1:
            writerPos = 0
    elif I == "+":
        valueList[writerPos] += 1
    elif I == "-":
        valueList[writerPos] -= 1
    elif I == "[":
        if valueList[writerPos] == 0:
            n = -1
            closingPos = lecteurPos
            for c in script[lecteurPos::]:
                if c == "]":
                    if n == 0:
                        break
                    else:
                        n -= 1
                if c == "[":
                    n += 1
                closingPos += 1
            lecteurPos = closingPos
    elif I == "]":
        n = 0
        closingPos = lecteurPos
        for c in script[0:lecteurPos][::-1]:
            if c == "[":
                if n == 0:
                    break
                else:
                    n -= 1
            if c == "]":
                n += 1
            closingPos -= 1
        lecteurPos = closingPos - 2
    return writerPos, valueList, lecteurPos




def render():
    print(valueList)
    print([int(n == writerPos) for n in range(len(valueList))])
    print(script)
    print(" " * lecteurPos + script[lecteurPos])
    #print (str([int(n == lecteurPos) for n in range(len(script))]))
    print("______________")

def runScript(writerPos=writerPos, valueList=valueList, lecteurPos=lecteurPos, script=script,renderStep = False,renderFinalResult=True,countIter = True):
    n = 0
    while True:
        temp = scriptIter(writerPos, valueList, lecteurPos, script)
        if type(temp) != str:
            writerPos, valueList, lecteurPos = temp
            n += 1
            if renderStep:
                render()
            lecteurPos += 1
        else:
            if renderFinalResult:
                render()
            if countIter:
                print("a pris", n, "instructions avant d'arriver")
            break


runScript()


