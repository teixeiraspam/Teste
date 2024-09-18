

from fastapi import FastAPI
from pydantic import BaseModel
import matplotlib.pyplot as plt
import yaml
from typing import List, Tuple
from fastapi.responses import StreamingResponse
import io



# Load all documents from the YAML file
with open(r'//SRVDABU02/Benutzerordner$/sofia.teixeira/Desktop/Projects/PythonProjects/Neu_Machine/BOM_test_draw.yaml') as file:
    BOM = yaml.safe_load(file)

shape_input = BOM.get("module-parameters", {}).get("shape", {}).get("shape-input", [])
shape_coordinates = [complex(num) for num in shape_input]

# Extract real and imaginary parts
real_parts = [num.real for num in shape_coordinates]
real_parts.append(real_parts[0])
imag_parts = [num.imag for num in shape_coordinates]
imag_parts.append(imag_parts[0])


################################################################     WORKING API !!!   ##############################################################################################


app = FastAPI()

class Point(BaseModel):
    real: float
    imag: float

class Points(BaseModel):
    points: List[Point]

@app.post("/plot")

async def draw_vectors(data: Points):

    plt.clf()  # Makes the plot always updated/Clear the current figure
    points = [(point.real, point.imag) for point in data.points]
    for point in points:
        plt.plot(point[0], point[1], 'ro')  # 'ro' for red dots
    plt.plot(real_parts, imag_parts, 'b-')  # 'b-' for blue lines
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")

# Example usage
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

def draw_vectors(data: Points):
    points = [(point.real, point.imag) for point in data.points]
    for point in points:
        plt.plot(point[0], point[1], 'ro')  # 'ro' for red dots
    plt.show()



# Example usage
points = [Point(real=0, imag=0), Point(real=0, imag=3), Point(real=3, imag=0), Point(real=3, imag=4)]


draw_vectors(Points(points=points))

# app.run() # começa a app e deixa a API no ar






"""
This API works in postman with the following JSON example:


{
    "points": [
        {"real": 0, "imag": 0},
        {"real": 50, "imag": 200},
        {"real": 310, "imag": 0},
        {"real": 0, "imag": -426}
    ]
}

""" 