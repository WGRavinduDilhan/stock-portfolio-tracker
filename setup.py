from setuptools import setup, find_packages

setup(
    name="stock-portfolio-tracker",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "streamlit",
        "yfinance",
        "pandas",
        "numpy",
        "plotly",
        "python-dotenv",
        "pytest",
    ],
)