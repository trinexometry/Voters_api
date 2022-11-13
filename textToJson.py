import json
filename = 'data2.txt'
dict1 = {}
with open(filename) as fh:
    for line in fh:
        command, description = line.strip().split(None, 1)
        dict1[command] = description.strip()
out_file = open("test2.json", "w")
f = open("data2.txt", "r")
print(f.read())
json.dump(dict1, out_file, indent=4, sort_keys=False)
out_file.close()