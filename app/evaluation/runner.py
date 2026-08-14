from app.evaluation.models import EvaluationResult

from app.evaluation.evaluator import Evaluator
from app.evaluation.report import EvaluationReporter


class EvaluationRunner:


    def __init__(

        self,

        runtime,

        session_manager,

    ):


        self.runtime = runtime

        self.session_manager = session_manager

        self.evaluator = Evaluator()
        self.reporter = EvaluationReporter()



    async def run(

        self,

        cases,

    ):


        results = []


        for case in cases:


            session = (
                self.session_manager
                .create_session()
            )


            response = await self.runtime.chat(

                session_id=session.session_id,

                message=case.input,

            )


            score = self.evaluator.evaluate(

                case,

                response,

            )


            results.append(

                EvaluationResult(

                    case_id=case.id,

                    input=case.input,

                    expected=case.expected,

                    response=response,

                    score=score,

                )

            )


        return results