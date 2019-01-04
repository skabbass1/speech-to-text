from dataclasses import dataclass

import pytest

import auth

def test_gcloud_cli_path(monkeypatch):
    """
    it raises AuthorizationException if gcloud cli not in found in $PATH
    """
    monkeypatch.setattr(auth, '_GC_EXE', 'does-not-exist')
    with pytest.raises(auth.AuthorizationException) as excinfo:
        auth._gcloud_cli_path()

    assert 'gcloud cli not found in path' in str(excinfo.value)

def test_get_auth_token(monkeypatch):
    """
    it returns the authorization token string
    """
    import subprocess

    @dataclass
    class MockCompletedProcess:
        returncode: int
        stdout: bytes
        stderr: bytes

    monkeypatch.setattr(
            subprocess,
            'run',
            lambda args, capture_output: MockCompletedProcess(0, b'gdstwe7354', b'')
            )
    token = auth.get_auth_token()
    assert token =='gdstwe7354'

def test_get_auth_token_raises(monkeypatch):
    """
    it raises AuthorizationException if authorization fails
    """
    import subprocess

    @dataclass
    class MockCompletedProcess:
        returncode: int
        stdout: bytes
        stderr: bytes

    monkeypatch.setattr(
            subprocess,
            'run',
            lambda args, capture_output: MockCompletedProcess(1, b'', b'failed to authenticate')
            )
    with pytest.raises(auth.AuthorizationException) as excinfo:
        auth.get_auth_token()

    assert 'failed to authenticate' in str(excinfo.value)

