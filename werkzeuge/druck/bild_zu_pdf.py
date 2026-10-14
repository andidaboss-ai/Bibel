"""Legt das gerenderte Umschlagbild als einzige Seite in ein PDF in exakter Größe (für KDP).

Aufruf: python3 bild_zu_pdf.py <bild.png> <ausgabe.pdf> <breite_zoll> <hoehe_zoll> <dpi> <vorschau.png>
Das Bild wird auf die exakte Pixelgröße zugeschnitten und als JPEG in höchster Qualität
(Qualität 97, ohne Farb-Unterabtastung) eingebettet. Ein flaches Bild, ohne Ebenen und Transparenz,
so wie KDP es empfiehlt.
"""
import io, sys
import img2pdf
from PIL import Image

Image.MAX_IMAGE_PIXELS = None
png, pdf, b, h, dpi, vorschau = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4]), int(sys.argv[5]), sys.argv[6]
bild = Image.open(png).convert("RGB")
bild = bild.crop((0, 0, round(b * dpi), round(h * dpi)))
puffer = io.BytesIO()
bild.save(puffer, "JPEG", quality=97, subsampling=0, dpi=(dpi, dpi))
groesse = (img2pdf.in_to_pt(b), img2pdf.in_to_pt(h))
with open(pdf, "wb") as f:
    f.write(img2pdf.convert(puffer.getvalue(), layout_fun=img2pdf.get_layout_fun(groesse, fit=img2pdf.FitMode.exact)))
klein = bild.copy()
klein.thumbnail((3000, 3000), Image.LANCZOS)
klein.save(vorschau)
print(f"  {bild.width} x {bild.height} Pixel ({dpi} dpi), PDF {len(open(pdf, 'rb').read()) / 1e6:.1f} MB")
