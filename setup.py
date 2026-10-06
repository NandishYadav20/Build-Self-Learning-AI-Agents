from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="self-learning-ai-agents",
    version="1.0.0",
    author="Nandish Yadav",
    author_email="nandishmalout1481@gmail.com",
    description="A production-ready framework for building self-learning AI agents with memory, retrieval, and agentic patterns",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/Build-Self-Learning-AI-Agents",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.9",
    install_requires=[
        "openai>=1.0.0",
        "pydantic>=2.0.0",
        "python-dotenv>=1.0.0",
        "mem0ai>=0.0.1",
        "qdrant-client>=2.7.0",
        "tenacity>=8.2.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
    },
)
