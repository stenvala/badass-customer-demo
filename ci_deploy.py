import os
from pathlib import Path
from ci_utils import run, print_lines
import json
import time

START = time.time()

ROOT = Path(__file__).parent.absolute()
CDK = ROOT / "cdk"


def create_env():
    print("python --version")
    print_lines("Create deployment context", True)
    env = json.dumps(
        {
            "stage": os.environ.get("STAGE", "dev").lower(),
            "stackSuffix": os.environ.get("STACK_SUFFIX", "none").lower(),
        },
        indent=2,
    )
    with open(CDK / "env.json", "w") as f:
        f.write(env)
    print_lines(env)


def install_cdk_deps():
    run("npm install", cwd=CDK)


def synth():
    print_lines("Deploy", True)
    # run(f"npx cdk synth --json", cwd=CDK)


def deploy():
    print_lines("Deploy", True)
    hotswap = "--hotswap" if os.environ.get("STAGE", "dev").lower() == "dev" else ""
    run(f"npx cdk deploy {hotswap} --outputs-file ../stack-data.json", cwd=CDK)


def invalidate_cache():
    print_lines("Invalidating cache", True)
    with open(ROOT / "stack-data.json", "r") as f:
        data = json.load(f)
        distribution_id = data[list(data.keys())[0]]["CloudFrontDistribution"]
    run(f'aws cloudfront create-invalidation --distribution-id {distribution_id} --paths "/*"')


if __name__ == "__main__":
    create_env()
    install_cdk_deps()
    synth()
    deploy()

    # invalidate_cache()

    duration = time.time() - START
    print_lines(f"Total duration {duration}")
