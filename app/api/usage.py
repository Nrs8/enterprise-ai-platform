"""
Usage analytics API.
"""


from fastapi import APIRouter, Request



router = APIRouter(
    prefix="/usage",
    tags=["usage"],
)



@router.get("")
def get_usage(
    http_request: Request,
):
    """
    Return AI usage statistics.
    """


    container = (
        http_request
        .app
        .state
        .container
    )


    tracker = (
        container
        .usage_tracker
    )


    records = tracker.get_all()


    return {

        "total_requests":
            len(records),


        "total_tokens":
            tracker.total_tokens(),


        "total_cost":
            round(
                tracker.total_cost(),
                6,
            ),


        "records":
            records,

    }