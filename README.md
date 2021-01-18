[snowboy-pmdls](https://github.com/Aculeasis/snowboy-pmdls)
============
[![Docker Pulls](https://img.shields.io/docker/pulls/aculeasis/snowboy-pmdls.svg)](https://hub.docker.com/r/aculeasis/snowboy-pmdls/)

[Snowboy own personal models trainer](https://github.com/seasalt-ai/snowboy) in Docker container.

### Usage

Install `docker run -d -p 8888:8888 aculeasis/snowboy-pmdls` and change snowboy's URL to IP in training code.

[Example](https://github.com/seasalt-ai/snowboy/blob/master/examples/REST_API/training_service.py#L13) for localhost:
```diff
def get_wave(fname):
    with open(fname) as infile:
        return base64.b64encode(infile.read())


- endpoint = "https://snowboy.kitt.ai/api/v1/train/"
+ endpoint = "http://127.0.0.1:8888/api/v1/train/"

############# MODIFY THE FOLLOWING #############
```

The API looks like a [snowboy API](http://docs.kitt.ai/snowboy/#api-v1-train), but all keys excluding `voice_samples` and `language` will be ignored.
