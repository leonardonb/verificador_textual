# 🔎 Verificador de Links com Metodologia PRISMA

Este projeto realiza a **verificação de links acadêmicos** com base em **termos-chave definidos pelo usuário**, buscando os termos no conteúdo dos links (HTML ou PDF), aplicando a **metodologia PRISMA** para sumarização dos resultados. A aplicação pode ser executada de três formas:

- ✅ via **terminal interativo**
- ✅ via **interface web com Flask**

---

## 🧰 Requisitos

```bash
pip install -r requirements.txt
```

---

## 🚀 Modos de Execução

### 📂 Terminal Interativo

Execute o script principal:

```bash
python main.py
```

Você poderá:
- Enviar um arquivo Excel contendo links (agora com seleção por **caixa de diálogo**),
- Ou realizar buscas em plataformas acadêmicas (SciELO e Google Scholar).

---

### 2. 🌐 Interface Web com Flask

Inicie o servidor web:

```bash
Escolher a opção 2
```

Abra no navegador:  
`http://127.0.0.1:5000`

Você poderá:
- Fazer upload de um arquivo Excel,
- Inserir termos-chave,
- Baixar os arquivos gerados.

---

## 🐳 Docker

Para rodar com Docker:

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
│   └── index.html        # Interface HTML com barra de progresso
├── Dockerfile            # Containerização da aplicação Flask
├── requirements.txt      # Dependências do projeto
└── README.md             # Instruções
```

---

## 🧪 Metodologia PRISMA

Este projeto implementa um resumo dos dados segundo os princípios do PRISMA:

- Identificados
- Avaliados
- Incluídos
- Excluídos

Gera automaticamente:
- `relatorio_prisma.json`
- `relatorio_prisma.csv`
- `fluxograma_prisma.png`

---

## 🧪 Fontes de Pesquisa Suportadas

- Upload de planilha `.xlsx` com coluna `link`
- (Opcional) Busca automatizada em **SciELO** e **Google Scholar** com `busca.py`

---

## 📦 Dependências

```txt
flask
pandas
requests
beautifulsoup
PyMuPDF
openpyxl
xlsxwriter
graphviz
lxml
scholarly
prisma
```

---
## 📌 Observações

- Para o Google Scholar, usamos a biblioteca `scholarly`.
- O SciELO é acessado por scraping.
- O projeto utiliza `PyMuPDF` para leitura de PDFs.
- Certifique-se de ter o `graphviz` instalado e configurado no sistema para gerar os fluxogramas.

---

## 📤 Exemplo de Execução

```bash
python main.py
# Escolha: 1
# → Escolha os termos
# → Selecione o arquivo Excel pela janela
```

---

## 👨‍💻 Autor

**Leonardo Nunes Barros**  
Projeto voltado para automação de revisões sistemáticas com apoio à metodologia PRISMA.