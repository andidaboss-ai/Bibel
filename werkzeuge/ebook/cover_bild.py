"""Bereitet das Titelbild für alle Cover vor (E-Book und Druck).

Grundlage ist die Vorlage cover_vorlage/vorlage.jpg (1152 x 1728 Pixel).
1. Der Titel oben wird abgeschnitten (er wird auf dem Cover scharf neu gesetzt),
   der Slogan unten wird entfernt (er wird ebenfalls neu gesetzt).
2. Das Bild wird mit EDSR (KI-Hochskalierung, OpenCV) 4-fach vergrößert, damit es für den Druck mit 300 dpi reicht.
   Das Ergebnis wird als cover_vorlage/kunst-4x.jpg gespeichert und nur einmal berechnet.
3. Für jede Ausgabe wird die Farbe verändert: Violett und Blau werden in die Farbe des Bandes gedreht,
   Gold, Weiß und Schwarz bleiben. Ergebnis: cover_vorlage/.farbig/kunst-<ausgabe>.jpg

Aufruf:  python3 werkzeuge/ebook/cover_bild.py
Braucht: pip install opencv-contrib-python-headless numpy pillow
"""
import os, sys, urllib.request
import numpy as np
from PIL import Image

HIER = os.path.dirname(os.path.abspath(__file__))
ORDNER = os.path.join(HIER, "cover_vorlage")
VORLAGE = os.path.join(ORDNER, "vorlage.jpg")
BASIS = os.path.join(ORDNER, "kunst-4x.jpg")
FARBIG = os.path.join(ORDNER, ".farbig")
MODELL_URL = "https://raw.githubusercontent.com/Saafke/EDSR_Tensorflow/master/models/EDSR_x4.pb"

OBEN = 500  # erste Zeile unter dem Titel „DIE BIBEL“ in der Vorlage

# Zielfarbton (Grad) je Ausgabe. None = Originalfarben (Violett).
FARBTON = {
    "gesamt": 40,
    "band-1": None,
    "band-2": 150,
    "band-3": 218,
    "band-4": 352,
}


def basis_bauen():
    import cv2
    modell = os.path.join(ORDNER, ".EDSR_x4.pb")
    if not os.path.exists(modell):
        urllib.request.urlretrieve(MODELL_URL, modell)
    bild = cv2.imread(VORLAGE)
    # Slogan unten entfernen (helle Schrift auf dunklem Grund) und die Stelle auffüllen
    maske = np.zeros(bild.shape[:2], np.uint8)
    feld = bild[1635:1700, 300:860]
    maske[1635:1700, 300:860] = (feld.min(axis=2) > 120).astype(np.uint8) * 255
    maske = cv2.dilate(maske, np.ones((7, 7), np.uint8))
    bild = cv2.inpaint(bild, maske, 9, cv2.INPAINT_TELEA)
    bild = bild[OBEN:]
    sr = cv2.dnn_superres.DnnSuperResImpl_create()
    sr.readModel(modell)
    sr.setModel("edsr", 4)
    # in Kacheln mit Überlappung rechnen (spart Speicher)
    K, U = 160, 16
    h, w = bild.shape[:2]
    aus = np.zeros((h * 4, w * 4, 3), np.uint8)
    for y in range(0, h, K):
        for x in range(0, w, K):
            y0, x0 = max(0, y - U), max(0, x - U)
            y1, x1 = min(h, y + K + U), min(w, x + K + U)
            gross = sr.upsample(bild[y0:y1, x0:x1])
            ya, xa = (y - y0) * 4, (x - x0) * 4
            hh, ww = (min(h, y + K) - y) * 4, (min(w, x + K) - x) * 4
            aus[y * 4:y * 4 + hh, x * 4:x * 4 + ww] = gross[ya:ya + hh, xa:xa + ww]
        print(f"  {min(h, y + K)}/{h} Zeilen", flush=True)
    cv2.imwrite(BASIS, aus, [cv2.IMWRITE_JPEG_QUALITY, 93])


def faerben(ziel):
    """Dreht Violett/Blau/Türkis (Farbton 170–335°) zum Zielfarbton. Gold, Weiß und Schwarz bleiben."""
    hsv = np.asarray(Image.open(BASIS).convert("HSV")).astype(np.float32)
    h = hsv[..., 0] * 360 / 255
    # Gewicht: 1 im Bereich 185–320°, weicher Übergang bis 160° und 340°
    gw = np.clip((h - 160) / 25, 0, 1) * np.clip((340 - h) / 20, 0, 1)
    quelle = 275.0  # Violett der Vorlage
    neu = (h + gw * (ziel - quelle)) % 360
    hsv[..., 0] = neu * 255 / 360
    if ziel in (40,):  # Gold: etwas weniger Sättigung, damit es edel und nicht orange wirkt
        hsv[..., 1] *= 1 - 0.25 * gw
    return Image.fromarray(hsv.astype(np.uint8), "HSV").convert("RGB")


def main():
    if not os.path.exists(BASIS):
        print("Vergrößere die Vorlage (einmalig, dauert einige Minuten) …")
        basis_bauen()
    os.makedirs(FARBIG, exist_ok=True)
    for name, ton in FARBTON.items():
        ziel = os.path.join(FARBIG, f"kunst-{name}.jpg")
        if os.path.exists(ziel) and os.path.getmtime(ziel) > max(os.path.getmtime(BASIS), os.path.getmtime(__file__)):
            continue
        bild = Image.open(BASIS).convert("RGB") if ton is None else faerben(ton)
        bild.save(ziel, quality=93)
        print(os.path.relpath(ziel, HIER))


if __name__ == "__main__":
    main()
