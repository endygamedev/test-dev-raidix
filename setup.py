from setuptools import setup, find_packages


setup (
    name="tcpchat",
    version="1.0.0",
    author="Egor Bronnikov",
    author_email="bronnikov.40@mail.ru",
    description="Simple TCP chat app for test task to the RAIDIX",
    license="MIT",
    url="https://github.com/endygamedev/test-dev-raidix",
    packages=find_packages(include="src*"),
    python_requirements=">=3.8",
    entry_points={
        "console_scripts": [
            "tcpchat = src.app:main"
        ]
    }
)