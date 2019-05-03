# My own module that attempts to encode strings in base64
import copy


def int_to_binary(number: int, min_len=8) -> str:
    completed_string = ""
    # Make a copy so as not to affect the original element
    num_copy = copy.copy(number)

    # The factor is the largest power of two that fits into our number
    # It is essentially the value of the largest binary place
    factor = 1
    while num_copy >= factor * 2:
        factor *= 2

    # We're building up our string from the left side to the right
    while factor > 0:
        # This will always be 1 or 0
        # 1 means the factor is less than or equal to the current value of num_copy
        # 0 means the factor is greater than the value of num_copy
        completed_string += str(num_copy // factor)

        # This accounts for the current factor and reduces num_copy appropriately for the next binary place check
        num_copy = num_copy % factor

        # Divide the factor by two to get the next value of the next binary place
        factor = factor // 2

    # Return the completed string after all of the 0's and 1's have been added
    # Pad the string with extra beginning 0's if it's shorter than the needed length
    return completed_string.rjust(min_len, '0')


# This string contains all characters used to encode in base64, in increasing order
base_64_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"


def to_base_64(content: str) -> str:
    current_index = -1
    current_counter = 0
    binary_list = []
    base_64_string = ""
    for letter in str(content):
        if current_counter == 0:
            current_index += 1
            binary_list.append([])
        current_counter = (current_counter + 1) % 3
        binary_list[current_index].append(int_to_binary(ord(letter)))

    for x in range(3 - len(binary_list[current_index])):
        binary_list[current_index].append("00000000")

    for triplet_index in range(len(binary_list)):
        complete_string = binary_list[triplet_index][0] + binary_list[triplet_index][1] + binary_list[triplet_index][2]
        twenty_four_bits = [
            complete_string[:6],
            complete_string[6:12],
            complete_string[12:18],
            complete_string[18:],
        ]

        for bit_index in range(len(twenty_four_bits)):
            base_64_char_bin = twenty_four_bits[bit_index]
            char_index = bin_to_int(base_64_char_bin)
            if triplet_index == len(binary_list) - 1 and bit_index >= 2 and char_index == 0:
                base_64_string += "="
            else:
                base_64_string += base_64_chars[char_index]
    return base_64_string


def bin_to_int(b0: str) -> int:
    factor = 1
    num = 0
    for x in b0[::-1]:
        num += int(x) * factor
        factor *= 2
    return num


print(to_base_64('ABBBc cdsfsd'))

# TODO MAKE A TRANSLATOR THAT CONVERTS BASE64 BACK TO A STRING
