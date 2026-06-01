
---

## Quick Start (2 commands)

```bash
# 1. Install dependencies
pip install flask werkzeug

# 2. Set up images (run once — place Sty_Images.zip in the project root first)
python setup_images.py

# 3. Create the database (run once)
python database.py

# 4. Start the app
python app.py
```

Then open http://127.0.0.1:5000 in your browser.

---

## Project Structure

```
styra-redesign/
├── app.py              ← Flask routes and logic
├── database.py         ← DB creation + outfit seeding
├── setup_images.py     ← Extract + organise images from zip
├── styra.db            ← SQLite database (auto-created)
├── Sty_Images.zip      ← Place your images zip here
├── static/
│   ├── css/
│   │   └── styra.css   ← All styling
│   └── images/
│       ├── english/
│       │   ├── casual/
│       │   ├── formal/
│       │   ├── office/
│       │   └── wedding/
│       └── traditional/
│           ├── casual/
│           ├── formal/
│           ├── office/
│           └── wedding/
└── templates/
    ├── base.html       ← Shared nav + layout
    ├── landing.html    ← Home page
    ├── register.html   ← Sign up
    ├── login.html      ← Sign in
    ├── quiz.html       ← 7-step style quiz
    ├── results.html    ← Outfit recommendations
    └── saved.html      ← User's saved looks
```

---

## Features

- **User accounts** — Register, login, logout with hashed passwords
- **7-step guided quiz** — Skin tone, body type, clothing preference, modesty, occasion, climate, style vibe
- **Auto-advance** — Selecting an option automatically moves to the next step
- **Progress bar** — Visual progress through the quiz
- **Smart recommendations** — Full match → partial match → fallback logic
- **Outfit rating** — 1–5 stars saved per user
- **Saved looks** — View all outfits rated 4+ stars
- **Responsive** — Works on mobile and desktop

---

## Technology Stack

| Layer      | Technology |
|------------|------------|
| Backend    | Python + Flask |
| Database   | SQLite |
| Frontend   | HTML5 + CSS3 + Vanilla JS |
| Auth       | Werkzeug password hashing |
| Fonts      | Playfair Display + DM Sans (Google Fonts) |

---

## Image Naming Convention

Images inside `static/images/` follow the pattern:
```
static/images/<clothing_type>/<occasion>/<N>_<clothing_type>_<occasion>.<ext>
```
Example: `static/images/traditional/wedding/3_traditional_wedding.jpg`

The database stores only the path relative to `static/`, e.g. `images/traditional/wedding/3_traditional_wedding.jpg`.

---

## Database Schema

```sql
users         (id, name, email, password, created)
user_profiles (user_id, skin_tone, body_type, clothing_type, modesty, occasion, climate, style_vibe)
outfits       (id, clothing_type, occasion, body_type, modesty, image, label, description)
ratings       (user_id, outfit_id, rating, rated_at)
```

---

*Built for final year project submission — Skyline University Nigeria 2025*
