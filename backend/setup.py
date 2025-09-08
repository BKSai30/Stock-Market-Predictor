from setuptools import setup, find_packages

setup(
    name="stock-market-predictor",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "flask>=3.0.3",
        "flask-cors>=4.0.1",
        "pandas>=2.1.0",
        "numpy>=1.26.0",
        "yfinance>=0.2.25",
        "scikit-learn>=1.4.0",
        "matplotlib>=3.8.0",
        "plotly>=5.17.0",
        "requests>=2.31.0"
    ],
    python_requires=">=3.9",
)
