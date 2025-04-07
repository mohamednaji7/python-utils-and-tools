# python-utils-and-tools

This repository contains various Python utilities and tools, including web scraping, data processing, and other helper scripts. The tools are modular and designed to handle specific tasks efficiently.

## Installation

Clone the repository:

```bash
git clone https://github.com/mohamednaji7/python-utils-and-tools.git python-utils-and-tools
```

## Setup

1. Navigate to the project directory:

```bash
cd python-utils-and-tools/src
```

2. Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Tools and Utilities

### Web Scraping

The `web-scrapping` tool is designed for scraping data from websites. It uses Selenium and BeautifulSoup for rendering and extracting content.

#### Run the Web Scraper

```bash
cd web-scrapping
python3 main.py
```

### RAG (Retrieval-Augmented Generation)

The `rag/` directory contains scripts for processing and embedding data for retrieval-augmented generation tasks.

#### Example Usage

- **Combine JSON files:**

  Combines multiple JSON files into a single deduplicated file.

  ```bash
  python3 rag/combine-json.py
  ```

- **Embed Metadata:**

  Generates embeddings for text data and stores metadata.

  ```bash
  python3 rag/embed.py
  ```

- **Upload Records:**

  Uploads records to a vector database for retrieval tasks.

  ```bash
  python3 rag/upload_records.py
  ```

### Utilities

The `utils/` directory contains helper scripts for file operations, logging, and time estimation.

#### Example Usage

- **File Processor:**

  Handles file operations like loading and saving JSON files.

  ```bash
  python3 utils/file_processor.py
  ```

- **Logger:**

  Provides rich logging capabilities for debugging and monitoring.

  ```bash
  python3 utils/logger.py
  ```

- **Time Estimator:**

  Estimates the time required for iterative tasks.

  ```bash
  python3 utils/time_estimator.py
  ```

## Data

The `rag_data/` directory contains input and output data for the RAG tools. Ensure that the required input files are present before running the scripts.

- **Input Data:** Located in `rag_data/input/`.
- **Output Data:** Results are saved in `rag_data/output/`.

## Notes

- Follow the `.gitignore` rules to avoid committing unnecessary files (e.g., `__pycache__/`, `*.pyc`, `venv/`, etc.).
- Backup your data files before running scripts that modify them.
- Ensure all environment variables are set correctly for scripts requiring API keys or database connections.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.