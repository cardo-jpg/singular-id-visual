# -*- coding: utf-8 -*-
"""Gera a previa de identidade da Singular Prime em vetor de verdade (curvas).
Fontes de licenca aberta (OFL): Cormorant Garamond e Jost."""
import os, io
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools.pens.svgPathPen import SVGPathPen

BASE = r'C:\Users\eleut\claudinho\singular-id-visual'
FONTES = os.path.join(BASE, 'fontes')
SAIDA = os.path.join(BASE, 'marca')
os.makedirs(SAIDA, exist_ok=True)

OURO      = '#B08D4F'
OURO_CLARO= '#C9A662'
NAVY      = '#0E1E33'
AREIA     = '#E6DFD2'
OFFWHITE  = '#F8F5EF'

_cache = {}
def fonte(arquivo, peso):
    ch = (arquivo, peso)
    if ch not in _cache:
        f = TTFont(os.path.join(FONTES, arquivo))
        _cache[ch] = instancer.instantiateVariableFont(f, {'wght': peso})
    return _cache[ch]

def curvas(arquivo, peso, texto, tamanho, tracking=0.0):
    """Texto convertido em curvas. Devolve (paths, largura)."""
    f = fonte(arquivo, peso)
    upm = f['head'].unitsPerEm
    cmap, gs, hmtx = f.getBestCmap(), f.getGlyphSet(), f['hmtx']
    esc = tamanho / upm
    paths, x = [], 0.0
    for ch in texto:
        nome = cmap.get(ord(ch))
        if nome is None:
            x += tamanho * 0.32
            continue
        pen = SVGPathPen(gs)
        gs[nome].draw(pen)
        d = pen.getCommands()
        if d:
            paths.append((d, x, esc))
        x += hmtx[nome][0] * esc + tracking * tamanho
    if texto and paths:
        x -= tracking * tamanho
    return paths, x

def render(paths, base_y, cor):
    return ''.join(
        '<path d="%s" transform="translate(%.2f %.2f) scale(%.5f %.5f)" fill="%s"/>'
        % (d, x, base_y, e, -e, cor) for d, x, e in paths)

CORM = 'CormorantGaramond[wght].ttf'
JOST = 'Jost[wght].ttf'

# ---------------------------------------------------------------- simbolo A
def simbolo_emblema(cor=OURO, anel=True, tam=200):
    """Montanha dos Dois Irmaos + ondas do calcadao, dentro de anel."""
    p = []
    if anel:
        p.append('<circle cx="100" cy="100" r="90" fill="none" stroke="%s" stroke-width="1.6"/>' % cor)
    # montanhas: dois picos assimetricos
    p.append('<path d="M 42 116 L 74 62 L 96 98 L 120 52 L 158 116 Z" fill="%s"/>' % cor)
    # ondas do calcadao, tres linhas
    for i, y in enumerate((134, 147, 160)):
        largura = (84, 68, 50)[i]
        x0 = 100 - largura
        d = 'M %d %d ' % (x0, y)
        passo = largura / 2.0
        for k in range(2):
            d += 'q %.1f -7 %.1f 0 q %.1f 7 %.1f 0 ' % (passo/4, passo/2, passo/4, passo/2)
        p.append('<path d="%s" fill="none" stroke="%s" stroke-width="3" stroke-linecap="round"/>' % (d, cor))
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d">%s</svg>'
            % (tam, tam, tam, tam, ''.join(p)))

# ---------------------------------------------------------------- simbolo B
def simbolo_monograma(cor=OURO, tam=200):
    """S e P entrelacados sobre a linha de onda."""
    s_paths, s_larg = curvas(CORM, 400, 'S', 132)
    p_paths, p_larg = curvas(CORM, 400, 'P', 132)
    total = s_larg + p_larg * 0.72
    x0 = (200 - total) / 2
    corpo = [render(s_paths, 138, cor)]
    corpo.append('<g transform="translate(%.2f 0)">%s</g>' % (s_larg * 0.78, render(p_paths, 138, cor)))
    onda = 'M 46 160 q 13 -8 27 0 q 14 8 27 0 q 13 -8 27 0 q 14 8 27 0'
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d">'
            '<g transform="translate(%.2f 0)">%s</g>'
            '<path d="%s" fill="none" stroke="%s" stroke-width="2.6" stroke-linecap="round"/></svg>'
            % (tam, tam, tam, tam, x0, ''.join(corpo), onda, cor))

# ---------------------------------------------------------------- lockups
def assinatura(cor_texto, cor_simbolo, vertical=False, com_simbolo=True, simbolo='emblema'):
    nome_p, nome_l = curvas(CORM, 500, 'SINGULAR PRIME', 68, tracking=0.13)
    desc_p, desc_l = curvas(JOST, 400, 'CONSULTORIA IMOBILIÁRIA', 15.5, tracking=0.34)
    sim = simbolo_emblema(cor_simbolo) if simbolo == 'emblema' else simbolo_monograma(cor_simbolo)
    sim_interno = sim.split('>', 1)[1].rsplit('</svg>', 1)[0]

    if vertical:
        larg = max(nome_l, desc_l, 200)
        alt = 300
        corpo = ['<g transform="translate(%.2f 0) scale(0.62)">%s</g>' % ((larg - 124) / 2, sim_interno)]
        corpo.append('<g transform="translate(%.2f 0)">%s</g>' % ((larg - nome_l) / 2, render(nome_p, 208, cor_texto)))
        corpo.append('<g transform="translate(%.2f 0)">%s</g>' % ((larg - desc_l) / 2, render(desc_p, 240, cor_texto)))
    else:
        sx = 104.0
        larg = (sx + 34 if com_simbolo else 0) + max(nome_l, desc_l)
        alt = 120
        corpo = []
        if com_simbolo:
            corpo.append('<g transform="translate(0 4) scale(0.56)">%s</g>' % sim_interno)
        base = (sx + 34) if com_simbolo else 0
        corpo.append('<g transform="translate(%.2f 0)">%s</g>' % (base, render(nome_p, 62, cor_texto)))
        corpo.append('<g transform="translate(%.2f 0)">%s</g>' % (base, render(desc_p, 92, cor_texto)))
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %.0f %.0f" width="%.0f" height="%.0f">%s</svg>'
            % (larg, alt, larg, alt, ''.join(corpo)))

arquivos = {
    'simbolo_emblema_ouro.svg':      simbolo_emblema(OURO),
    'simbolo_emblema_navy.svg':      simbolo_emblema(NAVY),
    'simbolo_monograma_ouro.svg':    simbolo_monograma(OURO),
    'assinatura_horizontal.svg':     assinatura(NAVY, OURO),
    'assinatura_horizontal_clara.svg': assinatura(OFFWHITE, OURO_CLARO),
    'assinatura_vertical.svg':       assinatura(NAVY, OURO, vertical=True),
    'assinatura_vertical_clara.svg': assinatura(OFFWHITE, OURO_CLARO, vertical=True),
    'assinatura_mono_horizontal.svg': assinatura(NAVY, OURO, simbolo='monograma'),
    'assinatura_so_texto.svg':       assinatura(NAVY, OURO, com_simbolo=False),
}
for nome, svg in arquivos.items():
    io.open(os.path.join(SAIDA, nome), 'w', encoding='utf-8').write(svg)
    print('%-34s %5d bytes | tem <text>? %s' % (nome, len(svg), 'SIM' if '<text' in svg else 'nao'))
print('\nem', SAIDA)
