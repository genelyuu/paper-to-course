import sys
# KS X 1001 Hangul syllables: decode EUC-KR rows 0xB0-0xC8
chars=set()
for hi in range(0xB0,0xC9):
    for lo in range(0xA1,0xFF):
        try: chars.add(bytes([hi,lo]).decode('euc-kr'))
        except: pass
# all KS X 1001 symbols rows A1-AC too
for hi in range(0xA1,0xAD):
    for lo in range(0xA1,0xFF):
        try: chars.add(bytes([hi,lo]).decode('euc-kr'))
        except: pass
chars=sorted(c for c in chars if len(c)==1)
cps=[ord(c) for c in chars]
ranges="U+0020-007E,U+00A0-00FF,U+2000-206F,U+2190-21FF,U+2200-22FF,U+2460-24FF,U+25A0-25FF,U+3000-303F,U+3131-318E,"+",".join("U+%04X"%c for c in cps)
open(sys.argv[1],'w').write(ranges)
print(len(cps))
