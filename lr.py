#use lr(1)

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


def build_lr1(url):
    cfgs = get_cfg(url)








if __name__ == '__main__':
    build_lr1('CFG_NUM')

