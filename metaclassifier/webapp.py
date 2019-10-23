from flask import Flask, send_file, jsonify, request, send_from_directory
from .Swapper import Swapper
from path import Path
from flask_cors import CORS

path = Path(__file__).parent
app = Flask(__name__, static_url_path='/assets')
CORS(app)

@app.route('/static/<path:filename>')
def assets(filename):
  # Add custom handling here.
  # Send a file download response.
  print(filename)
  return send_from_directory((path/'webdata').name, filename)

swapper: Swapper
@app.route('/')
def index():
    return send_file((path/'webdata'/'index.html'))


@app.route('/config')
def get_config():
    return jsonify({'options': swapper.options})

@app.route('/sample', methods=['POST'])
def solve_sample():
    sample = request.json
    if sample['hash']:
        swapper.samples[sample['hash']].save(sample['ans'])
        return jsonify({'status': 'ok'})

    return jsonify({'status': 'failed'})

@app.route('/sample')
def eval_samples():
    if not swapper.samples:
        return jsonify({'text': 'se acabó', 'id': '', 'additional_data': {}})
    return  jsonify(swapper.get_sample().to_dict())

def run_web(sp: Swapper, **kwargs):
        global swapper
        swapper = sp
        app.run(host='0.0.0.0', port='8080')