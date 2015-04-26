def top(ls):
    return ls[len(ls)-1]

def analyze(action,goto,cfgs):
    __doc__ = 'use action and lr to analyze the result from lex'

    numbers_stack = []
    string_buffer = []
    symbols_stack = []

    numbers_stack.append(0)
    symbols_stack.append('#')

    with open('test_result','r') as f:#read lex result
        for line in f.readlines():
            line = line.replace('\n','')
            ls = line.split(',')
            string_buffer.append(ls[0])

    string_buffer.append('#')
    #print string_buffer
    ip = 0
    while True:
    #    pdb.set_trace()
        s = top(numbers_stack)
        a = string_buffer[ip]
        s_r = None

        try:
            s_r = action[s][a]
        except:
            print 'former error'
            return
        #print 's_r',s_r
        #print numbers_stack
        #print symbols_stack

        if s_r[0] == 's':
            num = -1
            try:
                num = int(s_r[1:])
            except:
                print 'former error'
                break
            numbers_stack.append(num)
            symbols_stack.append(a)
            ip += 1
        elif s_r[0] == 'r':
            cfg_id = -1
            try:
                cfg_id = int(s_r[1:])
            except:
                print 'former error'
                return

            current_cfg = None
            for cfg in cfgs:
                if int(cfg['id']) == cfg_id:
                    current_cfg = cfg
            if current_cfg is None:
                print 'can\'t find cfg'
                return

            beta = len(current_cfg['cfg_bodys'])
            for i in range(beta):
                numbers_stack.pop()
                symbols_stack.pop()

            symbols_stack.append(current_cfg['cfg_head'])
            s1 = top(numbers_stack)
            new_number = -1
            try:
                new_number = goto[s1][current_cfg['cfg_head']]
            except:
                print 'r error'
                return
            numbers_stack.append(new_number)
            print 'cfg_id',current_cfg['id'],'symbols_stack',symbols_stack

        elif s_r == 'acc':
            print 'done'
            return

        else:
            print 'error'
            return

