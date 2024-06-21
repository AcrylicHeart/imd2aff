import os
TIMINGLENGTH = 12
OBJECTLENGTH = 11
LANEOFFSET = 1
for file in os.listdir('input'):
    filename,suffix=os.path.splitext(file)
    imd = open('input\\'+file,"rb").read()
    aff = open('output\\'+filename+'.aff',"w")
    aff.writelines("AudioOffset:0\n-\ntiming(0,120.00,4.00);\n")

    songname,mode,level=filename.split("_")
    songlength=int.from_bytes(imd[0:4],byteorder="little")
    beatlinenum=int.from_bytes(imd[4:8],byteorder="little")
    print("-"*20)
    print(f"谱面名称:{songname}\n模式:{mode}\n难度:{level}\n曲子长度为:{songlength}ms\n小节线个数为:{beatlinenum}")

    if mode == "4k": LANEOFFSET = 1
    elif mode == "5k": LANEOFFSET = 1;aff.writelines("scenecontrol(0,enwidenlanes,1,1);\ncamera(0,225.00,125.00,125.00,0.00,0.00,0.00,l,1);\n")
    elif mode == "6k": LANEOFFSET = 0;aff.writelines("scenecontrol(0,enwidenlanes,1,1);\nscenecontrol(0,enwidencamera,1,1);\n")
    for offset in range(14+TIMINGLENGTH*beatlinenum,len(imd),OBJECTLENGTH):
        object = imd[offset:offset+OBJECTLENGTH]
        time = int.from_bytes(object[2:6],byteorder="little")
        lane = int.from_bytes(object[6:7])+LANEOFFSET
        if object[0] == 0: #tap
            aff.writelines(f"({time},{lane});\n")
        elif object[0] == 1: #flick
            direct = int.from_bytes(object[7:],byteorder="little",signed=True)
            aff.writelines(f"arc({time},{time+1},{0.5*lane-0.75},{0.5*lane-0.75},s,{0.00},{0.00},{3},none,true)[arctap({time})];\n")
            aff.writelines(f"arc({time},{time},{0.5*lane-0.75},{0.5*(lane+direct)-0.75},s,{0.00},{0.00},{3},none,false);\n")
            aff.writelines(f"arc({time},{time+33},{0.5*(lane+direct)-0.75},{0.5*(lane+direct)-0.75},s,{0.00},{0.00},{3},none,false);\n")
        elif object[0] == 2: #hold
            length = int.from_bytes(object[7:],byteorder="little")
            if length > 33:
                aff.writelines(f"hold({time},{time+length},{lane});\n")
            else:
                aff.writelines(f"arc({time},{time+1},{0.5*lane-0.75},{0.5*lane-0.75},s,{0.00},{0.00},{3},none,true)[arctap({time})];\n")
        elif object[0] == 33: #折线 持续 flick
            direct = int.from_bytes(object[7:],byteorder="little",signed=True)
            aff.writelines(f"arc({time},{time},{0.5*lane-0.75},{0.5*(lane+direct)-0.75},s,{0.00},{0.00},{3},none,false);\n")
        elif object[0] in [34,98,162]: #折线 hold
            length = int.from_bytes(object[7:],byteorder="little")
            if object[0] == 98: aff.writelines(f"arc({time},{time+1},{0.5*lane-0.75},{0.5*lane-0.75},s,{0.00},{0.00},{3},none,true)[arctap({time})];\n")
            aff.writelines(f"arc({time},{time+length},{0.5*lane-0.75},{0.5*lane-0.75},s,{0.00},{0.00},{3},none,false);\n")
        elif object[0] == 97: #折线 开始 flick
            direct = int.from_bytes(object[7:],byteorder="little",signed=True)
            aff.writelines(f"arc({time},{time+1},{0.5*lane-0.75},{0.5*lane-0.75},s,{0.00},{0.00},{3},none,true)[arctap({time})];\n")
            aff.writelines(f"arc({time},{time},{0.5*lane-0.75},{0.5*(lane+direct)-0.75},s,{0.00},{0.00},{3},none,false);\n")
        elif object[0] == 161: #折线 结束 flick
            direct = int.from_bytes(object[7:],byteorder="little",signed=True)
            aff.writelines(f"arc({time},{time},{0.5*lane-0.75},{0.5*(lane+direct)-0.75},s,{0.00},{0.00},{3},none,false);\n")
            aff.writelines(f"arc({time},{time+33},{0.5*(lane+direct)-0.75},{0.5*(lane+direct)-0.75},s,{0.00},{0.00},{3},none,false);\n")