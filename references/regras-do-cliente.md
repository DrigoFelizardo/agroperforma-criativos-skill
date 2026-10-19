# Regras do cliente e decisões (histórico)

Criativos AgroPerforma (pasta do SSD `.../13 de OUT/Manhã/CRIATIVOS/SELECIONADOS`, takes RFZxxxx.MP4 4K HEVC verticais) são editados com HyperFrames. Teste aprovado para execução começou em 2026-10-14 com RFZ2548.

Kit em `/Users/rodrigofelizardo/Documents/SKILLS DE EDIÇÃO/CRIATIVOS - AGROPERFORMA`: Helvetica Now Display (legenda em Bold, letter-spacing ≈ -0.035em), `Fundo Degradê.png` (2160x3840, overlay sobre o vídeo escurecendo a base), `Color AgroPerforma 1.cube` (LUT), prints IDEIA-MOTION1-3 (tarjas azul #1f4cd7 + marinho #0c1f51, texto branco caixa alta, elipse azul contornando, seta azul).

Regras do usuário: cortar só o essencial; legenda ESTÁTICA (sem animação de entrada/pop), no meio do vídeo salvo se cobrir o rosto; em criativo muito curto (~10s) o usuário prefere sem legenda e com os motions no meio do vídeo (RFZ2548 ficou assim); em tarja de status usar ícone de check (círculo azul + check branco) alinhado ao texto, não bolinha; áudio vem com mics diferentes em L e R — escolher o canal da fala e duplicar nos dois lados (no RFZ2548 foi o R).

Workflow obrigatório (pedido 2026-10-14, para otimizar e não travar o computador):
1. Fazer só os cortes (cut.py) e enviar ao usuário para aprovação (proxy leve, não render 4K).
2. Após aprovar os cortes: planejar motions e enviar um rascunho com quadros-chave demonstrativos (snapshots), não todos os frames.
3. Só depois da aprovação do rascunho: executar e renderizar em 4K.
**MacBook superaquece e REINICIA (2026-10-16)** com whisper large-v3 + ffmpeg 4K + render em paralelo — era isso que derrubava as sessões e desmontava o volume. Regra: UM VÍDEO POR VEZ, de ponta a ponta (nada de fila de lote nem processos em paralelo; próximo só depois do anterior). Desempenho máximo liberado de novo pelo usuário (sem taskpolicy/limite de threads). Rodar um processo pesado por vez (o Mac fica travando com render 4K + ffmpeg + whisper juntos; disco interno com ~7 GB livres).

Tela dividida (aprovado 2026-10-16): padrão = fala EM CIMA, insert EMBAIXO (inverte só se o usuário pedir); 50/50 (60/40 quando insert é apoio); legenda na linha divisória; entrada/saída por deslize. Inserts = b-roll do usuário, foto ou motion meu. Fluxo: após aprovar o corte, enviar MAPA DE INSERTS numerado (tempo, frase, sugestão); usuário põe arquivos em `INSERTS/<código>/01.mp4, 02.jpg…`; número vazio = eu faço motion.

Nomes e registro (proposto 2026-10-16): cada vídeo ganha código + apelido (AP-xx AgroPerforma, FB-xx Fábrica Blindada), sugerido junto com o corte (etapa 1). Cada projeto tem `PROJETO.md` (bruto, canal, texto, cortes, motions/inserts, versões, notas) e há um `projetos/CATALOGO.md` geral. Versões numeradas (creative.vN.json, _vN_4K.mp4), nunca sobrescrever. Prévia de corte para aprovação = 1080p leve; 4K só na execução.

Padrão por TAG no nome do arquivo bruto (definido 2026-10-14):
- `-AgroPerforma` → tarjas/motions com fundo VERDE; `-FábricaBlindada` → fundo AZUL (#1f4cd7/#0c1f51, como RFZ2548).
- Duração: curto (basicamente CTA, ~10–15s) = só motions, sem legenda. Médio = legenda estática + motions em palavras-chave/partes importantes. `-GRANDE` ("aulinha") = só legenda o vídeo todo, motions apenas no CTA final.
- Enquanto um motion está na tela, esconder a legenda.
- Verde AgroPerforma = #62AE46 (passado pelo usuário); tarja secundária num verde escuro derivado.
- Arquivos `-PARTE01`/`-PARTE02` do mesmo take = juntar num único criativo, na ordem.

Cortes: NÃO usar vários <video> do mesmo arquivo com LUT — na troca de elemento sai 1 quadro sem LUT ("picotada"). Pré-juntar os trechos com ffmpeg (trim/atrim alinhados ao quadro + concat, fade de 20ms no áudio) e usar um único <video> com o LUT.

Ritmo (feedback RFZ2549, 2026-10-14): cortar pausas de forma mais agressiva — dinâmico e direto ao ponto (deixar só ~0.1s de respiro); estabilização: NÃO é padrão — perguntar antes se é necessária, a menos que a tag no nome do arquivo já peça (ffmpeg local não tem vidstab e o deshake piora; usar a estabilização própria: Vision VNTranslationalImageRegistration + trajetória suavizada aplicada como x/y por quadro num wrapper); variar o zoom — às vezes aproxima, às vezes afasta, não só escalar.

Padrões de corte (feedback FB-02/AP-05, 2026-10-16):
- Cortar "engasgos" (sílabas/palavras repetidas ou abortadas: "da, do programa", "tem em, um, uma reunião", "cli… clica") sempre mantendo a concordância da frase. Conferir no áudio bruto em janela curta — a transcrição longa do Whisper esconde engasgos e às vezes inventa repetições.
- O vídeo começa no início real da fala (nada de imagem morta antes).
- Fim: ~0,5 s após a última palavra, fade-out para preto (padrão em todos; `cut.py` faz sozinho). As tarjas de CTA ficam acesas sobre o fade (aprovado no FB-02, funcionam como CTA). Exceção: se a pessoa desvia o olhar logo no fim, corte seco na última palavra (`--no-fade`), como no AP-05.
- Para achar engasgo: `_kit/fine.sh` (RMS 20 ms) + emendar candidatos e transcrever o trecho emendado; isolar a sílaba suspeita e transcrever sozinha confirma ("da...").
- Dinâmica de zoom CALMA (feedback AP-08, 2026-10-17: "zooms seguidos a cada palavra, frenético"): poucos trechos de zoom (~5 em 40 s), ≥ ~6 s entre trocas, sem tarja de abertura com zoom próprio; centralização do rosto UMA vez por trecho de zoom (`trackMode: "shot"` no creative.base.json), nunca recentralizar a cada jump cut. Enquadramento sempre limitado quadro a quadro à margem do zoom (sem barra preta).
- Zoom in/out só em fim ou troca de raciocínio (pontos finais/mudança de assunto), nunca no meio de uma ideia; não é obrigatório trocar zoom em todo jump cut.

Punch-in nos cortes (usuário aprovou 1.0 → 1.18 → 1.30, com push lento +0.04): os takes não são centralizados, então em cada zoom recentralizar o rosto lateralmente — medir o centro do rosto por trecho com Apple Vision (swift VNDetectFaceRectanglesRequest em frames a 4fps) e aplicar x = s·(540 − faceX), limitado a 540·(s−1). Motions descem nos trechos ampliados para não encostar no rosto.

Exportação padrão: 4K (2160x3840) a 24 fps (pedido do usuário 2026-10-14) — proxies/cortes também em 4K para não perder nitidez.

Pausas mais curtas e zoom variado: confirmados pelo usuário como padrão.

**Onde trabalhar (Mac tem pouco espaço — usuário pediu tudo no SSD, 2026-10-14):** o SSD é exFAT (sem links → `hyperframes init` falha), então foi criado um volume APFS em imagem: `/Volumes/SSDDRIGO1/AGROPERFORMA/HyperFrames-Trabalho.sparsebundle` (300 GB, cresce sob demanda), montado em `/Volumes/AGROPERFORMA-HF` via `projetos/_kit/montar.sh` (rodar no início de cada sessão; `hdiutil attach ... -nobrowse`).
- Projetos: `/Volumes/AGROPERFORMA-HF/projetos/<take>/` (`~/Movies/AGROPERFORMA-HF` é atalho para lá). Kit de scripts em `projetos/_kit/` (cut.py, plan.py, analyze.sh, mkcfg.py, track.py, caps.py, stab*.py, render4k.sh, template.html); `source _kit/env.sh` põe TMPDIR/histórico/caches no volume.
- `~/.cache/hyperframes/whisper` e `/history` são atalhos para `/Volumes/AGROPERFORMA-HF/cache/` (modelo large-v3 lá). Temporários/transcrições do lote: `/Volumes/AGROPERFORMA-HF/_scratch`. Nunca gerar arquivos grandes no disco do Mac.
- O volume desmonta quando o app reinicia a sessão: sempre remontar antes de qualquer etapa e pedir keep-awake em renders longos (FB-02 caiu uma vez assim).
- Render final copiado para `SELECIONADOS/EDICAO/` (o usuário organiza em PRONTO/Testes e renomeia com notas).
