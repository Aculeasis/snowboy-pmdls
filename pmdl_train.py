# -*- coding: utf-8 -*-

import os
import tempfile
from io import BytesIO

from scipy.io import wavfile

from pmdl.snowboy import SnowboyPersonalEnroll, SnowboyTemplateCut

ENROLL_ERRORS = {
    -1: 'Error initializing streams or reading audio data',
    1: 'Hotword is too long',
    2: 'Hotword is too short',
}

DEFAULT_LANGUAGE = 'en'
PMDL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pmdl')
LNG_PATH = os.path.join(PMDL_PATH, 'lng')

LANGUAGES = {x.lower(): x for x in os.listdir(LNG_PATH)}


def check_snowboy(cut, enroll):
    data = [
            ['NumChannels', cut.NumChannels(), enroll.NumChannels()],
            ['SampleRate', cut.SampleRate(), enroll.SampleRate()],
            ['BitsPerSample', cut.BitsPerSample(), enroll.BitsPerSample()]
    ]
    for name, x, y in data:
        if x != y:
            raise SamplesException('', '{} in cut and enroll are different: {} != {}'.format(name, x, y))


def get_resource(lang):
    return os.path.join(LNG_PATH, LANGUAGES.get(lang.lower(), DEFAULT_LANGUAGE), 'personal_enroll.res')


def generate(samples, lang=DEFAULT_LANGUAGE):
    resource_filename = get_resource(lang)
    tmp_file = tempfile.NamedTemporaryFile()

    cut = SnowboyTemplateCut(resource_filename=resource_filename.encode())
    enroll = SnowboyPersonalEnroll(resource_filename=resource_filename.encode(), model_filename=tmp_file.name.encode())
    check_snowboy(cut, enroll)

    errors = []
    for sample in samples:
        _, data = wavfile.read(BytesIO(sample))
        data_cut = cut.CutTemplate(data.tobytes())
        enroll_ans = enroll.RunEnrollment(data_cut)
        errors.append(ENROLL_ERRORS.get(enroll_ans))
    if any(errors):
        raise SamplesException(errors, '')

    with open(tmp_file.name) as fd:
        return fd.read()


class SamplesException(Exception):
    def __init__(self, samples, msg):
        self.samples = samples
        super(SamplesException, self).__init__(msg)
