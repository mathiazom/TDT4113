"""
TDT4113 - Computer Science, Programming Project (Spring 2021)
Project 3 Cryptography
made with ❤ by mathiom

Collection of person classes
"""

from ciphers import CaesarCipher, MultiplicationCipher, AffineCipher, UnbreakableCipher


class Person:
    """Represents an entity taking part in an encrypted conversation"""

    def __init__(self):
        self.key = None

    def set_key(self, key):
        """Provide key to be used in conversation"""
        self.key = key

    def get_key(self):
        """Retrieve key"""
        return self.key

    def operate_cipher(self, cipher, text):
        """Take the appropriate cipher action on the given text"""
        raise NotImplementedError("Method not implemented")


class Sender(Person):
    """The person that encodes and sends the message"""

    def operate_cipher(self, cipher, text):
        return cipher.encode(text, self.key)


class Receiver(Person):
    """The person that receives and decodes a coded message"""

    def operate_cipher(self, cipher, text):
        return cipher.decode(text, self.key)


class Hacker(Receiver):
    """Person attempting to decode message by brute force"""

    def __init__(self):
        super().__init__()
        file = open("english_words.txt", "r")
        self.words = set(file.read().splitlines())
        file.close()

    def operate_cipher(self, cipher, text):
        """Delegate brute force to appropriate cipher"""
        possible_keys = cipher.possible_keys()
        if isinstance(cipher, CaesarCipher):
            return self.brute_force(possible_keys, CaesarCipher, text)
        if isinstance(cipher, MultiplicationCipher):
            return self.brute_force(possible_keys, MultiplicationCipher, text)
        if isinstance(cipher, AffineCipher):
            # lambda needed to unpack the two keys
            return self.brute_force(possible_keys, lambda key: AffineCipher(*key), text)
        if isinstance(cipher, UnbreakableCipher):
            return self.brute_force(possible_keys, UnbreakableCipher, text)
        raise Exception("Cipher not recognized", cipher.__class__)

    def brute_force(self, possible_keys, cipher_constructor_with_key, text):
        """Attempt to decode the message by checking every possible key value"""
        for key in possible_keys:
            cipher = cipher_constructor_with_key(key)
            self.set_key(cipher.generate_keys()[1])
            decoded = super().operate_cipher(cipher, text)
            # Check if decoded words are all valid english
            decoded_words = [str.lower(s) for s in decoded.split(" ")]
            if set(decoded_words).issubset(self.words):
                # Found correct key (probably...)
                return decoded
        return None
