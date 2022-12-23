
def put_featureReturn(t):
    output = '{\"name\" : \"' + t[1] + '\",\"args\" : [],\"instrs\" : ['
    return output

def put_MethodFunction(t):
    if t[1] == 'out_int':
        return '{\"op\":\"print\",\"args\": [' + str(t[2][0][1]) + ']},'
    output = '{\"op\":\"print\",\"args\": ['
    for id in t[2]:
        output+= str(id[1]) + ' '
    output = output [:-1] + ']}]}'
    return output

