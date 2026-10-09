# EduPredict Analytics · EPA-page

Site estático da pesquisa e do acompanhamento do **TGI II**, com o estudo e o banner do **TGI I** como referência histórica. O site está em `site/` e não depende de build ou instalação de pacotes.

## Páginas

- `/` — visão da pesquisa e navegação;
- `/estudo-anterior/` — TGI I, método, resultados reportados e limites;
- `/banner/` — pôster original em PDF e síntese web;
- `/pesquisa-atual/` — TGI II, questão, pipeline experimental e validação pendente;
- `/acompanhamento/` — etapas, biblioteca e rastreabilidade;
- `/documentos/pipeline/` e `/documentos/relatorio-inicial/` — espelhos revisados de dois documentos técnicos do EPA.

Os PDFs públicos selecionados ficam em `site/files/`: full paper e banner do TGI I, e 1º relatório do TGI II. Eles vieram de `EDUPREDICT_PACOTE_COMPLETO_2026-10-09.zip`, disponibilizado no workspace EPA. Documentos mestres do pacote foram usados como contexto, mas não foram publicados em massa.

## Prévia local

Na raiz deste repositório:

```bash
python -m http.server 8000 --directory site
```

Acesse `http://localhost:8000/`. Os links são relativos para funcionar também sob `/EPA-page/` no GitHub Pages.

## Atualização com revisão

`scripts/sync-epa.py` lê **somente** `research/README.md`, `research/reports/initial_pipeline_summary.md` e o último commit do repositório EPA. Ele gera duas páginas de documentação e `site/assets/project-status.json`; não altera o EPA.

O workflow `sync-epa.yml` roda a cada seis horas, manualmente ou por `repository_dispatch` com evento `epa-updated`. Ele propõe as mudanças em um **pull request**. O conteúdo novo só chega ao site depois de revisão e merge em `main`. O workflow `pages.yml` publica `site/` no GitHub Pages após esse merge.

O repositório EPA também possui `.github/workflows/notify-epa-page.yml`. Para disparar a proposta logo após cada push no EPA, configure nele o segredo `EPA_PAGE_DISPATCH_TOKEN` com permissão para enviar `repository_dispatch` à EPA-page. Sem esse segredo, a sincronização agendada da EPA-page continua disponível.

Para criar PRs com `GITHUB_TOKEN`, habilite em **Settings → Actions → General → Workflow permissions → Allow GitHub Actions to create and approve pull requests**. Se o EPA principal for privado, configure o segredo `EPA_SOURCE_TOKEN` com acesso de leitura ao repositório. Para Pages, selecione **GitHub Actions** como fonte de publicação nas configurações do repositório.

O EPA contém este repositório como submódulo Git. Atualizar a EPA-page não move automaticamente o ponteiro do submódulo no EPA; registre o novo commit do submódulo no EPA quando quiser fixar essa versão no projeto principal.

## Regras editoriais

- Identifique claramente TGI I, TGI II, plano, experimento e resultado validado.
- Não apresente os 62.400 registros sintéticos como alunos reais nem como dados operacionais da interface.
- Não use a acurácia histórica do TGI I como resultado ou meta garantida do TGI II.
- Não trate predição de desempenho como predição validada de evasão.
- Revise documentos e PDFs antes de tornar o repositório público ou mesclar uma proposta de sincronização.

Fontes principais: `00-PLANO-MESTRE.md`, `TGI-II-EduPredict-Escopo-Base.md`, 1º relatório do TGI II, full paper e banner do TGI I, e `research/README.md` do EPA.
