#!/usr/bin/env python
# encoding: utf-8

"""
@Author: rw
@Email: weiyanjie10@gmail.com
@Date:20150427
@Desc:lr1 with python
@Log:go and closure seems right
"""


class cfg(object):

    """
    Docstring for cfg.
    a cfg
    """

    def __init__(self,head,bodys,cfgid):
        self.head = head
        self.bodys = bodys
        self.id = cfgid
    def __eq__(self,other):
        return self.head == other.head and self.id == other.id and self.bodys == other.bodys


class lr1_cfg(object):

    """Docstring for lr1_cfg. """

    def __init__(self,cfg,index,lookahead):
        self.cfg = cfg
        self.lookahead = lookahead
        self.current_index = index
    def __eq__(self,other):
        if self.cfg == other.cfg:
            if self.lookahead == other.lookahead:
                if self.current_index == other.current_index:
                    return True
        return False

def get_cfg(url):
    """ Docstring for get_cfg.
    :url:a url to cfg file
    :returns: a list of cfg project
    """
    cfgs = []
    with open(url,'r') as f:
        for index,line in enumerate(f.readlines()):
            line = line.replace('\n','')
            lines = line.split(':')
            head = lines[0]
            bodys = lines[1].split()
            cfgid = index + 1
            newcfg = cfg(head,bodys,cfgid)
            cfgs.append(newcfg)
    return cfgs

def get_lr1_cfg0(cfgs):
    """ Docstring for get_lr1_cfg0.
    :cfgs:cfgs
    :returns: lr1_cfg0
    """
    for cfg in cfgs:
        if cfg.id == 1:
            lr1_cfg0 = lr1_cfg(cfg,0,'#')
            return lr1_cfg0

def get_type(B):
    """ Docstring for get_type.
    :B:a string
    :returns: 0 var 1 int
    """
    if str.isdigit(B):
        return 1
    else:
        return 0

def get_B(bodys,current_index):
    """ Docstring for get_B.
    :current_index:the current_index of B
    :returns: B or None
    """
    if current_index > len(bodys) - 1:
        return None
    B = bodys[current_index]
    type_B = get_type(B)
    if type_B == 1:
        return None
    else:
        return B

def get_VTs(cfgs,i):
    VTs = []
    for cfg in cfgs:
        if i == 0:
            if cfg.head not in VTs:
                VTs.append(cfg.head)
        for body in cfg.bodys:
            if get_type(body) == i and body not in VTs:
                VTs.append(body)
    return VTs

def first(cfgs):
    firsts = {}
    Ts = get_VTs(cfgs,1)
    for T in Ts:#2
        firsts[T] = [T]
    Vs = get_VTs(cfgs,0)
    for V in Vs:
        firsts[V] = []

    for V in Vs:
        firsts[V] = []
        a_s = []
        for cfg in cfgs:
            if cfg.head == V and get_type(cfg.bodys[0]) == 1:
                a_s.append(cfg.bodys[0])
        for a in a_s:
            if a not in firsts[V]:
                firsts[V].append(a)
    while True:
        if_change = False
        for V in Vs:
            for cfg in cfgs:
                if cfg.head == V and get_type(cfg.bodys[0]) == 0:
                    for a in firsts[cfg.bodys[0]]:
                        if a not in firsts[V]:
                            if_change = True
                            firsts[V].append(a)
        if if_change == False:
            break

    return firsts


def First(beta_a,cfgs):
    firsts = first(cfgs)
    bs = []
    for element in beta_a:
        if get_type(element) == 1:
            bs.append(element)
            return bs
        else:
            for a in firsts[element]:
                bs.append(a)
            return bs
    return bs

# def lr1_cfg_eual(lr1_cfg1,lr1_cfg2):
#     """Docstring for lr1_cfg_eual.

#     :lr1_cfg1,lr1_cfg2: lr1_cfg waiting to compare
#     :returns: True or False

#     """
#     if lr1_cfg1.cfg == lr1_cfg2.cfg and lr1_cfg1.lookahead == lr1_cfg2.lookahead and lr1_cfg1.current_index == lr1_cfg2.current_index:
#         return True
#     else:
#         return False




def closure(I,cfgs):
    """ Docstring for closure.
    :cfgs:cfgs
    :I:list of lr1_cfg object
    :returns: I
    """
    while True:
        if_change = False
        for lrcfg in I:
            bodys = lrcfg.cfg.bodys
            current_index = lrcfg.current_index
            lookahead  = lrcfg.lookahead
            B = get_B(bodys,current_index)
            if B is None:
                continue
            beta_a = []
            for beta in bodys[current_index+1:]:
                beta_a.append(beta)
            if lookahead != '#':
                beta_a.append(lookahead)
            bs = First(beta_a,cfgs)
            #bs.append('#')#here sharp is a problem
            if len(bs) == 0:
                bs.append('#')
            for cfg in cfgs:
                if cfg.head == B:
                    for b in bs:
                        newlrcfg = lr1_cfg(cfg,0,b)
                        if newlrcfg not in I:
                            I.append(newlrcfg)
                            if_change = True
        if if_change:
            continue
        else:
            break
    return I

def go(I,x,cfgs):
    j = []
    for lrcfg in I:
        cfg = lrcfg.cfg
        current_index = lrcfg.current_index
        lookahead = lrcfg.lookahead
        if current_index == len(cfg.bodys):
            continue
        if cfg.bodys[current_index] == x:
            newlrcfg = lr1_cfg(cfg,current_index+1,lookahead)
            if_add = True
            for lrcfg in j:
                if lrcfg == newlrcfg:
                    if_add = False
                    break
            if if_add:
                j.append(newlrcfg)
    return closure(j,cfgs)

def have(C,i):
    """ Docstring for have.
    :C:list of i
    :i:list of lrc_cfg object
    :returns: True or False
    """
    ifin = -1
    for index,I in enumerate(C):
        if len(I) != len(i):
            continue
        else:
            same = True
            for lc in I:
                if lc not in i:
                    ifin = -1
                    same = False
                    break
            if same:
                ifin = index
                break
    return ifin

def build_lr1_set(cfgs):
    """ Docstring for build_lr1_set.
    :cfgs:G1
    :returns: C
    """
    lr1_cfg0 = get_lr1_cfg0(cfgs)
    C = [closure([lr1_cfg0],cfgs)]
    vs = get_VTs(cfgs,0)
    ts = get_VTs(cfgs,1)
    v_ts = vs + ts
    while True:
        if_change = False
        for I in C:
            for v_t in v_ts:
                i = go(I,v_t,cfgs)
                if len(i)>0 and have(C,i) == -1:
                    C.append(i)
                    if_change = True
                    break
            if if_change:
                break
        if not if_change:
            break
    return C

def build_table(C,cfgs):
    """ Docstring for build_table.
    :C:C
    :cfgs:cfgs
    :returns: action and goto
    """
    action = []
    goto = []
    for index,I in enumerate(C):
        action.append({})
        goto.append({})
    for index,I in enumerate(C):
        for lrcfg in I:#1
            current_cfg = lrcfg.cfg
            current_index = lrcfg.current_index
            lookahead = lrcfg.lookahead
            if current_index < len(current_cfg.bodys):
                a = current_cfg.bodys[current_index]
                if get_type(a) == 1:
                    i = go(I,a,cfgs)
                    locate = have(C,i)
                    if locate == -1:
                        continue
                    else:
                        if not action[index].has_key(a):
                            action[index][a] = 's'+str(locate)
                        else:
                            if action[index][a] == 's'+str(locate):
                                pass
                            else:
                                print 'conflict'
                                exit(0)
            else:#3
                for locate,cfg in enumerate(cfgs):
                    if  cfg == current_cfg:
                        if action[index].has_key(lookahead):
                            if action[index][lookahead] != 'r'+str(locate+1):
                                print 'conflict'
                                exit(0)
                        else:
                            action[index][lookahead] = 'r' + str(locate+1)
                            break


        Vs = get_VTs(cfgs,0)
        for v in Vs:#2
            i = go(I,v,cfgs)
            locate = have(C,i)
            if locate != -1:
                if not goto[index].has_key(v):
                    goto[index][v] = locate
                else:
                    if goto[index][v] != locate:
                        print 'conflict'
                        exit(0)

        final_cfg = get_lr1_cfg0(cfgs)
        final_cfg.current_index += 1
        if final_cfg in I:
            action[index]['#'] = 'acc'
    return action,goto

def lr_analyze(url,action,goto,cfgs):
    """: Docstring for lr_analyze.

    :url:to lex6.py 's product
    :action:
    :goto:
    :cfgs:
    :returns:
    """
    string_buffer = []
    with open(url,'r') as f:
        for line in f.readlines():
            line = line.replace('\n','')
            lines = line.split(',')
            string_buffer.append(lines)
    string_buffer.append(['#','#'])
    number_stack = []
    symbol_stack = []
    number_stack.append('#')
    number_stack.append(0)
    symbol_stack.append(['#','#'])
    ip = 0
    while True:
        s = number_stack[len(number_stack)-1]
        a = string_buffer[ip]
        if action[s][a[0]][0] == 's':
            i = int(action[s][a[0]][1:])
            ip = ip + 1
            symbol_stack.append(a)
            number_stack.append(i)

        elif action[s][a[0]][0] == 'r':
            i = int(action[s][a[0]][1:])
            current_cfg = cfgs[i-1]
            symbols = []
            beta = len(current_cfg.bodys)
            for x in range(beta):
                symbol = symbol_stack.pop()
                symbols.append(symbol)
                number_stack.pop()
            print current_cfg.id,current_cfg.head,current_cfg.bodys
            A = current_cfg.head
            symbol_stack.append([A,A])
            S1 = number_stack[len(number_stack)-1]
            number_stack.append(goto[S1][A])
        elif action[s][a[0]] == 'acc':
            print 'done'
            return
        else:
            print 'error'
            exit(0)



if __name__ == '__main__':
    cfgs = get_cfg('test_cfg')
    #cfgs = get_cfg('CFG_NUM')
    C = build_lr1_set(cfgs)
    action,goto = build_table(C,cfgs)
    lr_analyze('my_result',action,goto,cfgs)
