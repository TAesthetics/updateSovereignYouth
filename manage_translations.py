import sys
import os
import subprocess
from pathlib import Path

def extract_translatable_strings():
    """Extract translatable strings from the codebase."""
    print("Extracting translatable strings...")
    cmd = [
        sys.executable, 'manage.py', 'makemessages',
        '--ignore=venv/*',
        '--ignore=node_modules/*',
        '--no-location',
        '--no-obsolete',
        '--keep-pot',
        '-a'
    ]
    subprocess.run(cmd, check=True)

def update_translation_files():
    """Update translation files with new strings."""
    print("Updating translation files...")
    # Update German translations
    update_translation('de')
    # Update English translations
    update_translation('en')

def update_translation(lang_code):
    """Update a specific translation file."""
    po_file = f'locale/{lang_code}/LC_MESSAGES/django.po'
    if not os.path.exists(po_file):
        print(f"Creating new translation file for {lang_code}...")
        subprocess.run([sys.executable, 'manage.py', 'makemessages', '-l', lang_code], check=True)
    
    # Add common translations
    translations = {
        'de': {
            'Sovereign Youth': 'Sovereign Youth',
            'Empowering the next generation through education, community, and leadership development.': 
                'Befähigung der nächsten Generation durch Bildung, Gemeinschaft und Führungskompetenz.',
            'Contact:': 'Kontakt:',
            'Navigation': 'Navigation',
            'Connect': 'Vernetzung',
            'Join The Digital Coil': 'Dem Digital Coil beitreten',
            'All rights reserved.': 'Alle Rechte vorbehalten.',
            'Impressum': 'Impressum',
            'Datenschutz': 'Datenschutz',
            'A student and youth organization for achievement, responsibility, and independent thinking.':
                'Eine Schüler- und Jugendorganisation für Leistung, Verantwortung und souveränes Denken.',
            'We work to improve education, enhance performance, and bring young people into responsibility early on - through projects, not activism.':
                'Wir arbeiten daran, Bildung besser zu machen, Leistung zu steigern und junge Menschen früh in Verantwortung zu bringen – durch Projekte, nicht durch Aktivismus.'
        },
        'en': {
            'Sovereign Youth': 'Sovereign Youth',
            'Empowering the next generation through education, community, and leadership development.': 
                'Empowering the next generation through education, community, and leadership development.',
            'Contact:': 'Contact:',
            'Navigation': 'Navigation',
            'Connect': 'Connect',
            'Join The Digital Coil': 'Join The Digital Coil',
            'All rights reserved.': 'All rights reserved.',
            'Impressum': 'Legal Notice',
            'Datenschutz': 'Privacy Policy',
            'A student and youth organization for achievement, responsibility, and independent thinking.':
                'A student and youth organization for achievement, responsibility, and independent thinking.',
            'We work to improve education, enhance performance, and bring young people into responsibility early on - through projects, not activism.':
                'We work to improve education, enhance performance, and bring young people into responsibility early on - through projects, not activism.'
        }
    }

    # Update the PO file with our translations
    with open(po_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add translations that don't exist yet
    for msgid, msgstr in translations[lang_code].items():
        if f'msgid "{msgid}"' not in content:
            content += f'''
#: templates/
msgid "{msgid}"
msgstr "{msgstr}"
'''
    
    # Write the updated content back to the file
    with open(po_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Updated {po_file}")

def compile_translations():
    """Compile translation files."""
    print("Compiling translations...")
    subprocess.run([sys.executable, 'manage.py', 'compilemessages'], check=True)

if __name__ == '__main__':
    # Ensure we're in the project root
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    extract_translatable_strings()
    update_translation_files()
    compile_translations()
    
    print("\nTranslation update complete!")
    print("Please review the .po files in the locale directory and update the translations as needed.")
    print("After making changes, run 'python manage.py compilemessages' to compile the translations.")
