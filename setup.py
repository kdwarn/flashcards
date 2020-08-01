from setuptools import setup, find_packages


setup(
    name="flashcards",
    version="1.1",
    description="Command-line interface for creating and studying flashcards",
    author="Jonathan Lalande, Kris Warner",
    author_email="kdwarn@protonmail.com",
    url="https://github.com/kdwarn/flashcards",
    packages=find_packages(),
    license="MIT",
    python_requires=">=3.7",
    install_requires=["click==7.1"],
    entry_points="""
        [console_scripts]
        flashcards=flashcards.main:cli
    """,
)
