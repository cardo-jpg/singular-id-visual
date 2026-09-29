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


# ---------------------------------------------------------------- simbolo C
def simbolo_janela(cor=OURO, larg=170, alt=240, traco=2.6):
    """A janela: arco que emoldura os Dois Irmaos e a linha do mar.
    Monolinha, sem preenchimento. O arco le como vao de janela, que e o que
    a Singular vende: a vista e o endereco."""
    p = []
    # arco: base reta, topo em meia-volta
    p.append('<path d="M 22 224 L 22 96 A 63 63 0 0 1 148 96 L 148 224 Z" '
             'fill="none" stroke="%s" stroke-width="%.1f" stroke-linejoin="round"/>' % (cor, traco))
    # Dois Irmaos: dois picos assimetricos, em linha
    p.append('<path d="M 40 178 L 66 134 L 84 156 L 106 124 L 132 178" '
             'fill="none" stroke="%s" stroke-width="%.1f" stroke-linecap="round" stroke-linejoin="round"/>'
             % (cor, traco))
    # o mar: tres linhas retas, decrescentes
    for y, x0, x1 in ((192, 42, 130), (203, 56, 116), (214, 70, 102)):
        p.append('<path d="M %d %d L %d %d" stroke="%s" stroke-width="%.1f" stroke-linecap="round"/>'
                 % (x0, y, x1, y, cor, traco))
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d">%s</svg>'
            % (larg, alt, larg, alt, ''.join(p)))


# ---------------------------------------------------------------- simbolo D
def _pao_de_acucar(traco, cor, y_base=186):
    """Morro da Urca (menor, esquerda) + Pao de Acucar (maior, direita).
    Domos arredondados, nao triangulos: e o perfil que o carioca reconhece."""
    # ovoides: arco de elipse mais alta que larga. E a forma que le como
    # Pao de Acucar mesmo reduzida (o proprio logo do supermercado usa isso).
    urca = 'M 32 %d A 30 36 0 0 1 92 %d' % (y_base, y_base)
    pao  = 'M 80 %d A 40 54 0 0 1 160 %d' % (y_base, y_base)
    molde = ('<path d="%s" fill="none" stroke="%s" stroke-width="%.1f" '
             'stroke-linecap="round" stroke-linejoin="round"/>')
    chao = ('<path d="M 22 %d L 170 %d" fill="none" stroke="%s" stroke-width="%.1f" '
            'stroke-linecap="round"/>' % (y_base, y_base, cor, traco))
    return (molde % (urca, cor, traco)) + (molde % (pao, cor, traco)) + chao

def _mar(traco, cor, ys=(205, 219), meia=64, ondas=2.0):
    """O calcadao: bandas sinuosas de amplitude larga, no ritmo do desenho
    de Burle Marx, em vez de ondinhas genericas."""
    out = []
    for k, y in enumerate(ys):
        m = meia - k * 18
        x0, x1 = 96 - m, 96 + m
        largura = (x1 - x0) / ondas
        d = 'M %.1f %.1f ' % (x0, y)
        for i in range(int(ondas)):
            d += 'c %.1f -9, %.1f -9, %.1f 0 ' % (largura * 0.18, largura * 0.32, largura * 0.5)
            d += 'c %.1f 9, %.1f 9, %.1f 0 ' % (largura * 0.18, largura * 0.32, largura * 0.5)
        out.append('<path d="%s" fill="none" stroke="%s" stroke-width="%.1f" stroke-linecap="round"/>'
                   % (d.strip(), cor, traco))
    return ''.join(out)

def padrao_calcadao(cor=OURO, fundo=AREIA, larg=520, alt=260, linhas=5, traco=9):
    """Textura da marca: o calcadao em bandas largas, para fundo de peca."""
    p = ['<rect width="%d" height="%d" fill="%s"/>' % (larg, alt, fundo)]
    for i in range(linhas):
        y = 18 + i * (alt - 36) / (linhas - 1)
        d = 'M -40 %.1f ' % y
        for _ in range(5):
            d += 'c 28 -30, 84 -30, 112 0 c 28 30, 84 30, 112 0 '
        p.append('<path d="%s" fill="none" stroke="%s" stroke-width="%d" stroke-linecap="round" opacity="0.5"/>'
                 % (d.strip(), cor, traco))
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d">%s</svg>'
            % (larg, alt, larg, alt, ''.join(p)))

def simbolo_pao_arco(cor=OURO, larg=196, alt=258, traco=2.6):
    """Pao de Acucar e mar, emoldurados pelo arco da janela."""
    p = ['<path d="M 12 232 L 12 100 A 78 78 0 0 1 168 100 L 168 232 Z" '
         'fill="none" stroke="%s" stroke-width="%.1f" stroke-linejoin="round"/>' % (cor, traco)]
    p.append(_pao_de_acucar(traco, cor))
    p.append(_mar(traco, cor))
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d">%s</svg>'
            % (larg, alt, larg, alt, ''.join(p)))

def simbolo_pao_circulo(cor=OURO, tam=200, traco=2.6):
    """Mesmo desenho, dentro de circulo."""
    p = ['<circle cx="96" cy="160" r="100" fill="none" stroke="%s" stroke-width="%.1f"/>' % (cor, traco)]
    p.append(_pao_de_acucar(traco, cor))
    p.append(_mar(traco, cor))
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="-8 56 208 208" width="%d" height="%d">%s</svg>'
            % (tam, tam, ''.join(p)))

def simbolo_pao_livre(cor=OURO, larg=180, alt=130, traco=2.8):
    """Sem moldura: so o perfil e o mar."""
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="22 124 152 100" width="%d" height="%d">%s%s</svg>'
            % (larg, alt, _pao_de_acucar(traco, cor), _mar(traco, cor)))

# ---------------------------------------------------------------- lockups
def assinatura(cor_texto, cor_simbolo, vertical=False, com_simbolo=True, simbolo='emblema'):
    nome_p, nome_l = curvas(CORM, 500, 'SINGULAR PRIME', 68, tracking=0.13)
    desc_p, desc_l = curvas(JOST, 400, 'CONSULTORIA IMOBILIÁRIA', 15.5, tracking=0.34)
    if simbolo == 'pao':       sim = simbolo_pao_arco(cor_simbolo)
    elif simbolo == 'pao_circulo': sim = simbolo_pao_circulo(cor_simbolo)
    elif simbolo == 'emblema': sim = simbolo_emblema(cor_simbolo)
    elif simbolo == 'janela':  sim = simbolo_janela(cor_simbolo)
    else:                      sim = simbolo_monograma(cor_simbolo)
    sim_interno = sim.split('>', 1)[1].rsplit('</svg>', 1)[0]

    if vertical:
        larg = max(nome_l, desc_l, 200)
        alt = 340 if simbolo in ('janela','pao') else 300
        esc_v = 0.60 if simbolo in ('janela','pao') else 0.62
        marca_l = (180 if simbolo=='pao' else 170) * esc_v if simbolo in ('janela','pao') else 124
        corpo = ['<g transform="translate(%.2f 0) scale(%.2f)">%s</g>' % ((larg - marca_l) / 2, esc_v, sim_interno)]
        base_nome = 248 if simbolo in ('janela','pao') else 208
        corpo.append('<g transform="translate(%.2f 0)">%s</g>' % ((larg - nome_l) / 2, render(nome_p, base_nome, cor_texto)))
        corpo.append('<g transform="translate(%.2f 0)">%s</g>' % ((larg - desc_l) / 2, render(desc_p, base_nome + 32, cor_texto)))
    else:
        sx = 104.0
        larg = (sx + 34 if com_simbolo else 0) + max(nome_l, desc_l)
        alt = 120
        corpo = []
        if com_simbolo:
            esc_s = 0.44 if simbolo in ('janela','pao') else 0.56
            dy = 2 if simbolo == 'janela' else 4
            corpo.append('<g transform="translate(0 %d) scale(%.2f)">%s</g>' % (dy, esc_s, sim_interno))
        base = (sx + 34) if com_simbolo else 0
        corpo.append('<g transform="translate(%.2f 0)">%s</g>' % (base, render(nome_p, 62, cor_texto)))
        corpo.append('<g transform="translate(%.2f 0)">%s</g>' % (base, render(desc_p, 92, cor_texto)))
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %.0f %.0f" width="%.0f" height="%.0f">%s</svg>'
            % (larg, alt, larg, alt, ''.join(corpo)))

arquivos = {
    'padrao_calcadao.svg':      padrao_calcadao(),
    'padrao_calcadao_navy.svg': padrao_calcadao(OURO, NAVY),
    'pao_arco_ouro.svg':        simbolo_pao_arco(OURO),
    'pao_circulo_ouro.svg':     simbolo_pao_circulo(OURO),
    'pao_livre_ouro.svg':       simbolo_pao_livre(OURO),
    'pao_horizontal.svg':       assinatura(NAVY, OURO, simbolo='pao'),
    'pao_horizontal_clara.svg': assinatura(OFFWHITE, OURO_CLARO, simbolo='pao'),
    'pao_vertical.svg':         assinatura(NAVY, OURO, vertical=True, simbolo='pao'),
    'pao_vertical_clara.svg':   assinatura(OFFWHITE, OURO_CLARO, vertical=True, simbolo='pao'),
    'simbolo_janela_ouro.svg':       simbolo_janela(OURO),
    'simbolo_janela_navy.svg':       simbolo_janela(NAVY),
    'janela_horizontal.svg':         assinatura(NAVY, OURO, simbolo='janela'),
    'janela_horizontal_clara.svg':   assinatura(OFFWHITE, OURO_CLARO, simbolo='janela'),
    'janela_vertical.svg':           assinatura(NAVY, OURO, vertical=True, simbolo='janela'),
    'janela_vertical_clara.svg':     assinatura(OFFWHITE, OURO_CLARO, vertical=True, simbolo='janela'),
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
