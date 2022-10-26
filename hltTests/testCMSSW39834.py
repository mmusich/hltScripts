
# runTheMatrix.py -w all -ne > a2.txt

output = []
skip = False
with open('a2.txt') as fff:
  lines = fff.read().splitlines()
  for lidx, lll in enumerate(lines):
    if skip:
      skip = False
      continue
    if ' reHLT' in lll:
      skip = True
      if ' reHLT' not in lines[lidx+1]:
        output += lines[lidx-3:lidx+3]
        output += ['', '']

for foo in output:
  print(foo)
