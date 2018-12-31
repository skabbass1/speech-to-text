import pathlib
from pydub import AudioSegment

def mp3_to_wav(src_path, dest_path=None):
    segment = AudioSegment.from_mp3(src_path)
    dest_path = dest_path or src_path
    dest_path = dest_path.replace(pathlib.Path(dest_path).suffix, '.wav')
    segment.export(dest_path, format='wav')

