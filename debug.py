def recursuve_roemer(dezimal,erg=""):
    zeichen = [(1000,"M"),(500,"D"),(100,"C"),(50,"L"),(10,"X"),(5,"V"),(1,"I")]
    if dezimal == 0:
        return erg
    else:
        for zahl,symbol in zeichen:
            if dezimal >= zahl:
                print(zahl)
                erg += symbol
                return recursuve_roemer(dezimal - zahl,erg)


print(recursuve_roemer(14))

