# -*- coding: utf-8 -*-
"""Marca da Singular Prime, versao editorial.
Composicao: SINGULAR protagonista / PRIME em ouro / fio / ASSESSORIA IMOBILIARIA.
Tudo em curvas, fontes OFL."""
import os, io
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen

BASE   = r'C:\Users\eleut\claudinho\singular-id-visual'
FONTES = os.path.join(BASE, 'fontes')
SAIDA  = os.path.join(BASE, 'marca_v2')
os.makedirs(SAIDA, exist_ok=True)

# paleta da propria Singular, refinada
AREIA    = '#F4EFE6'
FENDI    = '#D9C8B0'
VERDE    = '#5E6F68'
AZUL     = '#88A1A0'
TERRACOTA= '#C79C7C'
GRAFITE  = '#232A27'
OURO     = '#B08D4F'
OURO_CL  = '#CBA96A'

CORM = 'CormorantGaramond[wght].ttf'
JOST = 'Jost[wght].ttf'

_c = {}
def fonte(arq, peso=None):
    # o instancer do fontTools esta bloqueado por politica do Windows;
    # usamos a instancia padrao da fonte variavel (Cormorant ja nasce em 300)
    if arq not in _c:
        _c[arq] = TTFont(os.path.join(FONTES, arq))
    return _c[arq]

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

# ------------------------------------------------ 01 principal
def principal(cor=GRAFITE, ouro=OURO, fundo=None):
    n1, l1 = glifos(CORM, 300, 'SINGULAR', 150, tracking=0.19)
    n2, l2 = glifos(JOST, 300, 'PRIME',     46, tracking=0.72)
    n3, l3 = glifos(JOST, 300, 'ASSESSORIA IMOBILIÁRIA', 19, tracking=0.56)
    L = int(l1 + 200); A = 400
    c = [por(n1, 168, cor, (L - l1) / 2),
         por(n2, 238, ouro, (L - l2) / 2),
         '<path d="M %.1f 282 L %.1f 282" stroke="%s" stroke-width="1.4"/>' % (L/2 - 44, L/2 + 44, ouro),
         por(n3, 334, cor, (L - l3) / 2)]
    return svg(L, A, ''.join(c), fundo)

# ------------------------------------------------ 02 essencial
def essencial(cor=GRAFITE, ouro=OURO, fundo=None):
    n1, l1 = glifos(CORM, 300, 'SINGULAR', 150, tracking=0.19)
    n2, l2 = glifos(JOST, 300, 'PRIME',     46, tracking=0.72)
    L = int(l1 + 200); A = 290
    c = [por(n1, 168, cor, (L - l1) / 2), por(n2, 238, ouro, (L - l2) / 2)]
    return svg(L, A, ''.join(c), fundo)

# ------------------------------------------------ 03 monograma
def monograma(cor=OURO, fundo=None, traco=3.2):
    """S e P em peso leve, sobrepostos, com a haste do P alongada.
    Desenho tipografico, nao ilustrado."""
    s_, ls_ = glifos(CORM, 300, 'S', 210)
    p_, lp_ = glifos(CORM, 300, 'P', 210)
    L, A = 300, 320
    x0 = (L - (ls_ + lp_ * 0.46)) / 2
    c = [por(s_, 232, cor, x0),
         por(p_, 232, cor, x0 + ls_ * 0.54),
         # haste fina descendo, puxando o olho e dando a assinatura manual
         '<path d="M %.1f 232 L %.1f 292" stroke="%s" stroke-width="%.1f" stroke-linecap="round"/>'
         % (x0 + ls_ * 0.54 + 6, x0 + ls_ * 0.54 + 6, cor, traco * 0.5)]
    return svg(L, A, ''.join(c), fundo)

ARQUIVOS = {
    '01_principal_grafite.svg':  principal(),
    '01_principal_clara.svg':    principal(AREIA, OURO_CL),
    '02_essencial_grafite.svg':  essencial(),
    '02_essencial_clara.svg':    essencial(AREIA, OURO_CL),
    '03_monograma_ouro.svg':     monograma(),
    '03_monograma_claro.svg':    monograma(OURO_CL),
    '03_monograma_grafite.svg':  monograma(GRAFITE),
}
for nome, s in ARQUIVOS.items():
    io.open(os.path.join(SAIDA, nome), 'w', encoding='utf-8').write(s)
    print('%-28s %5d bytes' % (nome, len(s)))
print('\nem', SAIDA)
