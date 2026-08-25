"""
Evaluation execution runner.

Executes evaluation cases
against AgentRuntime.
"""


from __future__ import annotations


from app.evaluation.models import EvaluationResult

from app.evaluation.evaluator import Evaluator
from app.evaluation.report import EvaluationReporter



class EvaluationRunner:
    """
    Runs evaluation cases.

    Responsibilities:

    - Execute cases through AgentRuntime
    - Evaluate responses
    - Produce evaluation results

    Does not manage:

    - Agent lifecycle
    - Memory lifecycle
    - LLM execution
    - Tool execution
    """


    def __init__(

        self,

        runtime,

    ) -> None:


        self.runtime = runtime

        self.evaluator = Evaluator()

        self.reporter = EvaluationReporter()



    async def run(

        self,

        cases,

    ) -> list[EvaluationResult]:
        """
        Execute evaluation cases.
        """


        results: list[EvaluationResult] = []


        for case in cases:


            response = await self.runtime.chat(

                session_id=case.id,

                message=case.input,

                user_id="evaluation_user",

                tenant_id="evaluation",

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