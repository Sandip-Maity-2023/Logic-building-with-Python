def roman_to_integer(s: str) -> int:
    roman = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
    number = 0
    for i in range(len(s) - 1):
        if roman[s[i]] < roman[s[i + 1]]:
            number -= roman[s[i]]
        else:
            number += roman[s[i]]
    return number + roman[s[-1]]

def main():
    s = input("Enter a Roman numeral: ")
    result = roman_to_integer(s)
    print(f"The integer value of the Roman numeral {s} is {result}")

if __name__ == "__main__":
    main()
