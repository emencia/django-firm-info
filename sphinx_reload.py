#!/usr/bin/env python
"""
Basic script to launch a livereload server to watch and rebuild documentation
on "docs/" file changes.

Once launched, server will be available on port 8002, like: ::

    http://localhost:8002/

Borrowed from: ::

    https://livereload.readthedocs.io/en/latest/#script-example-sphinx

"""
from livereload import Server, shell


server = Server()

# Watch root documents
server.watch(
    "README.rst",
    shell(
        "make html",
        cwd="docs"
    )
)
server.watch(
    "docs/*.rst",
    shell(
        "make html",
        cwd="docs"
    )
)
server.watch(
    "docs/*/**.rst",
    shell(
        "make html",
        cwd="docs"
    )
)

# Watch Python modules for autodoc review
server.watch(
    "firm_info/*.py",
    shell(
        "make html",
        cwd="docs"
    )
)
server.watch(
    "firm_info/*/**.py",
    shell(
        "make html",
        cwd="docs"
    )
)

# Serve built documentation
server.serve(
    root="docs/_build/html",
    port=8002,
    host="0.0.0.0",
)
