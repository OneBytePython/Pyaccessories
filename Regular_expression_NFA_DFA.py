# Custom exception for illegal characters
class DfaIllegalCharacter(Exception):
    pass

# DFA class definition
class DFA:
    def __init__(self):
        self.state = 0  # initial internal state (not used as valid starting point)

    def set_initial(self):
        self.state = 1  # set actual initial state to 1

    # Transition function based on current state and input character
    def step(self, character):
        if self.state == 1:  # Start state
            if character == "-":
                self.state = 2  # Possible negative number
            elif character == "0":
                self.state = 3  # Leading zero
            elif "1" <= character <= "9":
                self.state = 4  # Starts with non-zero digit
            elif character == '.':
                self.state = 7  # Invalid: number cannot start with dot
            else:
                raise DfaIllegalCharacter()

        elif self.state == 2:  # Just saw a minus sign
            if character == "-":
                self.state = 7  # Invalid: two minus signs
            elif character == "0":
                self.state = 3  # Negative number starting with 0
            elif "1" <= character <= "9":
                self.state = 4  # Valid negative number
            elif character == '.':
                self.state = 7  # Invalid: negative number with no digits
            else:
                raise DfaIllegalCharacter()

        elif self.state == 3:  # Seen just '0'
            if character == "-":
                self.state = 7  # Invalid
            elif character == "0":
                self.state = 7  # Multiple leading zeros not allowed
            elif "1" <= character <= "9":
                self.state = 7  # Digits after leading zero are invalid
            elif character == '.':
                self.state = 5  # Move to fractional part
            else:
                raise DfaIllegalCharacter()

        elif self.state == 4:  # Reading integer part
            if character == "-":
                self.state = 7  # Invalid: minus in the middle
            elif character in "0123456789":
                self.state = 4  # Continue reading integer digits
            elif character == '.':
                self.state = 5  # Decimal point found, go to fractional part
            else:
                raise DfaIllegalCharacter()

        elif self.state == 5:  # Decimal point found, expect digit
            if character == "-":
                self.state = 7  # Invalid
            elif character in "0123456789":
                self.state = 6  # Start reading fractional digits
            elif character == '.':
                self.state = 7  # Double dot invalid
            else:
                raise DfaIllegalCharacter()

        elif self.state == 6:  # Reading fractional digits
            if character == "-":
                self.state = 7  # Invalid
            elif character in "0123456789":
                self.state = 6  # Continue fractional digits
            elif character == '.':
                self.state = 7  # Invalid: multiple decimal points
            else:
                raise DfaIllegalCharacter()

        elif self.state == 7:  # Error trap state
            if character in "-0123456789.":
                self.state = 7  # Stay in error state (absorbing)
            else:
                raise DfaIllegalCharacter()

    # Final (accepting) states: valid complete numbers
    def is_final(self):
        return self.state in {3, 4, 6}  # 3 = 0, 4 = integer, 6 = float

    # Full validation function for a number string
    def is_accepted(self, number):
        self.set_initial()  # Reset DFA
        for character in number:  # Step through each character
            self.step(character)
        return self.is_final()  # Accepted only if ends in a final state

# Entry point for testing
if __name__ == "__main__":

    # List of strings to test
    numbers = ["a", "1", "13", "103", "0.1", "0.01", "32.32", "-9", "-0.1689", "-12.6987", 
               "-10.1.1", "--2", "-0.1-", "05", "0.", "-0.", "4.20.", "345.", "12-12", "12.-14"]

    for numbers in numbers:  # Loop through test inputs
        try:
            if DFA().is_accepted(numbers):  # Run DFA on the string
                print(numbers, ": Accepted")
            else:
                print(numbers, ": Not accepted")
        except DfaIllegalCharacter:
            print("Illegal character.")
