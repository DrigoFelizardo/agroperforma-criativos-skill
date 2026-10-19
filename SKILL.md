---
name: agroperforma-criativos
description: Edita criativos verticais de Instagram (AgroPerforma / Fábrica Blindada) com HyperFrames a partir de takes brutos 4K — escolhe o canal de áudio certo, corta pausas, engasgos e recomeços pelo áudio, monta legenda estática + motions no estilo da marca (tarjas verde/azul, elipse, check, seta), aplica LUT e degradê, zoom calmo com rosto centralizado sem barra preta, fade no fim e renderiza 4K 24 fps. Use quando o pedido for editar/cortar criativos AgroPerforma ou Fábrica Blindada, "passar na fila para edição", fazer variações de gancho, ou corrigir um criativo já entregue.
---

# Criativos AgroPerforma · Fábrica Blindada

Pipeline de edição de criativos verticais (Reels/Ads) construída sobre o **HyperFrames**
(`npx hyperframes …`). Cada criativo vira um projeto com uma *receita* em JSON
(`creative.base.json`) que o `template.html` transforma na composição.

> Regras detalhadas do cliente, decisões e histórico de feedback: [`references/regras-do-cliente.md`](references/regras-do-cliente.md).
> Leia antes de editar — elas mandam sobre qualquer padrão daqui.

## Fluxo obrigatório (3 aprovações)

1. **Corte** → prévia 1080p leve (`cut.py --preview`) + nome sugerido (código + apelido, ex. `AP-08 · Tudo Depende de Você`). Usuário aprova.
2. **Rascunho** → quadros‑chave dos motions/legenda (`hyperframes snapshot`), não o vídeo inteiro. Para mudança de dinâmica (zoom), mandar prévia `render -q draft`.
3. **Execução** → recorte em 4K (`cut.py` sem `--preview`) + `render4k.sh` (4K 24 fps) + `barscan.sh` (borda preta).

**Um vídeo por vez, de ponta a ponta.** Whisper large‑v3 + ffmpeg 4K + render em paralelo superaquecem e reiniciam o MacBook.

## Ambiente

- O SSD do cliente é exFAT (sem links → `hyperframes init` falha). Trabalhe num volume APFS em imagem montado em `/Volumes/AGROPERFORMA-HF` (`scripts/montar.sh`). Os scripts assumem esse caminho: `projetos/<código>/`, `projetos/_kit/` (= esta pasta `scripts/` + `assets/`), `_scratch/` (temporários, `faces.swift`, `shift.swift`).
- `source scripts/env.sh` em todo comando: TMPDIR, histórico e caches do HyperFrames ficam no volume, nunca no disco do Mac.
- O volume desmonta quando o app reinicia — remontar antes de cada etapa; jobs longos com `nohup caffeinate -i`.
- Fonte: Helvetica Now Display **Bold** (licenciada — não está no repositório; copie para `projetos/_kit/fonts/`).

## Etapa 1 — corte

| Passo | Ferramenta |
|---|---|
| Canal da fala (mics diferentes em L e R; vale o mais forte, conferir quem fala quando a direção aparece) | `prep_lote.sh` (níveis + transcrição) |
| Frases do bruto, transcritas uma a uma (pausas do Whisper longo mentem) | `phrasemap.py <wav>` |
| Pausas > 0,2 s fora, 0,07 s de respiro | `plan.py <wav> a:b … --gap 0.2 --pad 0.07` |
| Engasgos ("da, do", "tem em, um, uma", "cli… clica"): RMS 20 ms + emendar candidatos e transcrever a emenda; isolar a sílaba confirma | `fine.sh`, `chunk.sh` |
| Corte contínuo alinhado ao quadro (um único `<video>` → o LUT nunca "picota"), canal escolhido nos dois lados, fade 0,5 s + 0,7 s para preto | `cut.py [--preview] [--no-fade] [--multi]` |

Começa no início real da fala; termina ~0,5 s após a última palavra com fade (exceção: se a pessoa desvia o olhar no fim → `--no-fade`).

## Etapa 2 — receita (`creative.base.json`)

```json
{
  "theme": "green",                       // green = AgroPerforma (#62AE46) · blue = Fábrica Blindada (#1f4cd7/#0c1f51)
  "adjust": {"highlights": -0.25, "shadows": -0.15},   // ou "exposure": 0.15
  "trackMode": "shot",                    // centraliza o rosto 1× por trecho de zoom
  "cam": [{"start": 0, "end": 6.78, "s": 1.12, "to": 1.04, "cx": 0.5}],
  "captions": [["texto estático", 1.12, 2.48]],
  "motions": [{"start": 5.45, "end": 6.78, "top": 900,
               "items": [{"text": "Tudo depende de você?", "at": 5.45, "kind": "secondary", "check": true, "ring": 5.8}],
               "arrow": 6.2}]
}
```

- `analyze.sh <projeto>` → rosto por quadro (Apple Vision) + transcrição do corte; `caps.py` gera legendas automáticas (agrupa 2–4 palavras, corrige "Eo/Ea/Eaí", funde órfãs).
- `mkcfg.py <projeto>` → completa zoom/rastreamento e gera `index.html` via `build.py`.
- Legenda **estática** no meio do quadro, some enquanto um motion estiver na tela.
- Tipos: curto (CTA ~10–15 s) só motions · médio legenda + motions em palavras‑chave · `-GRANDE` só legenda + motion de CTA final.
- **Zoom calmo:** ~5 trechos em 40 s, ≥ 6 s entre trocas, só em troca de raciocínio; alterna aproximar/afastar. Rosto centralizado por trecho, enquadramento limitado quadro a quadro à margem do zoom (nunca mostra borda).

## Etapa 3 — execução

```bash
python3 scripts/cut.py "<bruto>.MP4" media/cut.mp4 L <a:b> …     # 4K
python3 scripts/mkcfg.py projetos/<código>
HF_DEST="<pasta EDICAO>" scripts/render4k.sh <código> <Nome>_v1_4K
scripts/barscan.sh "<pasta EDICAO>/<Nome>_v1_4K.mp4"              # 0 quadros com borda preta
```

Registre tudo no `PROJETO.md` do projeto (bruto, canal, texto, o que saiu, versões) e no `projetos/CATALOGO.md`. Versões numeradas, nunca sobrescrever.

## Exemplos

`examples/` traz receitas reais (`creative.*.json`), `PROJETO.*.md`, o gerador de variações de gancho (`ap08_variants.py` — mesmo corpo, três frases de abertura) e filas de render (`fila_*.sh`).
