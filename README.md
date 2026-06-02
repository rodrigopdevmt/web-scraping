<div align="center">
  <img src="https://img.shields.io/badge/status-active-brightgreen" alt="Status" />
  <img src="https://img.shields.io/badge/python-3.10%2B-blue" alt="Python" />
  <img src="https://img.shields.io/github/license/rodrigopdevmt/estudo" alt="License" />
  <img src="https://img.shields.io/badge/contributions-welcome-orange" alt="Contributions" />
  <img src="https://img.shields.io/badge/docker-ready-2496ED?logo=docker" alt="Docker" />
</div>

<br />

<h1 align="center">🕵️ Estudo - Decifrador & Utilitários</h1>

<p align="center">
  <strong>Decifrador</strong> ·
  <strong>Gerador de Escada</strong> ·
  <strong>Gerador de Senhas</strong> ·
  <strong>Validador de CPF</strong> ·
  <strong>Cifra de César</strong> ·
  <strong>Conversor de Bases</strong> ·
  <strong>Analisador de Texto</strong> ·
  <strong>Algoritmos</strong> ·
  <strong>Schema Validation</strong> ·
  <strong>Armazenamento</strong>
</p>

<p align="center">
  Projeto pessoal de estudo em Python — web scraping, processamento de dados tabulares e algoritmos de manipulação de listas.
</p>

<br />

---

## 👨‍💻 Proprietário

<div align="center">
  <h3>Rodrigo Dev MT</h3>
  <p>
    <strong>Desenvolvedor Full Stack</strong>
    <br />
    Natural de Mato Grosso
  </p>
  <p>
    Minha jornada na tecnologia começou há mais de cinco anos, guiada pela paixão por criar soluções inovadoras que realmente façam diferença na vida das pessoas.
  </p>
  <p>
    <code>React</code> ·
    <code>TypeScript</code> ·
    <code>Node.js</code> ·
    <code>Supabase</code> ·
    <code>PostgreSQL</code> ·
    <code>Tailwind CSS</code> ·
    <code>Next.js</code>
  </p>
  <p>
    <a href="https://wa.me/5566996184323" target="_blank">
      <img src="https://img.shields.io/badge/WhatsApp-25D366?style=for-the-badge&logo=whatsapp&logoColor=white" alt="WhatsApp" />
    </a>
    <a href="https://t.me/rodrigodevmt" target="_blank">
      <img src="https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram" />
    </a>
    <a href="https://github.com/rodrigopdevmt" target="_blank">
      <img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub" />
    </a>
    <a href="https://www.linkedin.com/in/rodrigo-dev-mt-929293372" target="_blank">
      <img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" />
    </a>
  </p>
  <p>
    <a href="https://www.rodrigodevmt.com.br" target="_blank">
      https://www.rodrigodevmt.com.br
    </a>
    <br />
    <a href="mailto:developer@rodrigodevmt.com.br">developer@rodrigodevmt.com.br</a>
    <br />
    Mato Grosso, Brasil
  </p>
</div>

---

## 📋 Sobre o Projeto

Este projeto nasceu como um laboratório de estudos em Python, combinando **web scraping**, **expressões regulares** e **algoritmos clássicos** em ferramentas práticas e didáticas.

### Funcionalidades

| Módulo | Descrição |
|---|---|
| **🕵️ Decifrador** | Baixa HTML de um Google Docs publicado, extrai coordenadas (x, y) com caracteres `░` e `█` de tabelas, e reconstrói uma imagem/mensagem em grade 2D |
| **🪜 Gerador de Escada** | Organiza números em estrutura piramidal (1, 2, 3... por linha) — valida se a quantidade forma um número triangular perfeito |
| **🔑 Gerador de Senhas** | Gera senhas seguras configuráveis (tamanho, maiúsculas, minúsculas, números, símbolos) |
| **🔐 Auditor de Senhas** | Calcula entropia e tempo estimado de quebra por força bruta |
| **🆔 Validador de CPF** | Valida CPF com algoritmo dos dígitos verificadores (aceita formatado ou só números) |
| **🔡 Cifra de César** | Cifra/decifra textos com deslocamento configurável — criptografia clássica |
| **🔢 Conversor de Bases** | Converte números entre binário, octal, decimal e hexadecimal |
| **📊 Analisador de Texto** | Conta palavras, caracteres, frases e exibe frequência de ocorrência |
| **🕷️ Scraper Assíncrono** | Requisições async com `aiohttp` + suporte a sites dinâmicos com `playwright` |
| **📋 Algoritmos de Listas** | Two pointers, sliding window, two sum, palíndromo, merge sorted, chunked, flatten |
| **📊 Pandas vs Polars** | Benchmarks comparativos de performance (groupby, filtro, leitura/escrita) |
| **🔍 Schema Validation** | Validação de dados com `pydantic` (modelos) + `pandera` (DataFrames) |
| **🗄️ Armazenamento** | CSV, JSON, Parquet, DuckDB, SQLite — importação e consulta |
| **💻 Monitoramento** | Exibe uso de CPU, memória e informações da máquina |
| **🔒 Criptografia AES** | Protege resultados com criptografia via `cryptography.fernet` |

---

## 🚀 Instalação

### Local

```bash
# Clone o repositório
git clone https://github.com/rodrigopdevmt/estudo.git
cd estudo

# Crie um ambiente virtual
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# Instale as dependências
pip install -r requirements.txt

# Configure a senha (opcional)
cp .env.example .env
# Edite .env com sua senha
```

### Docker (recomendado)

```bash
# Interface web
docker compose up web

# CLI interativa
docker compose run --rm cli
```

### CLI interativa

```bash
python3 -m src.cli
```

Menu com 8 opções: Decifrador, Escada, Gerar Senha, Validar CPF, Cifra de César,
Conversor de Bases e Análise de Texto.

### Interface web

```bash
streamlit run app.py
# ou
docker compose up web
```

Acesse `http://localhost:8501` — 7 abas com todas as ferramentas.

---

## 🏗️ Estrutura do Projeto

```
estudo/
├── src/                  # Código fonte principal
│   ├── __init__.py
│   ├── cli.py            # CLI interativa
│   ├── decipher.py       # Decifrador de mensagens
│   ├── staircase.py      # Gerador de escada
│   ├── tools.py          # Utilitários (senha, CPF, cifra, bases, texto)
│   ├── scraper.py        # Scraping assíncrono (aiohttp + playwright)
│   ├── algorithms.py     # Algoritmos de listas
│   ├── benchmarks.py     # Pandas vs Polars benchmarks
│   ├── validation.py     # Schema validation (pydantic + pandera)
│   ├── storage.py        # Armazenamento (CSV, JSON, Parquet, DuckDB, SQLite)
│   └── config.py         # Configurações (senha via env var)
├── tests/                # Testes unitários
│   ├── __init__.py
│   ├── test_decipher.py
│   ├── test_staircase.py
│   ├── test_tools.py
│   ├── test_algorithms.py
│   ├── test_validation.py
│   ├── test_storage.py
│   └── test_scraper.py
├── archive/              # Versões antigas do decifrador
├── app.py                # Interface web Streamlit
├── Dockerfile            # Build da imagem Docker
├── docker-compose.yml    # Orquestração dos containers
├── sistema_consolidado.py # CLI original (legado)
├── create_staircase.py   # Algoritmo original (legado)
├── requirements.txt
├── pyproject.toml
├── .env.example
├── .dockerignore
├── .gitignore
├── LICENSE
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
└── SECURITY.md
```

---

## 🧪 Testes

```bash
pytest          # todos os testes
pytest -v       # modo verbose com nomes dos testes
```

## ✅ Cobertura

```bash
pip install pytest-cov
pytest --cov=src tests/
```

---

## 🧑‍🤝‍🧑 Contribuindo

Contribuições são bem-vindas! Veja o [CONTRIBUTING.md](CONTRIBUTING.md) para guia completo.

1. Faça um fork do projeto
2. Crie sua branch (`git checkout -b feature/FeatureIncrivel`)
3. Commit suas mudanças (`git commit -m 'Adiciona FeatureIncrivel'`)
4. Push para a branch (`git push origin feature/FeatureIncrivel`)
5. Abra um Pull Request

---

## 🛡️ Licença

Distribuído sob licença MIT. Veja [LICENSE](LICENSE) para mais informações.

---

## 📞 Contato

**Rodrigo Dev MT**

- 🌐 [rodrigodevmt.com.br](https://www.rodrigodevmt.com.br)
- 📧 [developer@rodrigodevmt.com.br](mailto:developer@rodrigodevmt.com.br)
- 📱 (66) 99618-4323
- 📍 Mato Grosso, Brasil

<p align="center">
  <sub>Feito com ❤️ por Rodrigo Dev MT</sub>
</p>
