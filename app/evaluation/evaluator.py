from app.evaluation.models import EvaluationCase



class Evaluator:



    def evaluate(

        self,

        case: EvaluationCase,

        response: str,

    ) -> float:


        if case.expected.lower() in response.lower():

            return 1.0


        return 0.0