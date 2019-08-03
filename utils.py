def get_arg_value(args, arg_name):
    for arg in args:
        for index in list(range(len(arg))):
            if index == len(arg_name) and arg[index] == '=':
                return arg[index+1:]
            elif index == len(arg_name):
                return ''
            elif arg[index] != arg_name[index]:
                break
    return ''
