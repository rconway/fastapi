from fastapi import FastAPI, Response, status
from pydantic import BaseModel


class RequestedBucket(BaseModel):
    bucketName: str
    secretName: str | None = None
    secretNamespace: str | None = None


class CreatedBucket(BaseModel):
    bucketname: str
    access_key: str
    access_secret: str
    projectid: str


app = FastAPI()


@app.post("/", status_code=200)
async def create_bucket(requestedBucket: RequestedBucket, response: Response) -> CreatedBucket:
    bucket = {
        "bucketname": requestedBucket.bucketName,
        "access_key": "123",
        "access_secret": "456",
        "projectid": "789",
    }
    response.status_code = status.HTTP_200_OK
    return CreatedBucket(**bucket)
