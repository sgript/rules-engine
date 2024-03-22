import pytest
from underwriting_engine import Rule, RulesEngine, build_rules_engine


@pytest.fixture
def rules_engine():

    # ((age > 18 AND credit > 700) OR profession != "Cookie Monster") AND income > 50000
    rules_json = {
        "logical_operator": "AND",
        "rules": [
            {
                "logical_operator": "OR",
                "rules": [
                    {
                        "logical_operator": "AND",
                        "rules": [
                            {"variable": "age", "operator": "gt", "value": 18},
                            {"variable": "credit", "operator": "gt", "value": 700},
                        ],
                    },
                    {
                        "variable": "profession",
                        "operator": "not_equals",
                        "value": "Cookie Monster",
                    },
                ],
            },
            {"variable": "income", "operator": "gt", "value": 50000},
        ],
    }
    return build_rules_engine(rules_json)


@pytest.fixture
def rules():
    rules = {
        "age": Rule("age", "gt", 18),
        "credit": Rule("credit", "gt", 80),
        "income": Rule("income", "gt", 50000),
    }
    return rules


def test_evaluate_gt(rules):
    age_rule = Rule("age", "gt", 16)

    data = {"age": 17}
    assert age_rule.evaluate(data)

    data = {"age": 16}
    assert not age_rule.evaluate(data)


def test_evaluate_lt(rules):
    credit_rule = Rule("credit", "lt", 90)

    data = {"credit": 89}
    assert credit_rule.evaluate(data)

    data = {"credit": 90}
    assert not credit_rule.evaluate(data)


def test_evaluate_gte():
    age_rule = Rule("age", "gte", 18)

    data = {"age": 18}
    assert age_rule.evaluate(data)

    data = {"age": 19}
    assert age_rule.evaluate(data)

    data = {"age": 17}
    assert not age_rule.evaluate(data)


def test_evaluate_lte():
    credit_rule = Rule("credit", "lte", 90)

    data = {"credit": 90}
    assert credit_rule.evaluate(data)

    data = {"credit": 89}
    assert credit_rule.evaluate(data)

    data = {"credit": 91}
    assert not credit_rule.evaluate(data)


def test_evaluate_equals():
    job_type_rule = Rule("profession", "not_equals", "Cookie Monster")

    data = {"profession": "Cookie Monster"}
    assert not job_type_rule.evaluate(data)  # we reject the cookie monster

    data = {"profession": "Software Engineer"}
    assert job_type_rule.evaluate(data)  # we accept software engineers

    data = {"profession": "Data Scientist"}
    assert job_type_rule.evaluate(data)  # we accept data scientists


def test_rules_engine_and():
    rule1 = Rule("age", "gt", 18)
    rule2 = Rule("credit", "gt", 80)
    engine = RulesEngine([rule1, rule2], "AND")  # age > 18 AND credit > 80

    data = {"age": 20, "credit": 90}
    assert engine.evaluate(data)

    data = {"age": 20, "credit": 70}
    assert not engine.evaluate(data)


def test_rules_engine_or():
    rule1 = Rule("age", "gt", 18)
    rule2 = Rule("credit", "gt", 80)
    engine = RulesEngine([rule1, rule2], "OR")  # age > 18 OR credit > 80

    data = {"age": 20, "credit": 90}
    assert engine.evaluate(data)

    data = {"age": 16, "credit": 90}
    assert engine.evaluate(data)

    data = {"age": 16, "credit": 70}
    assert not engine.evaluate(data)


def test_rules_engine_nested_and():
    rule1 = Rule("age", "gt", 18)
    rule2 = Rule("credit", "gt", 80)
    rule3 = Rule("income", "gt", 50000)

    engine1 = RulesEngine([rule1, rule2], "AND")
    engine2 = RulesEngine(
        [engine1, rule3], "AND"
    )  # (age > 18 AND credit > 80) AND income > 50000

    data = {"age": 20, "credit": 90, "income": 60000}
    assert engine2.evaluate(data)  # (true and true) and true = true

    data = {
        "age": 20,
        "credit": 70,
        "income": 60000,
    }
    assert not engine2.evaluate(data)  # (true and false) and true = false

    data = {
        "age": 20,
        "credit": 90,
        "income": 40000,
    }
    assert not engine2.evaluate(data)  # (true and true) and false = false


def test_rules_engine_nested_or():
    rule1 = Rule("age", "gt", 18)
    rule2 = Rule("credit", "gt", 80)
    rule3 = Rule("income", "gt", 50000)

    engine1 = RulesEngine([rule1, rule2], "OR")  # age > 18 OR credit > 80
    engine2 = RulesEngine(
        [engine1, rule3], "AND"
    )  # (age > 18 OR credit > 80) AND income > 50000

    data = {"age": 20, "credit": 90, "income": 60000}
    assert engine2.evaluate(data)  # (true or true) and true = true

    data = {
        "age": 20,  # true
        "credit": 70,  # false
        "income": 60000,  # true
    }
    assert engine2.evaluate(data)  # (true or false) and true = true

    data = {
        "age": 17,  # false
        "credit": 20,  # false
        "income": 100,  # false
    }
    assert not engine2.evaluate(data)  # (false or false) and false = false


def test_rules_engine_complex_nested(rules):
    """
    ((age > 18 AND credit > 80) OR profession != "Cookie Monster")
    AND income > 50000
    """
    engine1 = RulesEngine([rules["age"], rules["credit"]], "AND")
    engine2 = RulesEngine(
        [engine1, Rule("profession", "not_equals", "Cookie Monster")], "OR"
    )
    engine3 = RulesEngine([engine2, rules["income"]], "AND")

    data = {
        "age": 20,
        "credit": 90,
        "profession": "Software Engineer",
        "income": 60000,
    }
    assert engine3.evaluate(data)

    data = {
        "age": 20,
        "credit": 90,
        "profession": "Cookie Monster",
        "income": 60000,
    }
    assert engine3.evaluate(data)

    data = {
        "age": 16,
        "credit": 20,
        "profession": "Cookie Monster",
        "income": 60000,
    }
    assert not engine3.evaluate(data)

    data = {
        "age": 16,
        "credit": 20,
        "profession": "Cookie Monster",
        "income": 2,
    }
    assert not engine3.evaluate(data)


@pytest.mark.parametrize(
    "person, expected",
    [
        (
            {
                "age": 20,
                "credit": 750,
                "profession": "Software Engineer",
                "income": 60000,
            },
            True,
        ),
        (
            {"age": 16, "credit": 600, "profession": "Cookie Monster", "income": 60000},
            False,
        ),
        (
            {"age": 1, "credit": 1, "profession": "Cookie Monster", "income": 40000},
            False,
        ),
        (
            {
                "age": 90,
                "credit": 9000,
                "profession": "Cookie Monster",
                "income": 40000,
            },
            False,
        ),
    ],
)
def test_built_rules_engine(rules_engine, person, expected):
    assert rules_engine.evaluate(person) == expected


def test_rule_unknown_operator():
    smooth_operator = "🎵_hes_a_smooth_operator_🎵"
    with pytest.raises(ValueError, match=f"Unknown operator: {smooth_operator}"):
        Rule("age", smooth_operator, 18).evaluate({"age": 20})


def test_rules_engine_unknown_operator():
    smooth_operator = "🎵_hes_a_smooth_operator_🎵"
    rule1 = Rule("age", "gt", 18)
    rule2 = Rule("credit", "gt", 80)
    with pytest.raises(ValueError, match=f"Unknown operator: {smooth_operator}"):
        RulesEngine([rule1, rule2], smooth_operator).evaluate({"age": 20, "credit": 90})
