from fastapi import APIRouter, status

router = APIRouter(prefix="/temperature", tags=["Temperature"])


@router.post(
    "/today",
    status_code=status.HTTP_200_OK,
    summary="Get ",
)
async def todays_temperature():
    return {"message": "Ok"}
