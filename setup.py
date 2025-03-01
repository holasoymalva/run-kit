from setuptools import setup, find_packages

setup(
    name="run-kit",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click>=8.1.3",
        "inquirer>=3.1.3",
        "colorama>=0.4.6",
        "jinja2>=3.1.2",
    ],
    entry_points={
        "console_scripts": [
            "run-kit=run_kit.cli:main",
        ],
    },
    python_requires=">=3.9",
    author="RunKit Team",
    author_email="info@runkit.dev",
    description="AI Project Scaffolding Tool for the Modern Developer",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/holasoymalva/run-kit",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords="ai, llm, anthropic, gemini, ollama, streamlit, generator",
    project_urls={
        "Bug Reports": "https://github.com/holasoymalva/run-kit/issues",
        "Source": "https://github.com/holasoymalva/run-kit",
    },
)
