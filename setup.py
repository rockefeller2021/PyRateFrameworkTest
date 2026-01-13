from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
this_directory = Path(__file__).parent
try:
    long_description = (this_directory / "README.md").read_text(encoding="utf-8")
except FileNotFoundError:
    long_description = "PyRate Framework - Automation testing for API and UI inspired by Karate"

setup(
    name="pyrate-framework",  # Unique name for PyPI
    version="1.0.1",
    author="Rafael Enrique Alvarado García",  # TODO: Replace with actual author name
    author_email="magomlg@gmail.com",  # TODO: Replace with actual email
    description="Automation testing framework for API and UI inspired by Karate Framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/pyrate",  # TODO: Replace with actual repo URL
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/pyrate/issues",
        "Documentation": "https://github.com/yourusername/pyrate#readme",
        "Source Code": "https://github.com/yourusername/pyrate",
    },
    packages=find_packages(exclude=["tests*", "build*"]),
    classifiers=[
        # Development status
        "Development Status :: 4 - Beta",
        
        # Intended audience
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        
        # Topic
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Libraries :: Python Modules",
        
        # License
        "License :: OSI Approved :: MIT License",
        
        # Python versions
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        
        # OS
        "Operating System :: OS Independent",
        
        # Framework
        "Framework :: Pytest",
    ],
    keywords="testing automation api ui playwright karate gherkin bdd",
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.28.0",
        "playwright>=1.40.0",
        "colorama>=0.4.6",
        "python-dotenv>=1.0.0",
        "pandas>=2.0.0",
        "openpyxl>=3.1.0",  # For Excel data-driven testing
        "jinja2>=3.1.0",
        "python-docx>=1.0.0",  # For Word evidence generation
        "pyyaml>=6.0",  # For configuration files (future feature)
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
            "black>=23.0",
            "flake8>=6.0",
            "mypy>=1.0",
            "twine>=4.0",
        ],
    },
    entry_points={
        'console_scripts': [
            'pyrate=pyrate.cli:main',
        ],
    },
    include_package_data=True,
    zip_safe=False,
)