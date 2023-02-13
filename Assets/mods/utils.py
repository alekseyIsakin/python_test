import json

mp = []
cnt_floor = 2
max_h = 16
max_w = 16

def create_test_map():
  js = {}
  with open(r'mods/test/entity_list.json','r') as f:
    js = json.loads(''.join(f.readlines()))

    for floor in range(cnt_floor):
      mp.append([])
      for h in range(max_h):
        mp[floor].append([])
        for w in range(max_w):
          cell = 0

          if floor == 1:
            if (h == 0 or h == max_h-1) or (w == 0 or w== max_w-1):
              cell = js['walls']['simple_wall']
            elif (h == 1 or h == max_h-2) or (w == 1 or w== max_w-2):
              cell = js['floor']['floor']
            else:
              cell = js['SEPARATE']
          else:
            if (h == 1 or h == max_h-2) or (w == 1 or w== max_w-2):
              cell = js['walls']['simple_wall']
            else:
              cell = js['floor']['floor']
          mp[floor][h].append(cell)

    pass

  with open(r'mods/test/map.mp','bw') as f:
    f.write(bytearray([js['map']]))
    for floor in range(cnt_floor):
      for h in range(max_h):
        f.write(bytearray(mp[floor][h]))

        endline = js['endline']
        f.write(bytes([(endline)]))

      f.write(bytes([(js['endfloor'])]))
    f.write(bytes([(js['endmap'])]))

    f.write(bytes([(js['BOT'])]))
    f.write(bytes([(js['BOTID'])]))
    f.write((0).to_bytes(length=4,byteorder='little',signed = False))
    f.write(bytes([(js['BOTSTART'])]))
    f.write((2).to_bytes(length=4,byteorder='little',signed = False))
    f.write((0).to_bytes(length=4,byteorder='little',signed = False))
    f.write((13).to_bytes(length=4,byteorder='little',signed = False))

    f.write(bytes([(js['BOTID'])]))
    f.write((1).to_bytes(length=4,byteorder='little',signed = False))
    f.write(bytes([(js['BOTSTART'])]))
    f.write((13).to_bytes(length=4,byteorder='little',signed = False))
    f.write((0).to_bytes(length=4,byteorder='little',signed = False))
    f.write((2).to_bytes(length=4,byteorder='little',signed = False))

    f.write(bytes([(js['ENDBOT'])]))

create_test_map()
with open(r'mods/test/map.mp','br') as f:
  print(f.read())
