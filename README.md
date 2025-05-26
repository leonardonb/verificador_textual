# 🔍 Verificador de Conteúdo com Metodologia PRISMA

Este projeto permite analisar uma lista de links (em um arquivo Excel) e verificar se eles contêm um conjunto de palavras-chave fornecidas pelo usuário. Utiliza a metodologia PRISMA para gerar relatórios e fluxogramas explicando o processo de seleção dos artigos.

---

## 🧠 Funcionalidades

- Verificação de links em HTML e PDF
- Extração automática de palavras-chave
- Geração de relatórios:
  - Excel com formatação condicional
  - JSON e CSV com resumo PRISMA
  - Fluxograma PRISMA em PNG
- Interface Web (via Flask)
- Execução via terminal (modo texto ou interface local)
- Execução via Docker

---

## 📁 Estrutura do Projeto

```
verificador-prisma/
├── app.py                 # Interface Web Flask
├── main.py                # Executável com menu terminal
├── verificador.py         # Lógica de verificação
├── prisma.py              # Lógica PRISMA
├── requirements.txt       # Dependências Python
├── Dockerfile             # Container Docker
├── templates/
│   └── index.html         # Interface HTML da aplicação web
└── static/                # Arquivos gerados (resultados)
```

---

## ▶️ Como usar via Terminal

### 1. Instale as dependências

```bash
pip install -r requirements.txt
```

### 2. Execute o script principal

```bash
python main.py
```

### 3. Escolha o modo de uso:

- `[1]` Executar em **modo terminal**: você seleciona o arquivo e insere palavras-chave.
- `[2]` Executar **interface web local com Flask**: será aberta automaticamente no navegador em http://localhost:5000

---

## 🐳 Como rodar via Docker

### 1. Build da imagem

```bash
docker build -t verificador-flask .
```

### 2. Executar o container

```bash
docker run -p 5000:5000 verificador-flask
```

### 3. Acessar a aplicação

[http://localhost:5000](http://localhost:5000)

---

## 📦 Funcionalidade da interface Flask

- Upload de planilha `.xlsx` com links
- Campo para palavras-chave separadas por vírgulas
- Geração automática dos arquivos para download:
  - `resultado_formatado.xlsx`
  - `relatorio_prisma.json`
  - `relatorio_prisma.csv`
  - `fluxograma_prisma.png`

---

## ✅ Requisitos

- Python 3.10+
- Navegador moderno (Chrome, Firefox, etc.)
- Docker (opcional, para rodar como container)

---

## 📄 Licença

Este projeto é de uso acadêmico e educativo. Fique à vontade para adaptar às suas necessidades.

