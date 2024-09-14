# <div align="center">Kontext Copilot</div>

<div align="center">
<b>Kontext Copilot is an AI empowered assistant for data analytics that runs on your local computer.</b>
<p align="center">
  <a href="https://kontext.tech/copilot" target="_blank"><strong>Project</strong></a> ·
  <a href="https://discord.gg/MYna8q5J" target="_blank"><strong>Discord</strong></a> ·
  <a href="https://kontext.tech/diagram/1388/kontext-copilot-roadmap" target="_blank"><strong>Roadmap</strong></a> ·
  <a href="https://kontext.tech/article/1385/kontext-copilot-installation" target="_blank"><strong>Installation</strong></a> ·
  <a href="https://kontext.tech/article/1386/get-started-with-kontext-copilot" target="_blank"><strong>Docs</strong></a>
</p>
<hr/>

![kontext-copilot-example](https://cdn.kontext.tech/Images/ai/kontext-copilot-light.gif)

</div>

## Prerequisites

-  Python 3.9+
-  [Ollama](https://ollama.com/) or other compatible LLM serving tools. Ollama is recommended for the current release.

## Installation

```
pip install kontext-copilot
```

Launch the tool:

```
kontext-copilot
```

For more details about installation, refer to [**Kontext Copilot Installation**](https://kontext.tech/article/1385/kontext-copilot-installation)

## Get started

Kontext Copilot is still at early stage. Please follow the guide below to evaluate the tool and to provide feedbacks.

[**Get started with Kontext Copilot**](https://kontext.tech/article/1386/get-started-with-kontext-copilot)

## Roadmap

> Refer to [https://kontext.tech/diagram/1388/kontext-copilot-roadmap](https://kontext.tech/diagram/1388/kontext-copilot-roadmap) for latest roadmap.
> ![kontext-copilot-roadmap](https://kontext.tech/api/flex/diagram/diagram-1388?v=1)

## Change logs

[**Change logs**](https://github.com/kontext-tech/kontext-copilot/blob/main/CHANGELOG.md)

## For developers and contributors

This section shows you how to setup local environment to participate in development of kontext-copilot.

VS Code is recommended.

### Setup Python environment

Create virtual environment. Please use **Python 3.9**.

```
python -m venv .venv
```

Activate the virtual environment.

For Windows:

```
.\.venv\Scripts\activate
```

For UNIX-alike systems:

```
source ./.venv/bin/activate
```

Upgrade `pip`:

```
python -m pip install --upgrade pip
```

Install poetry:

```
pip install poetry
```

Refer to [https://python-poetry.org/docs/](https://python-poetry.org/docs/) for details about Poetry.

Install packages:

```
poetry install
```

### Install pre-commit & Commitizen

```
poetry add pre-commit
```

Install `pre-commit` hook scripts:

```
pre-commit install
pre-commit install --hook-type commit-msg --hook-type pre-push
```

(Optional) Run against all files:

```
pre-commit run --all-files
```

### Commit

Use the following command line to commit changes:

```
cz c
```

### Build package

```
poetry build
```

### Initialize local database

Run VS Code task `alembic: upgrade to head`
