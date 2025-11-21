# Outreach Worker

A Python-based email outreach automation tool designed to send personalized emails to a list of contacts.

## Features

- **Personalized Emails**: Use templates with placeholders like `{name}`, `{company}`, etc.
- **Bulk Sending**: Process contacts from a CSV file.
- **Retry Logic**: Automatically retries failed sends with exponential backoff.
- **Multiple Providers**: Supports Gmail, Outlook, Yahoo, and custom SMTP servers.
- **HTML Support**: Send professional HTML emails or simple text.
- **Logging**: Tracks sent emails and generates a campaign report.

## Installation

1.  **Clone the repository** (if applicable) or navigate to the project directory.
2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

1.  **Environment Variables**:
    Copy `.env.example` to `.env`:
    ```bash
    cp .env.example .env
    ```
    Edit `.env` and add your email credentials:
    ```ini
    EMAIL_ADDRESS=your_email@gmail.com
    EMAIL_PASSWORD=your_app_password
    EMAIL_SERVICE=gmail
    ```
    *Note: For Gmail, you must use an [App Password](https://support.google.com/accounts/answer/185833?hl=en) if 2FA is enabled.*

2.  **Contacts**:
    Edit `data/contacts.csv` with your contact list. The CSV must have at least an `email` column. Other columns like `name` can be used in templates.

## Usage

### Basic Usage
Run the script to start sending emails:
```bash
python main.py
```

### Command Line Options

| Option | Description | Default |
| :--- | :--- | :--- |
| `--contacts` | Path to contacts CSV file | `data/contacts.csv` |
| `--subject` | Email subject template | "Hello {name}" |
| `--body` | Email body template | "Hi {name}..." |
| `--html` | Send as HTML email | False |
| `--dry-run` | Simulate sending without delivery | False |
| `--delay` | Delay between emails (seconds) | 2.0 |

### Examples

**Dry Run (Test Mode):**
```bash
python main.py --dry-run
```

**Custom Subject and Body:**
```bash
python main.py --subject "Opportunity at {company}" --body "Hi {name}, I love what you do at {company}..."
```

**Send HTML Email:**
```bash
python main.py --html --subject "Weekly Newsletter"
```

## Project Structure

- `main.py`: Entry point CLI application.
- `src/`: Core logic (Agent, Email Service, Utils).
- `data/`: CSV files for contacts.
- `logs/`: Execution logs.
- `templates/`: (Optional) Directory for storing template files.
