#!/usr/bin/env python
"""
Localiza automaticamente as regioes de figura numa pagina do PDF.

Agrupa os desenhos vetoriais (get_drawings) e as imagens embutidas em blocos
contiguos e imprime as caixas delimitadoras candidatas, junto com a legenda
mais proxima. Serve para descobrir as coordenadas de recorte.

  python figuras.py listar 19            -> candidatos na pagina 19 do PDF
  python figuras.py salvar 19 saida.png  -> salva o maior candidato
"""
import sys
import os

import fitz

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from extrair import abrir, OFFSET


def caixas(page, margem=6.0):
    """Agrupa desenhos e imagens em caixas contiguas."""
    itens = [d["rect"] for d in page.get_drawings()]
    itens += [fitz.Rect(b[:4]) for b in page.get_image_info()]
    if not itens:
        return []
    # aglomera caixas que se tocam (com folga de `margem`)
    grupos = []
    for r in itens:
        if r.is_empty or r.width < 2 or r.height < 2:
            continue
        alvo = fitz.Rect(r) + (-margem, -margem, margem, margem)
        juntar = [g for g in grupos if g.intersects(alvo)]
        for g in juntar:
            grupos.remove(g)
            r = fitz.Rect(r) | g
        grupos.append(fitz.Rect(r))
    # repete ate estabilizar
    mudou = True
    while mudou:
        mudou = False
        for i in range(len(grupos)):
            for j in range(i + 1, len(grupos)):
                a = grupos[i] + (-margem, -margem, margem, margem)
                if a.intersects(grupos[j]):
                    grupos[i] |= grupos[j]
                    del grupos[j]
                    mudou = True
                    break
            if mudou:
                break
    return sorted(grupos, key=lambda r: -(r.width * r.height))


def expandir(page, rect, folga=14.0):
    """Cresce a caixa para abarcar os rotulos de texto da figura.

    Inclui blocos de texto contiguos (eixos, legendas internas, valores), mas
    nunca a legenda da figura -- "F I G U R E"/"T A B L E" delimitam o fim.
    """
    r = fitz.Rect(rect)
    mudou = True
    while mudou:
        mudou = False
        for b in page.get_text("blocks"):
            txt = b[4].strip()
            if not txt or "F I G U R E" in txt or "T A B L E" in txt:
                continue
            tb = fitz.Rect(b[:4])
            # ignora o corpo do texto: blocos largos que atravessam a pagina
            if tb.width > page.rect.width * 0.7:
                continue
            if tb in r:
                continue
            if (r + (-folga, -folga, folga, folga)).intersects(tb):
                r |= tb
                mudou = True
    return r


def legenda_proxima(page, rect):
    """Devolve o texto de legenda (F I G U R E / T A B L E) mais proximo da caixa."""
    melhor, dist = "", 1e9
    for b in page.get_text("blocks"):
        txt = b[4].strip().replace("\n", " ")
        if "F I G U R E" in txt or "T A B L E" in txt:
            r = fitz.Rect(b[:4])
            d = abs(r.y0 - rect.y1) if r.y0 > rect.y0 else abs(rect.y0 - r.y1)
            if d < dist:
                melhor, dist = txt[:70], d
    return melhor


def cmd_listar(args):
    n = int(args[0])
    doc = abrir()
    page = doc[n - 1]
    print(f"PDF p.{n} (livro p.{n - OFFSET})  mediabox={page.rect}")
    for i, r in enumerate(caixas(page)):
        area = r.width * r.height
        if area < 2000:
            continue
        print(f"  [{i}] x0={r.x0:.0f} y0={r.y0:.0f} x1={r.x1:.0f} y1={r.y1:.0f}"
              f"  ({r.width:.0f}x{r.height:.0f})  <- {legenda_proxima(page, r)}")


def cmd_salvar(args):
    n, saida = int(args[0]), args[1]
    idx = int(args[2]) if len(args) > 2 else 0
    doc = abrir()
    page = doc[n - 1]
    cs = [r for r in caixas(page) if r.width * r.height >= 2000]
    if not cs:
        raise SystemExit("nenhuma figura encontrada")
    r = cs[idx] + (-8, -8, 8, 8)
    pix = page.get_pixmap(dpi=300, clip=r)
    pix.save(saida)
    print(f"salvo: {saida}  ({pix.width}x{pix.height})  de {r}")


if __name__ == "__main__":
    cmds = {"listar": cmd_listar, "salvar": cmd_salvar}
    if len(sys.argv) < 2 or sys.argv[1] not in cmds:
        print(__doc__)
        sys.exit(1)
    cmds[sys.argv[1]](sys.argv[2:])
