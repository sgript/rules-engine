# Underwriting Engine

Simple underwriting engine to define rules with gt/gte/lt/lte/equals/not_equals operators and then group rules into an engine for logical behaviour and group engines together for nested logical behaviour, outputting true (accepted) and false (rejected).

## Getting Started

### Prerequisites

- Python 3
- Poetry

### Installing

Whilst inside `rule-engine/`:

```
python -m venv venv
source ./venv/bin/activate
poetry install
```

### Running the tests

```
poetry run pytest
poetry run behave
```

### Commandline

```
poetry run python main.py \
'{"logical_operator": "AND", "rules": [{"logical_operator": "OR", "rules": [{"logical_operator": "AND", "rules": [{"variable": "age", "operator": "gt", "value": 18}, {"variable": "credit", "operator": "gt", "value": 700}]}, {"variable": "profession", "operator": "not_equals", "value": "Cookie Monster"}]}, {"variable": "income", "operator": "gt", "value": 50000}]}' \
'{"age": 20, "credit": 750, "profession": "Software Engineer", "income": 60000}'
```
