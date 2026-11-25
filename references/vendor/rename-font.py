"""OFL 예약 글꼴 이름(RFN) 조건: 부분 집합(수정본)은 원래 이름을 쓰지 않는다.
사용: python3 rename-font.py in.woff2 out.woff2 "새 이름"   (fontTools + brotli 필요)"""
import sys
from fontTools.ttLib import TTFont
src, dst, fam = sys.argv[1:4]
f = TTFont(src)
ps = fam.replace(" ", "")
for rec in f["name"].names:
    nid = rec.nameID
    if nid in (1, 16, 21): rec.string = fam
    elif nid == 4: rec.string = fam
    elif nid == 6: rec.string = ps
    elif nid == 3: rec.string = ps + "-subset"
    elif nid in (17, 22): pass
    elif nid == 25: rec.string = ps
f.flavor = "woff2"
f.save(dst)
