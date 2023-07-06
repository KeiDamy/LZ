#LZ符号を行うプログラム

def incremental_decomposition(input_strings):
    dictionary = []
    temp = []
    
    for i in range(len(input_strings)):
        if len(temp) == 0:
            temp.append(input_strings[i])
        else:
            if not temp in dictionary:
                dictionary.append(temp)
                temp = []
            temp.append(input_strings[i])
    dictionary.append(temp)
    return dictionary

#既存の辞書にあった場合それのインデックスにする。ない場合は0にする
def lz_encoding(input_string):
    dictionary = ['']
    output = []
    temp = ''
    for char in input_string:
        temp += char
        if temp not in dictionary:
            output.append((dictionary.index(temp[:-1]) if temp[:-1] in dictionary else 0, char))
            dictionary.append(temp)
            temp = ''

    if temp:
        output.append((dictionary.index(temp) if temp in dictionary else 0, ''))
    return output


#２進数に変換したものを出力する。Aは00,Bは01,Cは10。[
#インデックスの桁数はそのインデックス-1を２進数にした場合の桁数にする.
def print_binary(encoded_string):
    cnt = 0
    output = ""
    for index, char in encoded_string:
        if cnt == 0:
            output += print_binary_char(char)
            cnt += 1
        else:
            output += bin(index)[2:].zfill(digit_length(cnt))
            output += print_binary_char(char)
            cnt += 1
    return output

def digit_length(num):
    number = 1
    cnt = 1
    if num == 0:
        return 0
    while True:
        number *= 2
        cnt += 1
        if number > num:
            return cnt - 1


def print_binary_char(char):
    if char == "A":
        return "00"
    elif char == "B":
        return "01"
    elif char == "C":
        return "10"
    
#エンコーダー終わり


#デコーダー
def binary_to_pairs(binary_string):
    pairs = []
    cnt = 0
    index = 0
    temp = ""
    binary = ""
    for i in range(len(binary_string)):
        if index != i:
            continue
        if i == 0:
            temp += binary_string[i]
            index += 1
        elif i == 1:
            temp += binary_string[i]
            pairs.append((0, binary_to_char(temp)))
            cnt += 1
            index += 1
            temp = ""
        else:
            num = digit_length(cnt)
            for j in range(num):
                binary += binary_string[index]
                index += 1
            temp += binary_string[index]
            index += 1
            temp += binary_string[index]
            index += 1
            pairs.append((binary_to_decimal(binary), binary_to_char(temp)))
            cnt += 1
            temp = ""
            binary = ""
    return pairs

def binary_to_decimal(binary_string):
    return int(binary_string, 2)

def binary_to_char(char_binary):
    if char_binary == "00":
        return "A"
    elif char_binary == "01":
        return "B"
    elif char_binary == "10":
        return "C"

def lz_decoding(pairs):
    dictionary = ['']
    output = ""
    for index, char in pairs:
        if index == 0:
            output += char
            dictionary.append(char)
        else:
            output += dictionary[index] + char
            dictionary.append(dictionary[index] + char)
    return output

if __name__ == "__main__":
    input_string = "BACBCBAACABBACAA"
    encoded_string = incremental_decomposition(input_string)
    print(encoded_string)
    encoded_string = lz_encoding(input_string)
    print(encoded_string)
    encoded_binary = print_binary(encoded_string)
    print(encoded_binary)

    pairs = binary_to_pairs(encoded_binary)
    print(pairs)
    decoded_string = lz_decoding(pairs)
    print(decoded_string)
