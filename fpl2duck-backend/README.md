
# fpl2duck-backend

## Setup development environment

The following tools are required

| Tool                                                          | Description                         |
|---------------------------------------------------------------|-------------------------------------|
| [Poetry](https://python-poetry.org/)                          | Dependency management and packaging |
| [pyenv](https://github.com/pyenv/pyenv)                       | Manage Python versions              |
| [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv) | Manage Python virtual environments  |

## Generate Pydantic models
Pydantic models are generated using `datamodel-code-generator`

```
datamodel-codegen --input api/dump/bootstrap.json --output api/models/bootstrap.py
```

## Interesting Libs
https://perspective.finos.org/docs/js/
