#!/usr/bin/env python3
"""
prepara_malhas.py — copia as malhas para o pacote, limpas para publicacao.

O QUE MUDA em cada meta.json:
  uuid        "flatten.tifxyz" (igual em todas) -> "<scroll>_z<janela>_w<wrap>"
  name        idem
  fit_config  caminhos absolutos da maquina local removidos; os PARAMETROS
              ficam, porque sao o que torna a malha reproduzivel
  model_source, external_surfaces  removidos (caminhos locais, sem uso externo)

O model.pt (560 KB, 80%% do peso) NAO e copiado: e artefato interno do flatten
e nao e preciso para usar a malha. So x/y/z.tif e meta.json vao.

Destino: meshes/<scroll>/z<janela>_w<wrap>/

Le data/index.csv para saber quais malhas entram (as 340 por janela; as 45 de
fase anterior, sem janela, ficam fora).
"""
import csv
import json
import os
import shutil

PAC = os.path.expanduser("~/challenges/vesuvius/pacote_malhas")
IDX = os.path.join(PAC, "data", "index.csv")
DST = os.path.join(PAC, "meshes")

if not os.path.exists(IDX):
    raise SystemExit(f"indice nao encontrado: {IDX}")

os.makedirs(DST, exist_ok=True)
n_ok = n_falta = 0
bytes_tot = 0
novas_linhas = []

with open(IDX) as fh:
    linhas = list(csv.DictReader(fh))

for r in linhas:
    src = os.path.expanduser(r["path"])
    if not os.path.isdir(src):
        print(f"  ausente: {src}")
        n_falta += 1
        novas_linhas.append(r)
        continue

    nome = f"z{r['window_z']}_{r['wrap']}"
    d = os.path.join(DST, r["scroll"], nome)
    os.makedirs(d, exist_ok=True)

    for f in ("x.tif", "y.tif", "z.tif"):
        s = os.path.join(src, f)
        if os.path.exists(s):
            shutil.copy2(s, os.path.join(d, f))
            bytes_tot += os.path.getsize(s)

    m = {}
    mp = os.path.join(src, "meta.json")
    if os.path.exists(mp):
        try:
            m = json.load(open(mp))
        except Exception:
            m = {}

    uuid = f"{r['scroll']}_{nome}"
    limpo = {
        "uuid": uuid,
        "name": uuid,
        "type": m.get("type", "seg"),
        "format": m.get("format", "tifxyz"),
        "scale": m.get("scale", [0.05, 0.05]),
    }
    if "bbox" in m:
        limpo["bbox"] = m["bbox"]
    if "area_vx2" in m:
        limpo["area_vx2"] = m["area_vx2"]

    # fit_config: mantem os parametros, remove tudo que e caminho local
    fc = m.get("fit_config")
    if isinstance(fc, dict):
        fc = dict(fc)
        fc.pop("external_surfaces", None)
        args = fc.get("args")
        if isinstance(args, dict):
            args = {k: v for k, v in args.items()
                    if not (isinstance(v, str) and v.startswith("/"))}
            args.pop("out-dir", None)
            fc["args"] = args
        limpo["fit_config"] = fc

    json.dump(limpo, open(os.path.join(d, "meta.json"), "w"), indent=2)

    r = dict(r)
    r["path"] = f"meshes/{r['scroll']}/{nome}"
    novas_linhas.append(r)
    n_ok += 1
    if n_ok % 50 == 0:
        print(f"  {n_ok} copiadas")

# reescreve o indice com os caminhos do pacote, nao os da maquina
with open(IDX, "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(linhas[0].keys()))
    w.writeheader()
    w.writerows(novas_linhas)

print(f"\ncopiadas: {n_ok}   ausentes: {n_falta}")
print(f"tamanho dos tifs: {bytes_tot/1e6:.1f} MB")
print(f"destino: {DST}")
print("\nverificacao — uuid de uma amostra:")
for s in sorted(os.listdir(DST))[:2]:
    for w_ in sorted(os.listdir(os.path.join(DST, s)))[:1]:
        mp = os.path.join(DST, s, w_, "meta.json")
        m = json.load(open(mp))
        tem_caminho = "/home/" in json.dumps(m)
        print(f"  {s}/{w_}: uuid={m['uuid']}  caminho local? {'SIM' if tem_caminho else 'nao'}")
