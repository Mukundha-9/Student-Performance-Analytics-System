import base64, sys
with open(sys.argv[1], 'rb') as f:
    data = f.read().strip()
with open(sys.argv[2], 'wb') as f:
    f.write(base64.b64decode(data))
print('Decoded ' + sys.argv[1] + ' -> ' + sys.argv[2])
