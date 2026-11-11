from pathlib import Path

CWD = Path(__file__).parent


def fixture_path(fixture: str) -> Path:
    return Path(CWD).joinpath(fixture)
