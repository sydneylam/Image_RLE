import console_gfx as console


def main():
    print("""Welcome to the RLE image encoder!

Displaying Spectrum Image:""")

    console.display_image(console.TEST_RAINBOW)
    print("\n")

    rle_menu()

    selection = int(input("Select a Menu Option: "))

    user_image = []

    while selection != 0:
        if selection == 1:  # Loading file
            fileName = input("Enter name of file to load: ")

            user_image = list(console.load_file(fileName))

            rle_menu()
            selection = int(input("Select a Menu Option: "))

        elif selection == 2:  # Load test image
            user_image = console.TEST_IMAGE
            print("Test image data loaded.")

            rle_menu()
            selection = int(input("Select a Menu Option: "))

        elif selection == 3:  # Reads RLE string
            rleString = input("Enter an RLE string to be decoded: ")
            rleString_list = list(string_to_rle(rleString))  # takes rle string and makes it a list
            rleString_unencoded = list(decode_rle(rleString_list))  # creates a list that is unencoded data

            user_image = rleString_unencoded

            rle_menu()
            selection = int(input("Select a Menu Option: "))

        elif selection == 4:  # Reads RLE Hex String
            rle_HexString = input("Enter the hex string holding RLE data: ")

            rle_HexString_list = list(string_to_data(rle_HexString))  # takes hex string input and makes it a list
            rle_HexString_unencoded = list(decode_rle(rle_HexString_list))  # creates a list that is unencoded data

            user_image = rle_HexString_unencoded

            print("RLE decoded length:", len(rle_HexString_unencoded))

            rle_menu()
            selection = int(input("Select a Menu Option: "))

        elif selection == 5:  # Read Data Hex String
            flat_dataHex = input("Enter the hex string holding flat data: ")
            num_runs = count_runs(flat_dataHex)

            print("Number of runs:", num_runs)

            # Storing the input as a list of unencoded data
            flat_dataHex_list = list(flat_dataHex)
            user_image = []

            for i in range(len(flat_dataHex_list)):
                user_image.append(int(str(flat_dataHex_list[i]), 16))

            rle_menu()
            selection = int(input("Select a Menu Option: "))

        elif selection == 6:

            if len(user_image) == 0:
                print("Displaying image...")
                print("(no data)")

            else:
                print("Displaying image...")

                console.display_image(user_image)

            rle_menu()
            selection = int(input("Select a Menu Option: "))

        elif selection == 7:

            if len(user_image) == 0:
                print("RLE representation: (no data)")

            else:

                encoded_data_list = list(encode_rle(user_image))
                readable_rle = to_rle_string(encoded_data_list)

                print("RLE representation: ", readable_rle)

            rle_menu()
            selection = int(input("Select a Menu Option: "))

        elif selection == 8:
            if len(user_image) == 0:
                print("RLE hex values: (no data)")

            else:
                rle_representation = list(encode_rle(user_image))  # returns a list of the rle representation
                print("RLE hex values: ", to_hex_string(rle_representation))

            rle_menu()
            selection = int(input("Select a Menu Option: "))

        elif selection == 9:

            if len(user_image) == 0:
                print("Flat hex values: (no data)")

            else:
                flat_hex_val = ""
                for i in range(len(user_image)):
                    flat_hex_val += str(hex(user_image[i])[2:])
                print("Flat hex values: ", flat_hex_val)

            rle_menu()
            selection = int(input("Select a Menu Option: "))

        elif selection < 0 or selection > 9:  # User inputs a number not listed
            print("Error! Invalid input.")

            rle_menu()
            selection = int(input("Select a Menu Option: "))


def rle_menu():
    print("""
RLE Menu
--------
0. Exit
1. Load File
2. Load Test Image
3. Read RLE String
4. Read RLE Hex String
5. Read Data Hex String
6. Display Image
7. Display RLE String
8. Display Hex RLE Data
9. Display Hex Flat Data
""")


def count_runs(flatData):  # returns number of runs of data in an image data set
    count = 1
    element_of_run = 1

    # Checking to see if a run exceeds 15
    for i in range(len(flatData) - 1):

        if flatData[i] == flatData[i + 1]:
            element_of_run += 1

        if element_of_run > 15:
            count += 1
            element_of_run = 1

        if flatData[i] != flatData[i + 1]:
            count += 1
            element_of_run = 1
    return count


def to_hex_string(data):  # translates data to hexadecimal string
    hex_data = []

    for i in range(len(data)):
        hex_element = hex(data[i])
        hex_data.append(hex_element[2:])  # modifies the hex so that it doesn't have prefix 0x

    return ''.join(map(str, hex_data))


def encode_rle(flat_data):  # returns an encoded rle representation of data
    pre_rle_data = []
    counter = 1
    rle_data = []

    for i in range(len(flat_data) - 1):
        if flat_data[i] == flat_data[i + 1]:
            counter += 1

        else:
            pre_rle_data.append(counter)
            pre_rle_data.append(flat_data[i])
            counter = 1

    pre_rle_data.append(counter)
    pre_rle_data.append(flat_data[i + 1])

    # handling run lengths greater than 15
    for i in range(0, len(pre_rle_data), 2):
        if pre_rle_data[i] > 15:
            runs = pre_rle_data[i] // 15
            remainder = pre_rle_data[i] % 15

            for j in range(runs):
                rle_data.append(15)
                rle_data.append(pre_rle_data[i + 1])

            rle_data.append(remainder)
            rle_data.append(pre_rle_data[i + 1])

        else:
            rle_data.append(pre_rle_data[i])
            rle_data.append(pre_rle_data[i + 1])

    return bytes(rle_data)


def get_decoded_length(rle_data):  # gives the total length of original data set
    count = 0

    for i in range(0, len(rle_data), 2):
        count += rle_data[i]
    return count


def decode_rle(rle_data):  # takes rle encoded and returns a decoded data set
    flat_data = []
    for i in range(0, len(rle_data) - 1, 2):
        for j in range(rle_data[i]):
            flat_data.append(rle_data[i + 1])

    return bytes(flat_data)


def string_to_data(data_string):  # puts a string into byte data format
    decimal_list = []

    data_list = list(data_string)
    for i in range(len(data_list)):
        toHex = int(data_list[i], 16)
        decimal_list.append(toHex)

    return bytearray(decimal_list)


def to_rle_string(rleData):  # transforms rle data into human comprehensible representation
    rleString = ""

    for i in range(0, len(rleData), 2):

        run_length = str(rleData[i])
        rleString += run_length

        hex_val = hex(rleData[i + 1])
        hex_run_value = hex_val[2:]  # modifies the hex so that it doesnt have prefix 0x
        rleString += hex_run_value

        if i < len(rleData) - 2:
            rleString += ":"

    return rleString


def string_to_rle(rleString):  # changes a string in rle format to rle byte data
    rle_list = []
    rle_temp_list = list(rleString.split(":"))

    for i in range(len(rle_temp_list)):
        if len(rle_temp_list[i]) == 3:  # for cases where the decimal value is 2 digits (ex. 10, 11, 12, etc)
            three_digit_elem = rle_temp_list[i]
            decimal_num = three_digit_elem[:2]
            hexadecimal_num = three_digit_elem[-1]

            rle_list.append(decimal_num)
            rle_list.append(hexadecimal_num)

        else:
            split_numbers = list(rle_temp_list[i])  # seperates decimal and hex numbers by putting them in a list
            rle_list.extend(split_numbers)

    for i in range(1, len(rle_list), 2):
        rle_list[i] = int(rle_list[i], 16)

    rle_list = [int(i) for i in rle_list]

    return bytes(rle_list)


if __name__ == "__main__":
    main()