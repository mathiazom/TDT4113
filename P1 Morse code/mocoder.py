"""
TDT4113 - Computer Science, Programming Project (Spring 2021)
Project 1 Morse Code
made with ❤ by mathiom
"""

import time
from termcolor import colored
from GPIOSimulator_v1 import GPIOSimulator, \
    PIN_BLUE_LED, PIN_RED_LED_0, PIN_RED_LED_1, PIN_RED_LED_2, PIN_BTN

# Simulator for button and LEDs
GPIO = GPIOSimulator()


def update_gpio_leds(blue, red):
    """Helper to update LEDs in bulk"""
    GPIO.output(PIN_BLUE_LED, GPIO.HIGH if blue else GPIO.LOW)
    GPIO.output(PIN_RED_LED_0, GPIO.HIGH if red else GPIO.LOW)
    GPIO.output(PIN_RED_LED_1, GPIO.HIGH if red else GPIO.LOW)
    GPIO.output(PIN_RED_LED_2, GPIO.HIGH if red else GPIO.LOW)


MORSE_CODE = {
    '.-': 'a',
    '-...': 'b',
    '-.-.': 'c',
    '-..': 'd',
    '.': 'e',
    '..-.': 'f',
    '--.': 'g',
    '....': 'h',
    '..': 'i',
    '.---': 'j',
    '-.-': 'k',
    '.-..': 'l',
    '--': 'm',
    '-.': 'n',
    '---': 'o',
    '.--.': 'p',
    '--.-': 'q',
    '.-.': 'r',
    '...': 's',
    '-': 't',
    '..-': 'u',
    '...-': 'v',
    '.--': 'w',
    '-..-': 'x',
    '-.--': 'y',
    '--..': 'z',
    '.----': '1',
    '..---': '2',
    '...--': '3',
    '....-': '4',
    '.....': '5',
    '-....': '6',
    '--...': '7',
    '---..': '8',
    '----.': '9',
    '-----': '0'}

SYMBOL_NOT_RECOGNIZED = "?"

# Unit signal duration
T = 0.3

# Duration definitions (adjusted for ease of use)
DOT_DURATION = 1 * T
DASH_DURATION = 3 * T
SYMBOL_PAUSE_DURATION = 4.5 * T
WORD_PAUSE_DURATION = 8 * T
MESSAGE_END_DURATION = 15 * T

# Signal definitions
DOT = "."
DASH = "-"
SYMBOL_PAUSE = "*"  # a space isn't very readable
WORD_PAUSE = "/"
MESSAGE_END = "$"


class MorseDecoder:
    """Input listener that interprets button presses and releases as morse code
    and converts it to messages"""

    current_word = None
    current_symbol = None
    current_message = None

    # Timestamps to determine press and pause durations
    pressed_timestamp = None
    released_timestamp = None

    # Most recent inputs to check input stability and mitigate GPIO inaccuracy (spikes)
    # The more inputs remembered the less likely it is for a spike to mess things up,
    # but this also increases the input delay
    recent_inputs = None

    def __init__(self):
        self.reset()

    def start(self):
        """Main loop continuously processing button signals"""
        while True:
            signal = self.read_one_signal()
            self.process_signal(signal)

    def reset(self):
        """ Reset variables for a new message """
        self.current_word = ""
        self.current_symbol = ""
        self.current_message = ""
        self.pressed_timestamp = None
        self.released_timestamp = None
        self.recent_inputs = [None] * 5

    def process_signal(self, signal):
        """Delegate signal to appropriate functions"""
        if signal in [DOT, DASH]:
            self.update_current_symbol(signal)
        elif signal == SYMBOL_PAUSE:
            self.handle_symbol_end()
        elif signal == WORD_PAUSE:
            self.handle_symbol_end()
            self.handle_word_end()
        elif signal == MESSAGE_END:
            self.handle_symbol_end()
            self.handle_word_end()
            self.handle_message_end()
        else:
            raise Exception("Signal not recognized", signal)

    def read_one_signal(self):
        """Read a signal from Raspberry Pi"""
        signal = None
        while signal is None:

            btn_input = GPIO.input(PIN_BTN)

            if not self.input_is_stable(btn_input):
                # Discard input as GPIO inaccuracy
                continue

            if btn_input == GPIO.PUD_DOWN:
                # Check if space has just been pressed
                if self.pressed_timestamp is None:
                    signal = self.process_button_press()
            elif btn_input == GPIO.PUD_UP:
                # Check if space has just been released
                if self.released_timestamp is None:
                    signal = self.process_button_release()
                # Else check if time since latest release is very large
                elif self.released_timestamp is not None and \
                        time.time() - self.released_timestamp > MESSAGE_END_DURATION:
                    # Register message end
                    signal = MESSAGE_END
            else:
                raise Exception("Button input not recognized", btn_input)

        return signal

    def process_button_press(self):
        """Process the event where the button has just been pressed"""
        signal = None
        current_timestamp = time.time()

        # Check if space has been released before
        if self.released_timestamp is not None:
            # Calculate pause duration
            pause_duration = current_timestamp - self.released_timestamp
            # Translate duration to signal
            if MESSAGE_END_DURATION > pause_duration >= WORD_PAUSE_DURATION:
                signal = WORD_PAUSE
            elif pause_duration >= SYMBOL_PAUSE_DURATION:
                signal = SYMBOL_PAUSE

        # Register timestamp to mark the start of the next button press period
        self.pressed_timestamp = current_timestamp
        # Discard timestamp to mark the end of the previous pause
        self.released_timestamp = None

        return signal

    def process_button_release(self):
        """Process the event where the button has just been released"""

        # Check if this is the start of the message (aka no input)
        if self.pressed_timestamp is None:
            return None

        # Calculate duration of button press
        current_timestamp = time.time()
        press_duration = current_timestamp - self.pressed_timestamp

        # Translate press duration to signal
        if press_duration <= DOT_DURATION:
            signal = DOT
        else:
            signal = DASH

        # Register timestamp to mark the start of the next pause
        self.released_timestamp = current_timestamp
        # Discard timestamp to mark the end of the previous button press period
        self.pressed_timestamp = None

        return signal

    def update_current_symbol(self, signal):
        """Append new signal to current symbol"""
        if signal == DOT:
            print(colored(f"Signal: {signal} (dot)", "cyan"))
            update_gpio_leds(True, False)
        else:
            print(colored(f"Signal: {signal} (dash)", "cyan"))
            update_gpio_leds(False, True)
        self.current_symbol += signal

    def handle_symbol_end(self):
        """Translate current symbol and append to current word"""
        decoded_symbol = self.decode_symbol(self.current_symbol)
        print(
            colored(
                f"Completed symbol: {self.current_symbol} -> {decoded_symbol}",
                "blue"))
        update_gpio_leds(False, False)
        self.current_word += decoded_symbol
        self.current_symbol = ""

    def handle_word_end(self):
        """Append current word to current message"""
        print(colored(f"Completed word: {self.current_word}", "magenta"))
        self.current_message += self.current_word + " "
        self.current_word = ""

    def handle_message_end(self):
        self.display_message()
        self.reset()

    def display_message(self):
        print(colored(f"Final message: {self.current_message}", "green"))

    def input_is_stable(self, inp):
        """Check if input is equal to recent inputs (aka stable)"""
        # Update recent inputs
        self.recent_inputs = [inp] + self.recent_inputs[:-1]
        # Evaluate current input stability (aka homogeneity)
        return self.recent_inputs.count(inp) == len(self.recent_inputs)

    @staticmethod
    def decode_symbol(symbol):
        """Translate morse symbol to text"""
        if symbol in MORSE_CODE:
            return MORSE_CODE[symbol]
        print(colored(f"Symbol not recognized {symbol}", "red"))
        return SYMBOL_NOT_RECOGNIZED


def main():
    """Set up GPIO simulator and prepare for listening"""
    GPIO.setup(PIN_BTN, GPIO.IN, GPIO.LOW)
    decoder = MorseDecoder()
    test(decoder)
    decoder.start()


def test(decoder):
    test_pattern(decoder, "....*.*.-..*.-..*---/.--*---*.-.*.-..*-..$")  # "hello world"
    test_pattern(decoder, "...*.-*.-..*..-*-*---*-./--*---*-.*-..*---$")  # "saluton mondo"


def test_pattern(decoder, pattern):
    """Feed decoder with test signals"""
    for signal in pattern:
        decoder.process_signal(signal)


if __name__ == "__main__":
    main()
