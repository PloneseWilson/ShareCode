d = {}
m = ["e","t","a","o","i","n","s","h","r","d","l","c",\
     "u","m","w","f","g","y","p","b","v","k","j","x","q",\
        "z"]

l = 0
with open('ct', 'r', encoding = "cp1252", ) as f:
    for line in f:
        if not line.strip():
            continue
        if not line[0].isalnum():
            continue
        if len(line) <= 5:
            continue
        if line in d:
            d[line] += 1
        else:
            d[line] = 1
        l+=1
f.close()

for i in d:
    print(i, d[i]/l)


keys = list(d.keys())
values = list(d.values())

s1 = sorted(zip(keys, values), key=lambda x: x[1], reverse= True )
mapping = {}
cnt = 0
for i in s1:
    mapping[i[0]] = m[cnt]
    cnt+=1
    if cnt>=26:
        break
    print(i[0], mapping[i[0]])

ans = {}
ans["eeae8cf93997ca2aebf40de49e58a835\n"] = "f"
ans["7edfff2d3d321fa584f792e477ea3ffc\n"] = "a"
ans["43007c16e77c2338ec89cd837f61d88b\n"] = "r"
ans["3fc469a4c6834a5da6ae7058277819a3\n"] = "w"
ans["386b6c665e62fc7eda81f5d35d9e9046\n"] = "y"
ans["7506cb520ab8a723dbbeede17f809a84\n"] = "b"
ans["1c545950714ce6de9db4b1a943990ddb\n"] = "e"
ans["a149b7acf57f38cbb107e0deca39e3a6\n"] = "h"
ans["a73291b35810967854644722f105fcf5\n"] = "i"
ans["6ed70c3b3415e45f88958c12ce96f90c\n"] = "n"
ans["d54f59ec9b3cc5e0de6e04073d335c98\n"] = "d"
ans["f39dcd881f35a4a3cb8705d6254bf593\n"] = "t"
ans["03daab0b8ab24f9cee24842b8fb48560\n"] = "o"
ans["5ee146c6b8bf650968db0369c8dd02d6\n"] = "m"
ans["2473f591d9b8f3dc81af5f6c3596b5b0\n"] = "c"
ans["8e55ade3d00028f9f87b9e7d0423ed25\n"] = "u"
ans["2cc7f85ed1aca6c4ea468a6e11eb0c93\n"] = "s"
ans["e0ce80336204505f9c57b859c1089bb2\n"] = "l"
ans["bd1009f175191d3f8fd0e97f47e893e9\n"] = "g"
ans["761f4503e85be8db96a38354945ea7f2\n"] = "v"
with open('ct', 'r', encoding = "cp1252", ) as f:
    for line in f:
        if not line.strip():
           print(" ", end = "")
        elif not line[0].isalnum():
            print(line[0], end = "")
        elif line[0].isnumeric() and len(line)<=5:
            print(line[0], end = "")
        elif line in ans:
            print(ans[line], end = "")
        else:
            print("?", end = "")




