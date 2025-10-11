from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class Device(BaseModel):
    id: int = Field(examples=[1])
    name : str = Field(examples=["Thermostat"])
    serial_number: str = Field(examples=["SN123456"])
    status: str = Field(examples=["active", "inactive"])
    type: str = Field(examples=["temperature", "humidity"])
    module_id: int = Field(examples=[1])
    house_id: int = Field(examples=[101])

class Message(BaseModel):
    message: str

@app.post("/devices",
          response_model=Message,
          tags=["Devices"],
          summary="Create a new device",
          responses={201: {"model": Message, "description": "Device created successfully"},
                     400: {"model": Message, "description": "Bad request"},
                     500: {"model": Message, "description": "Internal server error"}})
def create_device(device: Device):
    return {"message": "Device created successfully"}

@app.get("/devices/{device_id}",
        response_model=Device,
        tags=["Devices"],
        summary="Get device by ID",
        responses={404: {"model": Message, "description": "The device was not found"},
                   500: {"model": Message, "description": "Internal server error"}})
def get_device_by_id(device_id: int):
    if device_id < 0:
        raise HTTPException(status_code=404, detail="Device not found")
    return Device(
        id=device_id,
        name="Thermostat",
        serial_number="SN123456",
        status="active",
        type="temperature",
        module_id=1,
        house_id=101
    )

@app.put("/devices/{device_id}",
         response_model=Message,
         tags=["Devices"],
         summary="Update device by ID",
         responses={400: {"model": Message, "description": "Bad request"},
                    404: {"model": Message, "description": "The device was not found"},
                    500: {"model": Message, "description": "Internal server error"}})
def update_device(device_id: int, device: Device):
    if device_id != device.id:
        raise HTTPException(status_code=400, detail="Device ID mismatch")
    return {"message": "Device updated successfully"}

@app.delete("/devices/{device_id}",
            response_model=Message,
            tags=["Devices"],
            summary="Delete device by ID",
            responses={404: {"model": Message, "description": "The device was not found"},
                       500: {"model": Message, "description": "Internal server error"}})
def delete_device(device_id: int):
    if device_id < 0:
        raise HTTPException(status_code=404, detail="Device not found")
    return {"message": "Device deleted successfully"}

def main():
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)


if __name__ == "__main__":
    main()