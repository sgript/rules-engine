import json
import sys
from underwriting_engine import build_rules_engine


def main():
    if len(sys.argv) != 3:
        print(
            "Error: Please provide two arguments, first the ruleset and second the data to check against the ruleset."
        )
        sys.exit(1)

    try:
        rules_json = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        print("Error: The first argument is not valid JSON.")
        sys.exit(1)
    try:
        data_json = json.loads(sys.argv[2])
    except json.JSONDecodeError:
        print("Error: The second argument is not valid JSON.")
        sys.exit(1)

    try:
        rules_engine = build_rules_engine(rules_json).evaluate(data_json)
        print(rules_engine)
    except Exception as e:
        print(f"Error: An error occurred while evaluating the rules: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

"""
Accepts two arguments:
1. The entire ruleset
2. The data to check against the ruleset

Example:

python main.py \
'{"logical_operator": "AND", "rules": [{"logical_operator": "OR", "rules": [{"logical_operator": "AND", "rules": [{"variable": "age", "operator": "gt", "value": 18}, {"variable": "credit", "operator": "gt", "value": 700}]}, {"variable": "profession", "operator": "not_equals", "value": "Cookie Monster"}]}, {"variable": "income", "operator": "gt", "value": 50000}]}' \
'{"age": 20, "credit": 750, "profession": "Software Engineer", "income": 60000}'
"""
