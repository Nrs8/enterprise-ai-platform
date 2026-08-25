"""
Evaluation report generation.
"""

from __future__ import annotations


import json

from pathlib import Path
from dataclasses import asdict


from app.evaluation.models import (
    EvaluationReport,
    EvaluationResult,
)





class EvaluationReporter:
    """
    Generates evaluation reports.
    """



    def __init__(
        self,
        output_dir: str = "app/evaluation/reports",
    ) -> None:


        self.output_dir = Path(
            output_dir
        )

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )




    def generate(
        self,
        results: list[EvaluationResult],
    ) -> EvaluationReport:
        """
        Generate evaluation summary.
        """


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





    def save(
        self,
        report: EvaluationReport,
        results: list[EvaluationResult],
        filename: str = "evaluation_report.json",
    ) -> Path:
        """
        Save evaluation report as JSON.
        """


        output_file = (

            self.output_dir

            /

            filename

        )


        payload = {


            "report":

                asdict(report),



            "results":

                [

                    asdict(result)

                    for result in results

                ],

        }



        with output_file.open(
            "w",
            encoding="utf-8",
        ) as file:


            json.dump(

                payload,

                file,

                indent=4,

                ensure_ascii=False,

            )



        return output_file