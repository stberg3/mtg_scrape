def fix_dashes(strings):
    for string in range(len(strings)):
         for index in range(len(strings[string])):
             if ord(strings[string][index]) == 8212:
                strings[string] = \
                    strings[string][:index] + \
                    "-" + \
                    strings[string][index+1:]
         print(list(map(lambda x : ord(x), strings[string])))
