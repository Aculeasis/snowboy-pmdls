# -*- coding: utf-8 -*-

import base64
import json

from flask import Flask, request, make_response

from pmdl_train import SamplesException, generate

app = Flask(__name__, static_url_path='')


@app.route('/api/v1/train/', methods=['POST'])
@app.route('/api/v1/train', methods=['POST'])
@app.route('/', methods=['POST'])
def train():
    try:
        data = json.loads(request.data)
    except Exception as e:
        return make_response('Wrong request: {}'.format(e), 400)
    if 'voice_samples' not in data:
        return make_response('Missing key: voice_samples', 400)

    language, data = data.get('language', 'en'), data['voice_samples']
    if not isinstance(data, list) or len(data) != 3:
        return make_response('voice_samples must be list and contain 3 samples', 400)

    try:
        return _train(data, language)
    except SamplesException as e:
        return make_sample_exception(e)


def _train(data, language):
    errors, samples = [], []
    for sample in data:
        try:
            samples.append(base64.b64decode(sample['wave']))
            errors.append(None)
        except Exception as e:
            errors.append(str(e))
    if any(errors):
        raise SamplesException(errors, '')
    return generate(samples, language)


def make_sample_exception(e):
    # {"voice_samples":[{"wave":["Hotword is too short"]},{"wave":["Hotword is too short"]},{"wave":["Hotword is too short"]}]}
    # {"voice_samples":[{},{"wave":["Hotword is too long"]},{}]}
    if not e.samples:
        return make_response(e, 400)
    return make_response(json.dumps({'voice_samples': [{'wave': [x]} if x else {} for x in e.samples]}), 400)


if __name__ == "__main__":
     http://130.61.61.97/:8888/api/v1/train/
    app.run(host='0.0.0.0', port=8888, threaded=False)
