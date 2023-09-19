from pathlib import Path

GITHUB_ASSETS_NAMES = [f'yolov8{k}{suffix}.pt' for k in 'nsmlx' for suffix in ('', '6', '-cls', '-seg', '-pose')]

GITHUB_ASSETS_STEMS = [Path(k).stem for k in GITHUB_ASSETS_NAMES]
