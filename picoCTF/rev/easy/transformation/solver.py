# Transformation
flag = ''
''.join([
    (
        chr(
            (ord(flag[i]) << 8) +
            ord(flag[i + 1])
        )
    ) for i in range(0, len(flag), 2)
])

result = '灩捯䍔䙻ㄶ形楴獟楮獴㌴摟潦弸強㕤㐸㤸扽'
original = ''.join([
    (
        ''.join(
            (
                chr(ord(result[i]) >> 8),
                chr(ord(result[i]) & 0xFF),
            )
        )
    ) for i in range(0, len(result))
])

print(original)
