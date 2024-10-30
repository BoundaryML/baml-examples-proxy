# Setting up a proxy server for usage with BAML

This guide will help you set up a proxy server for usage with BAML. This is useful if you want to use BAML to call a model with your own provider.

## Prerequisites

Install `uv`:

See https://docs.astral.sh/uv/getting-started/installation/

Modify the API key in anthropic_proxy.py.

## Setup

Install the dependencies:

```bash
uv sync
```

Generate the BAML client:

```bash
uv run baml-cli generate
```

Run the anthropic proxy server:

```bash
uv run fastapi dev anthropic_proxy.py --port 8081
```

Run the  web server:

```bash
uv run fastapi dev hello.py
```

## Test

```bash
curl -X POST "http://localhost:8080/"
```

