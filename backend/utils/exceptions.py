from fastapi import HTTPException, status

habit_not_exists = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="The habit was not found",
)
