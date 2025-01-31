#!/usr/bin/env python3

def reverse_single_char_scramble(scrambled_char, mult):
    # Try all possible characters from 0 to 127 to find the original one
    for orig_char in range(128):
        if (orig_char * 42 * mult) % 128 == scrambled_char:
            return orig_char
    return None

# Manually reverse the scrambling for each character
def reverse_scramble_string_manually(scrambled_string):
    original = []
    for i, char in enumerate(scrambled_string):
        mult = 1
        for j in range(i + 1):
            mult *= i  # This is the same as in scramble_dream
        original_char = reverse_single_char_scramble(ord(char), mult)
        if original_char is not None:
            original.append(chr(original_char))
        else:
            print(f"Error: Couldn't reverse scramble for character {char} at index {i}")
            return None
    return ''.join(original)

# Example of manually reversing a scrambled string like "/bin/sh"
scrambled_ephemereal = "/bin/sh"  # The scrambled value we want to reverse
original_ephemereal = reverse_scramble_string_manually(scrambled_ephemereal)

print(f"Original ephemereal: {original_ephemereal}")
