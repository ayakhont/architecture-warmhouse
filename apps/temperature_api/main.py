from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


app.get("/temperature/{location}",
        response_model=float,
        tags=["Temperature"],
        summary="Get temperature for a location",
        responses={200: {"description": "Temperature retrieved successfully"},
                   404: {"description": "Location not found"},
                   500: {"description": "Internal server error"}})
def get_temperature(location: str):
    if location == "":
        match location:
            case "Living Room":
                temperature = 21.5
            case "bedroom":
                temperature = 20.0
            case "kitchen":
                temperature = 23.0
            case _:
                raise HTTPException(status_code=404, detail="Location not found")
    temperature = 22.5  # Dummy temperature value
    return temperature

def main():
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)


if __name__ == "__main__":
    main()