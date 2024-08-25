import random
try:
    from .helperegex import split, findpositions, searchmissing, re as regex
except:
    from helperegex import split, findpositions, searchmissing, re as regex


paterns = regex.compile(r'''
  \s      # one whitespace character, though I think this is perhaps unnecessary
  \d*     # 0 or more digits
  \.      # a dot
  \d{2}   # 2 digits
  ''', regex.VERBOSE)



def randomDigits(digits):
    try:
        lower = 10**(digits-1)
        upper = 10**digits - 1
        return random.randint(lower, upper)
    except:
        lower = "0"*(digits-1)
        upper = "9"*(digits-1)
        if lower != "" and upper != "":
            lower = "".join(["1", lower])
            upper = "".join(["9", upper])
        else:
            lower = "1"
            upper = "9"
        return random.randrange(int(lower), int(upper), upper.__len__())





#string = "echo 'fhfhf & ddd'  && 'fhfhfddd' && cd \"fhfhf && ddd\""
"""""def compiltes(string:str):
        if string == "":
            return []
        _output = []

        xout = findpositions(r"'(.*?)?'|\"(.*?)?\"", string)
        lenght = xout.__len__()
        cv = 0
        checkpoint = ()
        checkpoint2 = [] 
        place = "<%%"
        newstring = string
        keyplace = ""

        maxpend = []
        digit = 1
        xct = regex.finditer(r"<%%(.*?)?>", string)
        for xc in xct:
            if xc:  
                if xc.group(0).count(" ") == 0:
                    #search = regex.search("/d", xc.group(0))
                    maxdigit = xc.group(1)
                    maxpend.append(int(maxdigit))
                    #print(maxpend)

        if maxpend.__len__() != 0:
            _s_s = str(max(maxpend)).__len__()+1
            digit = int(_s_s)

        score_record = []
        for y in xout:
            for x in y:
                
                if x[0].find("&&") and x[0].count("&&") != 0:
                    keyplace = "&&"
                elif x[0].find("&") and x[0].count("&") != 0:
                    keyplace = "&"

                #print(keyplace)
                if lenght != 0:

                        score = randomDigits(digit)
                        if score not in score_record:
                            score_record.append(score)
                        else:
                            if score in score_record:
                                score = randomDigits(digit)
                                if score in score_record:
                                    score = randomDigits(digit)
                                    score_record.clear()
                            else:
                                score_record.append(score)

                        newword = "".join([place, str(score), ">"])
                        newpad = regex.sub(r"&&|&", newword, x[0]) #.replace(keyplace, newword)####bugss
                        if x[0].count("&") == 0:
                            cv +=1
                            #pass
                        else: 
                            if lenght ==  xout.__len__() - cv:
                                pass
                            else:
                                minus = newword.__len__()+keyplace.__len__()
                                checkpoint2.append((x[1][0]+minus-keyplace.__len__(), x[1][-1:][0]+minus+1))
                            

                            string = string.replace(x[0], newpad, 1)
                            checkpoint = checkpoint+((x[0], newword, score, keyplace), )
                            
                        lenght -= 1

        #print("checkpoint:", checkpoint, "\n")
        #print("Newkeys:", string)
        for x in split("&", string):
            for y in checkpoint:

                if x.count(y[1]) !=0:
                    oldstring = regex.search("'(.*?)?'", x) or regex.search("\"(.*?)?\"", x)
                    if oldstring:
                        x = x.replace(oldstring.group(0), y[0], 1)
                    #    print(1)
                    else:
                        x = x.replace(y[1], y[3])
                    #    print(2)
                    #print(oldstring, y)

            _output.append(x.strip())
        checkpoint = tuple(set(checkpoint)- set(checkpoint))
        return _output"""""

        #print("Missing :", searchmissing(string, newstring))
        #print(checkpoint, checkpoint2) 
        #print(split( checkpoint2[0], string))
 
        #import re
        #re.sub
        #print(string.split(keyplace))
