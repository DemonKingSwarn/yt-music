from setuptools import setup, find_packages
from yt_music.__version__ import __core__

with open("requirements.txt") as requirements_txt:
    requirements = requirements_txt.read().splitlines()

setup(
    name="yt-music",
    version=__core__,
    author="d3m0n@demonkingswarn",
    author_email="demonkingswarn@protonmail.com",
    description="A command line YouTube Music client",
    packages=find_packages(),
    url="https://github.com/DemonKingSwarn/yt-music",
    keywords=[
        "youtube",
        "youtube music",
        "yt-music"
    ],
    install_requires=requirements,
    entry_points="""
        [console_scripts]
        yt-music=yt_music.__main__:__ytmusic__
    """,
    include_package_data=True,
)
