# Zerlegt die World English Bible (gemeinfrei) in Kapiteldateien mit Versnummern.
import os, re, glob
NAMEN = """GEN 01_1-Mose EXO 02_2-Mose LEV 03_3-Mose NUM 04_4-Mose DEU 05_5-Mose JOS 06_Josua JDG 07_Richter RUT 08_Rut
1SA 09_1-Samuel 2SA 10_2-Samuel 1KI 11_1-Koenige 2KI 12_2-Koenige 1CH 13_1-Chronik 2CH 14_2-Chronik EZR 15_Esra
NEH 16_Nehemia EST 17_Ester JOB 18_Hiob PSA 19_Psalmen PRO 20_Sprueche ECC 21_Prediger SNG 22_Hoheslied
ISA 23_Jesaja JER 24_Jeremia LAM 25_Klagelieder EZK 26_Hesekiel DAN 27_Daniel HOS 28_Hosea JOL 29_Joel
AMO 30_Amos OBA 31_Obadja JON 32_Jona MIC 33_Micha NAM 34_Nahum HAB 35_Habakuk ZEP 36_Zefanja HAG 37_Haggai
ZEC 38_Sacharja MAL 39_Maleachi MAT 40_Matthaeus MRK 41_Markus LUK 42_Lukas JHN 43_Johannes ACT 44_Apostelgeschichte
ROM 45_Roemer 1CO 46_1-Korinther 2CO 47_2-Korinther GAL 48_Galater EPH 49_Epheser PHP 50_Philipper COL 51_Kolosser
1TH 52_1-Thessalonicher 2TH 53_2-Thessalonicher 1TI 54_1-Timotheus 2TI 55_2-Timotheus TIT 56_Titus PHM 57_Philemon
HEB 58_Hebraeer JAS 59_Jakobus 1PE 60_1-Petrus 2PE 61_2-Petrus 1JN 62_1-Johannes 2JN 63_2-Johannes 3JN 64_3-Johannes
JUD 65_Judas REV 66_Offenbarung""".split()
NAMEN = dict(zip(NAMEN[::2], NAMEN[1::2]))
n = 0
for f in sorted(glob.glob("quelle/web/eng-web_*_read.txt")):
    m = re.match(r".*eng-web_\d+_([A-Z0-9]+)_(\d+)_read\.txt", f)
    if not m: continue
    buch, kap = m.group(1), int(m.group(2))
    ordner = "englisch/" + (NAMEN.get(buch) or "apokryphen/" + buch)
    os.makedirs(ordner, exist_ok=True)
    zeilen = [z.strip() for z in open(f, encoding="utf-8-sig") if z.strip()]
    titel, verse = zeilen[0], zeilen[2:]
    with open(f"{ordner}/kapitel_{kap:03d}.txt", "w") as out:
        out.write(f"# {titel} Chapter {kap}\n\n")
        for i, v in enumerate(verse, 1):
            out.write(f"{i} {v}\n")
    n += 1
print(n, "Kapiteldateien")
