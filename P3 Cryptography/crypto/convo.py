"""
TDT4113 - Computer Science, Programming Project (Spring 2021)
Project 3 Cryptography
made with ❤ by mathiom

Test environment for encrypted conversations
"""

from termcolor import colored
from ciphers import CaesarCipher, MultiplicationCipher, AffineCipher, UnbreakableCipher
from persons import Sender, Receiver, Hacker

TEST_MESSAGE = "The quick brown fox jumps over the lazy dog"

for cipher in [
    CaesarCipher(17),
    MultiplicationCipher(34525),
    AffineCipher(143, 2132),
    UnbreakableCipher("cherrypicked"),
]:
    print(f"Conversation with {cipher.__class__.__name__}")

    keys = cipher.generate_keys()

    sender = Sender()
    sender.set_key(keys[0])
    encoded_message = sender.operate_cipher(cipher, TEST_MESSAGE)
    print(colored(f"\tSender's encoded message: {colored(encoded_message, 'cyan')}","white"))

    receiver = Receiver()
    receiver.set_key(keys[1])
    decoded_message = receiver.operate_cipher(cipher, encoded_message)
    print(colored(f"\tReceiver's decoded message: {colored(decoded_message, 'green')}","white"))

    print(colored("\r\tHacking...", "white"), end="")
    hacker = Hacker()
    hacked_message = hacker.operate_cipher(cipher, encoded_message)
    if hacked_message == decoded_message:
        print(colored("\r\tHacker brute forced ✔\n", "magenta"))
    else:
        print(colored("\r\tHacker failed ❌\n", "red"))
