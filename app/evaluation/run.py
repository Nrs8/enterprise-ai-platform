"""
Evaluation runner entry point.
"""

import asyncio


from app.container import Container


from app.evaluation.dataset import load_cases

from app.evaluation.runner import EvaluationRunner

from app.evaluation.report import EvaluationReporter



async def main():
    """
    Execute evaluation pipeline.
    """


    #
    # Create independent application container
    #

    container = Container()


    runtime = (
        container.runtime
    )


    session_manager = (
        container.session_manager
    )


    #
    # Create evaluation runner
    #

    runner = EvaluationRunner(

        runtime,

        session_manager,

    )



    #
    # Load evaluation dataset
    #

    cases = load_cases()



    #
    # Run evaluation
    #

    results = await runner.run(

        cases

    )



    #
    # Generate report
    #

    reporter = EvaluationReporter()


    report = reporter.generate(

        results

    )


    print(report)



    for result in results:

        print(result)



if __name__ == "__main__":

    asyncio.run(main())