# Projekt-Dokumentation: Sovereign Youth Web Platform

Diese Dokumentation erklärt den Aufbau und die Funktionsweise der Webseite `sovereign-youth.org` (Projektname: `updateSovereignYouth`). Sie richtet sich an Einsteiger ohne tiefes Vorwissen in Python oder Django.

---

## 1. Das Fundament: Die Technologien

### Python 🐍
Python ist die Programmiersprache, auf der alles hier basiert. Sie ist sehr gut lesbar (fast wie Englisch).
- **Beispiel:** `print("Hallo Welt")` gibt Text aus.
- **In diesem Projekt:** Wir nutzen Python für die gesamte Logik im Hintergrund (Backend): Daten speichern, Benutzer verwalten, Seiten ausliefern.

### Django 🎸
Django ist ein **Framework** für Python. Stell dir vor, du willst ein Haus bauen.
- **Ohne Framework:** Du musst Ziegel formen, Zement mischen, Rohre gießen.
- **Mit Django:** Du bekommst vorgefertigte Wände, fertige Rohre und ein Dach. Du musst sie "nur" noch zusammenstecken und anmalen.
- **Was Django uns schenkt:**
    - Eine fertige Benutzerverwaltung (Login/Logout).
    - Eine Datenbank-Verbindung (ohne SQL zu schreiben).
    - Ein Admin-Panel, um Daten zu bearbeiten.
    - Schutz gegen Hacker-Angriffe (z.B. SQL-Injection).

### SQL & SQLite 🗄️
SQL (Structured Query Language) ist die Sprache der Datenbanken.
- **Die Datenbank:** Hier werden alle Infos gespeichert (Benutzer, Blog-Posts, Mitglieder).
- **SQLite:** Das ist eine "Lite"-Version einer Datenbank. Statt eines riesigen Servers ist die ganze Datenbank einfach eine einzige Datei (`db.sqlite3`) in deinem Ordner. Perfekt für Entwicklung und kleinere Projekte.
- **Das Geniale an Django:** Du musst fast nie SQL schreiben! Django übersetzt deinen Python-Code automatisch in SQL (das nennt man ORM - Object Relational Mapper).

### HTML & Django Templates 🌐
HTML (HyperText Markup Language) ist das Skelett jeder Webseite. Es sagt dem Browser: "Hier ist eine Überschrift, hier ein Bild".
- **Django Templates:** Das sind HTML-Dateien mit "Superkräften". Man kann Python-ähnlichen Code direkt ins HTML schreiben.
    - `{{ variable }}`: Platzhalter, wird durch echten Inhalt ersetzt.
    - `{% if user.is_authenticated %}`: Logik, z.B. "Zeige diesen Knopf nur, wenn der Nutzer eingeloggt ist".

---

## 2. Die Projektstruktur (Ordner & Dateien)

Hier ist eine Karte deines Projekts:

```text
updateSovereignYouth-main-2/
├── manage.py              <-- Der Kommandant! (Server starten, DB aktualisieren)
├── db.sqlite3             <-- Die Datenbank-Datei
├── requirements.txt       <-- Einkaufsliste für Python-Pakete
├── cyberenigma_web/       <-- Das "Hauptquartier" (Einstellungen)
│   ├── settings.py        <-- Die Steuerzentrale (Konfiguration)
│   ├── urls.py            <-- Das Inhaltsverzeichnis (Welche URL führt wohin?)
│   └── wsgi.py / asgi.py  <-- Schnittstellen für Webserver (für Profis)
├── mainapp/               <-- Die eigentliche "App" (Funktionen & Inhalt)
│   ├── models.py          <-- Datenbank-Tabellen (Modelle)
│   ├── views.py           <-- Die Logik (Was passiert, wenn man eine Seite aufruft?)
│   ├── urls.py            <-- Unter-Verzeichnis für diese App
│   ├── templates/         <-- HTML-Dateien
│   └── static/            <-- Bilder, CSS, JavaScript
└── locale/                <-- Übersetzungen (Deutsch/Englisch)
```

---

## 3. Der Code im Detail (Erklärt)

### A. Die Steuerzentrale: `settings.py`

Diese Datei (`cyberenigma_web/settings.py`) konfiguriert alles.

```python
# Sagt Django, wo das Projekt auf der Festplatte liegt.
BASE_DIR = Path(__file__).resolve().parent.parent

# Ein geheimer Schlüssel für Verschlüsselung. NIEMALS teilen!
SECRET_KEY = '...'

# DEBUG = True heißt: Wenn es einen Fehler gibt, zeig mir genau wo.
# Auf einer echten Webseite muss das False sein (Sicherheit!).
DEBUG = True

# Welche Apps sind installiert?
INSTALLED_APPS = [
    'django.contrib.admin',  # Das Admin-Panel
    'django.contrib.auth',   # Benutzer-Login System
    'mainapp',               # Unsere eigene App!
    # ...
]

# Sprachen-Einstellungen
LANGUAGE_CODE = 'de'  # Standardsprache Deutsch
USE_I18N = True       # Internationalisierung (Übersetzung) aktivieren
```

### B. Die Datenbank-Modelle: `models.py`

In `mainapp/models.py` definieren wir, wie Daten aussehen. Django macht daraus Tabellen.

*Beispiel (vereinfacht):*
```python
class Member(models.Model):
    # Ein Textfeld für den Namen, max 100 Zeichen
    name = models.CharField(max_length=100)
    
    # Ein E-Mail Feld
    email = models.EmailField()
    
    # Ein Datum, wann das Mitglied beigetreten ist
    joined_at = models.DateTimeField(auto_now_add=True)
```
Django übersetzt das automatisch in SQL: `CREATE TABLE mainapp_member (name VARCHAR(100), ...);`

### C. Die URL-Verteilung: `urls.py`

Wenn jemand `deineseite.com/kontakt` aufruft, schaut Django in `urls.py`.

```python
from django.urls import path
from . import views

urlpatterns = [
    # Wenn die URL leer ist (''), rufe die Funktion 'home' in views.py auf
    path('', views.home, name='home'),
    
    # Wenn die URL 'login/' ist, rufe 'login_view' auf
    path('login/', views.login_view, name='login'),
]
```

### D. Die Logik: `views.py`

Hier passiert die Arbeit (`mainapp/views.py`). Eine "View" ist eine Python-Funktion, die eine Anfrage (Request) bekommt und eine Antwort (Response) zurückgibt.

```python
def home(request):
    # Hier könnte Logik stehen, z.B. "Hole alle News aus der Datenbank"
    
    # Gib die HTML-Datei 'home.html' zurück
    return render(request, 'home.html')
```

### E. Das Gesicht: Templates (`home.html`)

Hier wird das HTML mit Django-Logik gemischt.

```html
<!-- Lade Übersetzungs-Werkzeuge -->
{% load i18n %}

<h1>{% trans "Willkommen" %}</h1>

{% if user.is_authenticated %}
    <p>Hallo, {{ user.username }}!</p>
{% else %}
    <a href="{% url 'login' %}">Bitte einloggen</a>
{% endif %}
```
- `{% transString %}`: Dieser Text wird übersetzt (je nach Spracheinstellung).
- `{% url 'login' %}`: Django sucht in `urls.py` nach dem Namen 'login' und setzt den richtigen Link ein.

---

## 4. Cheat Sheet (Zum Nachschlagen) ⚡️

Hier hast du eine schnelle Übersicht über die wichtigsten Befehle und Syntax.

### Python Grundlagen (views.py, models.py)
| Code | Erklärung |
| :--- | :--- |
| `variable = "Text"` | Speichert Text in einer Variable |
| `if x > 5:` | Wenn x größer als 5 ist... (danach einrücken!) |
| `def funktion(req):` | Definiert eine neue Funktion |
| `return` | Gibt einen Wert zurück (z.B. die fertige Seite) |
| `import os` | Lädt ein Modul (hier: Betriebssystem-Funktionen) |
| `# Kommentare` | Alles nach `#` wird ignoriert (Notizen für dich) |

### HTML Grundlagen (Templates)
| Tag | Bedeutung |
| :--- | :--- |
| `<h1>Titel</h1>` | Hauptüberschrift (groß) |
| `<p>Text</p>` | Absatz (Paragraph) |
| `<a href="...">Link</a>` | Link zu einer anderen Seite |
| `<img src="...">` | Bild einfügen |
| `<div>...</div>` | Container (um Elemente zu gruppieren) |
| `<br>` | Zeilenumbruch |
| `<ul><li>Punkt</li></ul>` | Liste mit Punkten |
| `<form>...</form>` | Formular (Eingabefelder) |

### Django Template Syntax 🎸 (in HTML Dateien)
**1. Variablen ausgeben:** `{{ ... }}`
```html
<p>Hallo {{ user.username }}!</p>  <!-- Zeigt: Hallo Terence! -->
```

**2. Befehle & Logik:** `{% ... %}`
```html
{% if user.is_authenticated %}
  <p>Du bist eingeloggt.</p>
{% else %}
  <p>Bitte logge dich ein.</p>
{% endif %}
```

**3. Schleifen (etwas wiederholen):**
```html
<ul>
  {% for member in members %}
    <li>{{ member.name }}</li>
  {% endfor %}
</ul>
```

**4. Übersetzungen:**
```html
{% load i18n %}  <!-- Muss GANZ OBEN in der Datei stehen! -->

<!-- Einfacher Text -->
<h1>{% trans "Willkommen" %}</h1>

<!-- Text mit Variablen -->
{% blocktrans %}Hallo {{ name }}, wie geht es dir?{% endblocktrans %}
```

**5. Links (URLs):**
```html
<!-- Verweist auf den Namen, den du in urls.py definiert hast -->
<a href="{% url 'home' %}">Zur Startseite</a>
```

**6. Statische Dateien (Bilder, CSS):**
```html
{% load static %}
<img src="{% static 'logo.png' %}">
<link rel="stylesheet" href="{% static 'style.css' %}">
```

### Django Models (Datenbank-Felder) 🗄️
Wenn du Tabellen in `models.py` anlegst, brauchst du diese Typen:

| Feldtyp | Verwendung |
| :--- | :--- |
| `models.CharField(max_length=50)` | Kurzer Text (z.B. Name) |
| `models.TextField()` | Langer Text (z.B. Blog-Beitrag) |
| `models.IntegerField()` | Ganze Zahl (z.B. Alter) |
| `models.DecimalField(...)` | Kommazahl (z.B. Preis: 19.99) |
| `models.BooleanField()` | Ja/Nein (z.B. `is_active`) |
| `models.DateTimeField()` | Datum & Uhrzeit |
| `models.ForeignKey(...)` | Verknüpfung zu einer anderen Tabelle |

---

## 5. Wichtige Terminal-Befehle

Diese Befehle tippst du im Terminal ein (im Projektordner).

**Server:**
- `python3 manage.py runserver`: Startet deine Seite lokal.

**Datenbank:**
- `python3 manage.py makemigrations`: Erstelle Änderungen für die DB.
- `python3 manage.py migrate`: Wende Änderungen auf die DB an.
- `python3 manage.py createsuperuser`: Erstelle einen Admin-Account.

**Übersetzungen:**
- `python3 manage.py makemessages -l de`: Suche neue Texte für Deutsch.
- `python3 manage.py compilemessages`: Mache Übersetzungen nutzbar.
