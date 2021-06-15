import random
# min ascii accepted: 32 (espace)
# max ascii accepted: 126 (| ~)
class Encrp_class():
    def encriptar(strng):
        llave = ''
        strng_enc = ''
        for c in strng:
            num = random.randint(0,57)
            llave = chr(num+32) + llave
            enc = ord(c) + num
            if(enc > 127):
                enc = 32 + (enc)%127
            strng_enc += chr(enc)

        return [strng_enc,llave]
    def desencriptar(llave, strng_enc):
        strng = ''
        l = len(llave)
        for c in strng_enc:
            num = ord(llave[l - 1]) - 32
            des = ord(c) - num
            if(des < 32):
                des = 127 + des - 32
            strng += chr(des)
            l -= 1
        return strng

def test():
    text = 'Hola mundo!'
    enc_text, llave = Encrp_class.encriptar(text)
    desenc_text = Encrp_class.desencriptar(llave, enc_text)
    print('texto: ' + text)
    print('texto encriptado: ' + enc_text)
    print('llave: ' + llave)
    print('texto desencriptado: ' + desenc_text)
    return True

if __name__ == '__main__':
    test()
