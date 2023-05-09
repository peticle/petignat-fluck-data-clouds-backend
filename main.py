from fastapi import FastAPI, Request
import uvicorn


app = FastAPI()

PEOPLE = [
    {'name': 'Alice', 'age': 42, 'city': 'London'},
    {'name': 'Bob', 'age': 24, 'city': 'Paris'},
    {'name': 'Charlie', 'age': 18, 'city': 'New York'}
]


@app.get('/people')
async def people(request: Request):
    print('Request for people page received')
    return {'people': PEOPLE}


@app.get('/people/{index}')
async def person(request: Request, index: int):
    print('Request for person page received with index=%d' % index)
    return {'person': PEOPLE[index]}

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000)
