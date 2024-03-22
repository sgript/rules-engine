class Rule:
    OPERATORS = {
        "gt": lambda x, y: x > y,
        "gte": lambda x, y: x >= y,
        "lt": lambda x, y: x < y,
        "lte": lambda x, y: x <= y,
        "equals": lambda x, y: x == y,
        "not_equals": lambda x, y: x != y,
    }

    def __init__(self, variable, operator, value):
        self.variable = variable
        self.operator = operator
        self.value = value

    def __repr__(self):
        return f"Rule(variable={self.variable}, operator={self.operator}, value={self.value})"

    def evaluate(self, data):
        value = data.get(self.variable)
        operation = self.OPERATORS.get(self.operator)
        if operation is None:
            raise ValueError(f"Unknown operator: {self.operator}")
        return operation(value, self.value)


class RulesEngine:
    LOGICAL_OPERATORS = {
        "AND": all,
        "OR": any,
    }

    def __init__(self, rulesets, operator):
        self.rulesets = rulesets
        self.operator = operator

    def evaluate(self, data):
        logical_operator = self.LOGICAL_OPERATORS.get(self.operator)
        if logical_operator is None:
            raise ValueError(f"Unknown operator: {self.operator}")
        return logical_operator(rule.evaluate(data) for rule in self.rulesets)


def build_rules_engine(rules_json):
    if "logical_operator" in rules_json:
        rules = [build_rules_engine(rule_json) for rule_json in rules_json["rules"]]
        return RulesEngine(rules, rules_json["logical_operator"])
    else:
        return Rule(rules_json["variable"], rules_json["operator"], rules_json["value"])
