def convert(info):
    info = str(info)

    if info[0].isalpha():
        return info.lower()
    
    menor = False

    if "-" in info:
        menor = True
        info = info[1:]

    if "," in info:
        info_int, sep, info_dec = info.partition(",")
        info_int = int(info_int)

        if "%" in info_dec:
            info_dec = info_dec[:len(info_dec) - 1]
            info_dec = int(info_dec)/100
            info = round((info_int + info_dec) / 100, 4)
        else:
            info_dec = round(int(info_dec)/100, 2)
            info = info_int + info_dec
    else:
        info = info + "0"
        algarismos = ""

        for i in info.split("."):
            algarismos += i
        
        valor = 0

        for i in range(len(algarismos)):
            diferenca = len(algarismos) - (i+1)
            valor += int(algarismos[i]) * 10 ** diferenca
        
        info = valor

    if menor == True:
        return -1 * info
    
    return info     