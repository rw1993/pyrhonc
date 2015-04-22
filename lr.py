#use lr(1)
from get_first import one_first,First,ifT
from lr_analyze import analyze

def get_cfg(url):

    cfgs = []
    '''
    cfgs is a list contains cfg read from the url,the element in it should be  a dict like below:
    {
        'cfg_head':string,
        'cfg_bodys':[string,string,...]
        'id':a number CFG file will give
    }
    '''

    with open(url,'r') as f:

        for line in f.readlines():
            string = line.replace('\n',"")
            strings = string.split(':')
            head = strings[0]
            cfg_id = head[0]
            cfg_head = head.split()[1]
            bodys = strings[1].split()
            e = {}
            e['id'] = cfg_id
            e['cfg_head'] = cfg_head
            e['cfg_bodys'] = bodys
            cfgs.append(e)

        return cfgs

def get_B(element):
    begin = element['index']
    B = None
    for index,body in enumerate(element['e']['cfg_bodys']):
        if index == begin:
            try:
                num = int(body)
            except:
                if body != '#':
                    B = body
                    return B,index
    return B,-1

def get_first(element,begin):
    ret = []
    for index,body in enumerate(element['e']['cfg_bodys']):
        if index > begin:
            ret.append(body)
    ret.append(element['lookahead'])
    return ret

def get_closure(closure,cfgs):#i=[{s:.s1,#}] cfgs is cfgs
    firsts = one_first(cfgs)#get first set
    #repeat
    lenth = len(closure)
    while True:
        for c in closure:
            B,index = get_B(c)
            if B:
                beta_a = get_first(c,index)
                bs = First(beta_a,cfgs,firsts)
            else:
                continue
            for cfg in cfgs:
                if cfg['cfg_head'] == B:
                    for b in bs:
                        newc = {}
                        newc['lookahead'] = b
                        newc['index'] = 0
                        newc['e'] = cfg
                        if newc in closure:
                            pass
                        else:
                            closure.append(newc)
        if lenth == len(closure):
            break
        else:
            lenth = len(closure)
    return closure

    
def build_lr1_set(cfgs):
    i = []
    for e in cfgs:#s1:.s,#
        if e['id'] == '1':
            s = {}
            s['lookahead'] = '#'
            s['e'] = e
            s['index'] = 0
            i.append(s)
            break
    c = []
    c.append(get_closure(i,cfgs))#c:=[closure[begin]]
    ifchange = True
    v_t = get_v_t(cfgs)
    while ifchange:
        ifchange = False
        for i in c:
            for x in v_t:
                g = go(i,x,cfgs)
                if len(g)>0 and g not in c:
                    c.append(g)
                    ifchange = True
    return c

def get_v_t(cfgs):
    a = []
    for e in cfgs:
        if e['cfg_head'] not in a:
            a.append(e['cfg_head'])
        for body in e['cfg_bodys']:
            if body not in a:
                a.append(body)
    return a

def build_table(c,cfgs):
    action = []
    goto = []
    for index,i in enumerate(c):
        action.append({})
        goto.append({})
    for index,i in enumerate(c):
        for s in i:#1
            sindex = s['index']
            cfg = s['e']
            lookahead = s['lookahead']
            if sindex < len(cfg['cfg_bodys']):
                a = cfg['cfg_bodys'][sindex]
                if ifT(a) == 0:
                    g = go(i,a,cfgs)
                    if g in c:
                        j = c.index(g)
                        action[index][a] = 's'+str(j)
        
        var_list = get_var(cfgs)
        for var in var_list:#2
            g = go(i,var,cfgs)
            if g in c:
                l = c.index(g)
                goto[index][var] = l

        for s in i:#3
            sindex = s['index']
            cfg = s['e']
            lookahead = s['lookahead']
            if sindex == len(cfg['cfg_bodys']):
                j = cfg['id']
                '''
                tmp = 'r' +str(j)
                try:
                   tmp1 = action[index][lookahead]
                   if tmp1 != tmp:
                       print 'error'
                       exit(0)
                except:
                    pass
                '''
                action[index][lookahead] = 'r'+str(j)
        s = {}
        for e in cfgs:
            if e['id'] == '1':
                s['lookahead'] = '#'
                s['e'] = e
                s['index'] = 1
        if s in i:
            action[index]['#'] = 'acc'

    return action,goto

def get_var(cfgs):
    var_list = []
    for cfg in cfgs:
        if cfg['cfg_head'] not in var_list:
            var_list.append(cfg['cfg_head'])
    return var_list

def build_lr1(url):
    cfgs = get_cfg(url)
    c = build_lr1_set(cfgs)#C:=closure({s1:.s,#})
    action,goto = build_table(c,cfgs)
    print action
    print goto
    analyze(action,goto,cfgs)

def go(i,var,cfgs):
    j = []
    for s in i:
        if var in s['e']['cfg_bodys']:
            if s['e']['cfg_bodys'].index(var) == s['index'] and s['e']['cfg_bodys'] != '#':
                ifadd = True
                news = {}
                news['lookahead'] = s['lookahead']
                news['e'] = s['e']
                news['index'] = s['index'] + 1
                for js in j:
                    if js == news:
                        ifadd = False
                        break
                if ifadd:
                    j.append(news)
    return get_closure(j,cfgs)

if __name__ == '__main__':
    build_lr1('test_cfg')

