from pathlib import Path
import os
from ci_utils import run, print_lines
import argparse
import time
import sys

START = time.time()

ROOT = Path(__file__).parent.absolute()
BUILD_TARGET = ROOT / "output"
API = "api"


def create_build_target():
    if os.path.isdir(BUILD_TARGET):
        run(f"rm -rf {BUILD_TARGET}", cwd=ROOT)
    Path(BUILD_TARGET).mkdir(parents=True, exist_ok=True)


def copy_common_files():
    files = ["ci_deploy.py", "ci_utils.py", "deployspec.yml"]
    for i in files:
        run(f"cp {ROOT / i} {BUILD_TARGET}")


def copy_lambda_files(dir: str):
    print_lines(f"Copying {dir}", True)
    src = ROOT / "src"
    target = BUILD_TARGET / dir
    Path(target).mkdir(parents=True, exist_ok=True)
    folders_to_copy = [dir]
    for i in folders_to_copy:
        run(f"cp -r {src / i} {target}", cwd=ROOT)
    run(f'cp {src}/"aws_{dir}.py" {target / "main.py"}')
    run(f'cp {src / "Dockerfile"} { target / "Dockerfile"}')
    run(f'mv {target / dir / "requirements.txt"} { target / "requirements.txt"}')
    run(f'rm {target / dir / "requirements.in"}')


def copy_cdk():
    print_lines("Copying CDK", True)
    src = ROOT / "cdk"
    target = BUILD_TARGET / "cdk"
    Path(target).mkdir(parents=True, exist_ok=True)
    for i in os.listdir(src):
        if "node_modules" in i:
            continue
        run(f"cp -r {src / i} {target}")


def build_lambda(dir: str, use_docker: bool):
    print_lines(f"Building {dir}", True)
    dir = BUILD_TARGET / dir
    if use_docker:
        print_lines("Using docker", True)
        run(f"DOCKER_BUILDKIT=1 docker build --file Dockerfile --output . .", cwd=dir)
    else:
        run(f"pip install -r {dir}/requirements.txt -t .", cwd=dir)
    # To global to run tests
    run(f"pip install -r {dir}/requirements.txt", cwd=dir)
    to_remove = ["*.dist-info", "__pycache__", ".pytest_cache"]
    for i in to_remove:
        run(f"rm -rf {i}", cwd=dir)
    run(f"rm -rf Dockerfile", cwd=dir)
    run(f"rm -rf requirements.txt", cwd=dir)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--docker", action="store_true")
    args = ap.parse_args()

    #sys.exit(1)
    create_build_target()
    copy_common_files()
    copy_lambda_files(API)
    copy_cdk()
    build_lambda(API, args.docker)

    run(f"du -sh {BUILD_TARGET}/*", cwd=ROOT)

    print_lines("Build ready", True)
    duration = time.time() - START
    print_lines(f"Total duration {duration}")
