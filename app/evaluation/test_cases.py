"""
Evaluation datasets.

每个case模拟一次用户请求。
"""


TEST_CASES = [


    {
        "name": "calculator_add",

        "input": "What is 6 + 11?",

        "expected": "17",

        "category": "tool",

    },



    {
        "name": "calculator_second",

        "input": "Calculate 88 + 33",

        "expected": "121",

        "category": "tool",

    },



    {
        "name": "hello_chat",

        "input": "Hello",

        "expected": "Hello",

        "category": "chat",

    },


]