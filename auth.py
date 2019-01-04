import subprocess
import shutil

_GC_EXE = 'gcloud'
_GC_EXE_ARGS = ['auth', 'application-default', 'print-access-token']

class AuthorizationException(Exception):
    pass

def get_auth_token():
    return _authenticate_with_gcloud()

def _authenticate_with_gcloud():
    path = _gcloud_cli_path()
    out = subprocess.run([_GC_EXE] + _GC_EXE_ARGS, capture_output=True )
    if out.returncode !=0:
        raise AuthorizationException(out.stderr.decode('utf-8'))
    return out.stdout.decode('utf-8').strip()

def _gcloud_cli_path():
    path = shutil.which(_GC_EXE)
    if path is None:
        raise AuthorizationException('''
                gcloud cli not found in path. gcloud cli is required to get authentication token
                ''')
    return path


