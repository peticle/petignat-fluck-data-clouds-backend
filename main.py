"""Add routes for the application."""
import requests

import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.exceptions import HTTPException
from pydantic import BaseModel


app = FastAPI()

SD_ADDR = "10.0.0.5"
SD_PORT = "7860"
SD_URL = f"https://{SD_ADDR}:{SD_PORT}/sdapi/v1/txt2img/"


class StablePayload(BaseModel):
    """Represents a payload to generate an image with Stable Diffusion.

    Attributes:
        text: The prompt text used to generate an image.
        steps: The number of steps used to generate the image.
    """
    prompt: str
    steps: int


PEOPLE = [
    {'name': 'Alice', 'age': 42, 'city': 'London'},
    {'name': 'Bob', 'age': 24, 'city': 'Paris'},
    {'name': 'Charlie', 'age': 18, 'city': 'New York'}
]


@app.get('/people')
async def people(request: Request):
    print('Request for people page received')
    return {'people': PEOPLE}


@app.post('/imgen')
async def stable_diffusion(payload: StablePayload):
    """A route to generate an image with Stable Diffusion."""
    # Send the request to the Stable Diffusion instance
    PAYLOAD = payload.dict()
    response = requests.post(url=SD_URL, json=PAYLOAD)

    # Check if we received a response from Stable Diffusion
    if response.status_code != 200:
        raise HTTPException(
            status_code=500,
            detail="Could not contact Stable Diffusion",
        )

    # Return the generated image in base64
    r = response.json()
    return Response(r["images"][0])

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000)
