from pathlib import Path
from typing import Optional


class HTMLTemplates:
    """Pre-built HTML email templates."""
    
    @staticmethod
    def professional_template(title: str, content: str, footer: str = "") -> str:
        """
        Professional email template with modern design.
        
        Args:
            title: Email header title
            content: Main email content (HTML)
            footer: Footer text (HTML)
            
        Returns:
            Complete HTML email string
        """
        return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f4f4f4;">
    <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f4f4f4; padding: 20px;">
        <tr>
            <td align="center">
                <table width="600" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <!-- Header -->
                    <tr>
                        <td style="padding: 30px 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 8px 8px 0 0;">
                            <h1 style="color: #ffffff; margin: 0; font-size: 24px;">{title}</h1>
                        </td>
                    </tr>
                    <!-- Content -->
                    <tr>
                        <td style="padding: 40px; color: #333333; line-height: 1.6; font-size: 16px;">
                            {content}
                        </td>
                    </tr>
                    <!-- Footer -->
                    <tr>
                        <td style="padding: 20px 40px; background-color: #f8f9fa; border-radius: 0 0 8px 8px; text-align: center; color: #666666; font-size: 14px;">
                            {footer if footer else "© 2025 All rights reserved"}
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
"""
    
    @staticmethod
    def simple_template(content: str) -> str:
        """
        Simple, clean HTML template.
        
        Args:
            content: Main email content (HTML)
            
        Returns:
            Complete HTML email string
        """
        return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .content {{ background: #ffffff; padding: 30px; border-radius: 5px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="content">
            {content}
        </div>
    </div>
</body>
</html>
"""
    
    @staticmethod
    def minimal_template(content: str) -> str:
        """
        Minimal template with basic styling.
        
        Args:
            content: Main email content (HTML)
            
        Returns:
            Complete HTML email string
        """
        return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
</head>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; padding: 20px;">
    {content}
</body>
</html>
"""
    
    @staticmethod
    def load_from_file(file_path: str, **kwargs) -> str:
        """
        Load and format HTML template from file.
        
        Args:
            file_path: Path to HTML template file
            **kwargs: Variables to substitute in template
            
        Returns:
            Formatted HTML string
        """
        from string import Template
        
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Template file not found: {file_path}")
        
        with open(path, 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        template = Template(template_content)
        return template.safe_substitute(**kwargs)
