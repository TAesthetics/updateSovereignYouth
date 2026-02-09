from django.core.management.base import BaseCommand
from django.core.management import call_command
import os

class Command(BaseCommand):
    help = 'Update translation files with custom strings'

    def handle(self, *args, **options):
        # Extract messages
        self.stdout.write('Extracting messages...')
        call_command('makemessages', '--ignore=venv/*', '--no-location', '--no-obsolete', '-a')
        
        # Update PO files with custom translations
        self.update_po_file('de')
        self.update_po_file('en')
        
        # Compile messages
        self.stdout.write('Compiling messages...')
        call_command('compilemessages')
        
        self.stdout.write(self.style.SUCCESS('Successfully updated translations'))
    
    def update_po_file(self, lang_code):
        po_path = f'locale/{lang_code}/LC_MESSAGES/django.po'
        
        # Skip if file doesn't exist
        if not os.path.exists(po_path):
            self.stdout.write(self.style.WARNING(f'PO file not found: {po_path}'))
            return
        
        # Read existing content
        with open(po_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Add custom translations if they don't exist
        custom_translations = self.get_custom_translations(lang_code)
        
        for msgid, msgstr in custom_translations.items():
            if f'msgid "{msgid}"' not in content:
                content += f'\n#: mainapp/translations.py\nmsgid "{msgid}"\nmsgstr "{msgstr}"\n'
        # Write updated content back
        with open(po_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        self.stdout.write(f'Updated {po_path}')
    
    def get_custom_translations(self, lang_code):
        # German translations
        if lang_code == 'de':
            return {
                # Homepage
                "A student and youth organization for achievement, responsibility, and independent thinking.": 
                    "Eine Schüler- und Jugendorganisation für Leistung, Verantwortung und souveränes Denken.",
                "We work to improve education, enhance performance, and bring young people into responsibility early on - through projects, not activism.":
                    "Wir arbeiten daran, Bildung besser zu machen, Leistung zu steigern und junge Menschen früh in Verantwortung zu bringen – durch Projekte, nicht durch Aktivismus.",
                "Become a Member": "Mitglied werden",
                "The Digital Coil": "The Digital Coil",
                "Why join?": "Warum mitmachen?",
                # Add more translations as needed
            }
        # English translations (kept as is)
        else:
            return {
                # Homepage
                "A student and youth organization for achievement, responsibility, and independent thinking.": 
                    "A student and youth organization for achievement, responsibility, and independent thinking.",
                "We work to improve education, enhance performance, and bring young people into responsibility early on - through projects, not activism.":
                    "We work to improve education, enhance performance, and bring young people into responsibility early on - through projects, not activism.",
                "Become a Member": "Become a Member",
                "The Digital Coil": "The Digital Coil",
                "Why join?": "Why join?",
                # Add more translations as needed
            }
