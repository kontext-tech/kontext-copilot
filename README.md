# <div align="center">Kontext Copilot</div>

<div align="center">
<b>Kontext Copilot is an AI empowered assistant for data analytics that runs on your local computer.</b>

<a href="https://discord.gg/MYna8q5J" target="_blank" title="Discord">
    <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" fill="currentColor" class="bi bi-discord" viewBox="0 0 16 16">
        <path d="M13.545 2.907a13.2 13.2 0 0 0-3.257-1.011.05.05 0 0 0-.052.025c-.141.25-.297.577-.406.833a12.2 12.2 0 0 0-3.658 0 8 8 0 0 0-.412-.833.05.05 0 0 0-.052-.025c-1.125.194-2.22.534-3.257 1.011a.04.04 0 0 0-.021.018C.356 6.024-.213 9.047.066 12.032q.003.022.021.037a13.3 13.3 0 0 0 3.995 2.02.05.05 0 0 0 .056-.019q.463-.63.818-1.329a.05.05 0 0 0-.01-.059l-.018-.011a9 9 0 0 1-1.248-.595.05.05 0 0 1-.02-.066l.015-.019q.127-.095.248-.195a.05.05 0 0 1 .051-.007c2.619 1.196 5.454 1.196 8.041 0a.05.05 0 0 1 .053.007q.121.1.248.195a.05.05 0 0 1-.004.085 8 8 0 0 1-1.249.594.05.05 0 0 0-.03.03.05.05 0 0 0 .003.041c.24.465.515.909.817 1.329a.05.05 0 0 0 .056.019 13.2 13.2 0 0 0 4.001-2.02.05.05 0 0 0 .021-.037c.334-3.451-.559-6.449-2.366-9.106a.03.03 0 0 0-.02-.019m-8.198 7.307c-.789 0-1.438-.724-1.438-1.612s.637-1.613 1.438-1.613c.807 0 1.45.73 1.438 1.613 0 .888-.637 1.612-1.438 1.612m5.316 0c-.788 0-1.438-.724-1.438-1.612s.637-1.613 1.438-1.613c.807 0 1.451.73 1.438 1.613 0 .888-.631 1.612-1.438 1.612"></path>
    </svg> Discord
</a>

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
