import httpx
from fastapi import HTTPException, Depends, Request
import os

AUTH_SERVICE_URL = os.getenv('AUTH_SERVICE_URL')
GATEWAY_HOST = os.getenv('GATEWAY_HOST')

async def verify_token_via_auth_service(token: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(AUTH_SERVICE_URL, data={"token": token})
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Invalid token")
        return response.json()

async def verify_user_exists(user_id: int, authorization: str):
    try:
        authorization_header = f"Bearer {authorization}"
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"http://{GATEWAY_HOST}/user/{user_id}",
                headers={"Authorization": authorization_header,
                         "accept": "application/json"}
            )
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="User does not exist")
        elif response.status_code == 401:
            raise HTTPException(status_code=401, detail="Unauthorized: Invalid token")
        elif response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"User service error: {response.text}"
            )
        return response.json()

    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Error connecting to user service: {str(e)}")
