# Python Utils and Tools

A comprehensive collection of Python utilities and tools for various tasks including transcription, RAG (Retrieval-Augmented Generation), web scraping, and general utilities.

## Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/python-utils-and-tools.git
cd python-utils-and-tools

# Install the package
pip install -e .
```

## Quick Overview

### 1. Transcription Module (`pyut.transcribe`)
Transcribe and translate audio/video files using OpenAI's Whisper model.

**Quick Usage:**
```python
from pyut.transcribe import main as transcribe_main

config = {
    "MODEL": "base",
    "GPU": True,
    "FILES": [
        {
            "FILE_PATH": "path/to/your/file.mp4",
            "FILE_LANGUAGE": "en",
            "TRANSLATE": False,
            "TIMESTAMP": True
        }
    ]
}

transcribe_main.convert_to_text(config)
```

### 2. RAG Module (`pyut.rag`)
Process, embed, and manage data for retrieval-augmented generation tasks.

**Quick Usage:**
```python
from pyut.rag import combine_json, embed, upload_records

# Combine JSON files
combine_json.process_files("input_dir", "output.json")

# Generate embeddings
embed.make_metadata("input.json", "metadata.json")
embed.add_embedding("metadata.json", "embeddings.json")

# Upload to vector database
upload_records.supabase_upload_records("embeddings.json", "collection_name")
```

### 3. Web Scraping Module (`pyut.web-scrapping`)
Extract and process data from web sources with JavaScript rendering support.

**Quick Usage:**
```python
from pyut.web_scrapping import WebScraper

scraper = WebScraper(delay=2, number_of_urls_to_scrape=10)
urls = ["https://example.com/page1", "https://example.com/page2"]
scraping_states = [False] * len(urls)
scraper.scrape_urls(urls, scraping_states, subdir="category1")
```

### 4. Utilities Module (`pyut.utils`)
Common utilities for file operations, logging, and time estimation.

**Quick Usage:**
```python
from pyut.utils import TimeEstimator, FileSystemProcessor, logger

# Time estimation
estimator = TimeEstimator(number_of_iterations=100)
estimator.start_iteration()
# Your code here
estimator.update_processing_time()

# File processing
fsp = FileSystemProcessor(root_dir="data")
data = fsp.load_json("input.json")
fsp.save_json("output.json", data, backup=True)

# Logging
logger.info("Processing started")
```

## Dependencies

The project uses several key dependencies:

- `rich`: Terminal formatting and progress bars
- `openai`: OpenAI API integration
- `vecs`: Vector operations
- `tiktoken`: Token counting
- `python-dotenv`: Environment variable management
- `openai-whisper`: Audio transcription
- `python-magic`: File type detection

## Installation

1. **System Requirements:**
   - Python 3.x
   - FFmpeg (for transcription)
   - CUDA-compatible GPU (optional, for faster processing)
   - Chrome browser (for web scraping)

2. **Install the Package:**
   ```bash
   pip install -e .
   ```

3. **Environment Setup:**
   - Copy `.env.example` to `.env` in each module directory
   - Configure your API keys and settings

---

# Detailed Documentation

## 1. Transcription Module

A powerful tool for transcribing and translating audio/video files using OpenAI's Whisper model.

### Features

- 🎙️ Transcribe audio/video files to text
- 🌐 Translate audio/video content to English
- ⏱️ Optional timestamp support for transcriptions
- 📊 Progress visualization and duration plotting
- 🔄 Batch processing capabilities
- 🎯 GPU acceleration support
- 📝 Detailed logging and error handling

### Components

#### 1. Preprocessing (`preprocess.py`)

Handles file validation and preparation:
- Checks file existence and audio stream presence
- Calculates file durations
- Generates file status reports
- Creates visualization plots of file durations
- Prepares JSON configuration for batch processing

#### 2. Transcription (`main.py`)

Performs the actual transcription/translation:
- Supports multiple Whisper models
- GPU acceleration when available
- Timestamp generation
- Translation to English
- Progress tracking and logging

### Configuration

Create a JSON configuration file with the following structure:
```json
{
    "MODEL": "base",  // Whisper model size (tiny, base, small, medium, large)
    "GPU": true,     // Enable GPU acceleration
    "FILES": [
        {
            "FILE_PATH": "path/to/your/file.mp4",
            "FILE_LANGUAGE": "en",  // Source language code
            "TRANSLATE": false,     // Whether to translate to English
            "TIMESTAMP": true       // Whether to include timestamps
        }
    ]
}
```

### Output

The tool generates:
- Text files with transcriptions/translations
- Optional timestamps for each segment
- Progress visualization plots
- Success logs with processing time

### Notes

- The tool automatically skips files that have already been processed
- Processing time varies based on file duration and model size
- GPU acceleration significantly improves processing speed
- Supported input formats include MP4, MP3, WAV, and other common audio/video formats

## 2. RAG Module

A powerful module for processing, embedding, and managing data for retrieval-augmented generation tasks.

### Features

- 🔄 JSON data combination and deduplication
- 📝 Text chunking and embedding generation
- 🔍 Vector database integration
- ⏱️ Time estimation for long-running tasks
- 📊 Metadata management
- 🔐 Environment-based configuration

### Components

#### 1. JSON Data Management (`combine-json.py`)

Handles JSON data processing and deduplication:
- Combines multiple JSON files
- Removes duplicates based on specified keys
- Maintains category information
- Preserves data integrity

#### 2. Embedding Generation (`embed.py`)

Creates and manages vector embeddings:
- Text chunking with overlap
- Token counting and management
- Metadata generation
- Azure OpenAI integration
- Batch processing support

#### 3. Record Upload (`upload_records.py`)

Manages vector database operations:
- Vector database connection
- Batch record uploading
- Index creation and management
- Progress tracking

### Environment Variables

```env
AZURE_OPENAI_KEY=your_api_key
AZURE_OPENAI_MODELID=your_model_id
OPENAI_API_VERSION=your_api_version
AZURE_OPENAI_ENDPOINT=your_endpoint
user=your_db_user
host=your_db_host
port=your_db_port
dbname=your_db_name
password=your_db_password
```

### Text Chunking Parameters

- `max_tokens`: Maximum tokens per chunk (default: 500)
- `overlap`: Token overlap between chunks (default: 50)

### Error Handling

The module includes comprehensive error handling for:
- API connection issues
- Database connectivity problems
- File I/O operations
- Data validation
- Environment configuration

## 3. Web Scraping Module

A robust and efficient web scraping tool that provides advanced features for extracting and processing web content.

### Features

- 🌐 JavaScript-rendered page scraping
- 🧹 Intelligent content cleaning
- 📝 Markdown conversion
- ⏱️ Time estimation and progress tracking
- 📊 Content analysis and statistics
- 🔄 Batch processing capabilities
- 📁 Organized output management

### Components

#### 1. Web Client (`WebClient`)

Handles web page retrieval:
- Headless Chrome browser automation
- JavaScript rendering
- Anti-detection measures
- Error handling

#### 2. HTML Cleaner (`HtmlCleaner`)

Processes and cleans web content:
- Removes unwanted elements (ads, scripts, etc.)
- Extracts metadata
- Converts content to Markdown
- Maintains content structure

#### 3. Web Scraper (`WebScraper`)

Main scraping orchestration:
- URL processing
- Content extraction
- File management
- Progress tracking

### Output Structure

The scraper generates multiple output formats for each URL:
- `.txt`: Full content with metadata
- `.html`: Original HTML content
- `.md`: Markdown version of the content
- JSON summary of all scraped content

### Content Cleaning

The HTML cleaner removes:
- Scripts and styles
- Images and SVGs
- Headers and footers
- Navigation elements
- Ad-related content

### Best Practices

1. **Rate Limiting**
   - Set appropriate delays between requests
   - Respect robots.txt
   - Use batch processing for large datasets

2. **Content Processing**
   - Verify content extraction
   - Check output formats
   - Monitor file sizes

3. **Resource Management**
   - Close browser instances
   - Clean up temporary files
   - Monitor memory usage

## 4. Utilities Module

A collection of essential utility tools and helpers used across the project.

### Features

- ⏱️ Time estimation for long-running tasks
- 📁 File system operations
- 📝 Rich logging capabilities
- 🔄 JSON data handling
- 💾 Backup and restore functionality

### Components

#### 1. Time Estimator (`time_estimator.py`)

Provides time estimation for iterative tasks:
- Progress tracking
- Remaining time calculation
- Iteration counting
- Average processing time estimation

#### 2. File System Processor (`file_processor.py`)

Handles file operations:
- JSON file loading and saving
- File backup and restore
- Directory management
- Data validation

#### 3. Logger (`logger.py`)

Rich logging capabilities:
- Console output formatting
- Log level management
- Traceback handling
- Custom formatting options

### File Processor Options

- `root_dir`: Base directory for operations
- `process_subdirs`: Whether to process subdirectories
- `backup`: Enable/disable automatic backups
- `append_not_overwrite`: Append to existing files
- `ensure_ascii`: ASCII encoding for JSON

### Logger Settings

- `rich_print_or_logs`: Output mode ('rich_print' or 'logs')
- Log level: INFO, ERROR, WARNING, etc.
- Custom formatting options

### Best Practices

1. **Time Estimation**
   - Initialize with accurate iteration count
   - Update processing time regularly
   - Monitor for significant deviations

2. **File Operations**
   - Always use backup for critical files
   - Validate JSON data before saving
   - Handle encoding properly

3. **Logging**
   - Use appropriate log levels
   - Include relevant context
   - Format messages consistently

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

- **Mohamed Nagy** - [n4jidx@example.com](mailto:n4jidx@example.com)

## Acknowledgments

- OpenAI for the Whisper model
- The open-source community for various tools and libraries