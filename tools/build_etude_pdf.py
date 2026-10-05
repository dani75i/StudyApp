"""Met en page l'étude existante, sans modifier les fichiers du site."""
from pathlib import Path
import os
import re
import sys
from html import escape

sys.path.insert(0, str(Path(os.environ['TEMP']) / 'exodeclic-pdf-libs'))
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, Table, TableStyle, Spacer
from reportlab.lib.enums import TA_LEFT

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'documents' / 'ExoDeclic_Etude_concurrentielle_2026-09-30.pdf'
OUT.parent.mkdir(exist_ok=True)
FONT = Path('C:/Windows/Fonts')
for name, file in [('Arial', 'arial.ttf'), ('Arial-Bold', 'arialbd.ttf'), ('Arial-Italic', 'ariali.ttf')]:
    pdfmetrics.registerFont(TTFont(name, str(FONT / file)))
pdfmetrics.registerFontFamily('Arial', normal='Arial', bold='Arial-Bold', italic='Arial-Italic', boldItalic='Arial-Bold')

INK = colors.HexColor('#17243E')
PURPLE = colors.HexColor('#675CF2')
TEAL = colors.HexColor('#078777')
MUTED = colors.HexColor('#59657B')
PALE = colors.HexColor('#F2F1FC')
LINE = colors.HexColor('#DFE3EF')
W, H = 595.276, 841.89
M = 43
CW = W - M * 2

styles = {
    'body': ParagraphStyle('body', fontName='Arial', fontSize=10.2, leading=14.5, textColor=INK, spaceAfter=9),
    'h3': ParagraphStyle('h3', fontName='Arial-Bold', fontSize=13, leading=17, textColor=PURPLE, spaceBefore=9, spaceAfter=8),
    'small': ParagraphStyle('small', fontName='Arial', fontSize=8.4, leading=11.5, textColor=MUTED, spaceAfter=6),
    'cell': ParagraphStyle('cell', fontName='Arial', fontSize=8.7, leading=12, textColor=INK),
    'head': ParagraphStyle('head', fontName='Arial-Bold', fontSize=8.8, leading=12, textColor=colors.white),
    'title': ParagraphStyle('title', fontName='Arial-Bold', fontSize=25, leading=30, textColor=INK),
}

def inline(s):
    s = escape(s)
    s = re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)', r'<link href="\2" color="#5148CE"><u>\1</u></link>', s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)
    s = re.sub(r'`([^`]+)`', r'<font size="8.6" color="#59657B">\1</font>', s)
    return s

def para(s, style='body'):
    return Paragraph(inline(s), styles[style])

def table(lines, widths=None):
    rows = []
    for line in lines:
        cells = [x.strip() for x in line.strip().strip('|').split('|')]
        if all(re.fullmatch(r'[-: ]+', x) for x in cells):
            continue
        rows.append(cells)
    widths = widths or [CW / len(rows[0])] * len(rows[0])
    if len(rows[0]) == 5 and rows[0][0] == 'Priorité':
        rows[0][0] = 'Prio.'
    data = [[para(x, 'head' if i == 0 else 'cell') for x in row] for i, row in enumerate(rows)]
    t = Table(data, colWidths=widths, hAlign='LEFT')
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PURPLE),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F6FB')]),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 9),
        ('RIGHTPADDING', (0, 0), (-1, -1), 9),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LINEBELOW', (0, 0), (-1, 0), 0.5, PURPLE),
        ('LINEBELOW', (0, 1), (-1, -1), 0.4, LINE),
    ]))
    if len(rows[0]) == 5:
        t.setStyle(TableStyle([
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ]))
    return t

def markdown(text, widths=None):
    lines = text.strip().splitlines()
    result = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        if line.startswith('|'):
            group = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                group.append(lines[i]); i += 1
            result.extend([table(group, widths), Spacer(1, 12)])
            continue
        if line.startswith('### '):
            result.append(para(line[4:], 'h3'))
        elif line.startswith('- '):
            result.append(para('• ' + line[2:]))
        else:
            group = [line]
            while i + 1 < len(lines) and lines[i + 1].strip() and not lines[i + 1].startswith(('#', '|', '- ')):
                i += 1; group.append(lines[i].strip())
            result.append(para(' '.join(group)))
        i += 1
    return result

source = (ROOT / 'ETUDE_CONCURRENTIELLE_EXODECLIC_2026-09-30.md').read_text(encoding='utf-8')
sections = {}
for part in re.split(r'^## ', source, flags=re.M)[1:]:
    heading, body = part.split('\n', 1)
    sections[int(heading.split('.')[0])] = body.strip()
subsections = {}
for part in re.split(r'^### ', sections[5], flags=re.M)[1:]:
    heading, body = part.split('\n', 1)
    subsections[heading[0]] = '### ' + heading + '\n' + body.strip()

c = canvas.Canvas(str(OUT), pagesize=(W, H), pageCompression=1)
c.setTitle('ExoDéclic — Étude concurrentielle et feuille de route')
c.setAuthor('Étude préparée pour ExoDéclic')
c.setSubject('Acquisition, inscriptions et préparation d’une offre gratuite et payante')

def draw_flows(flows, top, bottom=57):
    heights = []
    for f in flows:
        _, h = f.wrap(CW, H)
        heights.append(h + f.getSpaceBefore() + f.getSpaceAfter())
    available = top - bottom
    total = sum(heights)
    if total > available:
        raise ValueError(f'Page {c.getPageNumber()} déborde : {total:.0f} > {available:.0f} points')
    y = top
    for f in flows:
        _, h = f.wrap(CW, H)
        y -= f.getSpaceBefore() + h
        f.drawOn(c, M, y)
        y -= f.getSpaceAfter()
    return y

def footer(n):
    c.setStrokeColor(LINE); c.line(M, 42, W-M, 42)
    c.setFont('Arial', 8); c.setFillColor(MUTED)
    c.drawString(M, 27, 'EXODÉCLIC  /  ÉTUDE DU 30 SEPTEMBRE 2026')
    c.drawRightString(W-M, 27, f'{n:02d} / 12')

def page(n, label, title, flows, subtitle=None):
    c.setFillColor(PURPLE); c.rect(M, H-43, 25, 4, fill=1, stroke=0)
    c.setFont('Arial-Bold', 8); c.drawString(M+34, H-43, label.upper())
    c.setFillColor(MUTED); c.setFont('Arial', 8); c.drawRightString(W-M, H-43, 'EXODÉCLIC')
    h = styles['title'].leading
    titlep = Paragraph(escape(title), styles['title'])
    _, th = titlep.wrap(CW, 100)
    titlep.drawOn(c, M, H-68-th)
    top = H-84-th
    if subtitle:
        p = para(subtitle, 'small'); _, sh = p.wrap(CW, 100); p.drawOn(c, M, top-sh); top -= sh+14
    c.bookmarkPage(f'page{n}')
    c.addOutlineEntry(title, f'page{n}', level=0)
    end = draw_flows(flows, top)
    footer(n); c.showPage()
    print(f'Page {n:02d}: bas du contenu {end:.1f} pt')

# Couverture : schéma vectoriel et typographie, sans illustration décorative générée.
c.setFillColor(INK); c.rect(0, 0, W, H, fill=1, stroke=0)
c.setFillColor(PURPLE); c.circle(W-40, H-70, 150, fill=1, stroke=0)
c.setFillColor(colors.HexColor('#8279FA')); c.circle(W-8, H-50, 100, fill=1, stroke=0)
c.setFillColor(colors.white); c.setFont('Arial-Bold', 23); c.drawString(M, H-65, 'ExoDéclic')
c.setFont('Arial', 10); c.drawString(M, H-90, 'ÉTUDE CONCURRENTIELLE  •  SEPTEMBRE 2026')
coverstyle = ParagraphStyle('cover', fontName='Arial-Bold', fontSize=39, leading=46, textColor=colors.white)
p = Paragraph('Attirer.<br/>Convaincre.<br/>Faire revenir.', coverstyle)
p.wrap(CW, 200); p.drawOn(c, M, 506)
coverbody = ParagraphStyle('coverbody', fontName='Arial', fontSize=14, leading=21, textColor=colors.HexColor('#E2E5F3'))
p = Paragraph('Une étude pour développer les inscriptions<br/>et préparer une offre gratuite et payante.', coverbody)
p.wrap(CW, 100); p.drawOn(c, M, 435)
for x, number, text in [(M, '6', 'offres comparées'), (M+174, '100', 'chapitres annoncés'), (M+348, '90', 'jours de feuille de route')]:
    c.setFillColor(colors.HexColor('#293550')); c.roundRect(x, 265, 160, 100, 12, fill=1, stroke=0)
    c.setFillColor(colors.white); c.setFont('Arial-Bold', 30); c.drawString(x+15, 315, number)
    c.setFont('Arial', 9); c.drawString(x+15, 289, text)
c.setStrokeColor(colors.HexColor('#536078')); c.line(M, 217, W-M, 217)
c.setFillColor(colors.HexColor('#C8D0E2')); c.setFont('Arial', 10)
c.drawString(M, 185, 'Analyse du code et des ressources publiques en ligne')
c.drawString(M, 166, 'Constats, recommandations, priorités et sources cliquables')
c.setFont('Arial', 8); c.drawString(M, 35, 'ÉTUDE DU 30 SEPTEMBRE 2026'); c.drawRightString(W-M, 35, '01 / 12')
c.bookmarkPage('page1'); c.addOutlineEntry('ExoDéclic — Étude concurrentielle', 'page1', level=0); c.showPage()

toc = '''### Parcours de lecture
| Pages | Contenu |
|---|---|
| 03–04 | Le socle existant et les six concurrents |
| 05–07 | Les améliorations de conversion et de pédagogie |
| 08–09 | Acquisition et offre gratuite / payante |
| 10–11 | Feuille de route et indicateurs de réussite |
| 12 | Méthode, limites et références |
'''
page(2, 'Synthèse', 'Le premier enjeu : prouver la valeur', markdown(sections[1]) + markdown(toc, [62, CW-62]))
page(3, 'État des lieux', 'Un catalogue déjà conséquent', markdown(sections[3], [90, 90, 90, CW-270]))
page(4, 'Comparaison', 'Six offres, six enseignements', markdown(sections[4], [75, 151, 139, CW-365]), 'Comparaison des propositions publiques ; les performances pédagogiques ne sont pas évaluées.')
page(5, 'Recommandations / 1', 'Donner envie de commencer', markdown('\n\n'.join(subsections[x] for x in 'ABC')))
page(6, 'Recommandations / 2', 'Guider et mieux expliquer', markdown('\n\n'.join(subsections[x] for x in 'DE')))
flows = markdown(subsections['F'])
flows += markdown('''### Le suivi à construire
| Étape | Ce que l’élève et le parent doivent comprendre |
|---|---|
| Réussi une fois | L’exercice a été résolu, éventuellement après une aide. |
| À consolider | Une nouvelle tentative permettra de vérifier la compréhension. |
| Confirmé | Une réussite sur une nouvelle tentative donne un indice plus solide. |
''', [110, CW-110])
page(7, 'Recommandations / 3', 'Rendre la progression crédible', flows, 'Le tableau ci-dessous illustre la recommandation ; ce ne sont pas des fonctionnalités déjà livrées.')
page(8, 'Acquisition', 'Recruter autour d’un besoin précis', markdown(sections[6]))
page(9, 'Modèle économique', 'Faire payer un accompagnement utile', markdown(sections[7], [CW/2, CW/2]))
page(10, 'Exécution', 'Une feuille de route progressive', markdown(sections[8], [42, 130, 80, 92, CW-344]))
page(11, 'Mesure', 'Suivre les usages après l’inscription', markdown(sections[9], [88, 220, CW-308]) + [para('Ce qui peut attendre', 'h3')] + markdown(sections[10]))

refs = '''### Références à consulter
Les liens détaillés sont conservés dans les tableaux et les constats. Références principales :
'''
flows = markdown(sections[2]) + markdown(refs)
for name, url in [
    ('ExoDéclic : catalogue et volumes', 'https://www.exodeclic.fr/api/public/catalog'),
    ('Afterclasse : présentation de l’offre', 'https://www.afterclasse.fr/'),
    ('Lumni : collège', 'https://www.lumni.fr/college'),
    ('Mathenpoche : ressources', 'https://mathenpoche.sesamath.net/'),
    ('Maths et tiques : cours par niveau', 'https://www.maths-et-tiques.fr/index.php/cours-maths'),
    ('Kartable : fonctionnalités et formules', 'https://www.kartable.fr/'),
    ('SchoolMouv : offre collège', 'https://www.schoolmouv.fr/college'),
    ('Éducation nationale : programmes du collège', 'https://www.education.gouv.fr/les-programmes-du-college-470408'),
]:
    flows.append(para(f'[{name}]({url})', 'small'))
flows.append(para('Base documentaire : ETUDE_CONCURRENTIELLE_EXODECLIC_2026-09-30.md. Les références de fichiers et numéros de ligne désignent le dépôt local examiné. Cette édition conserve le contenu de l’étude et ajoute un tableau explicatif du suivi.', 'small'))
page(12, 'Méthode & sources', 'Ce que cette étude permet de conclure', flows)
c.save()
print(OUT)
