a_file = open("pokemon.txt", "r")
lines = a_file.readlines()
a_file.close()
new_file = open("pokemon7.txt", "w")

for line in lines:
    line = line.replace("name=", "")
    new_file.write(line)


new_file.close()


