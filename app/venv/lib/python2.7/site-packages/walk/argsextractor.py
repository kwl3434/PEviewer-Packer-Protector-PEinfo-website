import sys
import getopt

from functools import reduce

def filter_args(argv:list, opts:list):
    shortopts = list(map(lambda o: o[0], opts))
    shortopts_str = reduce(lambda a,b: a + b, shortopts)

    longopts = list(map(lambda o: o[1], opts))
    try:
        found_opts = getopt.getopt(argv[1:], shortopts_str, longopts)
    except getopt.GetoptError as e:
        print(e)
        sys.exit(2)

    # filter args
    opts_map = {}
    for opt in opts:
        s_opt = opt[0].replace(':', '')
        l_opt = opt[1].replace('=', '')
        opts_map[s_opt] = opt[1]
        opts_map[l_opt] = opt[1]
    
    args = {}
    for oa in found_opts[0]:
        key = opts_map[oa[0].replace('-', '')]
        if key in args:
            args[key].append(oa[1].strip())
        else:    
            args[key] = [oa[1].strip()]

    return args