from invoke import task


@task
def coverage(ctx):
    ctx.run("coverage run --branch -m pytest src", pty=True)
    ctx.run("coverage report -m", pty=True)
    ctx.run("coverage html", pty=True)


@task
def test(ctx):
    ctx.run("pytest src", pty=True)


@task
def lint(ctx):
    ctx.run("pylint src", pty=True)


@task
def backend(ctx):
    ctx.run("source venv/bin/activate && python3 src/main.py", pty=True)


@task
def frontend(ctx):
    with ctx.cd("src/ui"):
        ctx.run("npm start", pty=True)
