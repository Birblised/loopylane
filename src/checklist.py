"""Builds ../loopy-lane-spotters-checklist.pdf: an A4 spotter's checklist with tick boxes and notes fields
that can be filled in on a phone or computer, or printed.  Run:  python src/checklist.py  (needs reportlab).

It wears the website's look: a brown SA tourism sign with the logo and the Sani Pass road (read from
template.html, so both stay the same), Pacifico section titles with pictogram tiles, and ochre stitching."""
import math, os, re
from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'loopy-lane-spotters-checklist.pdf')

PINE, SAGE, OCHRE, RUST, SLATE = (HexColor(c) for c in ('#1D3322', '#5C6F57', '#A67B4C', '#7B3E23', '#4E5D6A'))
INK, LINE, CREAM, PAPER = HexColor('#1D2A21'), HexColor('#D9CFB4'), HexColor('#F1E9D3'), HexColor('#FBF8F0')
SIGN_BROWN, SIGN_WHITE, BOLT = HexColor('#6A3A22'), HexColor('#FBF8F0'), HexColor('#AEB4B6')
POST, POST_EDGE = HexColor('#AEB4B6'), HexColor('#8D9497')

for name, file in (('Petrona', 'Petrona-SemiBold.ttf'), ('Nunito', 'Nunito-Regular.ttf'), ('Nunito-SemiBold', 'Nunito-SemiBold.ttf'),
                   ('Nunito-Italic', 'Nunito-Italic-Regular.ttf'), ('Pacifico', 'Pacifico-Regular.ttf')):
    pdfmetrics.registerFont(TTFont(name, os.path.join(HERE, 'fonts', file)))

# The Sani Pass road, exactly as drawn on the website's sign (620 x 89 units)
SANI = [tuple(map(float, xy.split(','))) for xy in re.findall(r'[\d.]+,[\d.]+',
        re.search(r'<svg class="sani-road"[^>]*>\s*<path[^>]* d="([^"]+)"', open(os.path.join(HERE, 'template.html'), encoding='utf-8').read()).group(1))]

# (common name, scientific name, where and when)
GROUPS = [
    ('Birds', 'bird', [
        ('Bearded vulture', 'Gypaetus barbatus', 'Cliffs, all year'),
        ('Cape vulture', 'Gyps coprotheres', 'Cliffs, all year'),
        ('Jackal buzzard', 'Buteo rufofuscus', 'Open grassland, all year'),
        ('Wattled crane', 'Bugeranus carunculatus', 'Wetlands, all year'),
        ('Grey crowned crane', 'Balearica regulorum', 'Wetlands and pasture, all year'),
        ('Blue crane', 'Grus paradisea', 'Grassland, all year'),
        ('Southern bald ibis', 'Geronticus calvus', 'Burnt grassland, winter and spring'),
        ('Ground woodpecker', 'Geocolaptes olivaceus', 'Rocky slopes, all year'),
        ("Gurney's sugarbird", 'Promerops gurneyi', 'Flowering proteas, summer'),
        ('Drakensberg rockjumper', 'Chaetops aurantius', 'High rocks near the top of Sani Pass'),
    ]),
    ('Mammals', 'buck', [
        ('Eland', 'Taurotragus oryx', 'Foothills, all year'),
        ('Grey rhebok', 'Pelea capreolus', 'High grassland, all year'),
        ('Mountain reedbuck', 'Redunca fulvorufula', 'Grassy slopes, all year'),
        ('Common duiker', 'Sylvicapra grimmia', 'Bush and forest edges, dawn and dusk'),
        ('Chacma baboon', 'Papio ursinus', 'Cliffs and valleys, all year'),
        ('Black-backed jackal', 'Lupulella mesomelas', 'Farmland, mostly at night'),
        ('Cape clawless otter', 'Aonyx capensis', 'Rivers and dams, look for tracks'),
    ]),
    ('Plants', 'flower', [
        ('Common sugarbush', 'Protea caffra', 'Rocky slopes, flowers in summer'),
        ('Red-hot poker', 'Kniphofia', 'Streams and seeps, summer'),
        ('Agapanthus', 'Agapanthus campanulatus', 'Grassland, summer'),
        ('Fire lily', 'Cyrtanthus', 'Burnt veld, spring'),
        ('Everlastings', 'Helichrysum', 'Grassland, summer and autumn'),
        ('Watsonia', 'Watsonia', 'Grassland, summer'),
        ('Tree fern', 'Cyathea dregei', 'Stream banks, all year'),
        ('Ouhout', 'Leucosidea sericea', 'Streamsides, all year'),
    ]),
]

W, H = A4
M = 16 * mm
ROW = 8.3 * mm
NOTE_W = 62 * mm


def stitch(c, x0, x1, y, amp=1.1 * mm, wave=16 * mm):
    """A gentle wave of ochre stitching, like the edges between sections on the site."""
    p = c.beginPath(); p.moveTo(x0, y)
    steps = max(2, int((x1 - x0) / (wave / 8)))
    for i in range(1, steps + 1):
        x = x0 + (x1 - x0) * i / steps
        p.lineTo(x, y + amp * math.sin((x - x0) / wave * 2 * math.pi))
    c.saveState(); c.setStrokeColor(OCHRE); c.setLineWidth(1.1); c.setLineCap(1); c.setDash(3.2, 2.6); c.drawPath(p, stroke=1, fill=0); c.restoreState()


def sign(c, x, y, w, h, radius=4 * mm, bolts=True):
    """A brown SA tourism sign: brown board, white inset border, and grey corner bolts."""
    c.setFillColor(SIGN_BROWN); c.roundRect(x, y, w, h, radius, stroke=0, fill=1)
    inset = 2.2 * mm
    c.setStrokeColor(SIGN_WHITE); c.setLineWidth(1.6); c.roundRect(x + inset, y + inset, w - 2 * inset, h - 2 * inset, radius - inset * .6, stroke=1, fill=0)
    if bolts:
        c.setFillColor(BOLT)
        for bx, by in ((x + 4.6 * mm, y + 4.6 * mm), (x + w - 4.6 * mm, y + 4.6 * mm), (x + 4.6 * mm, y + h - 4.6 * mm), (x + w - 4.6 * mm, y + h - 4.6 * mm)):
            c.circle(bx, by, .8 * mm, stroke=0, fill=1)


def pictogram(c, kind, x, y, size=7.5 * mm):
    """A white pictogram on a small brown tile, like the services plate on the site's sign."""
    c.setFillColor(SIGN_BROWN); c.roundRect(x, y, size, size, 1.6 * mm, stroke=0, fill=1)
    s = size / 24
    c.saveState(); c.translate(x, y + size); c.scale(s, -s)          # draw in a 24-unit box, y down like the site's icons
    c.setStrokeColor(SIGN_WHITE); c.setLineWidth(2); c.setLineCap(1); c.setLineJoin(1)
    p = c.beginPath()
    if kind == 'bird':
        p.moveTo(3, 13); p.curveTo(6, 9, 9, 9, 12, 13); p.curveTo(15, 9, 18, 9, 21, 13)
    elif kind == 'buck':
        p.moveTo(8, 4); p.curveTo(8, 7, 9, 9, 11, 10); p.moveTo(16, 4); p.curveTo(16, 7, 15, 9, 13, 10)
        p.moveTo(9, 10); p.lineTo(15, 10); p.lineTo(14, 17); p.lineTo(10, 17); p.close()
        p.moveTo(10.5, 17); p.lineTo(10.5, 21); p.moveTo(13.5, 17); p.lineTo(13.5, 21)
    elif kind == 'flower':
        for cx, cy in ((12, 6), (8, 10), (16, 10)):
            p.circle(cx, cy, 2.6)
        p.moveTo(12, 12); p.lineTo(12, 21); p.moveTo(12, 17); p.curveTo(10, 15, 8, 15, 7, 16)
    elif kind == 'lens':
        p.circle(10, 10, 5); p.moveTo(14, 14); p.lineTo(20, 20)
    elif kind == 'pencil':
        p.moveTo(5, 19); p.lineTo(6, 15); p.lineTo(16, 5); p.lineTo(19, 8); p.lineTo(9, 18); p.close(); p.moveTo(14, 7); p.lineTo(17, 10)
    c.drawPath(p, stroke=1, fill=0); c.restoreState()


def heading(c, y, title, kind, side='WHERE AND WHEN YOU SAW IT'):
    pictogram(c, kind, M, y - 1.8 * mm)
    c.setFillColor(INK); c.setFont('Pacifico', 16); c.drawString(M + 10 * mm, y - .6 * mm, title)
    if side:
        c.setFillColor(SLATE); c.setFont('Nunito-SemiBold', 7); c.drawRightString(W - M, y + .4 * mm, side)
    stitch(c, M, W - M, y - 4.6 * mm)
    return y - 4.6 * mm - ROW


def tickbox(c, name, tooltip, x, y):
    """A rounded sage box with a tickable field over it."""
    size = 4.8 * mm
    c.setStrokeColor(SAGE); c.setFillColor(white); c.setLineWidth(1.2); c.roundRect(x, y, size, size, 1.1 * mm, stroke=1, fill=1)
    c.acroForm.checkbox(name=name, tooltip=tooltip, x=x + .5 * mm, y=y + .5 * mm, size=size - 1 * mm, buttonStyle='check',
                        borderWidth=0, borderColor=white, fillColor=white, textColor=PINE)


def notefield(c, name, tooltip, x, y, w, font_size=8.5):
    c.acroForm.textfield(name=name, tooltip=tooltip, x=x, y=y, width=w, height=5.6 * mm, borderWidth=0, fillColor=None, textColor=INK,
                         fontName='Helvetica', fontSize=font_size)
    c.setStrokeColor(LINE); c.setLineWidth(.7); c.setDash(1.2, 1.8); c.line(x, y, x + w, y); c.setDash()


def header(c, first):
    """The road sign on the first page; a slim brown plate as the running title after that."""
    if not first:
        sign(c, M, H - 21 * mm, W - 2 * M, 13 * mm, radius=3 * mm, bolts=False)
        c.setFillColor(SIGN_WHITE); c.setFont('Pacifico', 11); c.drawString(M + 6 * mm, H - 16.2 * mm, "Loopy Lane  ·  Spotter's checklist")
        return H - 32 * mm

    sx, sw, sh = M, W - 2 * M, 50 * mm
    top = H - 11 * mm
    sy = top - sh
    # galvanised posts, flat two-tone like the site's, standing under the sign
    for px in (sx + sw * .24, sx + sw * .76 - 4 * mm):
        c.setFillColor(POST); c.rect(px, sy - 7 * mm, 4 * mm, 7 * mm, stroke=0, fill=1)
        c.setFillColor(POST_EDGE); c.rect(px + 2.5 * mm, sy - 7 * mm, 1.5 * mm, 7 * mm, stroke=0, fill=1)
    sign(c, sx, sy, sw, sh)
    # logo (white lettering) on the left, title on the right
    lw = 70 * mm
    c.drawImage(os.path.join(HERE, 'logo.png'), sx + 9 * mm, top - 9 * mm - lw * 181 / 606, width=lw, height=lw * 181 / 606, mask='auto')
    c.setFillColor(SIGN_WHITE); c.setFont('Pacifico', 21); c.drawRightString(sx + sw - 9 * mm, top - 19 * mm, "Spotter's checklist")
    c.setFillColor(CREAM); c.setFont('Nunito-SemiBold', 7.2)
    c.drawRightString(sx + sw - 9 * mm, top - 25.5 * mm, 'UNDERBERG  ·  SOUTHERN DRAKENSBERG  ·  KWAZULU-NATAL')
    # the Sani Pass road in white along the bottom, labelled like the site's sign
    rw = sw - 50 * mm; rs = rw / 620; rx, ry = sx + 9 * mm, sy + 7 * mm + 89 * rs
    p = c.beginPath(); p.moveTo(rx + SANI[0][0] * rs, ry - SANI[0][1] * rs)
    for px, py in SANI[1:]:
        p.lineTo(rx + px * rs, ry - py * rs)
    c.setStrokeColor(SIGN_WHITE); c.setLineWidth(1.3); c.setLineJoin(1); c.setLineCap(1); c.drawPath(p, stroke=1, fill=0)
    c.setFillColor(SIGN_WHITE); c.setFont('Nunito-SemiBold', 8.5); c.drawRightString(sx + sw - 9 * mm, sy + 9 * mm, 'SANI PASS', charSpace=2.2)

    y = sy - 13 * mm
    c.setFillColor(SLATE); c.setFont('Nunito', 9.5)
    c.drawString(M, y, 'Tick what you spot and note where and when. Fill it in on your phone, or print it for the car.')
    y -= 13 * mm
    for label, x, w in (('Name', M, 78 * mm), ('Dates of visit', M + 92 * mm, W - 2 * M - 92 * mm)):
        c.setFillColor(SLATE); c.setFont('Nunito-SemiBold', 7.2); c.drawString(x, y + 7.5 * mm, label.upper())
        c.acroForm.textfield(name=label.lower().replace(' ', '_'), x=x, y=y, width=w, height=6.5 * mm, borderWidth=0,
                             fillColor=None, textColor=INK, fontName='Helvetica', fontSize=10)
        c.setStrokeColor(LINE); c.setLineWidth(.8); c.line(x, y, x + w, y)
    return y - 12 * mm


def footer(c, page):
    stitch(c, M, W - M, 17 * mm, amp=.8 * mm)
    c.setFillColor(SLATE); c.setFont('Nunito', 7.5)
    c.drawString(M, 10.5 * mm, 'Keep your distance from nesting birds, close every gate, and stay on the road near private gardens.')
    c.drawRightString(W - M, 10.5 * mm, f'birblised.github.io/loopylane  ·  {page}')


def build():
    c = canvas.Canvas(OUT, pagesize=A4)
    c.setTitle("Loopy Lane spotter's checklist"); c.setAuthor('Loopy Lane'); c.setSubject('Birds, mammals and plants around Loopy Lane, Underberg')
    page, y = 1, header(c, True)
    count = 0
    for group, kind, rows in GROUPS:
        if y - (14 * mm + ROW * 2) < 24 * mm:          # keep a heading with at least two of its rows
            footer(c, page); c.showPage(); page += 1; y = header(c, False)
        y = heading(c, y, group, kind)
        for name, sci, where in rows:
            if y < 24 * mm:
                footer(c, page); c.showPage(); page += 1; y = header(c, False)
            count += 1
            tickbox(c, f'seen_{count}', f'Seen: {name}', M, y - .8 * mm)
            c.setFillColor(INK); c.setFont('Nunito-SemiBold', 10.5); c.drawString(M + 8 * mm, y + 1.6 * mm, name)
            c.setFillColor(SLATE); c.setFont('Nunito-Italic', 8.5)
            c.drawString(M + 8 * mm + pdfmetrics.stringWidth(name, 'Nunito-SemiBold', 10.5) + 2 * mm, y + 1.6 * mm, sci)
            c.setFillColor(RUST); c.setFont('Nunito-SemiBold', 6.8); c.drawString(M + 8 * mm, y - 1.7 * mm, where.upper())
            notefield(c, f'note_{count}', f'Where and when: {name}', W - M - NOTE_W, y - 1 * mm, NOTE_W)
            y -= ROW
        y -= 6 * mm

    # Blank rows for anything not on the list, then lined notes, filling the rest of the last page
    if y - (14 * mm + ROW * 3) < 24 * mm:
        footer(c, page); c.showPage(); page += 1; y = header(c, False)
    y = heading(c, y, 'Other sightings', 'lens')
    for i in range(1, 7):
        tickbox(c, f'other_seen_{i}', 'Seen', M, y - .8 * mm)
        nx = W - M - NOTE_W
        notefield(c, f'other_name_{i}', 'Species', M + 8 * mm, y - 1 * mm, nx - M - 14 * mm, font_size=9.5)
        notefield(c, f'other_note_{i}', 'Where and when', nx, y - 1 * mm, NOTE_W)
        y -= ROW
    y -= 8 * mm
    if y - 30 * mm > 24 * mm:
        y = heading(c, y, 'Notes', 'pencil', side=None) + ROW - 2 * mm
        bottom = 24 * mm
        c.acroForm.textfield(name='notes', tooltip='Notes', x=M, y=bottom, width=W - 2 * M, height=y - bottom, borderWidth=0,
                             fillColor=None, textColor=INK, fontName='Helvetica', fontSize=10, fieldFlags='multiline')
        c.setStrokeColor(LINE); c.setLineWidth(.7); c.setDash(1.2, 1.8)
        ly = y - 8 * mm
        while ly > bottom:
            c.line(M, ly, W - M, ly); ly -= 8 * mm
        c.setDash()
    footer(c, page)
    c.save()
    print(f'{count} species on {page} page(s) -> {os.path.normpath(OUT)}')


if __name__ == '__main__':
    build()
