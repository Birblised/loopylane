"""Builds ../loopy-lane-spotters-checklist.pdf: an A4 spotter's checklist with tick boxes and notes fields
that can be filled in on a phone or computer, or printed.  Run:  python src/checklist.py  (needs reportlab)."""
import os
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'loopy-lane-spotters-checklist.pdf')

PINE, SAGE, OCHRE, RUST, SLATE = (HexColor(c) for c in ('#1D3322', '#5C6F57', '#A67B4C', '#7B3E23', '#4E5D6A'))
INK, LINE, CREAM, PAPER = HexColor('#1D2A21'), HexColor('#D9CFB4'), HexColor('#F1E9D3'), HexColor('#FBF8F0')

for name, file in (('Petrona', 'Petrona-SemiBold.ttf'), ('Nunito', 'Nunito-Regular.ttf'), ('Nunito-SemiBold', 'Nunito-SemiBold.ttf'), ('Nunito-Italic', 'Nunito-Italic-Regular.ttf')):
    pdfmetrics.registerFont(TTFont(name, os.path.join(HERE, 'fonts', file)))

# (common name, scientific name, where and when)
GROUPS = [
    ('Birds', [
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
    ('Mammals', [
        ('Eland', 'Taurotragus oryx', 'Foothills, all year'),
        ('Grey rhebok', 'Pelea capreolus', 'High grassland, all year'),
        ('Mountain reedbuck', 'Redunca fulvorufula', 'Grassy slopes, all year'),
        ('Common duiker', 'Sylvicapra grimmia', 'Bush and forest edges, dawn and dusk'),
        ('Chacma baboon', 'Papio ursinus', 'Cliffs and valleys, all year'),
        ('Black-backed jackal', 'Lupulella mesomelas', 'Farmland, mostly at night'),
        ('Cape clawless otter', 'Aonyx capensis', 'Rivers and dams, look for tracks'),
    ]),
    ('Plants', [
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
ROW = 8.6 * mm


def header(c, first):
    """Deep Pine band with the logo on the first page; a slim running title after that."""
    if first:
        band = 46 * mm
        c.setFillColor(PINE); c.rect(0, H - band, W, band, stroke=0, fill=1)
        c.drawImage(os.path.join(HERE, 'logo.png'), M, H - 33 * mm, width=62 * mm, height=62 * mm * 181 / 606, mask='auto')
        c.setFillColor(CREAM); c.setFont('Petrona', 22); c.drawRightString(W - M, H - 20 * mm, "Spotter's checklist")
        c.setFillColor(HexColor('#C9BFA4')); c.setFont('Nunito', 8.5)
        c.drawRightString(W - M, H - 27 * mm, 'UNDERBERG  ·  SOUTHERN DRAKENSBERG  ·  KWAZULU-NATAL')
        c.setStrokeColor(OCHRE); c.setLineWidth(1.4); c.line(M, H - 39 * mm, W - M, H - 39 * mm)
        y = H - band - 9 * mm
        c.setFillColor(SLATE); c.setFont('Nunito', 9.5)
        c.drawString(M, y, 'Tick what you spot and note where and when. Fill it in on your phone, or print it for the car.')
        y -= 17 * mm
        form = c.acroForm
        for label, x, w in (('Name', M, 78 * mm), ('Dates of visit', M + 92 * mm, W - 2 * M - 92 * mm)):
            c.setFillColor(SLATE); c.setFont('Nunito', 7.5); c.drawString(x, y + 7.5 * mm, label.upper())
            form.textfield(name=label.lower().replace(' ', '_'), x=x, y=y, width=w, height=6.5 * mm, borderWidth=0,
                           fillColor=PAPER, textColor=INK, fontName='Helvetica', fontSize=10, borderColor=LINE)
            c.setStrokeColor(LINE); c.setLineWidth(.8); c.line(x, y, x + w, y)
        return y - 10 * mm
    c.setFillColor(PINE); c.rect(0, H - 12 * mm, W, 12 * mm, stroke=0, fill=1)
    c.setFillColor(CREAM); c.setFont('Petrona', 11); c.drawString(M, H - 8 * mm, "Loopy Lane  ·  Spotter's checklist")
    return H - 22 * mm


def footer(c, page):
    c.setStrokeColor(LINE); c.setLineWidth(.6); c.line(M, 16 * mm, W - M, 16 * mm)
    c.setFillColor(SLATE); c.setFont('Nunito', 7.5)
    c.drawString(M, 11 * mm, 'Keep your distance from nesting birds, close every gate, and stay on the road near private gardens.')
    c.drawRightString(W - M, 11 * mm, f'birblised.github.io/loopylane  ·  {page}')


def build():
    c = canvas.Canvas(OUT, pagesize=A4)
    c.setTitle("Loopy Lane spotter's checklist"); c.setAuthor('Loopy Lane'); c.setSubject('Birds, mammals and plants around Loopy Lane, Underberg')
    page, y = 1, header(c, True)
    count = 0
    for group, rows in GROUPS:
        if y - (14 * mm + ROW * 2) < 22 * mm:          # keep a heading with at least two of its rows
            footer(c, page); c.showPage(); page += 1; y = header(c, False)
        c.setFillColor(INK); c.setFont('Petrona', 15); c.drawString(M, y, group)
        c.setFillColor(SLATE); c.setFont('Nunito', 7); c.drawRightString(W - M, y + 1, 'WHERE AND WHEN YOU SAW IT')
        c.setStrokeColor(INK); c.setLineWidth(1.2); c.line(M, y - 2.5 * mm, W - M, y - 2.5 * mm)
        y -= 2.5 * mm + ROW
        for name, sci, where in rows:
            if y < 22 * mm:
                footer(c, page); c.showPage(); page += 1; y = header(c, False)
            count += 1
            c.acroForm.checkbox(name=f'seen_{count}', tooltip=f'Seen: {name}', x=M, y=y - 0.6 * mm, size=4.6 * mm,
                                buttonStyle='check', borderColor=SAGE, fillColor=PAPER, textColor=PINE, borderWidth=1, forceBorder=True)
            c.setFillColor(INK); c.setFont('Nunito-SemiBold', 10.5); c.drawString(M + 8 * mm, y + 1.6 * mm, name)
            c.setFillColor(SLATE); c.setFont('Nunito-Italic', 8.5)
            c.drawString(M + 8 * mm + pdfmetrics.stringWidth(name, 'Nunito-SemiBold', 10.5) + 2 * mm, y + 1.6 * mm, sci)
            c.setFillColor(RUST); c.setFont('Nunito', 7); c.drawString(M + 8 * mm, y - 1.6 * mm, where.upper())
            nx = W - M - 62 * mm
            c.acroForm.textfield(name=f'note_{count}', tooltip=f'Where and when: {name}', x=nx, y=y - 1 * mm, width=62 * mm, height=5.6 * mm,
                                 borderWidth=0, fillColor=PAPER, textColor=INK, fontName='Helvetica', fontSize=8.5)
            c.setStrokeColor(LINE); c.setLineWidth(.6); c.line(nx, y - 1 * mm, W - M, y - 1 * mm)
            y -= ROW
        y -= 6 * mm

    # Blank rows for anything not on the list, then lined notes, filling the rest of the last page
    if y - (14 * mm + ROW * 3) < 22 * mm:
        footer(c, page); c.showPage(); page += 1; y = header(c, False)
    c.setFillColor(INK); c.setFont('Petrona', 15); c.drawString(M, y, 'Other sightings')
    c.setFillColor(SLATE); c.setFont('Nunito', 7); c.drawRightString(W - M, y + 1, 'WHERE AND WHEN YOU SAW IT')
    c.setStrokeColor(INK); c.setLineWidth(1.2); c.line(M, y - 2.5 * mm, W - M, y - 2.5 * mm)
    y -= 2.5 * mm + ROW
    for i in range(1, 7):
        c.acroForm.checkbox(name=f'other_seen_{i}', tooltip='Seen', x=M, y=y - 0.6 * mm, size=4.6 * mm, buttonStyle='check',
                            borderColor=SAGE, fillColor=PAPER, textColor=PINE, borderWidth=1, forceBorder=True)
        nx = W - M - 62 * mm
        c.acroForm.textfield(name=f'other_name_{i}', tooltip='Species', x=M + 8 * mm, y=y - 1 * mm, width=nx - M - 14 * mm, height=5.6 * mm,
                             borderWidth=0, fillColor=PAPER, textColor=INK, fontName='Helvetica', fontSize=9.5)
        c.acroForm.textfield(name=f'other_note_{i}', tooltip='Where and when', x=nx, y=y - 1 * mm, width=62 * mm, height=5.6 * mm,
                             borderWidth=0, fillColor=PAPER, textColor=INK, fontName='Helvetica', fontSize=8.5)
        c.setStrokeColor(LINE); c.setLineWidth(.6)
        c.line(M + 8 * mm, y - 1 * mm, nx - 6 * mm, y - 1 * mm); c.line(nx, y - 1 * mm, W - M, y - 1 * mm)
        y -= ROW
    y -= 8 * mm
    if y - 30 * mm > 22 * mm:
        c.setFillColor(INK); c.setFont('Petrona', 15); c.drawString(M, y, 'Notes')
        c.setStrokeColor(INK); c.setLineWidth(1.2); c.line(M, y - 2.5 * mm, W - M, y - 2.5 * mm)
        top, bottom = y - 4 * mm, 22 * mm
        c.acroForm.textfield(name='notes', tooltip='Notes', x=M, y=bottom, width=W - 2 * M, height=top - bottom, borderWidth=0,
                             fillColor=PAPER, textColor=INK, fontName='Helvetica', fontSize=10, fieldFlags='multiline')
        c.setStrokeColor(LINE); c.setLineWidth(.6)
        ly = top - 8 * mm
        while ly > bottom:
            c.line(M, ly, W - M, ly); ly -= 8 * mm
    footer(c, page)
    c.save()
    print(f'{count} species on {page} page(s) -> {os.path.normpath(OUT)}')


if __name__ == '__main__':
    build()
