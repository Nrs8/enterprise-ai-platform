from app.evaluation.models import EvaluationCase




def load_cases():

    return [

        EvaluationCase(
            id="math_001",
            input="6 + 11",
            expected="17",
        ),


        EvaluationCase(
            id="math_002",
            input="88 + 33",
            expected="121",
        ),


        EvaluationCase(
            id="math_003",
            input="10 / 0",
            expected="undefined",
        ),

    ]