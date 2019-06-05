

fin = open("view_new11.csv", "rb")
fout = open("info_new12.csv", "wb")

data = fin.read()

print(len(data))

for i in range(len(data)):
    if int(data[i]) == 0x0A and int(data[i-1]) != 0x0D:
        fout.write(ord(' ').to_bytes(1, 'big'))
        continue
    fout.write(data[i].to_bytes(1, 'big'))

fin.close()
fout.close()

