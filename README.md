# Recurse

## Usage

```bash
recurse hello
recurse hello --name friend

recurse --help
```

## Development

Requires [uv](https://docs.astral.sh/uv/).

```bash
uv sync --dev
```

```bash
make lint        # ruff check + format check
make format      # ruff format + autofix
make typecheck   # ty
make test        # pytest
```

To run the checks automatically before each commit:

```bash
git config core.hooksPath .githooks
```
