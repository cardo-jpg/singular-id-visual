# -*- coding: utf-8 -*-
"""Rodada 3: mais oito caminhos. Monogramas, brasao, selo oval,
contraponto em sem serifa e lockup horizontal."""
import os, io, math
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools.pens.svgPathPen import SVGPathPen

BASE   = r'C:\Users\eleut\claudinho\singular-id-visual'
FONTES = os.path.join(BASE, 'fontes')
SAIDA  = os.path.join(BASE, 'previas3')
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

def assinatura_sob(L, y, cor, acento, serif, tam=54, tsub=12):
    nome, ln = glifos(serif, 300, 'SINGULAR PRIME', tam, tracking=0.28)
    sub,  ls = glifos(JOST, 300, 'CONSULTORIA IMOBILIÁRIA', tsub, tracking=0.58)
    return por(nome, y, cor, (L - ln) / 2) + por(sub, y + 32, cor, (L - ls) / 2), max(ln, ls)

# --------------------------------------------------- 6 · monograma entrelacado
def v6(serif, cor=NAVY, acento=OURO, fundo=None):
    T = 300; cx = cy = T / 2
    s_, ls_ = glifos(serif, 300, 'S', 132)
    p_, lp_ = glifos(serif, 300, 'P', 132)
    largura = ls_ + lp_ * 0.52
    x0 = cx - largura / 2
    c = ['<circle cx="%d" cy="%d" r="128" fill="none" stroke="%s" stroke-width="0.7"/>' % (cx, cy, acento)]
    c.append(por(s_, cy + 44, cor, x0))
    c.append(por(p_, cy + 44, cor, x0 + ls_ * 0.62))
    return svg(T, T, ''.join(c), fundo)

# --------------------------------------------------- 7 · monograma em quadro
def v7(serif, cor=NAVY, acento=OURO, fundo=None):
    L, A = 300, 300
    sp, lsp = glifos(serif, 300, 'SP', 92)
    c = ['<rect x="62" y="62" width="176" height="176" fill="none" stroke="%s" stroke-width="0.8"/>' % acento,
         '<rect x="72" y="72" width="156" height="156" fill="none" stroke="%s" stroke-width="0.4"/>' % acento,
         por(sp, 178, cor, L / 2 - lsp / 2)]
    return svg(L, A, ''.join(c), fundo)

# --------------------------------------------------- 8 · sem serifa leve
def v8(serif, cor=NAVY, acento=OURO, fundo=None):
    nome, ln = glifos(JOST, 300, 'SINGULAR PRIME', 68, tracking=0.34)
    sub,  ls = glifos(JOST, 300, 'CONSULTORIA IMOBILIÁRIA', 12.5, tracking=0.6)
    L = int(max(ln, ls) + 150); A = 220
    c = [por(nome, 116, cor, (L - ln) / 2), por(sub, 158, cor, (L - ls) / 2),
         fio(L / 2 - 30, 134, L / 2 + 30, acento, 0.6)]
    return svg(L, A, ''.join(c), fundo)

# --------------------------------------------------- 9 · PRIME deslocado
def v9(serif, cor=NAVY, acento=OURO, fundo=None):
    n1, l1 = glifos(serif, 300, 'SINGULAR', 104, tracking=0.16)
    n2, l2 = glifos(JOST, 300, 'PRIME', 22, tracking=0.72)
    sub, ls = glifos(JOST, 300, 'CONSULTORIA IMOBILIÁRIA', 11.5, tracking=0.6)
    L = int(l1 + 150); A = 250
    x0 = (L - l1) / 2
    c = [por(n1, 132, cor, x0),
         por(n2, 170, cor, x0 + l1 - l2),
         fio(x0, 152, x0 + l1, acento, 0.5),
         por(sub, 208, cor, x0)]
    return svg(L, A, ''.join(c), fundo)

# --------------------------------------------------- 10 · brasao minimo
def v10(serif, cor=NAVY, acento=OURO, fundo=None):
    nome_, ln_ = glifos(serif, 300, 'SINGULAR PRIME', 46, tracking=0.28)
    L, A = int(ln_ + 140), 372
    cx = L / 2
    escudo = ('<path d="M %.1f 84 L %.1f 84 L %.1f 200 Q %.1f 248 %.1f 274 Q %.1f 248 %.1f 200 Z" '
              'fill="none" stroke="%s" stroke-width="0.9"/>'
              % (cx-60, cx+60, cx+60, cx+60, cx, cx-60, cx-60, acento))
    sp, lsp = glifos(serif, 300, 'SP', 74)
    c = [escudo, por(sp, 190, cor, cx - lsp / 2), fio(cx-26, 210, cx+26, acento, 0.5)]
    ass, _ = assinatura_sob(L, 326, cor, acento, serif, 46, 11)
    c.append(ass)
    return svg(L, A, ''.join(c), fundo)

# --------------------------------------------------- 11 · fios verticais
def v11(serif, cor=NAVY, acento=OURO, fundo=None):
    nome, ln = glifos(serif, 300, 'SINGULAR PRIME', 80, tracking=0.26)
    sub,  ls = glifos(JOST, 300, 'CONSULTORIA IMOBILIÁRIA', 13, tracking=0.58)
    L = int(max(ln, ls) + 220); A = 240
    x0 = (L - ln) / 2
    c = [por(nome, 128, cor, x0), por(sub, 172, cor, (L - ls) / 2),
         '<path d="M %.1f 70 L %.1f 196" stroke="%s" stroke-width="0.7"/>' % (x0 - 46, x0 - 46, acento),
         '<path d="M %.1f 70 L %.1f 196" stroke="%s" stroke-width="0.7"/>' % (x0 + ln + 46, x0 + ln + 46, acento)]
    return svg(L, A, ''.join(c), fundo)

# --------------------------------------------------- 12 · selo oval
def v12(serif, cor=NAVY, acento=OURO, fundo=None):
    n1_, l1_ = glifos(serif, 300, 'SINGULAR', 48, tracking=0.22)
    rx = int(l1_ / 2 + 44); ry = int(rx * 1.24)
    L, A = rx * 2 + 40, ry * 2 + 40; cx, cy = L / 2, A / 2
    c = ['<ellipse cx="%d" cy="%d" rx="%d" ry="%d" fill="none" stroke="%s" stroke-width="0.8"/>' % (cx, cy, rx, ry, acento),
         '<ellipse cx="%d" cy="%d" rx="%d" ry="%d" fill="none" stroke="%s" stroke-width="0.4"/>' % (cx, cy, rx-12, ry-12, acento)]
    n1, l1 = glifos(serif, 300, 'SINGULAR', 48, tracking=0.22)
    n2, l2 = glifos(serif, 300, 'PRIME', 48, tracking=0.22)
    sub, ls = glifos(JOST, 300, 'CONSULTORIA IMOBILIÁRIA', 10, tracking=0.54)
    c += [por(n1, cy - 10, cor, cx - l1 / 2), por(n2, cy + 44, cor, cx - l2 / 2),
          fio(cx - 22, cy + 12, cx + 22, acento, 0.5),
          por(sub, cy + 86, cor, cx - ls / 2)]
    return svg(L, A, ''.join(c), fundo)

# --------------------------------------------------- 13 · lockup horizontal
def v13(serif, cor=NAVY, acento=OURO, fundo=None):
    sp, lsp = glifos(serif, 300, 'SP', 76)
    nome, ln = glifos(serif, 300, 'SINGULAR PRIME', 52, tracking=0.26)
    sub, ls = glifos(JOST, 300, 'CONSULTORIA IMOBILIÁRIA', 11.5, tracking=0.58)
    L = int(150 + max(ln, ls) + 80); A = 200
    c = [por(sp, 122, cor, 60),
         '<path d="M %.1f 58 L %.1f 142" stroke="%s" stroke-width="0.7"/>' % (60 + lsp + 34, 60 + lsp + 34, acento),
         por(nome, 108, cor, 60 + lsp + 68),
         por(sub, 138, cor, 60 + lsp + 68)]
    return svg(L, A, ''.join(c), fundo)

VARIANTES = [('06_entrelacado', v6), ('07_quadro', v7), ('08_sem_serifa', v8), ('09_prime_deslocado', v9),
             ('10_brasao', v10), ('11_fios_verticais', v11), ('12_selo_oval', v12), ('13_lockup', v13)]

for nome, fn in VARIANTES:
    io.open(os.path.join(SAIDA, '%s_claro.svg' % nome), 'w', encoding='utf-8').write(fn(CORM))
    io.open(os.path.join(SAIDA, '%s_escuro.svg' % nome), 'w', encoding='utf-8').write(fn(PLAY, OFFWHITE, OURO_CLARO, NAVY))
    print('%-20s ok' % nome)
print('\nem', SAIDA)
