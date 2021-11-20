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
        for c in script[:lecteurPos][::-1]:
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


def decompile(command:str, variable = {}):
    blocList = []
    bloctype = []
    for c in command:
        ctype = ""
        if c in "1234567890":
            ctype = "int"
        elif c in "<>+-[]":
            ctype = "log"
        else:
            ctype = "str"
        if len(blocList) == 0:
            blocList.append(c)
            bloctype.append(ctype)
        else:
            if bloctype[-1] == ctype:
                blocList[-1] += c
            else:
                blocList.append(c)
                bloctype.append(ctype)
    for a in range(len(blocList)):
        if blocList[a] in variable.keys():
            blocList[a] = variable[blocList[a]]

    tmp = ""
    for bloc in blocList:
        tmp += bloc
    return(tmp)

def multileveldecompile(command:str, variable={}, max_decompilation_depth = 5, show_necessary_steps = False):
    decompiled_command = command
    for a in range(max_decompilation_depth):
        next_decompilation_level = decompile(decompiled_command,variable=variable)
        if decompiled_command == next_decompilation_level:
            if show_necessary_steps:
                print("étapes nécessaires:",a)
            return decompiled_command
        decompiled_command = next_decompilation_level
    return  decompiled_command

