"""
Evaluation runner entry point.
"""


from __future__ import annotations


import asyncio

import logging


from app.container import Container


from app.evaluation.dataset import load_cases

from app.evaluation.runner import EvaluationRunner

from app.evaluation.report import EvaluationReporter



logger = logging.getLogger(
    "app.evaluation"
)



async def main() -> None:
    """
    Execute evaluation pipeline.
    """


    #
    # Create application container
    #

    container = Container()


    runtime = (

        container.runtime

    )


    #
    # Create evaluation runner
    #

    runner = EvaluationRunner(

        runtime,

    )


    #
    # Load evaluation dataset
    #

    cases = load_cases()


    logger.info(

        "Loaded evaluation cases: %d",

        len(cases),

    )


    #
    # Run evaluation
    #

    results = await runner.run(

        cases,

    )


    #
    # Generate report
    #

    reporter = EvaluationReporter()


    report = reporter.generate(

        results,

    )

    report_file = reporter.save(

        report,

        results,

    )


    logger.info(

        "Evaluation report: %s",

        report,

    )

    logger.info(

        "Report saved: %s",

        report_file,

    )


    for result in results:


        logger.info(

            "Evaluation result: %s",

            result,

        )



if __name__ == "__main__":


    logging.basicConfig(

        level=logging.INFO,

        format=(

            "%(asctime)s "

            "%(levelname)s "

            "%(name)s "

            "%(message)s"

        ),

    )


    asyncio.run(main())