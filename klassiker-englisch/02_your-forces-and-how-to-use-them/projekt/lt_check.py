import json, re, sys, urllib.parse, urllib.request, collections
paras = [p for p in open(sys.argv[1], encoding="utf-8").read().split("\n\n") if p.strip() and not p.startswith("#")]
hits = collections.Counter(); ctx = {}
for i in range(0, len(paras), 20):
    text = "\n\n".join(p.replace("*", "") for p in paras[i:i + 20])
    data = urllib.parse.urlencode({"language": "en-GB" if "--gb" in sys.argv else "en-US", "text": text, "enabledOnly": "false"}).encode()
    r = json.load(urllib.request.urlopen("http://localhost:8081/v2/check", data))
    for m in r["matches"]:
        rid = m["rule"]["id"]
        if rid not in ("MORFOLOGIK_RULE_EN_US", "ENGLISH_WORD_REPEAT_RULE", "EN_A_VS_AN", "THE_THE", "UPPERCASE_SENTENCE_START", "COMMA_PARENTHESIS_WHITESPACE", "DOUBLE_PUNCTUATION", "EN_UNPAIRED_BRACKETS", "EN_UNPAIRED_QUOTES", "PUNCTUATION_PARAGRAPH_END", "WHITESPACE_RULE", "SENTENCE_WHITESPACE"):
            continue
        w = text[m["offset"]:m["offset"] + m["length"]]
        hits[(rid, w)] += 1
        ctx.setdefault((rid, w), text[max(0, m["offset"] - 40):m["offset"] + m["length"] + 30].replace("\n", " "))
for (rid, w), n in sorted(hits.items(), key=lambda x: -x[1]):
    print(n, rid, repr(w), "|", ctx[(rid, w)])
