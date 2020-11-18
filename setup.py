import setuptools

#with open("README.md","r") as f:
#    long_description = f.read()

setuptools.setup(
    name="BirdJumpExtreme",
    version="0.0.1",
    author="Philipp Rados",
    author_email="phil.rados@gmail.com",
    description="A fun platform-jumping game for your terminal",
    #long_description=long_description,
    #long_description_content="text/markdown",
    url="https://github.com/PhilippRados/BirdJumpExtreme",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)