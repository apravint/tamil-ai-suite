from setuptools import setup, find_packages

setup(
    name="tamil-ai-suite",
    version="1.0.0",
    description="Comprehensive Tamil AI & NLP Toolkit: Transliteration, Sentiment Analysis, Prompt Engineering & TTS Bridge for Termux & Linux",
    author="Pravin Tamilan (@apravint)",
    author_email="apravint@users.noreply.github.com",
    packages=find_packages(),
    install_requires=[
        "rich>=13.0.0",
        "requests>=2.28.0",
    ],
    entry_points={
        "console_scripts": [
            "tamilai = tamilai.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Text Processing :: Linguistic",
    ],
    python_requires=">=3.8",
)
