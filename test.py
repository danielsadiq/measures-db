import difflib

vals = difflib.get_close_matches("appel", ["ape", "apple", "peach"])
print(vals)
myls = ["ape", "apple", "peach"]
myls = myls[::-1]
print(myls)