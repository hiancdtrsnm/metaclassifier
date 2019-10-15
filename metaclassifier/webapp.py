from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
from .Swapper import Swapper
from path import Path
import uvicorn
from starlette.responses import HTMLResponse

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'])

path = Path(__file__).parent
app.mount("/static", StaticFiles(directory=(path/'webdata')), name="static")

swapper: Swapper

@app.get('/')
def index():
    return HTMLResponse(content=(path/'webdata'/'index.html').text())


@app.get('/config')
def get_config():
    return {'options': swapper.options}

@app.post('/sample')
def solve_sample( sample: dict):
    if sample['hash']:
        swapper.samples[sample['hash']].save(sample['ans'])
        return {'status': 'ok'}

    return {'status': 'failed'}

@app.get('/sample')
def eval_samples():
    if not swapper.samples:
        return {'text': 'se acabó', 'id': ''}
    return swapper.get_sample().to_dict()


def run_web(sp: Swapper, **kwargs):
        global swapper
        swapper = sp
        uvicorn.run(app, **kwargs)