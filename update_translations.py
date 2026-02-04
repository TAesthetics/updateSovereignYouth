import os
import re
from pathlib import Path

def add_translation_tags(file_path):
    # Skip files that already have translation tags or are in static/admin
    if 'node_modules' in str(file_path) or 'venv' in str(file_path) or 'static/admin' in str(file_path):
        return False
        
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Skip if already has translation tags or is a base template
    if '{% trans ' in content or '{% load i18n %}' in content or file_path.name == 'base.html':
        return False
    
    # Add i18n load tag if not present
    if '{% load i18n %}' not in content:
        content = content.replace('{% load', '{% load i18n %}\n{% load', 1)
        if '{% load i18n %}' not in content:  # In case there was no load tag at all
            content = '{% load i18n %}\n' + content
    
    # Pattern to find text nodes that should be translated (excluding HTML tags, template tags, and variables)
    pattern = r'>([^<\n\r\f\v{]+[a-zA-Z][^<\n\r\f\v{]+)(?=<|\n|\r|$)'
    
    def replace_match(match):
        text = match.group(1).strip()
        # Skip empty strings, numbers, or very short strings
        if not text or len(text) < 3 or text.isdigit() or text.strip() in ('|', ':', ';', ',', '.', '!', '?'):
            return '>' + text
        # Don't translate if it's already in a tag or contains template variables
        if '{{' in text or '{%' in text or '&' in text:
            return '>' + text
        return '>{% trans \'' + text.replace("'", "\\'") + "' %}"
    
    new_content = re.sub(pattern, replace_match, content)
    
    # Save the file if changes were made
    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

def process_directory(directory):
    base_dir = Path(directory)
    html_files = list(base_dir.glob('**/*.html'))
    
    print(f"Found {len(html_files)} HTML files to process...")
    
    updated_files = 0
    for file_path in html_files:
        try:
            if add_translation_tags(file_path):
                print(f"Updated: {file_path.relative_to(base_dir)}")
                updated_files += 1
        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")
    
    print(f"\nUpdated {updated_files} out of {len(html_files)} files.")

if __name__ == "__main__":
    project_root = os.path.dirname(os.path.abspath(__file__))
    process_directory(project_root)
