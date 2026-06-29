
# Run's the requirements.txt file
# find's all packages from Machine_Learning_MLOPS_Project (FOLDER)

from setuptools import setup, find_packages

with open("requirements.txt") as file:
    requirements = file.read().splitlines()

setup(
    name="CC_MLOPS_PROJECT_1",
    version="0.0.1",
    author="Aparna",
    packages=find_packages(),
    install_requires=requirements,
)
