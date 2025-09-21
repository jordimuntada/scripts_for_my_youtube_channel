# YouTube Channel Scripts

A collection of Python scripts for YouTube channel automation, content creation, and management tasks.

## 🚀 Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/jordimuntada/scripts_for_my_youtube_channel.git
   cd scripts_for_my_youtube_channel
   ```

2. **Set up Python environment** (recommended)
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run example script**
   ```bash
   python examples/example_script.py --name "YouTube Creator"
   ```

## 📁 Project Structure

```
scripts_for_my_youtube_channel/
├── scripts/                 # Main Python scripts
│   ├── __init__.py
│   └── README.md           # Script documentation
├── utils/                  # Common utility functions
│   ├── __init__.py
│   └── common.py           # Helper functions
├── tests/                  # Unit tests
│   └── test_common.py
├── examples/               # Example scripts and usage
│   └── example_script.py
├── docs/                   # Documentation
├── requirements.txt        # Python dependencies
├── pyproject.toml         # Project configuration
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

## 🛠️ Development

### Adding New Scripts

1. Create your script in the `scripts/` directory
2. Follow the structure shown in `examples/example_script.py`
3. Use utilities from `utils/common.py`
4. Add tests in the `tests/` directory
5. Update documentation as needed

### Code Style

This project uses:
- **Black** for code formatting
- **Flake8** for linting
- **MyPy** for type checking

Install development dependencies:
```bash
pip install -e ".[dev]"
```

Format code:
```bash
black .
```

Run linting:
```bash
flake8 .
```

Run type checking:
```bash
mypy .
```

### Testing

Run tests using pytest:
```bash
pytest tests/
```

Run tests with coverage:
```bash
pytest --cov=scripts --cov=utils tests/
```

## 📝 Script Guidelines

1. **Documentation**: Include docstrings and comments
2. **Error Handling**: Implement proper error handling
3. **Logging**: Use the logging utilities from `utils.common`
4. **Configuration**: Externalize configuration (env vars, config files)
5. **Modularity**: Keep scripts focused and reusable
6. **Testing**: Write tests for your functions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-script`)
3. Make your changes following the guidelines above
4. Add tests for new functionality
5. Commit your changes (`git commit -am 'Add amazing script'`)
6. Push to the branch (`git push origin feature/amazing-script`)
7. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter any issues or have questions:
1. Check the documentation in the `docs/` directory
2. Look at example scripts in the `examples/` directory
3. Open an issue on GitHub
4. Check existing issues for similar problems

## 🎯 Common Use Cases

This repository is designed to support various YouTube channel automation tasks:

- **Content Creation**: Scripts for generating thumbnails, titles, descriptions
- **Data Analysis**: Analytics processing and reporting
- **Automation**: Upload scheduling, comment management
- **SEO Optimization**: Tag generation, keyword analysis
- **Social Media**: Cross-platform posting and management

Add your scripts to the appropriate directories and follow the established patterns!