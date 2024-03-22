Feature: Underwriting Engine
    The underwriting engine should correctly evaluate rules based on provided data.

    Background:
        Given the underwriting rules:
        """
        {
        "logical_operator": "AND",
        "rules": [
            {
            "logical_operator": "AND",
            "rules": [
                {
                "logical_operator": "AND",
                "rules": [
                    {"variable": "age", "operator": "gt", "value": 18},
                    {"variable": "credit", "operator": "gt", "value": 700},
                    {"variable": "age", "operator": "lt", "value": 900}
                ]
                },
                {
                "variable": "profession",
                "operator": "not_equals",
                "value": "Cookie Monster"
                }
            ]
            },
            {"variable": "income", "operator": "gt", "value": 50000}
        ]
        }
        """

    Scenario: Customer meets all criteria
        When I evaluate the rules with the data
        """
        {
            "age": 20,
            "credit": 800,
            "profession": "Engineer",
            "income": 60000
        }
        """
        Then the result should be "True"

    Scenario: Customer does not meet age and credit criteria
        When I evaluate the rules with the data
        """
        {
            "age": 16,
            "credit": 650,
            "profession": "Engineer",
            "income": 60000
        }
        """
        Then the result should be "False"

    Scenario: Customer is a Cookie Monster
        When I evaluate the rules with the data
        """
        {
            "age": 99,
            "credit": 9000,
            "profession": "Cookie Monster",
            "income": 60000
        }
        """
        Then the result should be "False"

    Scenario: Customer is Master Yoda
        When I evaluate the rules with the data
        """
        {
            "age": 900,
            "credit": 700,
            "profession": "Jedi",
            "income": 60000
        }
        """
        Then the result should be "False"