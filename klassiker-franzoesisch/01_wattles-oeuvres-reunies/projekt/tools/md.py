"""Tiny Markdown reader for the book texts (headings, paragraphs, quotes, lists, dividers, *italic*, **bold**)."""
import html, re


LANG = "en"


def smart(t):
    """Straight quotes → typographic quotes (American style; German „…“ when LANG is de)."""
    if LANG.startswith("de"):
        t = re.sub(r"(\w)'(\w)", "\\1’\\2", t)
        t = re.sub(r'(^|[\s(\[—–*_-])"', "\\1„", t).replace('"', "“")
        t = re.sub(r"(^|[\s(\[—–*_„-])'", "\\1‚", t).replace("'", "‘")
        return t.replace("...", "…").replace(" -- ", " – ")
    t = re.sub(r"(\w)'(\w)", "\\1’\\2", t)                 # don't, Shinn's
    t = re.sub(r"(^|[\s(\[—–*_“\"-])'(?=(?:[Tt]is|[Tt]was|[Tt]were|[Tt]will|[Tt]would|em|[Tt]’s|[Nn]eath|gainst|mid|[Ee]re)\b)", "\\1’", t)  # ’Tis, ’twas
    t = re.sub(r"""(^|[\s(\[—–*_“"-])'""", "\\1‘", t)
    t = t.replace("'", "’")
    t = re.sub(r'(^|[\s(\[—–*_“-])"', "\\1“", t)
    t = t.replace('"', "”")
    t = t.replace("...", "…").replace(" -- ", " — ")
    return t


def inline(t):
    t = t.replace("\\*", "\uE000")  # escaped asterisk = a real asterisk, not italics
    t = html.escape(smart(t), quote=False)
    t = re.sub(r"\*\*(.+?)\*\*(?!\*)", r"<strong>\1</strong>", t)  # "**a *b***" = bold with italics inside
    t = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", t)
    t = re.sub(r"\b(GOD|LORD|FATHER|JESUS|CHRIST|HOLY|SPIRIT)(?=’S\b|\b)(?![a-z])",
               lambda m: f'<span class="dn">{m.group(1).title()}</span>', t)  # divine names set in small caps
    return t.replace("\uE000", "*")


def blocks(md, numbered=False):
    """Markdown → list of (kind, payload). kinds: h1 h2 h3 h4 p quote ul ol hr."""
    out, para, kind = [], [], None

    def flush():
        nonlocal para, kind
        if para:
            out.append((kind, para if kind in ("ul", "ol", "verse") else " ".join(para)))
        para, kind = [], None

    for line in md.split("\n"):
        s = line.rstrip()
        if not s.strip():
            flush(); continue
        if s.startswith("%% "):
            flush(); out.append(("summary", s[3:].strip())); continue
        m = re.match(r"^(\^\^|=>|~~) (.*)", s)
        if m:  # ^^ salutation / headnote, => letter closing, ~~ footnote
            flush(); out.append(({"^^": "salute", "=>": "close", "~~": "fnote"}[m.group(1)], m.group(2).strip())); continue
        if s.strip() == "* * *":
            flush(); out.append(("hr", "")); continue
        m = re.match(r"^(#{1,4}) (.*)", s)
        if m:
            flush(); out.append((f"h{len(m.group(1))}", m.group(2).strip())); continue
        if s.startswith("| ") or s == "|":
            if kind != "verse": flush(); kind = "verse"
            para.append(s[2:].strip()); continue
        if s.startswith(">"):
            if kind != "quote": flush(); kind = "quote"
            para.append(s.lstrip("> ").strip()); continue
        m = re.match(r"^\s*([-*]|\d+\.)\s+(.*)", s)
        if m and numbered and m.group(1)[0].isdigit():
            m = None  # numbered sections of the original text are paragraphs, not lists
        if m and kind in (None, "ul", "ol"):
            k = "ol" if m.group(1)[0].isdigit() else "ul"
            if kind != k: flush(); kind = k
            para.append(m.group(2)); continue
        if kind in ("ul", "ol") and para:
            para[-1] += " " + s.strip(); continue
        if kind not in (None, "p"): flush()
        kind = "p"; para.append(s.strip())
    flush()
    return out


def sections(md, level="h2", numbered=False):
    """Split at headings of the given level → list of (title, blocks)."""
    res, cur = [], None
    for k, v in blocks(md, numbered):
        if k == level:
            cur = (v, []); res.append(cur)
        elif cur is not None:
            cur[1].append((k, v))
    return res


def slug(t):
    return re.sub(r"[^a-z0-9]+", "-", re.sub(r"[*_]", "", t).lower()).strip("-")
