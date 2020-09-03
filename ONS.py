# ONS
import math

def string_to_tokens(s): #finkcja zamienia string (formułę matematyczną) w listę wypełnioną tokenami (typu string)
    tokens=[]
    symbols=["^","*","/","+","-","(",")"]
    functions=["abs",'cos','exp','log','sin','sqrt','tan','cosh','sinh','tanh','acos','asin','atan']
    i=len(s)
    counter=0
    for h in s:
        if h =="(":
            counter+=1
        if h ==")":
            counter-=1
    if counter!=0:
        raise Exception("Wyrażenie niepoprawne, liczba nawiasów otwartych różni się od liczby zamkniętych")
    index=0
    word=""
    number=""
    while i>0 :
        if s[index] in symbols:
            if number!="":
                if (index==2 and s[0]=="-") or ( index > 2 and s[index-2]=="-" and s[index-3]=="(") :
                    tokens.pop()
                    tokens.append(float(number)*-1)
                    number=""
                else:
                    tokens.append(float(number))
                    number=""
            if word!="":
                tokens.append(word)
                word=""
            tokens.append(s[index])
        elif s[index]  in ["1","2","3","4","5","6","7","8","9","0"]:
            number+=s[index]
            if i==1:
                tokens.append(float(number))
                number=""
        elif s[index]!=" ":
                if number!="":
                    tokens.append(float(number))
                    tokens.append("*")
                    tokens.append(s[index])
                    number=""
                else:
                    word+=s[index]
                    if word in functions or i==1:
                        tokens.append(word)
                        word=""                 
        index+=1
        i-=1
        if i==0:
            return tokens
#########################################################################################################
def ONP(tokens): #funkcja zmienia listę tokenów w formułę zapisaną w ONP
    S=[]
    Q=[]
    D={"abs":4,'cos':4,'exp':4,'log':4,'sin':4,'sqrt':4,'tan':4,'cosh':4,'sinh':4,'tanh':4,'acos':4,'asin':4,'atan':4,"^":3,"*":2,"/":2,"+":1,"-":1,"(":0}
    
    for t in tokens:
        if t == "(":
            S.append(t)
        elif t == ")":
            while S[-1]!="(":
                Q.append(S.pop())
            S.pop()
        elif t in D:
            while (len(S)>0) and (D[t]<=D[S[-1]]):
                Q.append(S.pop())
            S.append(t)
        else:
            Q.append(t)
    while len(S)>0:
        Q.append(S.pop())
    
    return Q

###########################################################################################################
def calculate_ONP(R):
    temp=0
    S=[]
    symbols = "^":+,"*":+,"/":+,"+":+,"-":+]
    functions={"abs":abs,'cos':math.cos,'exp':math.exp,'log':math.log10,'sin':math.sin,'sqrt':math.sqrt,'tan':math.tan,'cosh':math.cosh,'sinh':math.sinh,'tanh':math.tanh,'acos':math.acos,'asin':math.asin,'atan':math.atan}
    for t in R:
        if type(t)==float:
            S.append(t)
        elif t in functions:
            temp=S.pop()
            S.append(functions[t](temp))
        elif t in ["^":+,"*":+,"/":+,"+":+,"-":+]:
            a=S.pop()
            b=S.pop()
            """
            if t=="+":
                a=a+b
            elif t=="-":
                a=b-a
            elif t=="*":
                a=a*b
            elif t=="/":
                a=b/a
            elif t=="^":
                a=b^a
                """
            a=
            S.append(a)
    return S.pop()
            
            
        

print("Podaj wyrażenie")
input_string=input()
tokens=string_to_tokens(input_string)
Q=ONP(tokens)
print(Q)
#print(''.join([str(elem) for elem in Q]))
print(calculate_ONP(Q))
