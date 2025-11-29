# git-size

Analyze Git repository size and identify files contributing to repo bloat

## Features

- Scan Git repository and list largest files across all history
- Display top N largest files with size, path, and commit information
- Show size contribution breakdown by directory
- Identify deleted files still consuming space in Git history
- Calculate total repository size vs working directory size
- Suggest candidates for Git LFS based on file size thresholds
- Support for custom size thresholds and result limits
- Human-readable size formatting (KB, MB, GB)
- Colorized output with rich tables for better readability
- Export results to JSON format for further processing
- Filter by file extensions or path patterns
- Show pack file size and object count statistics

## Installation

```bash
# Clone the repository
git clone https://github.com/KurtWeston/git-size.git
cd git-size

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

## Built With

- python using click

## Dependencies

- `click>=8.0.0`
- `gitpython>=3.1.0`
- `rich>=13.0.0`
- `pytest>=7.0.0`

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
