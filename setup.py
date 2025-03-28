from setuptools import setup, find_packages

setup(
    name="optimiist",
    version="0.1.0",
    packages=find_packages(exclude=['evaluation', 'evaluation.*']),
    include_package_data=True,
    install_requires=[
        "pandas",
        "pm4py",
        "pulp",
        "numpy",
        "click",
        "rich",
    ],
    entry_points={
        "console_scripts": [
            "optimiist=optimiist.cli:main",
        ],
    },
    python_requires=">=3.6",
    description="OptIMIIst process mining algorithm",
    author="Calvin Schröder",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
    ],
)
