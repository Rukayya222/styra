import sqlite3, os
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)
app.secret_key = 'styra-secret-key-change-in-production'
DB_PATH = os.path.join(os.path.dirname(__file__), 'styra.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        name  = request.form['name'].strip()
        email = request.form['email'].strip().lower()
        pw    = request.form['password']
        if not name or not email or not pw:
            flash('All fields are required.', 'error')
            return render_template('register.html')
        db = get_db()
        if db.execute('SELECT id FROM users WHERE email=?', (email,)).fetchone():
            flash('An account with that email already exists.', 'error')
            db.close(); return render_template('register.html')
        db.execute('INSERT INTO users (name,email,password) VALUES (?,?,?)',
                   (name, email, generate_password_hash(pw)))
        db.commit()
        user = db.execute('SELECT id FROM users WHERE email=?', (email,)).fetchone()
        db.close()
        session['user_id']   = user['id']
        session['user_name'] = name
        # Check if there are pending quiz results to save
        if 'pending_params' in session:
            return redirect(url_for('save_pending'))
        return redirect(url_for('quiz'))
    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        pw    = request.form['password']
        db    = get_db()
        user  = db.execute('SELECT * FROM users WHERE email=?', (email,)).fetchone()
        db.close()
        if user and check_password_hash(user['password'], pw):
            session['user_id']   = user['id']
            session['user_name'] = user['name']
            if 'pending_params' in session:
                return redirect(url_for('save_pending'))
            return redirect(url_for('quiz'))
        flash('Invalid email or password.', 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('landing'))

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/quiz')
def quiz():
    return render_template('quiz.html', user_name=session.get('user_name',''))

@app.route('/recommend', methods=['POST'])
def recommend():
    skin_tone     = request.form.get('skin_tone','')
    body_type     = request.form.get('body_type','')
    clothing_type = request.form.get('clothing_type','')
    modesty       = request.form.get('modesty','')
    occasion      = request.form.get('occasion','')
    climate       = request.form.get('climate','')
    style_vibe    = request.form.get('style_vibe','')

    params = dict(skin_tone=skin_tone, body_type=body_type,
                  clothing_type=clothing_type, modesty=modesty,
                  occasion=occasion, climate=climate, style_vibe=style_vibe)

    db = get_db()

    if 'user_id' in session:
        db.execute('''INSERT INTO user_profiles
            (user_id,skin_tone,body_type,clothing_type,modesty,occasion,climate,style_vibe)
            VALUES (?,?,?,?,?,?,?,?)
            ON CONFLICT(user_id) DO UPDATE SET
            skin_tone=excluded.skin_tone, body_type=excluded.body_type,
            clothing_type=excluded.clothing_type, modesty=excluded.modesty,
            occasion=excluded.occasion, climate=excluded.climate,
            style_vibe=excluded.style_vibe''',
            (session['user_id'], skin_tone, body_type, clothing_type,
             modesty, occasion, climate, style_vibe))
        db.commit()
    else:
        session['pending_params'] = params

    rows = db.execute(
        'SELECT * FROM outfits WHERE clothing_type=? AND occasion=?',
        (clothing_type, occasion)).fetchall()
    if not rows:
        rows = db.execute('SELECT * FROM outfits WHERE clothing_type=?',
                          (clothing_type,)).fetchall()

    db.close()

    scored = sorted(
        [(score_outfit(r, body_type, modesty, skin_tone), r) for r in rows],
        key=lambda x: x[0], reverse=True)

    outfits = []
    for score, row in scored[:2]:
        o = dict(row)
        o['match_score'] = score
        o['why_this'] = _build_why(o, body_type, modesty, skin_tone)
        outfits.append(o)

    explanation = _build_explanation(clothing_type, occasion, body_type, modesty, climate, style_vibe)
    is_guest = 'user_id' not in session

    return render_template('results.html',
        outfits=outfits, explanation=explanation,
        user_name=session.get('user_name',''),
        is_guest=is_guest, params=params)

@app.route('/save_pending')
@login_required
def save_pending():
    params = session.pop('pending_params', None)
    if params:
        db = get_db()
        db.execute('''INSERT INTO user_profiles
            (user_id,skin_tone,body_type,clothing_type,modesty,occasion,climate,style_vibe)
            VALUES (?,?,?,?,?,?,?,?)
            ON CONFLICT(user_id) DO UPDATE SET
            skin_tone=excluded.skin_tone, body_type=excluded.body_type,
            clothing_type=excluded.clothing_type, modesty=excluded.modesty,
            occasion=excluded.occasion, climate=excluded.climate,
            style_vibe=excluded.style_vibe''',
            (session['user_id'], params.get('skin_tone'), params.get('body_type'),
             params.get('clothing_type'), params.get('modesty'), params.get('occasion'),
             params.get('climate'), params.get('style_vibe')))
        db.commit()
        db.close()
        flash('Your style profile has been saved.', 'success')
    return redirect(url_for('quiz'))

@app.route('/rate', methods=['POST'])
@login_required
def rate():
    outfit_id = request.form.get('outfit_id')
    rating    = request.form.get('rating')
    if outfit_id and rating:
        db = get_db()
        db.execute('''INSERT INTO ratings (user_id,outfit_id,rating) VALUES (?,?,?)
            ON CONFLICT(user_id,outfit_id) DO UPDATE SET rating=excluded.rating''',
            (session['user_id'], outfit_id, rating))
        db.commit(); db.close()
    return '', 204

@app.route('/saved')
@login_required
def saved():
    db = get_db()
    rated = db.execute('''SELECT o.*, r.rating FROM outfits o
        JOIN ratings r ON o.id=r.outfit_id
        WHERE r.user_id=? AND r.rating>=4
        ORDER BY r.rating DESC''', (session['user_id'],)).fetchall()
    db.close()
    return render_template('saved.html', outfits=[dict(r) for r in rated],
        user_name=session.get('user_name',''))

def score_outfit(row, body_type, modesty, skin_tone):
    score = 0
    body_tags = [b.strip() for b in (row['body_type'] or '').split(',')]
    skin_tags  = [s.strip() for s in (row['skin_tone'] or '').split(',')]
    if body_type and body_type in body_tags: score += 3
    if modesty and row['modesty'] == modesty: score += 2
    if skin_tone and skin_tone in skin_tags: score += 1
    return score

def _build_why(outfit, body_type, modesty, skin_tone):
    parts = []
    body_tags = [b.strip() for b in (outfit.get('body_type','') or '').split(',')]
    skin_tags  = [s.strip() for s in (outfit.get('skin_tone','') or '').split(',')]
    if body_type and body_type in body_tags and outfit.get('why_body'):
        parts.append(outfit['why_body'])
    if skin_tone and skin_tone in skin_tags and outfit.get('why_skin'):
        parts.append(outfit['why_skin'])
    if not parts:
        parts.append(outfit.get('description','A great pick for your style profile.'))
    return ' '.join(parts[:2])

def _build_explanation(clothing_type, occasion, body_type, modesty, climate, style_vibe):
    ct  = 'Traditional' if clothing_type == 'traditional' else 'English (Western)'
    occ = {'casual':'casual outings','formal':'formal events','office':'the office','wedding':'weddings'}.get(occasion, occasion)
    bt  = {'hourglass':'hourglass figure','pear':'pear-shaped body','apple':'apple-shaped body','rectangle':'rectangular frame','petite':'petite frame'}.get(body_type,'')
    mo  = {'modest':'modest, full-coverage styling','balanced':'balanced, semi-modest styling','bold':'bold, expressive styling'}.get(modesty,'')
    cl  = {'hot':'hot weather','warm':'warm conditions','cold':'cooler temperatures'}.get(climate,'')
    sv  = {'elegant':'elegant and refined','comfy':'relaxed and comfortable','bold':'bold and statement-making'}.get(style_vibe,'')
    parts = [f"{ct} wear for {occ}"]
    if bt:  parts.append(f"tailored for a {bt}")
    if mo:  parts.append(mo)
    if cl:  parts.append(f"suited for {cl}")
    if sv:  parts.append(f"with a {sv} vibe")
    return ', '.join(parts) + '.'

# ═══════════════════════════════════════════════════════════════════════════
# ADMIN PANEL
# ═══════════════════════════════════════════════════════════════════════════
import uuid
from werkzeug.utils import secure_filename

# ── Admin config ─────────────────────────────────────────────────────────────
ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'styra2025')
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('is_admin'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated

# ── Admin Auth ────────────────────────────────────────────────────────────────
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if session.get('is_admin'):
        return redirect(url_for('admin_dashboard'))
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['is_admin'] = True
            return redirect(url_for('admin_dashboard'))
        flash('Invalid credentials.', 'error')
    return render_template('admin/login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('is_admin', None)
    return redirect(url_for('admin_login'))

# ── Dashboard ─────────────────────────────────────────────────────────────────
@app.route('/admin')
@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    db = get_db()

    # Core counts
    total_outfits  = db.execute('SELECT COUNT(*) FROM outfits').fetchone()[0]
    total_users    = db.execute('SELECT COUNT(*) FROM users').fetchone()[0]
    total_ratings  = db.execute('SELECT COUNT(*) FROM ratings').fetchone()[0]
    traditional    = db.execute("SELECT COUNT(*) FROM outfits WHERE clothing_type='traditional'").fetchone()[0]
    english        = db.execute("SELECT COUNT(*) FROM outfits WHERE clothing_type='english'").fetchone()[0]

    # Outfits by occasion breakdown
    by_occasion = []
    for occ in ['casual', 'formal', 'office', 'wedding']:
        t = db.execute("SELECT COUNT(*) FROM outfits WHERE occasion=? AND clothing_type='traditional'", (occ,)).fetchone()[0]
        e = db.execute("SELECT COUNT(*) FROM outfits WHERE occasion=? AND clothing_type='english'", (occ,)).fetchone()[0]
        by_occasion.append({'occasion': occ, 'traditional': t, 'english': e, 'total': t + e})

    # Recent users
    recent_users = db.execute(
        'SELECT name, email, created FROM users ORDER BY id DESC LIMIT 6'
    ).fetchall()

    # Top rated outfits
    top_rated = db.execute('''
        SELECT o.label, o.clothing_type, o.occasion, o.image,
               AVG(r.rating) as avg_rating, COUNT(r.rating) as vote_count
        FROM outfits o
        JOIN ratings r ON o.id = r.outfit_id
        GROUP BY o.id
        ORDER BY avg_rating DESC, vote_count DESC
        LIMIT 5
    ''').fetchall()

    db.close()

    stats = {
        'total_outfits': total_outfits, 'total_users': total_users,
        'total_ratings': total_ratings, 'traditional': traditional, 'english': english,
        'by_occasion': by_occasion
    }
    return render_template('admin/dashboard.html', stats=stats,
                           recent_users=recent_users, top_rated=top_rated)

# ── Outfits ───────────────────────────────────────────────────────────────────
@app.route('/admin/outfits')
@admin_required
def admin_outfits():
    db   = get_db()
    q    = request.args.get('q', '').strip()
    t    = request.args.get('type', '')
    occ  = request.args.get('occasion', '')
    mod  = request.args.get('modesty', '')

    sql  = 'SELECT * FROM outfits WHERE 1=1'
    args = []
    if q:
        sql += ' AND (label LIKE ? OR description LIKE ?)'; args += [f'%{q}%', f'%{q}%']
    if t:
        sql += ' AND clothing_type=?'; args.append(t)
    if occ:
        sql += ' AND occasion=?'; args.append(occ)
    if mod:
        sql += ' AND modesty=?'; args.append(mod)
    sql += ' ORDER BY clothing_type, occasion, id'

    outfits = db.execute(sql, args).fetchall()
    db.close()
    return render_template('admin/outfits.html', outfits=outfits)

@app.route('/admin/outfits/add', methods=['GET', 'POST'])
@admin_required
def admin_add_outfit():
    if request.method == 'POST':
        label         = request.form.get('label', '').strip()
        description   = request.form.get('description', '').strip()
        clothing_type = request.form.get('clothing_type', '').strip()
        occasion      = request.form.get('occasion', '').strip()
        modesty       = request.form.get('modesty', '').strip()
        body_type     = request.form.get('body_type', '').strip()
        skin_tone     = request.form.get('skin_tone', '').strip()
        why_body      = request.form.get('why_body', '').strip()
        why_skin      = request.form.get('why_skin', '').strip()

        # Handle image upload
        image_path = None
        file = request.files.get('image_file')
        if file and file.filename and allowed_file(file.filename):
            ext        = file.filename.rsplit('.', 1)[1].lower()
            folder     = f'images/{clothing_type}/{occasion}'
            dest_dir   = os.path.join(app.root_path, 'static', folder)
            os.makedirs(dest_dir, exist_ok=True)
            filename   = f"{uuid.uuid4().hex[:8]}_{secure_filename(file.filename)}"
            file.save(os.path.join(dest_dir, filename))
            image_path = f'{folder}/{filename}'
        else:
            flash('A valid image file is required.', 'error')
            return render_template('admin/outfit_form.html', outfit=None)

        db = get_db()
        db.execute('''INSERT INTO outfits
            (clothing_type, occasion, body_type, modesty, skin_tone, image, label, description, why_body, why_skin)
            VALUES (?,?,?,?,?,?,?,?,?,?)''',
            (clothing_type, occasion, body_type, modesty, skin_tone,
             image_path, label, description, why_body, why_skin))
        db.commit()
        db.close()
        flash(f'Outfit "{label}" added successfully.', 'success')
        return redirect(url_for('admin_outfits'))

    return render_template('admin/outfit_form.html', outfit=None)

@app.route('/admin/outfits/<int:outfit_id>/edit', methods=['GET', 'POST'])
@admin_required
def admin_edit_outfit(outfit_id):
    db     = get_db()
    outfit = db.execute('SELECT * FROM outfits WHERE id=?', (outfit_id,)).fetchone()
    if not outfit:
        db.close()
        flash('Outfit not found.', 'error')
        return redirect(url_for('admin_outfits'))

    if request.method == 'POST':
        label         = request.form.get('label', '').strip()
        description   = request.form.get('description', '').strip()
        clothing_type = request.form.get('clothing_type', '').strip()
        occasion      = request.form.get('occasion', '').strip()
        modesty       = request.form.get('modesty', '').strip()
        body_type     = request.form.get('body_type', '').strip()
        skin_tone     = request.form.get('skin_tone', '').strip()
        why_body      = request.form.get('why_body', '').strip()
        why_skin      = request.form.get('why_skin', '').strip()

        # Handle image — new upload takes priority, then manual path, then keep existing
        image_path = outfit['image']
        file = request.files.get('image_file')
        if file and file.filename and allowed_file(file.filename):
            ext      = file.filename.rsplit('.', 1)[1].lower()
            folder   = f'images/{clothing_type}/{occasion}'
            dest_dir = os.path.join(app.root_path, 'static', folder)
            os.makedirs(dest_dir, exist_ok=True)
            filename = f"{uuid.uuid4().hex[:8]}_{secure_filename(file.filename)}"
            file.save(os.path.join(dest_dir, filename))
            image_path = f'{folder}/{filename}'
        elif request.form.get('image_path', '').strip():
            image_path = request.form.get('image_path').strip()

        db.execute('''UPDATE outfits SET
            clothing_type=?, occasion=?, body_type=?, modesty=?, skin_tone=?,
            image=?, label=?, description=?, why_body=?, why_skin=?
            WHERE id=?''',
            (clothing_type, occasion, body_type, modesty, skin_tone,
             image_path, label, description, why_body, why_skin, outfit_id))
        db.commit()
        db.close()
        flash(f'Outfit "{label}" updated.', 'success')
        return redirect(url_for('admin_outfits'))

    db.close()
    return render_template('admin/outfit_form.html', outfit=outfit)

@app.route('/admin/outfits/<int:outfit_id>/delete', methods=['POST'])
@admin_required
def admin_delete_outfit(outfit_id):
    db     = get_db()
    outfit = db.execute('SELECT label FROM outfits WHERE id=?', (outfit_id,)).fetchone()
    if outfit:
        db.execute('DELETE FROM ratings WHERE outfit_id=?', (outfit_id,))
        db.execute('DELETE FROM outfits WHERE id=?', (outfit_id,))
        db.commit()
        flash(f'Outfit "{outfit["label"]}" deleted.', 'success')
    db.close()
    return redirect(url_for('admin_outfits'))

# ── Users ─────────────────────────────────────────────────────────────────────
@app.route('/admin/users')
@admin_required
def admin_users():
    db = get_db()
    users = db.execute('''
        SELECT u.id, u.name, u.email, u.created,
               p.clothing_type, p.occasion, p.modesty,
               COUNT(r.outfit_id) as rating_count
        FROM users u
        LEFT JOIN user_profiles p ON u.id = p.user_id
        LEFT JOIN ratings r ON u.id = r.user_id
        GROUP BY u.id
        ORDER BY u.id DESC
    ''').fetchall()
    db.close()
    return render_template('admin/users.html', users=users)

@app.route('/admin/users/<int:user_id>/delete', methods=['POST'])
@admin_required
def admin_delete_user(user_id):
    db = get_db()
    user = db.execute('SELECT name FROM users WHERE id=?', (user_id,)).fetchone()
    if user:
        db.execute('DELETE FROM ratings WHERE user_id=?', (user_id,))
        db.execute('DELETE FROM user_profiles WHERE user_id=?', (user_id,))
        db.execute('DELETE FROM users WHERE id=?', (user_id,))
        db.commit()
        flash(f'User "{user["name"]}" deleted.', 'success')
    db.close()
    return redirect(url_for('admin_users'))

# ── Ratings ───────────────────────────────────────────────────────────────────
@app.route('/admin/ratings')
@admin_required
def admin_ratings():
    db = get_db()
    ratings = db.execute('''
        SELECT u.name as user_name, o.label, o.clothing_type, o.occasion,
               r.rating, r.rated_at
        FROM ratings r
        JOIN users u ON r.user_id = u.id
        JOIN outfits o ON r.outfit_id = o.id
        ORDER BY r.rated_at DESC
    ''').fetchall()
    db.close()
    return render_template('admin/ratings.html', ratings=ratings)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
