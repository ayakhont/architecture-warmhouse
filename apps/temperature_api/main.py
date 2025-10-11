import random
from typing import Optional

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


app.get("/health", tags=["Health"], summary="Health check endpoint")
def health_check():
    return {"status": "ok"}


@app.get("/temperature")
@app.get("/temperature/{sensor_id}")
def get_temperature(
    sensor_id: Optional[str] = None,
    location: str = Query(default="", description="Название комнаты"),
) :
    if sensor_id:
        match sensor_id:
            case "1":
                location = "Living Room"
            case "2":
                location = "Bedroom"
            case "3":
                location = "Kitchen"
            case _:
                location = "Unknown"
    else:
        match location:
            case "Living Room":
                sensor_id = "1"
            case "Bedroom":
                sensor_id = "2"
            case "Kitchen":
                sensor_id = "3"
            case _:
                sensor_id = "0"
    temperature = round(random.uniform(15.0, 30.0), 2)

    return {"value":temperature, "sensorId": sensor_id, "location": location}

def main():
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)


if __name__ == "__main__":
    main()