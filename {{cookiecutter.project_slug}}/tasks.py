#!/usr/bin env python
"""Project automation code using Invoke.py as replacement for `make`."""

import os
import webbrowser
from urllib.request import pathname2url
from pathlib import Path

from logzero import logger as log

from invoke import task
from invoke.exceptions import UnexpectedExit

PROJECT_ROOT = str(Path(__file__).parent)
HOME = Path(os.environ["HOME"])

try:
    MY_CONDA_ROOT = os.environ["MY_CONDA_ROOT"]
except KeyError:
    MY_CONDA_ROOT = list(HOME.glob("*naconda*/"))[0]

PACKAGE_NAME = "{{ cookiecutter.project_slug }}"
CONDA_ENV_NAME = "{{ cookiecutter.project_slug }}"
SRC_DIR = "{{ cookiecutter.project_slug }}"
SOURCE_CONDA = f"source {MY_CONDA_ROOT}/etc/profile.d/conda.sh"
ACTIVATE = f"{SOURCE_CONDA} && conda activate {CONDA_ENV_NAME}"


def browser(path):
    webbrowser.open("file://" + pathname2url(os.path.abspath(path)))


@task
def clean_build(ctx):
    """Remove build artifacts."""
    with ctx.prefix(ACTIVATE):
        ctx.run("rm -fr build/")
        ctx.run("rm -fr dist/")
        ctx.run("rm -fr .eggs/")
        ctx.run("find . -name '*.egg-info' -exec rm -fr {} +")
        ctx.run("find . -name '*.egg' -exec rm -f {} +")


@task
def clean_pyc(ctx):
    """Remove Python file artifacts."""
    with ctx.prefix(ACTIVATE):
        ctx.run("find . -name '*.pyc' -exec rm -f {} +")
        ctx.run("find . -name '*.pyo' -exec rm -f {} +")
        ctx.run("find . -name '*~' -exec rm -f {} +")
        ctx.run("find . -name '__pycache__' -exec rm -fr {} +")


@task
def clean_test(ctx):
    """Remove test and coverage artifacts."""
    with ctx.prefix(ACTIVATE):
        ctx.run("rm -fr .tox/")
        ctx.run("rm -f .coverage")
        ctx.run("rm -fr htmlcov/")


@task
def clean_docs(ctx):
    """Remove docs artifacts."""
    with ctx.prefix(ACTIVATE):
        ctx.run("make -C docs clean")


@task
def mypy(ctx):
    """Check typing with mypy."""
    with ctx.prefix(ACTIVATE):
        ctx.run(f"mypy --ignore-missing-imports {PACKAGE_NAME}")


@task(clean_build, clean_pyc, clean_test)
def clean(ctx):
    """Remove all build, test, coverage and Python artifacts."""
    with ctx.prefix(ACTIVATE):
        ctx.run("echo clean")


@task
def lint(ctx):
    """Check style with flake8."""
    with ctx.prefix(ACTIVATE):
        ctx.run(f"flake8 {SRC_DIR}")


@task
def test(ctx):
    """Run tests quickly with the default Python."""
    with ctx.prefix(ACTIVATE):
        ctx.run(f"pytest")


@task
def test_all(ctx):
    """Run tests on every Python version with tox."""
    with ctx.prefix(ACTIVATE):
        ctx.run(f"tox")


@task
def coverage(ctx):
    """Check code coverage quickly with the default Python."""
    with ctx.prefix(ACTIVATE):
        ctx.run(f"coverage run --source {SRC_DIR} -m pytest")
        ctx.run(f"coverage report -m")
        ctx.run(f"coverage html")
        browser(path="htmlcov/index.html")


@task
def docs(ctx):
    """Generate Sphinx HTML documentation, including API docs."""
    with ctx.prefix(ACTIVATE):
        ctx.run(f"rm -f docs/{PACKAGE_NAME}.rst")
        ctx.run(f"rm -f docs/{PACKAGE_NAME}.*.rst")
        # ctx.run(f"rm -f docs/modules.rst")
        ctx.run(f"make -C docs clean")
        ctx.run(f"make -C docs html")
        # browser(path="docs/_build/html/index.html")


@task(docs)
def servedocs(ctx):
    """Compile the docs watching for changes."""
    with ctx.prefix(ACTIVATE):
        ctx.run(f"watchmedo shell-command -p '*.rst' -c 'make -C docs html' -R -D .")


@task(clean)
def release(ctx):
    """Package and upload a release."""
    with ctx.prefix(ACTIVATE):
        ctx.run(f"python setup.py sdist upload")
        ctx.run(f"python setup.py bdist_wheel upload")


@task(clean)
def dist(ctx):
    """Builds source and wheel package."""
    with ctx.prefix(ACTIVATE):
        ctx.run(f"python setup.py sdist")
        ctx.run(f"python setup.py bdist_wheel")
        ctx.run(f"ls -l dist")


@task
def jupyter_notebook(ctx):
    """Serve the jupyter notebook."""
    with ctx.prefix(ACTIVATE):
        ctx.run(f"jupyter notebook --notebook-dir jupyter")


@task
def jupyter_lab(ctx, aws=False):
    """Serve the jupyter lab."""
    with ctx.prefix(ACTIVATE):
        if aws:
            ctx.run(f"jupyter lab --no-browser --port=8888 --notebook-dir jupyter")
        else:
            ctx.run(f"jupyter lab --notebook-dir jupyter")


@task
def install_jupiterlab_extensions(ctx):
    """Installs a set of jupyterlab extensions."""
    with ctx.prefix(ACTIVATE):
        ctx.run(f"jupyter labextension install jupyterlab-toc")


@task
def install_nodejs(ctx):
    log.info("install nodejs with conda")
    ctx.run("conda install nodejs --yes")


@task
def install_conda_env(ctx):
    """Installs virtual environment."""
    try:
        with ctx.prefix(SOURCE_CONDA):
            log.info("install conda environment")
            ctx.run(
                f"conda create -n {CONDA_ENV_NAME} 'python >=3.6' --file requirements.txt --yes"
            )
    except UnexpectedExit as err:
        result = err.args[0]
        if "prefix already exists" in result.stderr:
            log.info("Conda env already exists; moving to next step.")
        else:
            log.error(err)
            raise err


@task(install_conda_env)
def install(ctx):
    """Installs virtual environments and requirements."""
    with ctx.prefix(ACTIVATE):
        log.info("install reqs from conda")
        ctx.run("conda install --file requirements.jupyter.txt --yes")
        ctx.run("conda install --file requirements.dev.txt --yes")

        log.info("install reqs from pip that have no conda pkg")
        ctx.run("pip install -r requirements.pip.txt")
        ctx.run("pip install -r requirements.dev.pip.txt")

        log.info("install this code to allow importing from jupyter notebooks")
        ctx.run("pip install -e .")

        log.info("install this code to allow importing from jupyter notebooks")
        ctx.run(
            f"""python -m ipykernel install --sys-prefix --name {CONDA_ENV_NAME} --display-name "{CONDA_ENV_NAME}" """
        )
        try:
            ctx.run("jupyter labextension install @jupyterlab/toc")
        except Exception as err:
            log.warning(f"Skipped install of jupyterlab-toc: \n{err}")


@task
def uninstall(ctx):
    """Uninstalls virtual environments and requirements."""
    with ctx.prefix(SOURCE_CONDA):
        ctx.run(f"conda remove -n {CONDA_ENV_NAME} --all -y")


@task
def nb_to_html(ctx, nbfile, outdir=None):
    """Convert nbfile to an HTML file with imgs embedded."""
    if outdir is None:
        outdir = "."

    with ctx.prefix(ACTIVATE):
        ctx.run(
            f"""jupyter nbconvert --to html_toc --ExtractOutputPreprocessor.enabled=False {nbfile} --output-dir {outdir}"""
        )
