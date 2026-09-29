# -*- coding: utf-8 -*-
"""Teste de capacidade: gerar logo em VETOR de verdade (curvas, nao texto),
para saber se da para entregar o que a apresentacao promete."""
import os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen

SAIDA = r'C:\Users\eleut\claudinho\singular-id-visual\teste'
os.makedirs(SAIDA, exist_ok=True)

def texto_em_curvas(fonte, texto, tamanho=100, tracking=0.0):
    """Devolve (lista de paths, largura total, metricas) com o texto ja convertido em curvas."""
    f = TTFont(fonte)
    upm = f['head'].unitsPerEm
    cmap = f.getBestCmap()
    gs = f.getGlyphSet()
    hmtx = f['hmtx']
    esc = tamanho / upm
    paths, x = [], 0.0
    for ch in texto:
        nome = cmap.get(ord(ch))
        if nome is None:
            x += tamanho * 0.3
            continue
        pen = SVGPathPen(gs)
        gs[nome].draw(pen)
        d = pen.getCommands()
        if d:
            paths.append((d, x, esc))
        av = hmtx[nome][0] * esc
        x += av + tracking * tamanho
    return paths, x, esc

def svg_de(paths, larg, alt, cor='#1d2a24', desloc_y=0):
    corpo = []
    for d, x, esc in paths:
        corpo.append(
            '<path d="%s" transform="translate(%.2f %.2f) scale(%.5f %.5f)" fill="%s"/>'
            % (d, x, alt - desloc_y, esc, -esc, cor))
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %.0f %.0f" width="%.0f" height="%.0f">%s</svg>'
            % (larg, alt, larg, alt, ''.join(corpo)))

GEO = r'C:\Windows\Fonts\georgia.ttf'

# 1) marca principal em curvas, com tracking largo (cara de alto padrao)
paths, larg, esc = texto_em_curvas(GEO, 'SINGULAR', tamanho=100, tracking=0.14)
svg = svg_de(paths, larg, 140, desloc_y=30)
open(os.path.join(SAIDA, 'marca_curvas.svg'), 'w', encoding='utf-8').write(svg)
print('marca_curvas.svg     largura %.0f  | paths: %d  | tem <text>? %s'
      % (larg, len(paths), 'sim' if '<text' in svg else 'nao'))

# 2) monograma S dentro de circulo
p2, l2, _ = texto_em_curvas(GEO, 'S', tamanho=120)
mono = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">'
        '<circle cx="100" cy="100" r="96" fill="none" stroke="#1d2a24" stroke-width="3"/>'
        + ''.join('<path d="%s" transform="translate(%.2f %.2f) scale(%.5f %.5f)" fill="#1d2a24"/>'
                  % (d, 100 - l2/2 + x, 142, e, -e) for d, x, e in p2)
        + '</svg>')
open(os.path.join(SAIDA, 'monograma.svg'), 'w', encoding='utf-8').write(mono)
print('monograma.svg        ok')
print('\nArquivos em', SAIDA)
