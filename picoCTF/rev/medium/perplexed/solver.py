SOURCE = b"\xe1\xa7\x1e\xf8u#{a\xb9\x9d\xfcZ[\xdfi\xd2\xfe\x1b\xed\xf4\xedg\xf4"

input_bits = [0]
input_counter = 1
result = b""
for byte in SOURCE:
    for i in range(8):
        source_bit = (byte >> (7 - i)) & 0b1
        input_bits.append(source_bit)

        input_counter += 1
        if input_counter == 8:
            result += sum(input_bits[j] << (7 - j) for j in range(8)).to_bytes(1, signed=False)
            input_bits = [0]
            input_counter = 1

print(result)
