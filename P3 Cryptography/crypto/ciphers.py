"""
TDT4113 - Computer Science, Programming Project (Spring 2021)
Project 3 Cryptography
made with ❤ by mathiom

Collection of ciphers
"""

from random import randint
import math
from termcolor import colored
from utils.crypto_utils import \
    modular_inverse, generate_random_prime, blocks_from_text, text_from_blocks

# Message to be used in cipher verification
VERIFY_MESSAGE = "The quick brown fox jumps over the lazy dog"

ALPHABET_START = 32
ALPHABET_END = 126
ALPHABET = [chr(i) for i in range(ALPHABET_START, ALPHABET_END + 1)]
ALPHABET_SIZE = ALPHABET_END - ALPHABET_START


def wrap_to_alphabet(ordinal):
    """Convert number to letter within alphabet (with wrapping)"""
    return ALPHABET[ordinal % ALPHABET_SIZE]


class Cipher:
    """Generic cipher using encode and decode key pairs"""

    def encode(self, message, key):
        """Return coded text"""
        raise NotImplementedError("Method not implemented")

    def decode(self, code, key):
        """Return original text"""
        raise NotImplementedError("Method not implemented")

    def generate_keys(self):
        """Generate matching keys"""
        raise NotImplementedError("Method not implemented")

    @staticmethod
    def possible_keys():
        """All possible key values for cipher use"""

    def verify(self, encode_key, decode_key):
        """Make sure decoding returns original text of encoded message"""
        encoded = self.encode(VERIFY_MESSAGE, encode_key)
        print(colored(encoded, "magenta"))
        decoded = self.decode(encoded, decode_key)
        print(colored(decoded, "cyan"))
        return decoded == VERIFY_MESSAGE


class CaesarCipher(Cipher):
    """Cipher utilizing shifting of character ASCII-codes (with wrapping)"""

    def __init__(self, shift):
        super().__init__()
        self.shift = shift

    def generate_keys(self):
        return self.shift, ALPHABET_SIZE - self.shift

    def encode(self, message, key):
        return self.shift_each(message, key)

    def decode(self, code, key):
        return self.shift_each(code, key)

    @staticmethod
    def shift_each(text, amount):
        """Perform shift on characters one by one"""
        return "".join([wrap_to_alphabet(ALPHABET.index(c) + amount) for c in text])

    @staticmethod
    def possible_keys():
        return list(range(ALPHABET_SIZE))


class MultiplicationCipher(Cipher):
    """Cipher utilizing multiplication of character ASCII-codes (with wrapping)"""

    def __init__(self, multiplier):
        super().__init__()
        self.multiplier = multiplier

    def generate_keys(self):
        return self.multiplier, modular_inverse(self.multiplier, ALPHABET_SIZE)

    def encode(self, message, key):
        return self.multiply_each(message, key)

    def decode(self, code, key):
        return self.multiply_each(code, key)

    @staticmethod
    def multiply_each(text, multiplier):
        """Perform multiplication and wrapping on each charachter"""
        return "".join([wrap_to_alphabet((ALPHABET.index(c)) * multiplier) for c in text])

    @staticmethod
    def possible_keys():
        return list(range(ALPHABET_SIZE))


class AffineCipher(Cipher):
    """Combination of Caesar and Multiplication cipher"""

    def __init__(self, key1, key2):
        super().__init__()
        self.c_cipher = CaesarCipher(key1)
        self.m_cipher = MultiplicationCipher(key1)
        self.c_key = key1
        self.m_key = key2

    def generate_keys(self):
        c_keys = self.c_cipher.generate_keys()
        m_keys = self.m_cipher.generate_keys()
        return (c_keys[0], m_keys[0]), (c_keys[1], m_keys[1])

    def encode(self, message, key):
        return self.m_cipher.encode(self.c_cipher.encode(message, key[0]), key[1])

    def decode(self, code, key):
        return self.c_cipher.decode(self.m_cipher.decode(code, key[1]), key[0])

    @staticmethod
    def possible_keys():
        return [(a, b) for a in CaesarCipher.possible_keys()
                for b in MultiplicationCipher.possible_keys()]


def values_from_text(text):
    """Map text characters to alphabet indices"""
    return [(ord(k) - ALPHABET_START) % ALPHABET_SIZE for k in text]


def text_from_values(values):
    """Map indices (from values_from_text()) to alphabet characters"""
    return "".join([ALPHABET[v] for v in values])


class UnbreakableCipher(Cipher):
    """Cipher utilizing a secret keyword"""

    def __init__(self, keyword):
        super().__init__()
        self.keyword = keyword

    def generate_keys(self):
        e_numeric = values_from_text(self.keyword)
        d_numeric = [ALPHABET_SIZE - e for e in e_numeric]
        return self.keyword, text_from_values(d_numeric)

    def encode(self, message, key):
        return self.shift_with_keyword(message, key)

    def decode(self, code, key):
        return self.shift_with_keyword(code, key)

    @staticmethod
    def shift_with_keyword(text, keyword):
        """Perform shift on each text character decided individually by keyword values"""
        t_numeric = values_from_text(text)
        k_numeric = repeat_list_to_length(values_from_text(keyword), len(t_numeric))
        s_numeric = [(t + k) % ALPHABET_SIZE for t, k in zip(t_numeric, k_numeric)]
        return text_from_values(s_numeric)

    @staticmethod
    def possible_keys():
        file = open("english_words.txt", "r")
        words = file.read().splitlines()
        file.close()
        return words


class RSACipher(Cipher):
    """Cipher utilizing large primes and modular inverse to generate random keys"""

    BITS = 64
    BLOCK_SIZE = 16

    def generate_keys(self):

        # Retrieve unique prime numbers
        q = None
        p = generate_random_prime(self.BITS)
        while q is None or q == p:
            q = generate_random_prime(self.BITS)

        # Generate compatible private and public keys
        e = None
        phi = None
        gcd = None
        while gcd != 1:
            phi = (p - 1) * (q - 1)
            e = randint(3, phi - 1)
            gcd = math.gcd(e, phi)
        d = modular_inverse(e, phi)
        n = p * q
        return (e, n), (d, n)

    def encode(self, message, key):
        blocks = blocks_from_text(message, self.BLOCK_SIZE)
        return [self.encode_int(i, key) for i in blocks]

    def decode(self, code, key):
        return text_from_blocks([self.decode_int(c, key) for c in code], self.BITS)

    @staticmethod
    def encode_int(i, public_key):
        """Encode a single integer using public key"""
        return pow(i, *public_key)

    @staticmethod
    def decode_int(c, private_key):
        """Decode a single integer using private key"""
        return pow(c, *private_key)


def repeat_list_to_length(lst, length):
    """Repeat list elements until it has reached a given length
       return truncated version of the list in case the list is
       longer than given length"""
    repeated = lst[:]
    list_len = len(lst)
    if length > list_len:
        for i in range(length - list_len):
            repeated.append(lst[i % list_len])
    else:
        repeated = lst[:length]
    return repeated


def verify_ciphers():
    """Perform encoding and decoding to check if
    final message equals original message"""
    for cipher in [
        CaesarCipher(5),
        MultiplicationCipher(9),
        AffineCipher(3, 2),
        UnbreakableCipher("UNBREAKABLE"),
        RSACipher()
    ]:
        if cipher.verify(*cipher.generate_keys()):
            print(colored(f"{cipher.__class__.__name__} verified ✔\n", "green"))
        else:
            print(colored(f"{cipher.__class__.__name__} failed ❌\n", "red"))


verify_ciphers()
