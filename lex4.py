import re
import copy
from name import name
import pickle


class Lex:
    
   
    def __init__(self):
        self.keywords = []
        self.symbols = []
        self.numbers = ['0','1','2','3','4','5','6','7','8','9']
        self.special = ['n','t','a','b','f','r','v','\\',"'",'"','0']
        self.names = []
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
    
    def DFA(self,string,result):
        state = 'state0'
        tmp = ''
        while len(string)>0:
            if string[0] == ' ' or string[0] == '\n' or string[0] == '\t':
                if state == 'state0':
                    string = string[1:]
                elif state == 'Char':
                    if string[0] == ' ':
                        tmp += string[0]
                        string[1:]
                    else:
                        print 'illegal char'
                        break
                elif state == 'sharp':
                    if string[0] == ' ':
                        tmp += string[0]
                        string = string[1:]
                    elif string[0] == '\n':
                        result.append((state,tmp))
                        string = string[1:]
                        state = 'state0'
                        tmp = ''
                    else:
                        print 'sharp error'
                        break
                elif state == 'string':
                    if string[0] == '/n':
                        print 'strint error'
                        break
                    else:
                        tmp += string[0]
                        string = string[1:]
                elif state == 'f_d':
                    result.append(('Int',int(tmp)))
                    tmp = ''
                    state = 'state0'
                    string = string[1:]
                elif state == 'float':
                    result.append((state,float(tmp)))
                    tmp = ''
                    state ='state0'
                    string = string[1:]
                elif state == 'v_k':
                    if tmp in self.keywords:
                        result.append((tmp,tmp))
                    else:
                        n = name(tmp)
                        self.names.append(n)
                        result.append(('var',len(self.names)-1))
                    state = 'state0'
                    tmp = ''
                    string = string[1:]

            
            else:
                if state == 'state0':
                    if string[0] in self.symbols:#handle symbols
                        result.append((string[0],string[0]))
                        string = string[1:]
                    elif string[0] == "#":#handle sharp
                        state = "sharp"
                        string = string[1:]
                    elif string[0] == "'":#handle Char
                        state = 'Char'
                        string = string[1:]
                    elif string[0] == '"':#handle string
                        state = 'string'
                        string = string[1:]
                    elif string[0]  in self.numbers:#handle int and float
                        tmp += string[0]
                        state = 'f_d'
                        string = string[1:]
                    else:#handle var and key
                        state = 'v_k'
                        tmp += string[0]
                        string = string[1:]

                elif state == 'v_k':
                    if string[0] in self.symbols:
                        if tmp in self.keywords:
                            result.append((tmp,tmp))
                        else:
                            n = name(tmp)
                            self.names.append(n)
                            result.append(('var',len(self.names)-1))
                        state = 'state0'
                        tmp = ''
                    else:
                        tmp += string[0]
                        string = string[1:]
                elif state == 'float':
                    if string[0] in self.numbers:
                        tmp += string[0]
                        string = string[1:]
                    else:
                        result.append((state,float(tmp)))
                        tmp = ''
                        state = 'state0'

                elif state == 'f_d':
                    if string[0] in self.numbers:
                        if tmp[0] != '0':
                            tmp += string[0]
                            string = string[1:]
                        else:
                            print 'Int error'
                            break
                    elif string[0] == '.':
                        tmp += string[0]
                        state = 'float'
                        string = string[1:]
                    else:
                        result.append(('Int',int(tmp)))
                        state = 'state0'
                        tmp = ''


                elif state == 'string':
                    if string[0] == '"' and tmp[-1] != '\\':
                        result.append((state,tmp))
                        state = 'state0'
                        tmp = ''
                        string = string[1:]
                    else:
                        tmp += string[0]
                        string = string[1:]
                elif state == 'Char':
                    if string[0] == "'":
                        result.append((state,tmp))
                        tmp = ''
                        state = 'state0'
                        string = string[1:]
                    else:
                        if len(tmp) == 0:
                            tmp += string[0]
                            string = string[1:]
                        else:
                            if tmp == '\\' and string[0] in self.special:
                                tmp += string[0]
                                string = string[1:]
                            else:
                                print 'Char error'
                                break

                elif state == 'sharp':
                    tmp += string[0]
                    string = string[1:]
        
        with open('result1','w') as f:
            for re in result:
                f.write(str(re[0])+','+str(re[1]))
                f.write('\n')
        
        with open('names','wb') as f:
            pickle.dump(self.names,f)
        for n in self.names:
            print 'var_name'
            print n.var_name



    
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
   
