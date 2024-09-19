from enum import Enum

from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from http import HTTPStatus


class ModelName(str, Enum):
    navigation = "navigation"
    communications = "communications"
    life_support = "life_support"
    engines = "engines"
    deflector_shield = "deflector_shield"


app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key="supersecretkey")


@app.get("/status")
async def status(request: Request, system: ModelName):
    damaged_system = system

    request.session["damaged_system"] = damaged_system

    return {"damaged_system": damaged_system + " idenfied, please wait for help."}


@app.get("/repair-bay", response_class=HTMLResponse)
async def repair_bay(request: Request):
    damaged_system = request.session.get("damaged_system")

    if not damaged_system:
        return "Please refer to our Status service to assess your requirements."

    system_codes = {
        "navigation": "NAV-01",
        "communications": "COM-02",
        "life_support": "LIFE-03",
        "engines": "ENG-04",
        "deflector_shield": "SHLD-05",
    }

    code = system_codes.get(damaged_system, "UNKNOWN")

    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Repair</title>
    </head>
    <body>
    <div class="anchor-point">{code}</div>
    </body>
    </html>
    """

    return HTMLResponse(content=html_template)


@app.post("/teapot")
async def teapot_endpoint():
    return Response(status_code=HTTPStatus.IM_A_TEAPOT)


@app.get("/phase-change-diagram/")
def get_specific_volumes(pressure: float):

    critical_pressure = 10.0  # MPa
    critical_temperature = 500.0  # °C at 10 MPa
    specific_volume_liquid_critical = 0.0035  # m³/kg
    specific_volume_vapor_critical = 0.0035  # m³/kg

    normal_pressure = 0.05  # MPa
    normal_temperature = 30.0  # °C
    specific_volume_liquid_normal = 0.00105  # m³/kg
    specific_volume_vapor_normal = 30.0  # m³/kg

    def linear_interpolate(x, x1, y1, x2, y2):
        return y1 + (y2 - y1) * (x - x1) / (x2 - x1)

    if pressure < normal_pressure:
        temperature = normal_temperature
    elif pressure > critical_pressure:
        temperature = critical_temperature
    else:
        temperature = linear_interpolate(
            pressure,
            normal_pressure,
            normal_temperature,
            critical_pressure,
            critical_temperature,
        )

    if pressure < normal_pressure:
        specific_volume_liquid = specific_volume_liquid_normal
    elif pressure > critical_pressure:
        specific_volume_liquid = specific_volume_liquid_critical
    else:
        specific_volume_liquid = linear_interpolate(
            pressure,
            normal_pressure,
            specific_volume_liquid_normal,
            critical_pressure,
            specific_volume_liquid_critical,
        )

    if pressure < normal_pressure:
        specific_volume_vapor = specific_volume_vapor_normal
    elif pressure > critical_pressure:
        specific_volume_vapor = specific_volume_vapor_critical
    else:
        specific_volume_vapor = linear_interpolate(
            pressure,
            normal_pressure,
            specific_volume_vapor_normal,
            critical_pressure,
            specific_volume_vapor_critical,
        )

    alert_wall_e = temperature > 30.0
    wall_e_message = (
        "Alert Wall-E! Temperature is above 30°C. Hurry!"
        if alert_wall_e
        else "Temperature is safe, don't worry Wall-E."
    )

    return {
        "specific_volume_liquid": specific_volume_liquid,
        "specific_volume_vapor": specific_volume_vapor,
        "temperature": temperature,
        "wall_e_alert": alert_wall_e,
        "message": wall_e_message,
    }
