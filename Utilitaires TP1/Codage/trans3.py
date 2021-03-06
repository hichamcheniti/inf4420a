#!/usr/bin/env python
import sys
from Crypto import Random
from Crypto.Cipher import DES
from Crypto.Util.number import long_to_bytes
from time import time


def main(argv=None):
    """
    Ce script implemente le codeur 3 suivi du chiffrement DES
    Usage:
        trans3 nouveauNIP ancienNIP

    Les NIPs doivent avoir exactement 4 chiffres
    """
    if argv is None:
        argv = sys.argv

    if len(argv) != 3:
        print 'Erreur de syntaxe'
        print main.__doc__
        return 1

    pin = argv[1]
    oldpin = argv[2]
    if (len(pin) != 4 or not(pin.isdigit()) or len(oldpin) != 4
            or not(oldpin.isdigit())):
        print "Les NIPs doivent avoir exactement 4 chiffres"
        return 2

    timestamp = long_to_bytes(int(time()))

    pin_bin = bin(int(pin))[2:].zfill(14)
    pin_bin += str(pin_bin[:7].count('1') % 2)
    pin_bin += str(pin_bin[7:].count('1') % 2)

    oldpin_bin = bin(int(oldpin))[2:].zfill(14)
    oldpin_bin += str(oldpin_bin[:7].count('1') % 2)
    oldpin_bin += str(oldpin_bin[7:].count('1') % 2)

    code = chr(int(pin_bin[:8], 2)) \
        + chr(int(pin_bin[8:], 2)) \
        + chr(int(oldpin_bin[:8], 2)) \
        + chr(int(oldpin_bin[8:], 2)) \
        + '\x00' * (4 - len(timestamp)) \
        + timestamp

    # Cle generee par Random.new().read(DES.key_size)
    key = '\xe8\x8e\x0e\x16-\x88\xf6\x10'

    # IV genere par Random.new().read(DES.block_size)
    iv = '\x9a=\xa7#+\x85\xf3\xab'

    cipher = DES.new(key, DES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(code)
    sys.stdout.write(ciphertext)

if __name__ == '__main__':
    main()
