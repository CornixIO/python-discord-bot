import json
from os import path

from setuptools import setup

here = path.abspath(path.dirname(__file__))
root = path.dirname(here)

readme = path.join(here, 'README.md')
package_json = path.join(here, 'package.json')

with open(readme, "r") as fh:
    long_description = fh.read()

with open(package_json, encoding='utf-8') as f:
    package = json.load(f)

setup(
    name=package['name'],
    author=package['author']['name'],
    author_email=package['author']['email'],
    version=package['version'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=package['homepage'],
    packages=['discord_bot', 'discord_bot.models', 'discord_bot.common', 'discord_bot.apis'],
    python_requires=">=3.6",
    include_package_data=True,
    exclude=("__pycache__",),
    install_requires=["requests==2.31.0"],
)
