from fastapi import APIRouter, status

router = APIRouter(prefix="/weather", tags=["Temperature"])


@router.post(
    "/today",
    status_code=status.HTTP_200_OK,
    summary="Get ",
)
async def todays_temperature():
    return {"message": "Ok"}

@router.get("/today", response_model=URLListResponse, summary="Get all URLs for current user")
async def todays_temperature(
    request: Request,
    current_user: Annotated[UserResponse, Depends(get_current_active_user)],
    url_service: Annotated[URLService, Depends(get_url_service)],
    url_filter: URLFilter = FilterDepends(URLFilter),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
) -> URLListResponse:
    """
    Get all shortened URLs created by the current user with pagination.

    - **page**: Page number (starts from 1)
    - **page_size**: Number of items per page (1-100)
    """
    urls, total = await url_service.get_user_urls(
        current_user.id, page, page_size, url_filter
    )

    url_responses = [
        URLResponse(
            id=url.id,
            original_url=url.original_url,
            short_code=url.short_code,
            short_url=build_short_url(request, url.short_code),
            title=url.title,
            clicks=url.clicks,
            is_active=url.is_active,
            created_at=url.created_at,
            user_id=url.user_id,
        )
        for url in urls
    ]

    return URLListResponse(
        urls=url_responses,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=ceil(total / page_size) if total > 0 else 0,
    )
