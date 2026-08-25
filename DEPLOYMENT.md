# Publicação no Streamlit Community Cloud

Aplicação publicada em: <https://cesar-aaron-llms.streamlit.app>

Esta etapa precisa ser feita pela conta do aluno, pois ela vincula o aplicativo ao seu GitHub e cria uma URL pública.

## 1. Teste local

No terminal, dentro da pasta do projeto:

```bash
source .venv/bin/activate
streamlit run app.py
```

Abra a URL informada, visite as quatro páginas e teste ao menos dois filtros.

## 2. Prepare o repositório GitHub

1. No GitHub, crie um repositório vazio, por exemplo `cp1-dashboard-llms`.
2. No terminal do projeto, execute:

   ```bash
   git init
   git add app.py fetch_and_prepare_dataset.py requirements.txt README.md DEPLOYMENT.md presentation_coringa.md data .gitignore
   git commit -m "Dashboard CP1 sobre LLMs"
   git branch -M main
   git remote add origin https://github.com/SEU_USUARIO/cp1-dashboard-llms.git
   git push -u origin main
   ```

3. Confirme no GitHub que `app.py`, `requirements.txt` e `data/llm_leaderboard.csv` foram enviados.

Não envie `.venv/`, senhas, tokens, currículo com dados de contato ou arquivos confidenciais.

## 3. Publique

1. Entre em [share.streamlit.io](https://share.streamlit.io/) com sua conta.
2. Escolha **Create app** e conecte o GitHub, se solicitado.
3. Selecione o repositório, a branch `main` e o arquivo **`app.py`**.
4. Clique em **Deploy** e aguarde a instalação das dependências.
5. Copie a URL pública gerada e teste-a em uma janela anônima.

## 4. Validação final

- A URL abre sem login.
- As quatro abas aparecem.
- A página de análise mostra indicadores e gráficos.
- A fonte e a data de extração aparecem na página de análise.
- Os textos pessoais e a conclusão estão completos e são seus.
- O arquivo ZIP de entrega contém o código, `data/`, README e apresentação.

## 5. Criação do ZIP, se solicitada

Pelo gerenciador de arquivos, compacte a pasta do projeto excluindo `.venv` e `__pycache__`. O ZIP deve conter o código-fonte e a base de dados, mas não o ambiente virtual.
