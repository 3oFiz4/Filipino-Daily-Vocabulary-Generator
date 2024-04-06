import os

direct = "./Exclude_deck"
appended_file = "././__excluded.txt"

with open(appended_file, 'a') as outfile:
    for filename in os.listdir(direct):
        if filename.endswith(".txt"):
            filepath = os.path.join(direct, filename)
            with open(filepath, 'r') as infile:
                lines = infile.readlines()
                for line in lines:
                    if not line.startswith("#"):
                        first_word = line.split()[0]
                        outfile.write(first_word + '\n')
