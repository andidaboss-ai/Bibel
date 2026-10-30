"""Subset the Noto CJK JP fonts (SIL OFL) to the characters of this book and convert CFF -> TrueType outlines,
so Chromium embeds them as CID TrueType fonts in the print PDF (instead of Type 3).
Usage: python3 tools/make_cjk_fonts.py   (writes fonts/NotoSerifJP-*.ttf, fonts/NotoSansJP-Regular.ttf)"""
import glob, os
from fontTools.ttLib import TTCollection, newTable
from fontTools import subset
from fontTools.pens.cu2quPen import Cu2QuPen
from fontTools.pens.ttGlyphPen import TTGlyphPen

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = "/usr/share/fonts/opentype/noto/"
text = "".join(open(p, encoding="utf-8").read() for p in glob.glob(os.path.join(ROOT, "text", "*.md")) + [os.path.join(ROOT, "book.json")])
extra = "".join(chr(c) for c in range(0x3000, 0x3100)) + "".join(chr(c) for c in range(0xFF01, 0xFF5F)) + "﹅﹆―…‥・〇一二三四五六七八九十百千万年月日章第部目次"
chars = sorted(set(text + extra))

def to_ttf(font):
    gs = font.getGlyphSet(); order = font.getGlyphOrder(); glyf = {}
    for n in order:
        pen = TTGlyphPen(None)
        gs[n].draw(Cu2QuPen(pen, 1.0, reverse_direction=True))
        glyf[n] = pen.glyph()
    font["loca"] = newTable("loca"); font["glyf"] = g = newTable("glyf")
    g.glyphOrder = order; g.glyphs = glyf
    del font["CFF "]
    if "VORG" in font: del font["VORG"]
    font["maxp"] = m = newTable("maxp"); m.tableVersion = 0x00010000
    for a in ("maxZones", "maxTwilightPoints", "maxStorage", "maxFunctionDefs", "maxInstructionDefs", "maxStackElements", "maxSizeOfInstructions", "maxComponentElements"):
        setattr(m, a, 0)
    m.maxZones = 1
    font["head"].glyphDataFormat = 0; font["head"].indexToLocFormat = 0
    font["post"].formatType = 2.0; font["post"].extraNames = []; font["post"].mapping = {}
    font.sfntVersion = "\x00\x01\x00\x00"

for ttc, out in (("NotoSerifCJK-Regular.ttc", "NotoSerifJP-Regular.ttf"), ("NotoSerifCJK-Bold.ttc", "NotoSerifJP-Bold.ttf"),
                 ("NotoSansCJK-Regular.ttc", "NotoSansJP-Regular.ttf")):
    f = TTCollection(SRC + ttc).fonts[0]
    opt = subset.Options(); opt.layout_features = ["*"]; opt.name_IDs = ["*"]; opt.notdef_outline = True; opt.desubroutinize = True
    s = subset.Subsetter(opt); s.populate(text="".join(chars)); s.subset(f)
    to_ttf(f)
    f.save(os.path.join(ROOT, "fonts", out)); print(out, len(f.getGlyphOrder()), "glyphs")
