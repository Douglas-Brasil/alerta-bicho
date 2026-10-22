# 🚀 Inicialização do Projeto

## 1. Instalação do uv

O [uv](https://docs.astral.sh/uv/) é uma ferramenta utilizada para gerenciar dependências e ambientes Python.

No Windows, abra o PowerShell e execute:

```
winget install --id astral-sh.uv -e
```

Após a instalação, feche e abra o terminal novamente e verifique se o uv foi instalado corretamente:

```
uv --version
```

## 2. Executando o projeto

Com o uv instalado, abra o terminal na pasta raiz do projeto e execute:

```
uv run fastapi dev
```

O comando inicia o servidor de desenvolvimento do FastAPI. Após a inicialização, o terminal exibirá o endereço local para acessar a aplicação pelo navegador.

## 📁 Arquitetura do Projeto

```
projeto/
│
├── app.py
│
└── view/
    ├── home.html
    └── style.css
```

### Principais arquivos

- **`app.py`** — arquivo principal da aplicação, responsável pela configuração e execução do servidor FastAPI.
- **`view/home.html`** — arquivo HTML responsável pela estrutura da interface da aplicação.
- **`view/style.css`** — arquivo CSS responsável pela estilização e aparência visual da interface.

