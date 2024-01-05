import random

if __name__ == '__main__':

    from rapidfuzz import fuzz
    from thefuzz import fuzz
    fuzz.token_sort_ratio("fuzzy wuzzy was a bear", "wuzzy fuzzy was a bear")

    chars = """!@#$%^&*()-_=+[]{}\|,.<>/?'"`~"""
    chars1 = "!@#$%"
    chars2 = "^&*()"
    chars3 = """-_=+[]{}\|,.<>/?'"`~"""
    chars4 = "[]{}-_=+]"
    chars = chars4
    # convert string to list and shuffle it
    chars = list(chars)
    output = ""
    for i in range(50 ):
        random.shuffle(chars)

        output = output + "".join(chars[0:2]) + " "
    print(output)