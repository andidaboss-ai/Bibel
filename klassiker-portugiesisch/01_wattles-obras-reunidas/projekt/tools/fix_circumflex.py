"""Rebuild lowercase circumflex glyphs (â ê ô) from base letter + the (well-formed) uppercase accent."""
import sys
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

def contours(rec):
    out, cur = [], []
    for op, args in rec.value:
        cur.append((op, args))
        if op in ('closePath', 'endPath'):
            out.append(cur); cur = []
    return out

def bounds(gs, ops):
    bp = BoundsPen(gs)
    for op, args in ops: getattr(bp, op)(*args)
    return bp.bounds

f = TTFont(sys.argv[1]); gs = f.getGlyphSet(); cm = f.getBestCmap()
cap = f['OS/2'].sCapHeight; xh = f['OS/2'].sxHeight
rec = RecordingPen(); gs[cm[ord('Ê')]].draw(rec)
acc = [c for c in contours(rec) if bounds(gs, c)[1] > cap * 0.95]
ab = bounds(gs, [o for c in acc for o in c])
gap = ab[1] - cap
for lc, base in (('â', 'a'), ('ê', 'e'), ('ô', 'o')):
    rb = RecordingPen(); gs[cm[ord(base)]].draw(rb)
    bb = bounds(gs, rb.value)
    s = 0.92
    dx = (bb[0] + bb[2]) / 2 - (ab[0] + ab[2]) / 2 * s
    dy = xh + gap * 0.9 - ab[1] * s
    pen = TTGlyphPen(gs)
    rb.replay(pen)
    tp = TransformPen(pen, (s, 0, 0, s, dx, dy))
    for c in acc:
        for op, args in c: getattr(tp, op)(*args)
    name = cm[ord(lc)]
    f['glyf'][name] = pen.glyph()
    f['hmtx'][name] = f['hmtx'][cm[ord(base)]]
f.save(sys.argv[2]); print('fixed', sys.argv[2])
