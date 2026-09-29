# -*- coding: utf-8 -*-
"""Rodada 2: refinamento da linha A (filete) e C (selo).
Fios mais finos, mais ar, peso leve e comparacao entre tres serifadas."""
import os, io, math
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools.pens.svgPathPen import SVGPathPen

BASE   = r'C:\Users\eleut\claudinho\singular-id-visual'
FONTES = os.path.join(BASE, 'fontes')
SAIDA  = os.path.join(BASE, 'previas2')
os.makedirs(SAIDA, exist_ok=True)

OURO, OURO_CLARO = '#B08D4F', '#C9A662'
NAVY, OFFWHITE   = '#0E1E33', '#F8F5EF'
CORM = 'CormorantGaramond[wght].ttf'
PLAY = 'PlayfairDisplay[wght].ttf'
GARA = 'EBGaramond[wght].ttf'
JOST = 'Jost[wght].ttf'

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
            x += tam * 0.30; continue
        pen = SVGPathPen(gs); gs[n].draw(pen); d = pen.getCommands()
        av = hmtx[n][0] * esc
        if d: saida.append((d, x, esc, av))
        x += av + tracking * tam
    if saida: x -= tracking * tam
    return saida, x

def por(gs, y, cor, dx=0.0):
    return ''.join('<path d="%s" transform="translate(%.2f %.2f) scale(%.5f %.5f)" fill="%s"/>'
                   % (d, dx + x, y, e, -e, cor) for d, x, e, _ in gs)

def svg(L, A, corpo, fundo=None):
    f = '<rect width="%d" height="%d" fill="%s"/>' % (L, A, fundo) if fundo else ''
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d">%s%s</svg>'
            % (L, A, L, A, f, corpo))

def fio(x1, y, x2, cor, w=0.7):
    return '<path d="M %.1f %.1f L %.1f %.1f" stroke="%s" stroke-width="%.2f"/>' % (x1, y, x2, y, cor, w)

# --------------------------------------------------- 1 · filete, peso leve
def v1(serif, cor=NAVY, acento=OURO, fundo=None, peso=300):
    nome, ln = glifos(serif, peso, 'SINGULAR PRIME', 84, tracking=0.28)
    sub,  ls = glifos(JOST, 300, 'CONSULTORIA IMOBILIÁRIA', 14, tracking=0.56)
    L = int(max(ln, ls) + 150); A = 250
    c = [por(nome, 132, cor, (L - ln) / 2), por(sub, 184, cor, (L - ls) / 2),
         fio((L - ln) / 2 - 16, 72, (L + ln) / 2 + 16, acento, 0.6),
         fio((L - ln) / 2 - 16, 208, (L + ln) / 2 + 16, acento, 0.6)]
    return svg(L, A, ''.join(c), fundo)

# --------------------------------------------------- 2 · duas linhas, fio curto
def v2(serif, cor=NAVY, acento=OURO, fundo=None):
    n1, l1 = glifos(serif, 300, 'SINGULAR', 96, tracking=0.30)
    n2, l2 = glifos(serif, 300, 'PRIME', 96, tracking=0.30)
    sub, ls = glifos(JOST, 300, 'CONSULTORIA IMOBILIÁRIA', 13, tracking=0.58)
    L = int(max(l1, l2, ls) + 160); A = 330
    c = [por(n1, 128, cor, (L - l1) / 2), por(n2, 236, cor, (L - l2) / 2),
         fio(L / 2 - 30, 160, L / 2 + 30, acento, 0.6),
         por(sub, 292, cor, (L - ls) / 2)]
    return svg(L, A, ''.join(c), fundo)

# --------------------------------------------------- 3 · selo refinado
def v3(serif, cor=NAVY, acento=OURO, fundo=None):
    T = 360; cx = cy = T / 2
    c = ['<circle cx="%d" cy="%d" r="164" fill="none" stroke="%s" stroke-width="0.7"/>' % (cx, cy, acento),
         '<circle cx="%d" cy="%d" r="126" fill="none" stroke="%s" stroke-width="0.4"/>' % (cx, cy, acento)]
    texto = 'SINGULAR PRIME   ·   CONSULTORIA IMOBILIÁRIA   ·   '
    gs, larg = glifos(JOST, 300, texto, 13, tracking=0.44)
    raio = 146
    ang0 = -90 - (larg / (2 * math.pi * raio)) * 180
    for d, x, e, av in gs:
        ang = ang0 + ((x + av / 2) / (2 * math.pi * raio)) * 360
        c.append('<g transform="translate(%.2f %.2f) rotate(%.2f) translate(0 %.2f)">'
                 '<path d="%s" transform="translate(%.2f 0) scale(%.5f %.5f)" fill="%s"/></g>'
                 % (cx, cy, ang + 90, -raio, d, -av / 2, e, -e, cor))
    sp, lsp = glifos(serif, 300, 'SP', 104)
    c.append(por(sp, cy + 34, cor, cx - lsp / 2))
    c.append(fio(cx - 26, cy + 56, cx + 26, acento, 0.6))
    return svg(T, T, ''.join(c), fundo)

# --------------------------------------------------- 4 · monograma de perfil
def v4(serif, cor=NAVY, acento=OURO, fundo=None):
    T = 240; cx = cy = T / 2
    sp, lsp = glifos(serif, 300, 'SP', 96)
    c = ['<circle cx="%d" cy="%d" r="108" fill="none" stroke="%s" stroke-width="0.7"/>' % (cx, cy, acento),
         por(sp, cy + 30, cor, cx - lsp / 2),
         fio(cx - 24, cy + 52, cx + 24, acento, 0.6)]
    return svg(T, T, ''.join(c), fundo)

# --------------------------------------------------- 5 · filete com iniciais
def v5(serif, cor=NAVY, acento=OURO, fundo=None):
    sp, lsp = glifos(serif, 300, 'SP', 62)
    nome, ln = glifos(serif, 300, 'SINGULAR PRIME', 62, tracking=0.28)
    sub, ls = glifos(JOST, 300, 'CONSULTORIA IMOBILIÁRIA', 12, tracking=0.58)
    L = int(max(ln, ls) + 150); A = 300
    c = [por(sp, 112, cor, L / 2 - lsp / 2),
         fio(L / 2 - 46, 140, L / 2 + 46, acento, 0.6),
         por(nome, 210, cor, (L - ln) / 2), por(sub, 246, cor, (L - ls) / 2)]
    return svg(L, A, ''.join(c), fundo)

VARIANTES = [('1_filete', v1), ('2_duas_linhas', v2), ('3_selo', v3),
             ('4_monograma', v4), ('5_filete_iniciais', v5)]
SERIFS = {'corm': CORM, 'play': PLAY, 'gara': GARA}

for nome, fn in VARIANTES:
    for sig, serif in SERIFS.items():
        io.open(os.path.join(SAIDA, '%s_%s_claro.svg' % (nome, sig)), 'w', encoding='utf-8').write(fn(serif))
        io.open(os.path.join(SAIDA, '%s_%s_escuro.svg' % (nome, sig)), 'w', encoding='utf-8').write(
            fn(serif, OFFWHITE, OURO_CLARO, NAVY))
    print('%-18s ok' % nome)
print('\nem', SAIDA)
