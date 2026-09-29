# -*- coding: utf-8 -*-
"""Cinco caminhos de marca para a Singular Prime, todos apoiados em
tipografia e geometria exata. Sem paisagem desenhada a mao."""
import os, io, math
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools.pens.svgPathPen import SVGPathPen

BASE   = r'C:\Users\eleut\claudinho\singular-id-visual'
FONTES = os.path.join(BASE, 'fontes')
SAIDA  = os.path.join(BASE, 'previas')
os.makedirs(SAIDA, exist_ok=True)

OURO, OURO_CLARO = '#B08D4F', '#C9A662'
NAVY, OFFWHITE   = '#0E1E33', '#F8F5EF'
CORM, JOST = 'CormorantGaramond[wght].ttf', 'Jost[wght].ttf'

_c = {}
def fonte(arq, peso):
    if (arq, peso) not in _c:
        _c[(arq, peso)] = instancer.instantiateVariableFont(
            TTFont(os.path.join(FONTES, arq)), {'wght': peso})
    return _c[(arq, peso)]

def glifos(arq, peso, texto, tam, tracking=0.0):
    f = fonte(arq, peso); upm = f['head'].unitsPerEm
    cmap, gs, hmtx = f.getBestCmap(), f.getGlyphSet(), f['hmtx']
    esc = tam / upm; saida, x = [], 0.0
    for ch in texto:
        n = cmap.get(ord(ch))
        if n is None:
            x += tam * 0.32; continue
        pen = SVGPathPen(gs); gs[n].draw(pen); d = pen.getCommands()
        av = hmtx[n][0] * esc
        if d: saida.append((d, x, esc, av))
        x += av + tracking * tam
    if saida: x -= tracking * tam
    return saida, x

def por(gs, y, cor, dx=0.0):
    return ''.join('<path d="%s" transform="translate(%.2f %.2f) scale(%.5f %.5f)" fill="%s"/>'
                   % (d, dx + x, y, e, -e, cor) for d, x, e, _ in gs)

def svg(larg, alt, corpo, fundo=None):
    f = '<rect width="%d" height="%d" fill="%s"/>' % (larg, alt, fundo) if fundo else ''
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d">%s%s</svg>'
            % (larg, alt, larg, alt, f, corpo))

# ---------------------------------------------------------------- A · filete
def dir_a(cor=NAVY, acento=OURO, fundo=None):
    """Wordmark puro entre dois filetes. O caminho das casas de leilao."""
    nome, ln = glifos(CORM, 400, 'SINGULAR PRIME', 78, tracking=0.20)
    sub,  ls = glifos(JOST, 400, 'CONSULTORIA IMOBILIÁRIA', 15, tracking=0.42)
    L = max(ln, ls) + 120
    c = [por(nome, 128, cor, (L - ln) / 2), por(sub, 172, cor, (L - ls) / 2)]
    for y in (74, 196):
        c.append('<path d="M %.1f %d L %.1f %d" stroke="%s" stroke-width="1.1"/>'
                 % ((L - ln) / 2 - 10, y, (L + ln) / 2 + 10, y, acento))
    return svg(int(L), 250, ''.join(c), fundo)

# ---------------------------------------------------------------- B · placa
def dir_b(cor=NAVY, acento=OURO, fundo=None):
    """Moldura fina de passe-partout. Le como placa de bronze."""
    nome, ln = glifos(CORM, 400, 'SINGULAR', 66, tracking=0.22)
    n2,   l2 = glifos(CORM, 400, 'PRIME', 66, tracking=0.22)
    sub,  ls = glifos(JOST, 400, 'CONSULTORIA IMOBILIÁRIA', 13, tracking=0.44)
    L, A = 420, 300
    c = ['<rect x="26" y="26" width="%d" height="%d" fill="none" stroke="%s" stroke-width="1.2"/>' % (L-52, A-52, acento),
         '<rect x="36" y="36" width="%d" height="%d" fill="none" stroke="%s" stroke-width="0.6"/>' % (L-72, A-72, acento),
         por(nome, 140, cor, (L - ln) / 2), por(n2, 206, cor, (L - l2) / 2),
         por(sub, 246, cor, (L - ls) / 2)]
    return svg(L, A, ''.join(c), fundo)

# ---------------------------------------------------------------- C · selo
def dir_c(cor=NAVY, acento=OURO, fundo=None):
    """Selo circular com o nome correndo na borda. Classico de alto padrao."""
    T, A = 340, 340
    cx = cy = T / 2
    c = ['<circle cx="%d" cy="%d" r="152" fill="none" stroke="%s" stroke-width="1.2"/>' % (cx, cy, acento),
         '<circle cx="%d" cy="%d" r="120" fill="none" stroke="%s" stroke-width="0.6"/>' % (cx, cy, acento)]
    # texto correndo no anel, glifo a glifo
    texto = 'SINGULAR PRIME  ·  CONSULTORIA IMOBILIÁRIA  ·  '
    gs, larg = glifos(JOST, 400, texto, 15, tracking=0.30)
    raio = 136
    total = larg
    ang0 = -90 - (total / (2 * math.pi * raio)) * 360 / 2
    for d, x, e, av in gs:
        ang = ang0 + ((x + av / 2) / (2 * math.pi * raio)) * 360
        c.append('<g transform="translate(%.2f %.2f) rotate(%.2f) translate(0 %.2f)">'
                 '<path d="%s" transform="translate(%.2f 0) scale(%.5f %.5f)" fill="%s"/></g>'
                 % (cx, cy, ang + 90, -raio, d, -av / 2, e, -e, cor))
    # monograma no centro
    sp, lsp = glifos(CORM, 400, 'SP', 88)
    c.append(por(sp, cy + 30, cor, cx - lsp / 2))
    c.append('<path d="M %d %d L %d %d" stroke="%s" stroke-width="1"/>' % (cx-34, cy+50, cx+34, cy+50, acento))
    return svg(T, A, ''.join(c), fundo)

# ---------------------------------------------------------------- D · portal
def dir_d(cor=NAVY, acento=OURO, fundo=None):
    """Portal: arco fino e vazio, com as iniciais. Arquitetonico, sem paisagem."""
    sp, lsp = glifos(CORM, 400, 'SP', 58)
    nome, ln = glifos(CORM, 400, 'SINGULAR PRIME', 54, tracking=0.20)
    sub,  ls = glifos(JOST, 400, 'CONSULTORIA IMOBILIÁRIA', 12.5, tracking=0.44)
    L, A = int(max(ln, ls) + 90), 340
    cx = L / 2
    arco = ('<path d="M %.1f 232 L %.1f 148 A 50 50 0 0 1 %.1f 148 L %.1f 232" fill="none" '
            'stroke="%s" stroke-width="1.6"/>' % (cx-50, cx-50, cx+50, cx+50, acento))
    c = [arco, por(sp, 192, cor, cx - lsp / 2),
         '<path d="M %.1f 232 L %.1f 232" stroke="%s" stroke-width="1.6"/>' % (cx-50, cx+50, acento),
         por(nome, 292, cor, (L - ln) / 2), por(sub, 322, cor, (L - ls) / 2)]
    return svg(L, A, ''.join(c), fundo)

# ---------------------------------------------------------------- E · losango
def dir_e(cor=NAVY, acento=OURO, fundo=None):
    """Losango fino com as iniciais. Discreto e facil de reduzir."""
    nome, ln = glifos(CORM, 400, 'SINGULAR PRIME', 52, tracking=0.20)
    sub,  ls = glifos(JOST, 400, 'CONSULTORIA IMOBILIÁRIA', 12.5, tracking=0.44)
    L, A = int(max(ln, ls) + 90), 330
    cx = L / 2
    c = ['<path d="M %.1f 96 L %.1f 158 L %.1f 220 L %.1f 158 Z" fill="none" stroke="%s" stroke-width="1.4"/>'
         % (cx, cx+58, cx, cx-58, acento),
         '<path d="M %.1f 112 L %.1f 158 L %.1f 204 L %.1f 158 Z" fill="none" stroke="%s" stroke-width="0.6"/>'
         % (cx, cx+44, cx, cx-44, acento)]
    sp, lsp = glifos(CORM, 500, 'SP', 46)
    c.append(por(sp, 174, cor, cx - lsp / 2))
    c.append(por(nome, 278, cor, (L - ln) / 2))
    c.append(por(sub, 306, cor, (L - ls) / 2))
    return svg(L, A, ''.join(c), fundo)

CAMINHOS = {'A_filete': dir_a, 'B_placa': dir_b, 'C_selo': dir_c, 'D_portal': dir_d, 'E_losango': dir_e}
for nome, fn in CAMINHOS.items():
    io.open(os.path.join(SAIDA, '%s_claro.svg' % nome), 'w', encoding='utf-8').write(fn(NAVY, OURO))
    io.open(os.path.join(SAIDA, '%s_escuro.svg' % nome), 'w', encoding='utf-8').write(fn(OFFWHITE, OURO_CLARO, NAVY))
    print('%-10s ok' % nome)
print('\nem', SAIDA)
