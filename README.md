# Stoic Reflections Flask App

A modern, refactored Flask application for daily stoic reflections and journaling.

## Features

- **Daily Reflection Forms**: Morning and evening reflections with rating system
- **Modern UI**: Responsive, accessible design with calm dark theme
- **Data Management**: Centralized storage with JSON persistence
- **Export Options**: CSV and PDF export functionality  
- **Search & Sort**: Client-side search and sorting capabilities
- **Clean Architecture**: Modular design with separation of concerns

## Project Structure

```
stoic_app/
│
├── app.py                # Main Flask application with routes
├── app_config.py         # Application configuration (dev/prod/test)
├── storage.py            # Centralized data storage and helper functions
├── requirements.txt      # Python dependencies
│
├── storage/              # Data storage directory
│   └── reflections.json  # JSON data persistence
│
├── templates/            # Jinja2 HTML templates
│   ├── base.html         # Base template with Bootstrap integration
│   ├── index.html        # Entry creation form
│   ├── edit.html         # Entry editing form
│   └── reflections.html  # Reflections listing page
│
├── static/               # Static assets
│   └── css/
│       └── main.css      # Custom styling with calm dark theme
│
└── README.md             # This file
```

## Getting Started

1. **Create and activate a virtual environment:**
   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

2. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```powershell
   python app.py
   ```

4. **Access the application:**
   Open your browser to `http://127.0.0.1:5000`

## Key Improvements

### Code Organization
- **Centralized Storage**: All data operations moved to `storage.py` module
- **Configuration Management**: Environment-specific configurations in `app_config.py`
- **Helper Functions**: Consistent patterns for entry creation, validation, and export
- **Template Structure**: Proper Flask templates with Bootstrap integration

### Functionality
- **Rating System**: Complete implementation across creation, editing, and export
- **Error Handling**: Consistent validation and bounds checking
- **Export Features**: CSV and PDF generation with proper formatting
- **Responsive Design**: Mobile-friendly interface with modern styling

### Best Practices
- **Application Factory**: Configurable app creation pattern
- **Type Hints**: Full typing for better code maintainability  
- **Separation of Concerns**: Clear boundaries between presentation, logic, and data
- **Consistent Patterns**: Unified approach to redirects, validation, and error handling

## Configuration

The application supports multiple environments through `app_config.py`:

- **Development**: Debug mode enabled, local storage
- **Production**: Optimized settings, environment-based secrets
- **Testing**: Isolated test data storage

## Future Enhancements

- Database integration (SQLite/PostgreSQL)
- User authentication and multi-user support
- Advanced search and filtering
- Data visualization and analytics
- API endpoints for mobile app integration
- Automated testing suite
