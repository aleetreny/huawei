"""Builds the Cut 3 presentation slides (docs/entrega/cut3-video/slides.pptx).

Speaker notes come from docs/entrega/cut3-video/guion.md: every paragraph after
a `**[Sn]**` marker goes to slide n, so the deck and the script stay in step.

    uv run --with python-pptx python scripts/entrega/cut3_video_slides.py
"""

from __future__ import annotations

import re
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Emu, Inches, Pt

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "docs/entrega/cut3-video"
SCRIPT = OUT_DIR / "guion.md"

# Palette: deep graphite (the office at night), amber (promotion), brick (risk), teal (safe).
INK = RGBColor(0x1C, 0x24, 0x2B)
INK_SOFT = RGBColor(0x4A, 0x55, 0x5F)
MUTED = RGBColor(0x7A, 0x84, 0x8D)
PAPER = RGBColor(0xFF, 0xFF, 0xFF)
TINT = RGBColor(0xF1, 0xF3, 0xF4)
AMBER = RGBColor(0xE0, 0x9A, 0x2B)
AMBER_TINT = RGBColor(0xFB, 0xEF, 0xD9)
BRICK = RGBColor(0xB5, 0x48, 0x3B)
BRICK_TINT = RGBColor(0xF6, 0xE1, 0xDD)
TEAL = RGBColor(0x2A, 0x7F, 0x7A)
TEAL_TINT = RGBColor(0xDC, 0xEE, 0xEC)
DARK_LINE = RGBColor(0x3A, 0x45, 0x4F)

HEAD = "Cambria"
BODY = "Calibri"
MONO = "Courier New"

W, H = Inches(13.333), Inches(7.5)
MARGIN = Inches(0.6)
FOOTER = "Gradient Depression · Career Survival · Cut 3 (mv-3)"
DEV_NOTE = "Development careers: official runner + DeepSeek, not official scores."


def speaker_notes() -> dict[int, str]:
    text = SCRIPT.read_text(encoding="utf-8")
    text = text.split("## Notas de grabación")[0]
    notes: dict[int, list[str]] = {}
    current = None
    for line in text.splitlines():
        m = re.match(r"\*\*\[S(\d+)\]\*\*", line.strip())
        if m:
            current = int(m.group(1))
            notes[current] = []
            continue
        if line.startswith("## ") or line.startswith("---"):
            current = None
            continue
        if current is not None:
            notes[current].append(line.replace("*", ""))
    return {k: "\n".join(v).strip() for k, v in notes.items()}


class Deck:
    def __init__(self) -> None:
        self.prs = Presentation()
        self.prs.slide_width, self.prs.slide_height = W, H
        self.blank = self.prs.slide_layouts[6]
        self.count = 0

    # -- primitives ---------------------------------------------------------
    def slide(self, dark: bool = False):
        s = self.prs.slides.add_slide(self.blank)
        self.count += 1
        bg = s.background.fill
        bg.solid()
        bg.fore_color.rgb = INK if dark else PAPER
        if not dark:
            self.text(s, FOOTER, MARGIN, H - Inches(0.5), Inches(8), Inches(0.3), size=10, color=MUTED)
            self.text(s, str(self.count), W - MARGIN - Inches(1), H - Inches(0.5), Inches(1), Inches(0.3),
                      size=10, color=MUTED, align=PP_ALIGN.RIGHT)
        return s

    def text(self, s, content, x, y, w, h, *, size=16, color=INK, bold=False, font=BODY,
             align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, italic=False, spacing=None):
        """content: str (\n = new paragraph) or list of paragraphs, each a str or list of (text, opts)."""
        tb = s.shapes.add_textbox(x, y, w, h)
        tf = tb.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = anchor
        for side in ("margin_left", "margin_right", "margin_top", "margin_bottom"):
            setattr(tf, side, 0)
        paras = content.split("\n") if isinstance(content, str) else content
        for i, para in enumerate(paras):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.alignment = align
            if spacing:
                p.space_after = Pt(spacing)
            runs = [(para, {})] if isinstance(para, str) else para
            for run_text, opts in runs:
                r = p.add_run()
                r.text = run_text
                f = r.font
                f.name = opts.get("font", font)
                f.size = Pt(opts.get("size", size))
                f.bold = opts.get("bold", bold)
                f.italic = opts.get("italic", italic)
                f.color.rgb = opts.get("color", color)
        return tb

    def box(self, s, x, y, w, h, fill, *, line=None, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.08):
        shp = s.shapes.add_shape(shape, x, y, w, h)
        shp.fill.solid()
        shp.fill.fore_color.rgb = fill
        if line is None:
            shp.line.fill.background()
        else:
            shp.line.color.rgb = line
            shp.line.width = Pt(1.25)
        shp.shadow.inherit = False
        if shape == MSO_SHAPE.ROUNDED_RECTANGLE:
            shp.adjustments[0] = radius
        shp.text_frame.text = ""
        return shp

    def badge(self, s, label, x, y, d, fill, color=PAPER, size=20):
        c = self.box(s, x, y, d, d, fill, shape=MSO_SHAPE.OVAL)
        tf = c.text_frame
        for side in ("margin_left", "margin_right", "margin_top", "margin_bottom"):
            setattr(tf, side, 0)
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        r = p.add_run()
        r.text = label
        r.font.name, r.font.size, r.font.bold, r.font.color.rgb = HEAD, Pt(size), True, color
        return c

    def arrow(self, s, x1, y1, x2, y2, color=INK_SOFT, width=2.0):
        ln = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, x1, y1, x2, y2)
        ln.line.color.rgb = color
        ln.line.width = Pt(width)
        tail = ln.line._get_or_add_ln().makeelement(qn("a:tailEnd"), {"type": "triangle", "w": "med", "len": "med"})
        ln.line._get_or_add_ln().append(tail)
        return ln

    def title(self, s, kicker, title, *, dark=False):
        self.text(s, kicker.upper(), MARGIN, Inches(0.45), Inches(11), Inches(0.35), size=13, bold=True,
                  color=AMBER if not dark else AMBER)
        self.text(s, title, MARGIN, Inches(0.8), W - 2 * MARGIN, Inches(0.9), size=34, bold=True, font=HEAD,
                  color=PAPER if dark else INK)

    def notes(self, s, n, notes):
        s.notes_slide.notes_text_frame.text = notes.get(n, "")


def build() -> Path:
    notes = speaker_notes()
    d = Deck()
    cw = W - 2 * MARGIN  # content width

    # 1. Title -----------------------------------------------------------------
    s = d.slide(dark=True)
    d.text(s, "GRADIENT DEPRESSION", MARGIN, Inches(1.6), Inches(10), Inches(0.4), size=16, bold=True, color=AMBER)
    d.text(s, "mv-3: one Skill,\none reply per decision", MARGIN, Inches(2.1), Inches(11), Inches(2.2),
           size=52, bold=True, font=HEAD, color=PAPER)
    d.text(s, "Huawei TechArena UK 2026 · Career Survival · Cut 3, final submission", MARGIN, Inches(4.6),
           Inches(11), Inches(0.4), size=18, color=RGBColor(0xC9, 0xD0, 0xD6))
    d.text(s, "Five questions, in order: design · logs · scripts · robustness · agents and Skills", MARGIN,
           Inches(6.3), Inches(11), Inches(0.4), size=14, color=MUTED)
    d.notes(s, 1, notes)

    # 2. The task --------------------------------------------------------------
    s = d.slide()
    d.title(s, "The task", "A DeepSeek agent lives a 48-month career")
    facts = [("48", "months of career"), ("3", "stories a month,\neffects hidden"), ("16", "quarterly phases:\nEnergy + a main action"),
             ("6", "months between\npromotion reviews")]
    bw, gap = Inches(2.75), Inches(0.33)
    for i, (big, small) in enumerate(facts):
        x = MARGIN + i * (bw + gap)
        d.box(s, x, Inches(2.0), bw, Inches(2.1), TINT)
        d.text(s, big, x + Inches(0.3), Inches(2.2), bw - Inches(0.6), Inches(0.9), size=48, bold=True, font=HEAD,
               color=AMBER)
        d.text(s, small, x + Inches(0.3), Inches(3.1), bw - Inches(0.6), Inches(0.9), size=16, color=INK_SOFT)
    d.box(s, MARGIN, Inches(4.5), Inches(6.0), Inches(1.9), BRICK_TINT)
    d.text(s, [[("Ways to lose", {"bold": True, "color": BRICK, "size": 18})],
               "Never promoted (dismissal)", "Hidden risk blows up twice (trust crisis)", "Burnout or ruin"],
           MARGIN + Inches(0.3), Inches(4.7), Inches(5.4), Inches(1.6), size=16, spacing=4)
    d.box(s, MARGIN + Inches(6.4), Inches(4.5), cw - Inches(6.4), Inches(1.9), AMBER_TINT)
    d.text(s, [[("The only gauge of hidden risk", {"bold": True, "color": INK, "size": 18})],
               "The tone of the monthly HR remark.",
               "Story effects are not shown before choosing."],
           MARGIN + Inches(6.7), Inches(4.7), cw - Inches(7.0), Inches(1.6), size=16, spacing=4)
    d.notes(s, 2, notes)

    # 3. Q1: three questions ------------------------------------------------------
    s = d.slide()
    d.title(s, "Q1 · How we thought", "Three questions behind every decision")
    qs = [("1", "What does this option probably change?", "Reading guide: what tends to move each stat and hidden risk",
           AMBER),
          ("2", "What does the career need now?", "Fixed priorities: stay in the run → win the next review → grow",
           TEAL),
          ("3", "Which rule applies in this phase?", "Scope: a self-computed switch, Review in N", INK_SOFT)]
    for i, (n, q, a, col) in enumerate(qs):
        y = Inches(2.0) + i * Inches(1.45)
        d.badge(s, n, MARGIN, y, Inches(0.8), col)
        d.text(s, q, MARGIN + Inches(1.1), y - Inches(0.02), Inches(6.6), Inches(0.5), size=22, bold=True, font=HEAD)
        d.text(s, a, MARGIN + Inches(1.1), y + Inches(0.5), Inches(6.6), Inches(0.6), size=16, color=INK_SOFT)
    x0 = MARGIN + Inches(8.2)
    d.box(s, x0, Inches(2.0), cw - Inches(8.2), Inches(4.3), TINT)
    d.text(s, "Why question 1 is the hardest", x0 + Inches(0.3), Inches(2.2), Inches(3.6), Inches(0.4), size=16,
           bold=True)
    d.text(s, "83%", x0 + Inches(0.3), Inches(2.7), Inches(3.6), Inches(0.8), size=48, bold=True, font=HEAD,
           color=BRICK)
    d.text(s, "of risky options spotted by DeepSeek", x0 + Inches(0.3), Inches(3.5), Inches(3.6), Inches(0.4),
           size=14, color=INK_SOFT)
    d.text(s, "45–49%", x0 + Inches(0.3), Inches(4.2), Inches(3.6), Inches(0.8), size=48, bold=True, font=HEAD,
           color=AMBER)
    d.text(s, "of options that raise Skill or Output", x0 + Inches(0.3), Inches(5.0), Inches(3.6), Inches(0.4),
           size=14, color=INK_SOFT)
    d.text(s, "Isolated-option tests, no Skill", x0 + Inches(0.3), Inches(5.75), Inches(3.6), Inches(0.4), size=12,
           color=MUTED, italic=True)
    d.notes(s, 3, notes)

    # 4. Decision loop -------------------------------------------------------------
    s = d.slide()
    d.title(s, "Q1 · How we thought", "The decision loop the Skill sets")
    y = Inches(2.1)
    bh = Inches(1.5)
    d.box(s, MARGIN, y, Inches(2.6), bh, TINT)
    d.text(s, [[("observe", {"bold": True, "font": MONO, "size": 18})],
               "Read events first: HR remark, review talk, warnings"],
           MARGIN + Inches(0.2), y + Inches(0.2), Inches(2.2), bh - Inches(0.3), size=14, spacing=4)
    d.arrow(s, MARGIN + Inches(2.7), y + bh / 2, MARGIN + Inches(3.2), y + bh / 2)
    # branch boxes
    bx = MARGIN + Inches(3.3)
    d.box(s, bx, Inches(1.85), Inches(5.1), Inches(1.05), AMBER_TINT)
    d.text(s, [[("Story: five ordered steps", {"bold": True, "size": 16})],
               "Survive → Risk → Wellbeing → Review close → Grow"],
           bx + Inches(0.2), Inches(1.95), Inches(4.8), Inches(0.9), size=15, spacing=2)
    d.box(s, bx, Inches(3.05), Inches(5.1), Inches(1.05), TEAL_TINT)
    d.text(s, [[("Quarter: first matching line wins", {"bold": True, "size": 16})],
               "Last quarter · near a limit · HR remark · plan per level"],
           bx + Inches(0.2), Inches(3.15), Inches(4.8), Inches(0.9), size=15, spacing=2)
    d.arrow(s, bx + Inches(5.2), y + bh / 2, bx + Inches(5.7), y + bh / 2)
    rx = bx + Inches(5.8)
    d.box(s, rx, y, cw - (rx - MARGIN), bh, INK)
    d.text(s, [[("ONE reply", {"bold": True, "size": 18, "color": AMBER})],
               [("take_action + observe", {"font": MONO, "size": 15, "color": PAPER})],
               [("the result and the next situation come back together", {"size": 13, "color": PAPER})]],
           rx + Inches(0.2), y + Inches(0.15), cw - (rx - MARGIN) - Inches(0.4), bh - Inches(0.2), spacing=3)
    # loop back
    d.arrow(s, rx + (cw - (rx - MARGIN)) / 2, y + bh + Inches(0.1), rx + (cw - (rx - MARGIN)) / 2,
            Inches(4.45), color=MUTED, width=1.5)
    d.text(s, "next situation", rx, Inches(4.45), cw - (rx - MARGIN), Inches(0.3), size=12, color=MUTED,
           align=PP_ALIGN.CENTER)
    # status line
    d.text(s, "Every note starts with the status line: memory and scope switch", MARGIN, Inches(4.95),
           Inches(11), Inches(0.4), size=16, bold=True)
    d.box(s, MARGIN, Inches(5.4), cw, Inches(0.75), TINT)
    d.text(s, "Review in N | Now S.. N.. O.. | Best S.. N.. O.. | Reviews here: 0", MARGIN + Inches(0.3),
           Inches(5.4), cw - Inches(0.6), Inches(0.75), size=20, font=MONO, anchor=MSO_ANCHOR.MIDDLE)
    d.text(s, "Review rules switch on only when N is 1 or 2 · Best resets on promotion · notes survive summaries",
           MARGIN, Inches(6.3), cw, Inches(0.35), size=14, color=INK_SOFT)
    d.notes(s, 4, notes)

    # 5. One Skill + manifest -------------------------------------------------------
    s = d.slide()
    d.title(s, "Q1 · How we thought", "One Skill, with the essentials repeated in the manifest")
    colw = (cw - Inches(0.4)) / 2
    d.box(s, MARGIN, Inches(2.0), colw, Inches(3.6), TINT)
    d.text(s, [[("skills/career-rules/SKILL.md", {"font": MONO, "bold": True, "size": 16})],
               "Turn loop", "Status line", "Story decisions: reading guide + five steps",
               "Quarterly phases: first matching line wins", "Near a limit: quick reference"],
           MARGIN + Inches(0.3), Inches(2.2), colw - Inches(0.6), Inches(3.3), size=16, spacing=6)
    x2 = MARGIN + colw + Inches(0.4)
    d.box(s, x2, Inches(2.0), colw, Inches(3.6), AMBER_TINT)
    d.text(s, [[("manifest.json instruction", {"font": MONO, "bold": True, "size": 16})],
               "The two-call turn loop", "Stories and quarters decided apart",
               "Drop options that may bury a problem", "Protect Skill, Network, Output before a review",
               "Quarterly plan from level 4 · one-line note"],
           x2 + Inches(0.3), Inches(2.2), colw - Inches(0.6), Inches(3.3), size=16, spacing=6)
    d.text(s, "Why: with several Skills the agent opened one and missed rules in another; it reads the Skill early "
              "and then works from context.",
           MARGIN, Inches(5.85), cw, Inches(0.7), size=16, color=INK_SOFT)
    d.notes(s, 5, notes)

    # 6. Timeline -------------------------------------------------------------------
    s = d.slide()
    d.title(s, "Q2 · From the logs to the changes", "Three cuts, three versions")
    yline = Inches(3.0)
    ln = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, MARGIN + Inches(0.4), yline, W - MARGIN - Inches(0.4), yline)
    ln.line.color.rgb, ln.line.width = MUTED, Pt(2)
    cuts = [("Cut 1 · 27 Oct", "t13-read-v4", "64.75", "official · 13th of 34",
             "Reading guide, five story steps, review protection, status line", INK_SOFT),
            ("Cut 2 · 30 Oct", "mv-5r", "45.44", "official",
             "One reply per decision; hidden costs named at the starting level only", BRICK),
            ("Cut 3 · 1 Nov", "mv-3", "?", "official score not yet known",
             "Hidden costs named before every review; no extra manifest line", AMBER)]
    cwid = (cw - Inches(0.6)) / 3
    for i, (when, name, score, sub, what, col) in enumerate(cuts):
        x = MARGIN + i * (cwid + Inches(0.3))
        d.badge(s, "", x + cwid / 2 - Inches(0.17), yline - Inches(0.17), Inches(0.34), col)
        d.text(s, when, x, Inches(2.1), cwid, Inches(0.4), size=15, bold=True, color=INK_SOFT, align=PP_ALIGN.CENTER)
        d.text(s, name, x, Inches(3.4), cwid, Inches(0.5), size=22, bold=True, font=MONO, align=PP_ALIGN.CENTER)
        d.text(s, score, x, Inches(3.95), cwid, Inches(0.9), size=48, bold=True, font=HEAD, color=col,
               align=PP_ALIGN.CENTER)
        d.text(s, sub, x, Inches(4.85), cwid, Inches(0.35), size=14, color=MUTED, align=PP_ALIGN.CENTER)
        d.text(s, what, x + Inches(0.2), Inches(5.35), cwid - Inches(0.4), Inches(0.9), size=15, color=INK_SOFT,
               align=PP_ALIGN.CENTER)
    d.notes(s, 6, notes)

    # 7. Logs -> rules ---------------------------------------------------------------
    s = d.slide()
    d.title(s, "Q2 · From the logs to the changes", "What the logs showed, and the rule it became")
    rows = [("Promotions lost by one point of Network or Output in the last story before a review",
             "Best value per level; protect Network and Output two months before a review, repair losses at once"),
            ("Responsible-sounding options (a private talk, a phased fix) carried hidden risk",
             "List of risky wording; strict mode when the HR remark is not friendly"),
            ("The agent obeyed the review rule but misread costs: “a polite refusal keeps Network”",
             "Hidden costs named: Network falls when someone is let down, even politely; Output falls when your "
             "time goes to someone else's work")]
    lw, rw = Inches(5.6), cw - Inches(5.6) - Inches(0.9)
    d.text(s, "IN THE LOGS", MARGIN, Inches(1.85), lw, Inches(0.3), size=12, bold=True, color=MUTED)
    d.text(s, "IN THE SKILL", MARGIN + lw + Inches(0.9), Inches(1.85), rw, Inches(0.3), size=12, bold=True,
           color=MUTED)
    for i, (left, right) in enumerate(rows):
        y = Inches(2.2) + i * Inches(1.45)
        d.box(s, MARGIN, y, lw, Inches(1.25), BRICK_TINT)
        d.text(s, left, MARGIN + Inches(0.25), y, lw - Inches(0.5), Inches(1.25), size=15,
               anchor=MSO_ANCHOR.MIDDLE)
        d.arrow(s, MARGIN + lw + Inches(0.15), y + Inches(0.62), MARGIN + lw + Inches(0.75), y + Inches(0.62))
        d.box(s, MARGIN + lw + Inches(0.9), y, rw, Inches(1.25), TEAL_TINT)
        d.text(s, right, MARGIN + lw + Inches(1.15), y, rw - Inches(0.5), Inches(1.25), size=15,
               anchor=MSO_ANCHOR.MIDDLE)
    d.notes(s, 7, notes)

    # 8. Tokens ------------------------------------------------------------------------
    s = d.slide()
    d.title(s, "Q2 · From the logs to the changes", "Every call resends the whole history")
    d.text(s, "1.4 M", MARGIN, Inches(2.0), Inches(4), Inches(1.1), size=66, bold=True, font=HEAD, color=BRICK)
    d.text(s, "tokens per game month, Cut 1", MARGIN, Inches(3.15), Inches(4), Inches(0.4), size=16, color=INK_SOFT)
    d.arrow(s, MARGIN + Inches(4.1), Inches(2.6), MARGIN + Inches(5.0), Inches(2.6), width=3)
    d.text(s, "0.5–0.8 M", MARGIN + Inches(5.3), Inches(2.0), Inches(5), Inches(1.1), size=66, bold=True, font=HEAD,
           color=TEAL)
    d.text(s, "tokens per game month, mv-3 (complete careers)", MARGIN + Inches(5.3), Inches(3.15), Inches(6),
           Inches(0.4), size=16, color=INK_SOFT)
    # before / after
    colw = (cw - Inches(0.4)) / 2
    d.box(s, MARGIN, Inches(4.0), colw, Inches(2.2), TINT)
    d.text(s, [[("Before: several replies per decision", {"bold": True, "size": 16})],
               [("reply → take_action", {"font": MONO, "size": 15})],
               [("reply → observe", {"font": MONO, "size": 15})],
               [("each reply resends everything so far", {"size": 14, "color": INK_SOFT})]],
           MARGIN + Inches(0.3), Inches(4.2), colw - Inches(0.6), Inches(1.9), spacing=5)
    x2 = MARGIN + colw + Inches(0.4)
    d.box(s, x2, Inches(4.0), colw, Inches(2.2), TEAL_TINT)
    d.text(s, [[("Now: one reply, two tool calls", {"bold": True, "size": 16})],
               [("tool_calls: [take_action(...), observe(...)]", {"font": MONO, "size": 15})],
               [("DeepSeek kept this pattern only when the Skill showed the literal shape of the reply",
                 {"size": 14, "color": INK_SOFT})]],
           x2 + Inches(0.3), Inches(4.2), colw - Inches(0.6), Inches(1.9), spacing=5)
    d.text(s, "Official rule: token efficiency is full at 0.5 M tokens per month or fewer.", MARGIN, Inches(6.4),
           cw, Inches(0.35), size=13, color=MUTED, italic=True)
    d.notes(s, 8, notes)

    # 9. mv-3 vs mv-4 --------------------------------------------------------------------
    s = d.slide()
    d.title(s, "Q2 · From the logs to the changes", "A fix that made play worse")
    d.box(s, MARGIN, Inches(1.85), cw, Inches(0.8), AMBER_TINT)
    d.text(s, [[("mv-4 = mv-3 + one manifest line:  ", {"bold": True}),
                ("“Never end a reply with text only … put the decision in the take_action call, not in prose.”",
                 {"italic": True})]],
           MARGIN + Inches(0.3), Inches(1.85), cw - Inches(0.6), Inches(0.8), size=16, anchor=MSO_ANCHOR.MIDDLE)
    data = [("", "mv-3 (submitted)", "mv-4"),
            ("Careers completed", "7 of 9", "6 of 11"),
            ("Mean of complete careers", "70.1", "64.2"),
            ("Reached the sixth level", "2", "0"),
            ("Ended early", "1 stopped by the runner\n1 ended at month 24", "3 trust crises, 1 dismissal,\n1 broke")]
    tbl = s.shapes.add_table(len(data), 3, MARGIN, Inches(2.85), cw, Inches(3.0)).table
    tbl.columns[0].width = Inches(4.1)
    tbl.columns[1].width = Inches(4.0)
    tbl.columns[2].width = cw - Inches(8.1)
    for r, row in enumerate(data):
        for c, val in enumerate(row):
            cell = tbl.cell(r, c)
            cell.fill.solid()
            cell.fill.fore_color.rgb = INK if r == 0 else (TEAL_TINT if c == 1 else (TINT if c == 0 else PAPER))
            cell.margin_left = cell.margin_right = Inches(0.2)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            tf = cell.text_frame
            tf.word_wrap = True
            for i, part in enumerate(val.split("\n")):
                p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
                run = p.add_run()
                run.text = part
                big = r in (1, 2, 3) and c > 0
                run.font.name = HEAD if big else BODY
                run.font.size = Pt(24 if big else 15)
                run.font.bold = r == 0 or big or c == 0
                run.font.color.rgb = PAPER if r == 0 else INK
    d.text(s, "Hypothesis, not proven: the line removes the short written reasoning the model needs when its provider "
              "does not reason privately. " + DEV_NOTE,
           MARGIN, Inches(6.1), cw, Inches(0.6), size=13, color=MUTED, italic=True)
    d.notes(s, 9, notes)

    # 10. Cheap tests vs careers -----------------------------------------------------------
    s = d.slide()
    d.title(s, "Q2 · From the logs to the changes", "Cheap tests misled us. Full careers did not")
    d.text(s, "WHAT THE CHEAP TEST SAID", MARGIN + Inches(2.9), Inches(1.85), Inches(4.5), Inches(0.3), size=12,
           bold=True, color=MUTED)
    d.text(s, "WHAT FULL CAREERS SHOWED", MARGIN + Inches(7.75), Inches(1.85), Inches(4.4), Inches(0.3), size=12,
           bold=True, color=MUTED)
    rows = [("Cut 2", "Bank of recorded situations: hidden-cost text adds risk at later levels → keep it to the "
                      "starting level", "2 of 3 careers collapsed at the starting level; 45.44 officially"),
            ("Cut-1 rules rebuilt", "Replays of the first months: leaves the starting level 79% vs 73%; top text "
                                    "score from two reviewers", "3 of 5 careers dismissed at the starting level"),
            ("Bolder variant", "Accept one mild risk a month to climb faster",
             "No higher than mv-3; blow-ups in two careers")]
    for i, (name, cheap, real) in enumerate(rows):
        y = Inches(2.2) + i * Inches(1.45)
        d.text(s, name, MARGIN, y, Inches(2.7), Inches(1.25), size=18, bold=True, font=HEAD,
               anchor=MSO_ANCHOR.MIDDLE)
        d.box(s, MARGIN + Inches(2.9), y, Inches(4.5), Inches(1.25), TINT)
        d.text(s, cheap, MARGIN + Inches(3.1), y, Inches(4.1), Inches(1.25), size=15, anchor=MSO_ANCHOR.MIDDLE)
        d.box(s, MARGIN + Inches(7.75), y, cw - Inches(7.75), Inches(1.25), BRICK_TINT)
        d.text(s, real, MARGIN + Inches(7.95), y, cw - Inches(8.15), Inches(1.25), size=15, anchor=MSO_ANCHOR.MIDDLE)
    d.notes(s, 10, notes)

    # 11. Q3 no scripts ----------------------------------------------------------------------
    s = d.slide()
    d.title(s, "Q3 · Scripts and reference files", "None, by choice")
    cards = [("Advisor script\n(a teammate's line)", "Its best career reached the sixth level, but 3 of 7 careers "
                                                     "ended early and complete ones used ~1.6× the tokens", AMBER),
             ("Script with state\n(our research replica)", "Added nothing: what fails is reading the options, and a "
                                                           "script reads no better than the model that feeds it",
              INK_SOFT),
             ("Reference files", "The agent read the Skill early and did not reopen supporting files", TEAL)]
    cwid = (cw - Inches(0.8)) / 3
    for i, (head, body, col) in enumerate(cards):
        x = MARGIN + i * (cwid + Inches(0.4))
        d.box(s, x, Inches(2.0), cwid, Inches(3.4), TINT)
        d.badge(s, str(i + 1), x + Inches(0.3), Inches(2.25), Inches(0.6), col, size=16)
        d.text(s, head, x + Inches(0.3), Inches(3.0), cwid - Inches(0.6), Inches(0.8), size=18, bold=True, font=HEAD)
        d.text(s, body, x + Inches(0.3), Inches(3.85), cwid - Inches(0.6), Inches(1.5), size=15, color=INK_SOFT)
    d.text(s, "Scripts that use only data from the current run were allowed by the organisers. mv-3 has one Skill and "
              "the manifest: no scripts, no reference files.",
           MARGIN, Inches(5.7), cw, Inches(0.7), size=16)
    d.notes(s, 11, notes)

    # 12. Q4 robustness -----------------------------------------------------------------------
    s = d.slide()
    d.title(s, "Q4 · Generality and robustness", "Built only on what the agent can see")
    colw = (cw - Inches(0.4)) / 2
    d.box(s, MARGIN, Inches(2.0), colw, Inches(4.2), TEAL_TINT)
    d.text(s, [[("The Skill relies on", {"bold": True, "size": 18, "color": TEAL})],
               "The tone of the HR remark", "Review talks and warnings", "Effects shown in the quarterly menu",
               "Its own one-line notes", "The published calendar: a review every six months",
               [("No event titles, fixed answers or hidden thresholds; our observations are marked as ours and the "
                 "game's signals come first", {"size": 14, "color": INK_SOFT})]],
           MARGIN + Inches(0.3), Inches(2.2), colw - Inches(0.6), Inches(3.9), size=16, spacing=5)
    x2 = MARGIN + colw + Inches(0.4)
    d.box(s, x2, Inches(2.0), colw, Inches(4.2), BRICK_TINT)
    d.text(s, [[("Known limits", {"bold": True, "size": 18, "color": BRICK})],
               "Perception: about one career in four still collapses, mostly at the starting level",
               "Third review at the starting level: won by 1 of the 11 careers that reached it; hidden risk, not "
               "missing stats",
               "The countdown assumes the six-month cycle",
               "Some providers sometimes write a tool call as text",
               [("Turn loop verified with two model providers", {"size": 14, "color": INK_SOFT})]],
           x2 + Inches(0.3), Inches(2.2), colw - Inches(0.6), Inches(3.9), size=16, spacing=5)
    d.notes(s, 12, notes)

    # 13. Q5 agents and Skills ------------------------------------------------------------------
    s = d.slide()
    d.title(s, "Q5 · Agents and Skills", "Skills change how an agent works, not what it sees")
    colw = (cw - Inches(0.4)) / 2
    d.box(s, MARGIN, Inches(2.0), colw, Inches(2.9), TEAL_TINT)
    d.text(s, [[("Strong at", {"bold": True, "size": 18, "color": TEAL})],
               "Format: one reply per decision cut tokens per month to less than half on average",
               "Concrete quarterly directions are followed far more often than general goals"],
           MARGIN + Inches(0.3), Inches(2.2), colw - Inches(0.6), Inches(2.6), size=16, spacing=6)
    x2 = MARGIN + colw + Inches(0.4)
    d.box(s, x2, Inches(2.0), colw, Inches(2.9), BRICK_TINT)
    d.text(s, [[("Weak at", {"bold": True, "size": 18, "color": BRICK})],
               "Perception: “protect Output” is obeyed, but the model still misses which option costs Output",
               "Scope: an earlier manual changed about 1 in 5 unrelated story choices",
               "One sentence can change how the model plays (mv-4)"],
           x2 + Inches(0.3), Inches(2.2), colw - Inches(0.6), Inches(2.6), size=16, spacing=6)
    d.box(s, MARGIN, Inches(5.2), cw, Inches(1.2), INK)
    d.text(s, "Skills give an agent priorities and discipline, not understanding.", MARGIN + Inches(0.4),
           Inches(5.2), cw - Inches(0.8), Inches(1.2), size=26, bold=True, font=HEAD, color=PAPER,
           anchor=MSO_ANCHOR.MIDDLE)
    d.notes(s, 13, notes)

    # 14. Closing ---------------------------------------------------------------------------------
    s = d.slide(dark=True)
    d.title(s, "Why we submitted mv-3", "The Skill of our best complete careers", dark=True)
    pts = [("70.1", "mean of 7 complete development careers out of 9; two reached the sixth level"),
           ("< ½", "the tokens per month of our first cut, on average"),
           ("0", "event titles, fixed answers or hidden thresholds")]
    for i, (big, small) in enumerate(pts):
        y = Inches(2.2) + i * Inches(1.25)
        d.text(s, big, MARGIN, y, Inches(2.4), Inches(1.0), size=44, bold=True, font=HEAD, color=AMBER,
               anchor=MSO_ANCHOR.MIDDLE)
        d.text(s, small, MARGIN + Inches(2.6), y, Inches(9), Inches(1.0), size=20, color=PAPER,
               anchor=MSO_ANCHOR.MIDDLE)
    d.text(s, "Scores are from our development careers with the official runner and DeepSeek, except the two "
              "official cut scores (64.75 and 45.44).  Thank you.",
           MARGIN, Inches(6.2), cw, Inches(0.7), size=14, color=RGBColor(0xC9, 0xD0, 0xD6))
    d.notes(s, 14, notes)

    out = OUT_DIR / "slides.pptx"
    d.prs.save(out)
    missing = [n for n in range(1, d.count + 1) if not notes.get(n)]
    if missing:
        raise SystemExit(f"slides without speaker notes: {missing}")
    return out


if __name__ == "__main__":
    print(build())
