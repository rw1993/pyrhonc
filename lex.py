import re
import copy


def my_split(s,seps):
    res=[s]
    for sep in seps:
        s,res=res,[]
        for seq in s:
            res+=seq.split(sep)
    return res
numbers = ['0','1','2','3','4','5','6','7','8','9']

class Lex:

    keywords = []
    symbols = []
   
    def __init__(self):
        self.get_words_symbols('keywords',self.keywords)
        self.get_words_symbols('symbols',self.symbols)
    
    def get_words_symbols(self,url,ls):
        with open(url,'r') as f:
            if url == 'symbols':
                string = f.readline()
                strings = string.split()
                for s in strings:
                    ls.append(s)
                return
            
            raw_string = f.readline()
            raw_string = raw_string.replace('"','')
            string = raw_string.replace('\n','')
            strings = string.split(',')
            for keyword in strings:
                ls.append(keyword)
    
    def delete_note(self,strings):
        pattern1 = r'//.*\n'
        sub_string = re.sub(pattern1,' ',strings)
        pattern2 = r'/\*.*\*/'
        p = re.compile(pattern2,re.S)
        sub_string = re.sub(p," ",sub_string)
        return sub_string

    def DFA(self,string,result,state = 'state0',tmp=''):
        print state
        print result

        if len(string) == 0:
            if state == 'state0':
                with open('result','w') as f:
                    for r in result:
                        f.write(str(r[0])+','+str(r[1]))
                        f.write('\n')
                exit()
                    
        
        if string[0] == '\n' or string[0] == ' ' or string[0] == '\t':
            if state == 'state0':
                self.DFA(string[1:],result)
            elif state == 'sharp':
                if string[0] == ' ':
                    tmp += string[0]
                    self.DFA(string[1:],result,state,tmp)
                else:
                    result.append(('#',tmp))
                    self.DFA(string[1:],result)
            elif state == 'char':
                if len(tmp) == 0 and string[0] == ' ':
                    tmp += string[0]
                    self.DFA(string[1:],result,state,tmp)
                else:
                    print "error"
            elif state == 'string':
                if string[0] != '\n':
                    tmp += string[0]
                    self.DFA(string[1:],result,state,tmp)
                else:
                    print "error"
            elif state == 'f_d':
                result.append(('Int',int(tmp)))
                self.DFA(string[1:],result)
            elif state == 'f':
                result.append(('Float',float(tmp)))
                self.DFA(string[1:],result)
            elif state == 'v_k':
                if tmp in self.keywords:
                    result.append((tmp,tmp))
                    self.DFA(string[1:],result)
                else:
                    result.append(('var',tmp))
                    self.DFA(string[1:],result)
                    
                
        else:
            if state == 'state0':
                if string[0] in self.symbols:#handle symbol
                    result.append((string[0],string[0]))
                    self.DFA(string[1:],result)
                elif string[0] == '#':#handle sharp
                    state = 'sharp'
                    self.DFA(string[1:],result,state)
                elif string[0] == "'":#handle char
                    state = 'char'
                    self.DFA(string[1:],result,state)
                elif string[0] == '"':#handlle string
                    state = 'string'
                    self.DFA(string[1:],result,state)
                elif string[0] in numbers:#handle float and digit
                    state = 'f_d'
                    tmp += string[0]
                    self.DFA(string[1:],result,state,tmp)
                else:#handle var and key
                    state = 'v_k'
                    tmp += string[0]
                    self.DFA(string[1:],result,state,tmp)

            elif state == 'v_k':
                if string[0] in self.symbols:
                    if tmp in self.keywords:
                        result.append((tmp,tmp))
                        self.DFA(string,result)
                    else:
                        result.append(('var',tmp))
                        self.DFA(string,result)
                else:
                    tmp += string[0]
                    self.DFA(string[1:],result,state,tmp)

                    
            elif state == 'f_d':
                if string[0] in numbers:
                    if tmp[0] == '0':
                        print 'error'
                    else:
                        tmp += string[0]
                        self.DFA(string[1:],result,state,tmp)
                elif string[0] == '.':
                    tmp += string[0]
                    state = 'f'
                    self.DFA(string[1:],result,state,tmp)
                elif string[0] in self.symbols:
                    result.append(('Int',int(tmp)))
                    self.DFA(string,result)
                else:
                    print "error"

            elif state == 'f':
                if string[0] in numbers:
                    tmp += string[0]
                    self.DFA(string[1:],result,state,tmp)
                elif string[0] in self.symbols:
                    result.append(('Float',float(tmp)))
                    self.DFA(string,result)
                else:
                    print 'error'

            elif state == 'string':
                if string[0] == '"':
                    if len(tmp)>0 and tmp[-1] == '\\':
                        tmp += '"'
                        self.DFA(string[1:],result,state,tmp)
                    else:
                        result.append(('string',tmp))
                        self.DFA(string[1:],result)
                else:
                    tmp += string[0]
                    self.DFA(string[1:],result,state,tmp)

                    
            elif state == 'char':
                if string[0] == "'":
                    result.append(('char',tmp))
                    self.DFA(string[1:],result)
                elif len(tmp) == 0:
                    tmp += string[0]
                    self.DFA(string[1:],result,state,tmp)
                elif tmp == '\\':
                    special = ['n','t','a','b','f','r','v','\\',"'",'"','0']
                    if string[0] in special or string[0] == 'd' or string[0] == 'x':
                        tmp += string[0]
                        self.DFA(string[1:],result,state,tmp)
                elif tmp == 'd' or tmp == 'dd':
                    if string[0] == 'd':
                        tmp += string[0]
                        self.DFA(string[1:],result,state,tmp)
                    else:
                        print "error"
                elif tmp == 'x' or tmp == 'xh':
                    if string[0] == 'h':
                        tmp += string[0]
                        self.DFA(string[1:],result,state,tmp)
                    else:
                        print "error"
                else:
                    print "error"
            elif state == 'sharp':
                tmp += string[0]
                self.DFA(string[1:],result,state,tmp)

    def analyze(self,url):
        result = []
        with open(url,'r') as f:
            strings = ""
            for string in f.readlines():
                strings += string
            strings = self.delete_note(strings)#delete the note
            self.DFA(strings,result)
        
                        


if __name__ == '__main__':
    l = Lex()
    l.analyze('test.c')
    '''
    print l.reg('int')
    print l.reg('int_123')
    print l.reg('0.1')
    print l.reg('1123123.1345145145145')
    print l.reg("'a'")
    print l.reg("''")
    print l.reg("'ab'")
    print l.reg('"what?int,123"')
    '''
   
