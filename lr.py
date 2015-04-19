#use lr(1)
from get_first import one_first,First
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
            '''
            print e['id']
            print e['cfg_head']
            print e['cfg_bodys']
            '''
            cfgs.append(e)

        return cfgs

def get_B(element):
    begin = element['index']
    B = None
    for index,body in enumerate(element['e']['cfg_bodys']):
        if index >= begin:
            try:
                num = int(body)
            except:
                if B != '#':
                    B = body
                    return B,index
    return B,-1

def get_first(element,index):
    begin = index
    ret = []
    for index,body in enumerate(element['e']['cfg_bodys']):
        if index > begin:
            ret.append(body)
    ret.append(element['lookahead'])
    return ret

def get_closure(cfgs):
    firsts = one_first(cfgs)#get first set
    print firsts
    clousure = []
#C:=I
    for e in cfgs:
        if e['id'] == '0':
            s = {}
            s['lookahead'] = '#'
            s['e'] = e
            s['index'] = 0
            clousure.append(s)
            break
#repeat
    ifchange = True
    lenth = len(clousure)
    while ifchange:
        for element in clousure:
            B,index = get_B(element)#get B
            #print 'b',B
            if B is None:
                pass
            else:
                first = get_first(element,index)#get [beta,a]
                #print 'first', first
                bs = First(first,cfgs,firsts)
                #print 'bs',bs
                B_heads = []
                for cfg in cfgs:
                    if cfg['cfg_head'] == B:
                        B_heads.append(cfg)
                for cfg in B_heads:
                    for b in bs:
                        ifadd = True
                        for s in clousure:
                            if s['index'] == 0 and s['e'] == cfg and s['lookahead'] == b:
                                ifadd = False
                                break
                        if ifadd:
                            s ={}
                            s['lookahead'] = b
                            s['e'] = cfg
                            s['index'] = 0
                            clousure.append(s)

        if len(clousure) == lenth:
            ifchange = False
        else:
            lenth = len(clousure)
    return clousure
       

def build_lr1(url):
    cfgs = get_cfg(url)
    #clousure = get_closure(cfgs)
    #print clousure
    firsts = one_first(cfgs)
    print firsts









if __name__ == '__main__':
    build_lr1('first_test')

