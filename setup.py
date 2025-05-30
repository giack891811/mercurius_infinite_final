from setuptools import setup, find_packages

setup(
    name="mercurius-infinite",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=open("requirements.txt").read().splitlines(),
    entry_points={"console_scripts": ["merc-start=start_fullmode:main"]},
    author="Giacomo Germano",
    description="AI evolutiva cosciente stile Jarvis",
)