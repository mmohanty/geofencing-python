import json
from fastapi import FastAPI
import uvicorn
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

map = dict()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

@app.on_event("startup")
async def setup_feature():
    # Opening JSON file
    f = open('us-states.json')

    # returns JSON object as
    # a dictionary
    data = json.load(f)

    # Iterating through the json
    # list
    for feature in data['features']:
        map.__setitem__(feature['id'], feature['geometry'])

    # Closing file
    f.close()

@app.get("/test/{feature_id}")
async def read_root(feature_id: str):
    return {"Hello": map.get(feature_id)}


@app.get("/states/{accountNumber}")
async def get_states(accountNumber: str):
    print(accountNumber)
    if(accountNumber == '103245'):
        return JSONResponse({"states": [{'state_name': 'Alabama', 'id': '01'}]})
    if(accountNumber == '103545'):
        return JSONResponse({"states": [{'state_name': 'Puerto Rico', 'id': '72'}]})
    if (accountNumber == '104245'):
        return JSONResponse({"states": [{'state_name': 'West Virginia', 'id': '54'}]})

@app.get("/accounts")
async def get_states():
    return JSONResponse({"accounts": ['100023', '100024']})

class State(BaseModel):
    account_number: str
    state_map: dict

@app.post("/states")
async def update_states(states: State):
    print(states)
    return JSONResponse({"accounts": ['100023', '100024']})

if __name__ == "__main__":
   uvicorn.run(app, host="127.0.0.1", port=8090)


