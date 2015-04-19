
def ifT(var):
    try:
        num = int(var)
        return 0
    except:
        if var == '#':
            return 1
        else:
            return 2

def union(fs,var):
    if var in fs:
        return False
    else:
        fs.append(var)
        return True
def specil_union(l1,l2):
    ifadd = False
    for l in l2:
        if l in l1 or l == '#':
            pass
        else:
            l1.append(l)
            ifadd = True
    return ifadd

def First(first,cfgs,firsts):
    bs = []
    begin = first[0]
    specil_union(bs,firsts[begin])
    k = 0
    while '#' in firsts[first[k]] and k < len(first) - 1:
        specil_union(bs,firsts[first[k]])
        k += 1
    if k == len(first) -1 and '#' in firsts[first[k]]:
        bs.append('#')
    return bs

def one_first(cfgs):
    '''
    return a dict
    {
        'varname':fs list []
    }
    '''
    first = {}
    vars_list = []
    for cfg in cfgs:#get every var
        union(vars_list,cfg['cfg_head'])
    
    for cfg in cfgs:#get every T
        for body in cfg['cfg_bodys']:
            if ifT(body) == 0 or ifT(body) == 1:
                first[body] = [body]
    
    for var in vars_list:#4,5
        fs = []
        var_cfg = []
        for cfg in cfgs:
            if cfg['cfg_head'] == var:
                var_cfg.append(cfg)

        for cfg in var_cfg:
            f = cfg['cfg_bodys'][0]
            if ifT(f) == 1 or ifT(f) == 0:
                union(fs,f)
        first[var] = fs
    
    ifchange = True
    while ifchange:
        ifchange = False

        for var in vars_list:
            var_cfg = []
            for cfg in cfgs:
                if cfg['cfg_head'] == var:
                    var_cfg.append(cfg)

            for cfg in var_cfg:#7
                f = cfg['cfg_bodys'][0]
                if ifT(f) == 2:
                    tmp = specil_union(first[var],first[f])
                    if   tmp == True:
                        ifchange = True

            for cfg in var_cfg:##8,9
                sharp_index = -1
                for index,body in enumerate(cfg['cfg_bodys']):
                    if ifT(body) == 2 and '#' in first[body]:
                        sharp_index = index
                    else:
                        break
                #print 'out',sharp_index
                if sharp_index >= 0:
                    for body in cfg['cfg_bodys'][1:sharp_index]:
                        #print 'in',sharp_index
                        tmp = specil_union(first[var],first[body])
                        if tmp:
                            ifchange = tmp
                if sharp_index == len(cfg['cfg_bodys'])-1:
                    tmp = specil_union(first[var],['#'])
                    if tmp:
                        ifchange = tmp
    return first



    



         




       











