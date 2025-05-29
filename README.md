# 🔎 Verificador de Links com Metodologia PRISMA

Este projeto realiza a **verificação de links acadêmicos** com base em **termos-chave definidos pelo usuário**, buscando os termos no conteúdo dos links (HTML ou PDF), aplicando a **metodologia PRISMA** para sumarização dos resultados.

A aplicação pode ser executada de duas formas:

- ✅ via **terminal interativo**
- ✅ via **interface web com Flask**

---

## 🧰 Requisitos

Instale todas as dependências com:

```bash
pip install -r requirements.txt
```

---

## 🚀 Como Utilizar

Ao executar o script principal (`main.py`), você será questionado sobre:

1. **Qual interface deseja usar**:
    - Terminal (modo 1)
    - Interface Web com Flask (modo 2)

2. **Qual a origem dos links**:
    - Enviar um **arquivo Excel** com os links (coluna `link`)
    - Ou realizar uma **busca automática** nos portais **SciELO** e **Google Scholar** com os termos-chave

Após a verificação, os relatórios serão gerados automaticamente.

---

## 📂 Execução via Terminal

```bash
python main.py
```

- ✅ Permite selecionar o Excel via **caixa de diálogo**
- ✅ Ou realizar a **busca automática** nas plataformas acadêmicas
- ✅ Gera o resultado da verificação e permite escolher o local para salvar

---

## 🌐 Execução via Interface Web (Flask)

1. Execute o script e escolha a **opção 2** no terminal:

```bash
python main.py
```

2. O navegador será aberto automaticamente em:  
   `http://127.0.0.1:5000`

3. Na interface web, você poderá:

- Inserir os **termos-chave** separados por vírgulas
- Escolher entre **enviar um arquivo Excel** ou realizar a **busca automática**
- Visualizar uma **barra de progresso**
- Baixar os arquivos gerados

---

## 🐳 Docker (Opcional)

```bash
docker build -t verificador_textual .
docker run -p 5000:5000 verificador_textual
```

---

## 📄 Estrutura do Projeto

```
verificador_textual/
├── app.py                # Interface web com Flask
├── main.py               # Execução interativa via terminal
├── verificador.py        # Lógica de verificação e extração textual
├── prisma.py             # Geração de relatórios e fluxograma PRISMA
├── busca.py              # Buscas reais no SciELO e Google Scholar
├── templates/
│   └── index.html        # Interface HTML com Bootstrap e barra de progresso
├── static/
│   └── arquivos gerados (Excel, JSON, CSV, PNG)
├── Dockerfile            # Containerização da aplicação Flask
├── requirements.txt      # Dependências do projeto
└── README.md             # Instruções
```

---

## 🧪 Metodologia PRISMA

Este projeto implementa um resumo automatizado com base na metodologia PRISMA, incluindo:

- ✅ Identificados
- ✅ Avaliados
- ✅ Incluídos
- ✅ Excluídos

Arquivos gerados:

- `relatorio_prisma.json`
- `relatorio_prisma.csv`
- `fluxograma_prisma.png`

---

## 📤 Fontes de Pesquisa Suportadas

- ✅ Upload de planilha `.xlsx` com coluna `link`
- ✅ Busca automatizada em **SciELO** e **Google Scholar**

---

## 📦 Dependências

```txt
flask
pandas
requests
beautifulsoup4
PyMuPDF
openpyxl
xlsxwriter
graphviz
lxml
scholarly
```

---

## 📌 Observações

- Para o Google Scholar, utilizamos a biblioteca `scholarly`.
- O SciELO é acessado via scraping com `BeautifulSoup`.
- Os PDFs são lidos com `PyMuPDF`.
- Para gerar os fluxogramas PRISMA, é necessário ter o `Graphviz` instalado no sistema.
- Os arquivos gerados são salvos na pasta `static/`.

---

## 👨‍💻 Autor

**Leonardo Nunes Barros**  
Projeto voltado para automação de revisões sistemáticas com apoio à metodologia PRISMA.
