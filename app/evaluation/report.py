from app.evaluation.models import (
    EvaluationReport,
    EvaluationResult,
)


class EvaluationReporter:


    def generate(
        self,
        results: list[EvaluationResult],
    ) -> EvaluationReport:


        total = len(results)


        passed = sum(
            1
            for result in results
            if result.score == 1.0
        )


        failed = total - passed


        accuracy = (
            passed / total
            if total > 0
            else 0.0
        )


        return EvaluationReport(
            total_cases=total,
            passed_cases=passed,
            failed_cases=failed,
            accuracy=accuracy,
        )