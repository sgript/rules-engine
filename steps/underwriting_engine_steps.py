from behave import given, when, then
import json
from underwriting_engine import build_rules_engine


@given("the underwriting rules")
def step_given_the_underwriting_rules(context):
    rules_json_str = json.loads(context.text)
    context.rules_engine = build_rules_engine(rules_json_str)


@when("I evaluate the rules with the data")
def step_when_i_evaluate_the_rules(context):
    data = json.loads(context.text)
    context.result = context.rules_engine.evaluate(data)


@then('the result should be "{expected_result}"')
def step_then_the_result_should_be(context, expected_result):
    assert (
        str(context.result) == expected_result
    ), f"Expected {expected_result}, but got {context.result}"
