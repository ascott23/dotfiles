import itertools

arr = []
while True:
    try:
        arr.append(raw_input('> ')) # Or whatever prompt you prefer to use.
    except EOFError:
        break

for i in range(1, len(arr) + 1):
   subset = itertools.combinations(arr, i)
   for x in subset:
      for y in x:
         print y,
      print
