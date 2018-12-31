import pathlib

import pytest
import pydub

from mp3_to_wav import mp3_to_wav

def test_mp3_to_wav(src_dest):
    """
    Given an mp3 file, it correctly converts it to wav
    """
    mp3_to_wav(src_dest[0], src_dest[1])

    # the following call with raise an exception
    # if the file being read is not encoded as wav
    pydub.AudioSegment.from_wav(src_dest[1])



@pytest.fixture
def src_dest():
    src = 'data/dnc-2004-speech.mp3'
    dest = 'tests/dnc-2004-speech.wav'
    yield  src, dest
    pathlib.Path(dest).unlink()

