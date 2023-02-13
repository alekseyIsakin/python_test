import json

mp = []


def create_test_map():
  js = {}
  with open(r'mods/test/entity_list.json','r') as f:
    js = json.loads(''.join(f.readlines()))

    for floor in range(2):
      mp.append([])
      for h in range(6):
        mp[floor].append([])
        for w in range(6):
          mp[floor][h].append(int(js['floor']['floor'], 16))
    pass

  with open(r'mods/test/map.mp','bw') as f:
    for floor in range(2):
      for h in range(6):
        f.write(bytearray(mp[floor][h]))
        d = int(js['endline'], 16)
        f.write(bytes([(int(js['endline'], 16))]))
      f.write(bytes([(int(js['endfloor'], 16))]))

create_test_map()
with open(r'mods/test/map.mp','br') as f:
  print(f.read())
