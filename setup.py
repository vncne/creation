from setuptools import setup, find_packages

setup(
    name="ecosystem_sim",
    version="0.1.0",
    packages=find_packages(),
    description="A simple ecosystem simulation with plants, water cycle, and atmospheric conditions.",
    author="System Developer",
    author_email="example@example.com",
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "ecosim=ecosystem_sim.main:main",
        ],
    },
) 