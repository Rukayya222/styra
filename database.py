"""
Styra Database — Full outfit catalogue with real names, descriptions,
and smart tagging: body_type, modesty, skin_tone per outfit.

Run once:  py database.py
"""
import sqlite3, os

DB_PATH = os.path.join(os.path.dirname(__file__), 'styra.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS user_profiles (
        user_id INTEGER PRIMARY KEY REFERENCES users(id),
        skin_tone TEXT, body_type TEXT, clothing_type TEXT,
        modesty TEXT, occasion TEXT, climate TEXT, style_vibe TEXT,
        updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')

    c.execute('''DROP TABLE IF EXISTS outfits''')
    c.execute('''CREATE TABLE outfits (
        id            INTEGER PRIMARY KEY AUTOINCREMENT,
        clothing_type TEXT,
        occasion      TEXT,
        body_type     TEXT,   -- comma-separated best fits e.g. "hourglass,pear"
        modesty       TEXT,   -- modest | balanced | bold
        skin_tone     TEXT,   -- comma-separated e.g. "deep,tan,medium"
        image         TEXT,
        label         TEXT,
        description   TEXT,
        why_body      TEXT,   -- one-line reason this suits the body type(s)
        why_skin      TEXT    -- one-line reason this suits the skin tone(s)
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS ratings (
        user_id INTEGER REFERENCES users(id),
        outfit_id INTEGER REFERENCES outfits(id),
        rating INTEGER CHECK(rating BETWEEN 1 AND 5),
        rated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (user_id, outfit_id)
    )''')
    conn.commit()

    # ─────────────────────────────────────────────────────────────────────────
    # BODY TYPE LOGIC GUIDE (applied per outfit silhouette):
    #   hourglass  → fitted waist, A-line, wrap, defined silhouette
    #   pear       → flowy tops, A-line skirts, volume on top, dark bottoms
    #   apple      → empire waist, flowy/draped, kaftan, no tight middle
    #   rectangle  → peplum, belted, layered, creates curves
    #   petite     → fitted, vertical lines, monochrome, not too voluminous
    #
    # MODESTY GUIDE:
    #   modest   → full coverage, long sleeves, high neck, hijab-friendly
    #   balanced → mostly covered, some skin or fitted silhouette acceptable
    #   bold     → form-fitting, open neckline, shorter sleeves, expressive
    #
    # SKIN TONE COLOUR GUIDE:
    #   light/light_warm → soft neutrals, blush, pastels, dusty rose, camel
    #   medium/tan       → earth tones, terracotta, olive, mustard, warm red
    #   deep             → rich jewel tones, cobalt, emerald, burgundy, bold prints
    # ─────────────────────────────────────────────────────────────────────────

    outfits = [

        # ══════════════════════════════════════════════════════════════════
        # ENGLISH · CASUAL (13)
        # ══════════════════════════════════════════════════════════════════
        ("english","casual","hourglass,pear","modest","light,light_warm,medium",
         "images/english/casual/1_english_casual.jpg",
         "Floral Maxi Skirt & Turtleneck Set",
         "A rich brown ribbed turtleneck paired with a voluminous ivory floral maxi skirt. Modest, polished, and warm-weather ready.",
         "The full A-line skirt balances wider hips beautifully while the fitted top defines the waist.",
         "The warm brown and ivory tones glow against light and medium complexions."),

        ("english","casual","apple,rectangle","bold","medium,tan,deep",
         "images/english/casual/2_english_casual.jpg",
         "Wide-Leg Jeans & Graphic Tee",
         "A relaxed oversized graphic tee tucked loosely into wide-leg light-wash jeans. Effortless street style with a headband finish.",
         "The loose top skims the midsection and the wide-leg cut elongates and balances the frame.",
         "The bold white tee and light denim pop beautifully against tan and deep skin tones."),

        ("english","casual","rectangle,pear","balanced","medium,tan,deep",
         "images/english/casual/3_english_casual.jpg",
         "Red Oversized Shirt & Wide-Leg Jeans",
         "A bold red oversized button-down shirt layered over a white inner with wide-leg grey denim. Vibrant and easy to wear.",
         "The open shirt adds volume and visual interest at the top, creating shape on straighter frames.",
         "Red is a power colour that pops on medium to deep skin tones."),

        ("english","casual","hourglass,pear,petite","modest","light,light_warm,medium",
         "images/english/casual/4_english_casual.jpg",
         "Pleated Mauve Skirt & Cream Blouse",
         "A dusty mauve pleated maxi skirt paired with a cream button blouse and matching hijab. Clean, modest, and feminine.",
         "The pleated skirt flows over the hips gracefully, and the tucked blouse highlights the waist.",
         "Soft dusty mauve and cream complement lighter and medium skin tones perfectly."),

        ("english","casual","apple,rectangle,petite","modest","light,light_warm,medium",
         "images/english/casual/5_english_casual.jpg",
         "Camel Tiered Pinafore Dress",
         "A warm camel tiered pinafore sundress layered over a white long-sleeve top. Relaxed, modest hijab-friendly styling.",
         "The tiered skirt adds shape and movement while the layered top covers the arms without bulk.",
         "Warm camel tones are a dream on lighter, warm-undertoned complexions."),

        ("english","casual","hourglass,rectangle","balanced","medium,tan,deep",
         "images/english/casual/6_english_casual.jpg",
         "Burgundy Floral Chiffon Maxi",
         "A rich burgundy A-line maxi with a bold floral chiffon top and a bow-tied waist. Dramatic and feminine.",
         "The defined bow waist emphasises curves and the flared skirt flatters both hourglass and straighter shapes.",
         "Deep burgundy is stunning on medium to deep complexions, adding richness and depth."),

        ("english","casual","apple,petite,rectangle","modest","light,light_warm",
         "images/english/casual/7_english_casual.jpg",
         "White Broderie Anglaise Midi Dress",
         "A white puff-sleeve tiered midi dress with blue floral embroidery. Fresh, airy, and modestly covered.",
         "The empire waist and A-line silhouette skim the midsection while the puff sleeves add feminine volume.",
         "Crisp white and sky blue details are most striking against lighter complexions."),

        ("english","casual","hourglass,pear","balanced","light,light_warm,medium",
         "images/english/casual/8_english_casual.jpg",
         "Cow-Print Blouse & Brown Lace Skirt",
         "A cow-print button blouse with a full chocolate-brown lace maxi skirt and leather belt. Chic and editorial.",
         "The cinched waist on the lace skirt defines curves while the full skirt balances the hips.",
         "The warm brown and neutral palette harmonises with light and warm-medium complexions."),

        ("english","casual","petite,rectangle","modest","light,light_warm,medium",
         "images/english/casual/9_english_casual.jpg",
         "Black Puff-Sleeve Blouse & Gingham Skirt",
         "A structured black puff-sleeve blouse with a black and white gingham tiered skirt. Classic monochrome with a playful twist.",
         "Vertical contrast and a defined shoulder line create structure and height on petite or straight frames.",
         "Monochrome black and white is universally flattering and works beautifully on lighter complexions."),

        ("english","casual","pear,hourglass","modest","light,medium",
         "images/english/casual/10_english_casual.jpg",
         "Striped Blouse & Mauve Pinafore Skirt",
         "A striped long-sleeve blouse with shoulder bows paired with a full mauve pinafore skirt and white sneakers.",
         "The striped top draws the eye upward, balancing fuller hips, while the full skirt flows freely.",
         "The muted mauve and soft stripe palette is gentle and lovely on lighter complexions."),

        ("english","casual","rectangle,apple,petite","balanced","medium,tan,deep",
         "images/english/casual/11_english_casual.jpg",
         "Magenta Oversized Shirt & Wide-Leg Jeans",
         "A vibrant magenta oversized linen shirt loosely tucked into wide-leg light-wash jeans. Bold colour, relaxed fit.",
         "The oversized top skims the middle and the wide-leg jeans add a long, balanced silhouette.",
         "Vibrant magenta is electrifying against tan and deep skin tones."),

        ("english","casual","hourglass,pear","modest","light,light_warm,medium",
         "images/english/casual/12_english_casual.png",
         "Dusty Purple Stripe Midi & Suspender Skirt",
         "A lilac and white striped long-sleeve top layered under a dusty purple suspender maxi skirt. Modest and softly feminine.",
         "The suspender skirt defines the waist from the hips upward and the A-line skirt flows over curves.",
         "Dusty purple and lilac are particularly flattering on cooler, lighter skin tones."),

        ("english","casual","rectangle,petite","balanced","light,medium,tan",
         "images/english/casual/13_english_casual.jpg",
         "Blue Stripe Shirt & Black Wide-Leg Trousers",
         "A sky-blue oversized stripe shirt layered over a fitted black turtleneck with tailored black trousers.",
         "The vertical layering creates a long, clean silhouette that adds height and structure to straight frames.",
         "Cool blue and black is a crisp, clean combo that suits cool and neutral skin undertones."),

        # ══════════════════════════════════════════════════════════════════
        # ENGLISH · FORMAL (12)
        # ══════════════════════════════════════════════════════════════════
        ("english","formal","hourglass,petite","balanced","light,light_warm,medium",
         "images/english/formal/1_english_formal.jpg",
         "Ivory Square-Neck A-Line Gown",
         "A minimalist ivory structured A-line gown with a square neckline and cap sleeves. Timeless elegance.",
         "The square neck broadens the shoulder line and the A-line skirt perfectly flatters an hourglass figure.",
         "Ivory and cream glow warmly against light and warm-medium skin tones."),

        ("english","formal","rectangle,pear","balanced","medium,tan",
         "images/english/formal/2_english_formal.jpg",
         "Olive Blazer & Wide-Leg Trouser Set",
         "An olive-green structured blazer over a white shirt with cream wide-leg trousers and a tan bag.",
         "The blazer adds structure at the shoulders and the wide-leg trousers create a long, powerful silhouette.",
         "Olive and earth tones are richly complementary to medium and warm-tan skin tones."),

        ("english","formal","rectangle,petite","balanced","light,light_warm",
         "images/english/formal/3_english_formal.jpg",
         "Black Cardigan & Cream Tailored Trousers",
         "A fitted black V-neck cardigan layered over a white collar shirt with cream wide-leg trousers.",
         "The contrast of dark top and light trousers draws the eye and creates length on straighter or petite frames.",
         "The clean black and cream palette is crisp and elegant on cooler, lighter complexions."),

        ("english","formal","apple,hourglass","modest","medium,tan,deep",
         "images/english/formal/4_english_formal.jpg",
         "Black Wrap-Front Gown with Lantern Sleeves",
         "A floor-length black formal gown with a wrap front, crystal buttons at the hip, and bishop sleeves.",
         "The wrap front skims the midsection and the A-line flare flatters both full-figured and hourglass bodies.",
         "Classic black is universally flattering and especially powerful on deep and tan skin tones."),

        ("english","formal","hourglass,pear","modest","light,light_warm,medium",
         "images/english/formal/5_english_formal.jpg",
         "Ivory Blouse & Burgundy Chiffon Maxi Skirt",
         "A draped ivory long-sleeve blouse with a wine-burgundy floor-length chiffon skirt and gold chain belt.",
         "The defined waist created by the gold belt emphasises the waist; the full skirt balances the hips beautifully.",
         "The burgundy and ivory contrast is particularly luminous on warm light and medium skin tones."),

        ("english","formal","hourglass,pear","modest","medium,tan,deep",
         "images/english/formal/6_english_formal.jpg",
         "Black Top & Burgundy A-Line Chiffon Skirt",
         "A fitted black long-sleeve top with a burgundy tied A-line chiffon maxi skirt and quilted chain bag.",
         "The tied waist clearly defines the narrowest point and the full skirt elegantly balances the hips.",
         "Deep burgundy against a black top is richly dramatic and beautiful on medium to deep skin tones."),

        ("english","formal","apple,petite,rectangle","modest","medium,tan,deep",
         "images/english/formal/7_english_formal.jpg",
         "Plum Pleated Chiffon Gown with Sheer Sleeves",
         "A full-length plum pleated gown with sheer bishop sleeves and a mock high collar. Ethereal and dramatic.",
         "The empire waist and flowing pleated skirt skim the midsection while the sheer sleeves add coverage and grace.",
         "Plum and deep purple are gorgeous jewel tones that enrich medium, tan, and deep complexions."),

        ("english","formal","rectangle,petite","balanced","light,light_warm,medium",
         "images/english/formal/8_english_formal.jpg",
         "Camel Blazer, White Tee & Black Trousers",
         "A relaxed camel oversized blazer over a white T-shirt with black wide-leg trousers and crossbody bag.",
         "The blazer adds structured shoulders and the monochrome bottom creates a long, elongating line.",
         "Warm camel is soft and sophisticated against light, warm-undertoned skin."),

        ("english","formal","hourglass,pear","modest","medium,tan",
         "images/english/formal/9_english_formal.jpg",
         "Purple Knit Top & Plum Pleated Maxi Skirt",
         "A dusty purple round-neck knit top paired with a deep plum A-line pleated maxi skirt. Rich and warm.",
         "The fitted knit top defines the waist and the A-line pleated skirt gracefully balances fuller hips.",
         "The warm plum-to-purple tonal look is stunning against medium and golden tan complexions."),

        ("english","formal","apple,rectangle","modest","light,light_warm",
         "images/english/formal/10_english_formal.png",
         "All-White Wide-Leg Abaya Suit",
         "A striking all-white wide-sleeve abaya-style coat over white wide-leg trousers with silver accessories.",
         "The flowing coat silhouette is universally flattering — it skims all body types and creates a powerful, elegant presence.",
         "All-white is clean and luminous against lighter skin tones; the silver accessories add sparkle."),

        ("english","formal","hourglass,petite","modest","light,light_warm",
         "images/english/formal/11_english_formal.jpg",
         "Ivory White Structured Abaya Coat",
         "A long structured ivory abaya-style coat with wide sleeves, worn with white trousers. Minimal and luxurious.",
         "The structured silhouette defines the figure from top to bottom, ideal for hourglass and petite frames.",
         "Pure ivory is luminous and elegant against light, cool-toned complexions."),

        ("english","formal","hourglass,rectangle","bold","light,medium,tan",
         "images/english/formal/12_english_formal.jpg",
         "Ink Floral Puff-Sleeve Midi Dress",
         "An ivory midi dress with dramatic ink-sketched floral print and puff sleeves. Artistic, romantic, and editorial.",
         "The cinched waist creates an hourglass silhouette and the A-line skirt adds feminine movement.",
         "The soft ivory and grey floral palette is delicate and stunning against light to medium skin."),

        # ══════════════════════════════════════════════════════════════════
        # ENGLISH · OFFICE (6)
        # ══════════════════════════════════════════════════════════════════
        ("english","office","hourglass,pear","balanced","medium,tan,deep",
         "images/english/office/1_english_office.jpg",
         "Burgundy Waistcoat & Flared Maxi Skirt",
         "A structured burgundy waistcoat over a white shirt with a matching full burgundy maxi skirt. Commanding and polished.",
         "The fitted waistcoat defines the waist and the full skirt creates a beautiful hourglass-like silhouette.",
         "Burgundy is richly authoritative and glows on medium to deep complexions."),

        ("english","office","hourglass,petite","balanced","medium,tan,deep",
         "images/english/office/2_english_office.jpg",
         "Wine Double-Breasted Pinafore Dress",
         "A deep wine double-breasted sleeveless dress over a white long-sleeve blouse. Tailored and elegant.",
         "The double-breasted detail draws the eye inward, defining the waist, and the A-line skirt flatters the hips.",
         "Deep wine is particularly striking and polished on tan and deep skin tones."),

        ("english","office","rectangle,petite","modest","light,light_warm,medium",
         "images/english/office/3_english_office.jpg",
         "Grey Waistcoat & Pleated Maxi Skirt Set",
         "A charcoal grey V-neck waistcoat with a matching pleated maxi skirt, worn over a cream long-sleeve top.",
         "The defined waistcoat creates structure and the pleated skirt adds body to straighter frames.",
         "Cool grey is clean and professional on lighter, cool-undertoned complexions."),

        ("english","office","hourglass,apple","balanced","medium,tan",
         "images/english/office/4_english_office.jpg",
         "Grey Pinstripe Vest & Pencil Skirt",
         "A structured grey pinstripe belted vest over a powder-blue frilled blouse with a matching pencil skirt.",
         "The belt at the waist and fitted pencil skirt create structure while the flowing blouse softens the look.",
         "The cool grey and soft blue palette is crisp and flattering on warm medium to tan skin."),

        ("english","office","apple,rectangle","modest","light,light_warm,medium",
         "images/english/office/5_english_office.png",
         "Cream Button-Down & Wide-Leg Trousers",
         "A relaxed cream wide-sleeve button shirt tucked into cream wide-leg trousers with a thin belt.",
         "The monochrome tonal look creates a clean vertical line that elongates all body types.",
         "Head-to-toe cream is soft and luminous on lighter, warm-undertoned skin."),

        ("english","office","petite,rectangle","balanced","light,light_warm,medium",
         "images/english/office/6_english_office.jpg",
         "Grey Double-Button Vest Dress",
         "A soft grey double-button vest top over a white frill-neck blouse with a matching grey A-line skirt.",
         "The vest draws attention to the waist and the A-line skirt adds gentle feminine shape to straighter frames.",
         "Soft grey is understated and professional, ideal for cooler and neutral-toned complexions."),

        # ══════════════════════════════════════════════════════════════════
        # ENGLISH · WEDDING (13)
        # ══════════════════════════════════════════════════════════════════
        ("english","wedding","pear,hourglass","modest","light,light_warm,medium",
         "images/english/wedding/1_english_wedding.jpg",
         "Blush Rose Floral Chiffon Maxi",
         "A blush pink floral chiffon maxi dress with lace trim tiers, long sleeves, and a gold belt. Dreamy and romantic.",
         "The tiered A-line skirt and defined belt create a beautiful waist while the full skirt flows over the hips.",
         "Blush rose florals are ethereal and luminous on light and warm-medium skin tones."),

        ("english","wedding","hourglass,rectangle","modest","light,light_warm",
         "images/english/wedding/2_english_wedding.webp",
         "Navy Tulle Long-Sleeve Gown",
         "A floor-length navy blue gown with a sheer-sleeved bodice, full tulle skirt, and A-line silhouette.",
         "The structured bodice highlights the bust and waist while the full tulle skirt creates a dramatic hourglass silhouette.",
         "Navy blue is polished and elegant, complementing cool-toned lighter skin beautifully."),

        ("english","wedding","apple,rectangle","modest","light,light_warm,medium",
         "images/english/wedding/3_english_wedding.png",
         "Ice Blue Chiffon Tiered Gown",
         "An ice-blue chiffon layered gown with ruffle shoulders and a self-tie waist. Light and effortlessly elegant.",
         "The tiered ruffled layers skim the body gracefully, flatter the midsection, and are ideal for fuller or straight frames.",
         "Ice blue is fresh and cool, most luminous on lighter and cool-medium complexions."),

        ("english","wedding","hourglass,pear","modest","light,medium,tan",
         "images/english/wedding/4_english_wedding.jpg",
         "Midnight Navy Long-Sleeve Tulle Gown",
         "A formal midnight navy gown with sheer bishop sleeves, round neck, and a sweeping A-line tulle skirt.",
         "The fitted bodice defines the waist and the full A-line skirt flatters hourglass and pear shapes elegantly.",
         "Midnight navy is sophisticated and universally flattering across medium to lighter skin tones."),

        ("english","wedding","apple,petite","modest","light,light_warm,medium",
         "images/english/wedding/5_english_wedding.jpg",
         "Blush Chiffon Flutter-Sleeve Gown",
         "A soft blush chiffon gown with wide flutter sleeves and fine pin-tuck pleating on the bodice.",
         "The flutter sleeves add gentle volume to the arms and the flowing silhouette skims the figure gracefully.",
         "Soft blush is feminine and delicate, particularly flattering on warm-light and medium complexions."),

        ("english","wedding","hourglass,pear","modest","light,light_warm,medium",
         "images/english/wedding/6_english_wedding.jpg",
         "Sage Green Cape-Sleeve Embroidered Maxi",
         "A sage green chiffon maxi dress with flowing cape sleeves, self-tie waist, and delicate hem embroidery.",
         "The cape adds graceful arm coverage while the tied waist defines the figure beautifully.",
         "Sage green is fresh and cool-toned, glowing beautifully on lighter and medium complexions."),

        ("english","wedding","hourglass,pear,petite","modest","light,light_warm,medium",
         "images/english/wedding/7_english_wedding.jpg",
         "Powder Blue Floral Organza Ball Gown",
         "A breathtaking powder-blue organza ball gown with delicate all-over floral print and sheer bishop sleeves.",
         "The full ball gown skirt creates a dramatic hourglass silhouette and the sheer sleeves add modesty and romance.",
         "Powder blue is soft and magical, especially radiant on light and warm-medium skin tones."),

        ("english","wedding","rectangle,petite","balanced","light,medium",
         "images/english/wedding/8_english_wedding.webp",
         "Ice Blue Tweed Jacket & Flare Skirt Set",
         "A structured ice blue tweed cropped jacket with pearl buttons over a matching A-line midi skirt.",
         "The cropped jacket creates the illusion of curves and the A-line skirt adds shape to straighter or petite frames.",
         "Ice blue tweed is delicate and cool-toned, perfect for lighter and neutral-medium complexions."),

        ("english","wedding","hourglass,pear","modest","light,light_warm,medium",
         "images/english/wedding/9_english_wedding.jpg",
         "Sky Blue Tweed Co-Ord Set",
         "A sky blue textured tweed structured jacket with pearl buttons over a matching pleated midi skirt.",
         "The defined jacket waist and pleated A-line skirt together create an elegant, balanced silhouette.",
         "Sky blue is fresh and cool; pearl buttons add softness and suit lighter complexions beautifully."),

        ("english","wedding","apple,rectangle","modest","medium,tan,deep",
         "images/english/wedding/10_english_wedding.jpg",
         "Teal Ruffle-Neck Button-Down Gown",
         "A rich teal floor-length gown with dramatic layered ruffle collar, tiered bell sleeves, and pearl buttons.",
         "The high ruffle neck and flowing silhouette are universally flattering, skimming the body without clinging.",
         "Rich teal is a jewel tone that absolutely glows on medium, tan, and deep complexions."),

        ("english","wedding","hourglass,pear","balanced","light,light_warm,medium",
         "images/english/wedding/11_english_wedding.jpg",
         "Blush & Sage Printed Pleated Gown",
         "A floor-length pleated gown in blush and sage gradient print with wide flutter sleeves and a delicate waist belt.",
         "The fitted waist and full pleated skirt create a lovely silhouette; the flutter sleeves add romantic volume.",
         "The soft blush-to-sage palette is dreamlike on lighter, warm-toned complexions."),

        ("english","wedding","hourglass,apple","balanced","light,light_warm,medium",
         "images/english/wedding/12_english_wedding.jpg",
         "Dusty Rose Pleated Flutter-Sleeve Gown",
         "A dusty rose V-neck pleated maxi gown with butterfly flutter sleeves. Feminine, flowy, and romantic.",
         "The V-neck elongates the neckline, the flutter sleeves balance the bust, and the pleated skirt flows freely.",
         "Dusty rose is warmly feminine and radiant on light to medium skin tones."),

        ("english","wedding","hourglass,pear","bold","medium,tan,deep",
         "images/english/wedding/13_english_wedding.jpg",
         "Midnight Blue Dramatic Sleeve Gown",
         "A deep midnight navy fitted gown with a square-sweetheart neckline and dramatic cascading sheer sleeves.",
         "The fitted bodice celebrates the hourglass shape while the flowing sleeves add dramatic elegance.",
         "Midnight blue is bold and intense — a breathtaking combination with medium, tan, and deep complexions."),

        # ══════════════════════════════════════════════════════════════════
        # TRADITIONAL · CASUAL (10)
        # ══════════════════════════════════════════════════════════════════
        ("traditional","casual","apple,rectangle","modest","deep,tan",
         "images/traditional/casual/1_traditional_casual.jpg",
         "Green Geometric Ankara Kaftan",
         "A bold lime-green and black geometric Ankara kaftan with matching gele and wide sleeves. Effortlessly modest.",
         "The wide kaftan silhouette is generous and freeing, ideal for apple shapes and those who prefer relaxed coverage.",
         "Lime green and black is vibrant and striking on deep and tan skin tones."),

        ("traditional","casual","apple,rectangle","modest","medium,tan,deep",
         "images/traditional/casual/2_traditional_casual.jpg",
         "Gold & Ivory Embroidered Bubu Kaftan",
         "A flowing ivory and gold batik-embroidered bubu kaftan with wide batwing sleeves. Rich in cultural detail.",
         "The bubu silhouette is classically flattering for all body types, flowing freely without clinging.",
         "The warm ivory and gold palette lights up beautifully on medium to deep skin tones."),

        ("traditional","casual","rectangle,petite","modest","medium,tan,deep",
         "images/traditional/casual/3_english_casual.jpg",
         "Navy & Gold Teardrop Embroidered Kaftan",
         "A midnight navy kaftan with gold teardrop embroidery and teal lace flounce cuffs. Detailed and cultural.",
         "The vertical embroidery creates a long, clean line ideal for petite and straight-framed figures.",
         "Navy and gold is bold and regal — beautiful on medium to deep complexions."),

        ("traditional","casual","hourglass,pear","balanced","light,light_warm,medium",
         "images/traditional/casual/4_traditional_casual.jpg",
         "Mint Green Embellished Top & Ankara Skirt",
         "A pale mint chiffon embellished top with sequin trim over an Ankara print midi skirt. Delicate and festive.",
         "The flared top skims the hips and the Ankara skirt adds pattern and movement below the waist.",
         "Soft mint green and warm Ankara tones complement lighter warm-medium complexions beautifully."),

        ("traditional","casual","hourglass,pear","bold","medium,tan,deep",
         "images/traditional/casual/5_traditional_casual.jpg",
         "Purple Spiral Print Fitted Kaftan",
         "A form-fitting lavender and black spiral-print Ankara kaftan with wide lace-trimmed cuffs. Bold and eye-catching.",
         "The fitted cut celebrates curves, especially on hourglass and pear figures, while the print adds visual energy.",
         "The lavender and black contrast is vivid and powerful on tan and deep skin tones."),

        ("traditional","casual","apple,rectangle","modest","medium,tan,deep",
         "images/traditional/casual/6_traditional_casual.jpg",
         "Royal Purple Brocade Kaftan",
         "A striking royal purple Ankara brocade kaftan with dramatic wide pleated sleeves and silver embroidery.",
         "The flowing wide sleeves and relaxed body of the kaftan are universally flattering for fuller or straight builds.",
         "Royal purple is a rich jewel tone that is absolutely radiant on medium to deep skin tones."),

        ("traditional","casual","apple,rectangle","modest","light,medium,tan",
         "images/traditional/casual/7_traditional_casual.jpg",
         "Ivory & Navy Botanical Ankara Two-Piece",
         "A cream and navy botanical Ankara tunic top with navy lace cuffs over a matching straight skirt.",
         "The tunic top provides elegant coverage and the lace cuffs add detail without adding bulk.",
         "Ivory and navy is a clean, classic combination that suits a wide range of complexions."),

        ("traditional","casual","apple,pear","modest","medium,tan,deep",
         "images/traditional/casual/8_traditional_casual.jpg",
         "Yellow-Green Floral Mermaid Bubu",
         "A vibrant yellow-green and blue floral print mermaid-style bubu with wide sleeves and ruffle hem.",
         "The flared hem and draped bust are ideal for pear and apple shapes, adding volume at the hem and coverage at the top.",
         "The vivid yellow-green palette is bold and energetic, best suited to tan and deep complexions."),

        ("traditional","casual","apple,rectangle","modest","light,medium",
         "images/traditional/casual/9_traditional_casual.jpg",
         "Lilac & Green Adire Kaftan",
         "A soft lilac and emerald-green patterned Adire kaftan with scalloped lace centre trim.",
         "The relaxed kaftan silhouette provides full coverage and comfort for all figure types.",
         "Soft lilac and green tones are gentle and flattering on lighter and cool-medium skin tones."),

        ("traditional","casual","rectangle,petite","balanced","medium,tan,deep",
         "images/traditional/casual/10_traditional_casual.jpg",
         "Blue Batik Print Suit",
         "A structured blue batik Ankara long top with matching straight-leg trousers. Sleek and contemporary traditional.",
         "The matching two-piece creates a seamless long line that adds height and definition to petite or straight frames.",
         "Rich indigo blue Ankara print is vibrant and bold on medium to deep complexions."),

        # ══════════════════════════════════════════════════════════════════
        # TRADITIONAL · FORMAL (8)
        # ══════════════════════════════════════════════════════════════════
        ("traditional","formal","hourglass,pear","modest","medium,tan,deep",
         "images/traditional/formal/1_traditional_formal.jpg",
         "Sapphire Blue Lace & Ankara Formal Set",
         "A richly decorated sapphire blue Ankara top with intricate lace overlay, beaded collar, and matching maxi skirt.",
         "The structured bodice defines the waist while the maxi skirt flows gracefully over the hips.",
         "Sapphire blue and silver embellishment is regal and luminous on medium to deep skin tones."),

        ("traditional","formal","hourglass,petite","balanced","medium,tan,deep",
         "images/traditional/formal/2_traditional_formal.jpg",
         "Rust Orange Ankara Wrap Dress",
         "A form-fitting rust orange Ankara wrap dress with matching headwrap. Defined, warm, and elegant.",
         "The wrap silhouette creates a natural waist definition, ideal for hourglass and petite figures.",
         "Warm rust orange is earthly and powerful on golden tan and deep complexions."),

        ("traditional","formal","apple,rectangle","modest","medium,tan",
         "images/traditional/formal/3_traditional_formal.jpg",
         "Navy & Gold Abstract Kaftan with Fringe",
         "A dramatic navy and gold Ankara kaftan with bold abstract print, gold fringe bodice, and wide sleeves.",
         "The wide silhouette and statement fringe draw the eye upward, flattering fuller figures and straight builds.",
         "Navy and gold Ankara is powerful and warm on medium and golden-tan complexions."),

        ("traditional","formal","apple,rectangle","modest","light,medium,tan",
         "images/traditional/formal/4_traditional_formal.jpg",
         "Pink & Gold Metallic Aso-Oke Bubu",
         "A luxurious pink and gold metallic Aso-Oke kaftan with gold chain trim and matching gele. Owambe royalty.",
         "The flowing kaftan silhouette is universally flattering and the gold trim adds a regal, celebratory touch.",
         "Pink and gold tones are delicate and beautiful on warm light-to-medium and rich tan complexions."),

        ("traditional","formal","rectangle,petite","balanced","medium,tan,deep",
         "images/traditional/formal/5_traditional_formal.jpg",
         "Mustard Yellow Ankara Midi Dress",
         "A mustard yellow Ankara midi dress with a fitted bodice and flared lace skirt panel. Clean and structured.",
         "The fitted waist creates shape on straight figures and the flared hem adds movement and femininity.",
         "Mustard yellow is a warm earth tone that glows beautifully on tan and medium complexions."),

        ("traditional","formal","hourglass,pear","bold","medium,tan,deep",
         "images/traditional/formal/6_traditional_formal.jpg",
         "Teal & Gold Peplum Ankara Set",
         "A bold teal and gold Ankara two-piece with a dramatic peplum top and matching fitted maxi skirt.",
         "The peplum top defines the waist and adds volume at the hip, beautifully flattering hourglass and pear figures.",
         "Teal and gold Ankara is vivid and commanding on medium to deep complexions."),

        ("traditional","formal","hourglass,petite","modest","light,light_warm,medium",
         "images/traditional/formal/7_traditional_formal.jpg",
         "Blush Pink Embroidered Column Dress",
         "A blush pink fitted column dress with a cascading vine embroidery detail and wide bell sleeves.",
         "The column silhouette with defined sleeves is clean and elegant, ideal for hourglass and petite builds.",
         "Blush pink with floral embroidery is romantic and delicate on lighter and warm-medium complexions."),

        ("traditional","formal","hourglass,pear","bold","medium,tan,deep",
         "images/traditional/formal/8_traditional_formal.jpg",
         "Brown & Silver Floral Ankara Mermaid Gown",
         "A stunning brown and silver Ankara mermaid gown with 3D floral appliqué and a dramatic train. Show-stopping.",
         "The mermaid cut celebrates the figure from bust to knee and flares into a dramatic train, ideal for hourglass curves.",
         "Brown and silver is rich and regal — absolutely striking on tan and deep complexions."),

        # ══════════════════════════════════════════════════════════════════
        # TRADITIONAL · OFFICE (4)
        # ══════════════════════════════════════════════════════════════════
        ("traditional","office","apple,rectangle","modest","medium,tan,deep",
         "images/traditional/office/1_traditional_office.jpg",
         "Black & White Adire Circle-Print Kaftan",
         "A structured black Adire kaftan with bold white circle pattern and a V-neck line. Professional and cultural.",
         "The kaftan's structured drape and vertical neckline are flattering for fuller and straight builds.",
         "The strong black and white contrast is graphic and powerful on all skin tones, especially deep and tan."),

        ("traditional","office","apple,pear","modest","light,medium,tan",
         "images/traditional/office/2_traditional_office.jpg",
         "Brown Abstract Ankara Cape & Skirt Set",
         "A wide-sleeved brown and blue abstract Ankara cape top over a matching midi skirt. Artistic and professional.",
         "The cape skims over the hips and midsection beautifully, making it a graceful choice for apple and pear figures.",
         "Warm brown and dusty blue tones are earthy and sophisticated on lighter and medium complexions."),

        ("traditional","office","rectangle,petite","modest","medium,tan,deep",
         "images/traditional/office/3_traditional_office.jpg",
         "Green Tropical Ankara Maxi Dress",
         "A teal and green tropical leaf Ankara maxi dress with a notched V-neck and three-quarter sleeves.",
         "The vertical print and clean silhouette create a long, structured line that adds height to petite and straight frames.",
         "Vibrant green is energetic and fresh, most striking on tan and deep complexions."),

        ("traditional","office","apple,rectangle","modest","medium,tan,deep",
         "images/traditional/office/4_traditional_office.jpg",
         "Pink & Grey Geometric Bubu",
         "A relaxed pink and grey geometric Ankara bubu with short sleeves. Easy to wear for a full day in the office.",
         "The bubu silhouette is comfortable and inclusive — it flows freely without clinging to any specific area.",
         "Pink and grey Ankara is warm and approachable on medium to deep skin tones."),

        # ══════════════════════════════════════════════════════════════════
        # TRADITIONAL · WEDDING (9)
        # ══════════════════════════════════════════════════════════════════
        ("traditional","wedding","rectangle,petite","balanced","light,medium",
         "images/traditional/wedding/1_traditional_wedding.jpg",
         "Green & Pink Ankara Ruffle-Cuff Midi",
         "A fitted sage green and pink Ankara top with ruffle bell cuffs and a matching midi skirt. Festive and detailed.",
         "The fitted structured top adds shape to straight frames while the ruffle cuffs add visual interest.",
         "Sage green and pink Ankara is warm and festive on light and medium complexions."),

        ("traditional","wedding","hourglass,pear","bold","medium,tan,deep",
         "images/traditional/wedding/2_traditional_wedding.jpg",
         "Forest Green Ankara Ruffle-Sleeve Gown",
         "A deep forest green Ankara mermaid gown with dramatic ruffle sleeves and V-neck bodice overlay.",
         "The mermaid silhouette celebrates hourglass and pear figures, and the ruffled sleeves draw the eye upward.",
         "Forest green is a bold jewel tone that is incredibly striking on tan and deep skin tones."),

        ("traditional","wedding","hourglass,petite","modest","light,light_warm,medium",
         "images/traditional/wedding/3_traditional_wedding.jpg",
         "Ice Blue Floral Embroidered Peplum Set",
         "An ice blue Ankara peplum top with floral embroidery and matching flared skirt. Delicate and ceremonial.",
         "The peplum creates a defined waist and the flared skirt adds elegant movement, flattering hourglass and petite builds.",
         "Ice blue florals are cool and ethereal, most beautiful on lighter and cool-medium complexions."),

        ("traditional","wedding","apple,rectangle","modest","light,medium",
         "images/traditional/wedding/4_traditional_wedding.jpg",
         "Blush Pink Embroidered Ankara Kaftan",
         "A flowing blush pink satin-feel Ankara kaftan with circle embroidery and scalloped sleeves.",
         "The full kaftan skims all figures gracefully and the embroidery draws the eye beautifully.",
         "Soft blush pink with silver embroidery is gentle and radiant on lighter and medium complexions."),

        ("traditional","wedding","apple,pear","modest","medium,tan,deep",
         "images/traditional/wedding/5_traditional_wedding.jpg",
         "Yellow-Green & Purple Sparkle Ankara Cape",
         "A dazzling yellow-green and purple sparkle Ankara cape gown with scalloped overlay. Energetic and festive.",
         "The cape overlay skims the hips and the flowing skirt underneath flatters apple and pear shapes.",
         "The electric yellow-green and purple is explosive and joyful on tan and deep complexions."),

        ("traditional","wedding","rectangle,petite","balanced","medium,tan,deep",
         "images/traditional/wedding/6_traditional_wedding.jpg",
         "Coral & Brown Ankara Fitted Maxi",
         "A coral pink and brown Ankara fitted maxi dress with puff sleeves and a high boat neckline.",
         "The fitted cut adds definition to straight and petite frames, and the puff sleeves add proportion at the shoulder.",
         "Warm coral and brown is a beautiful earth palette on medium to deep skin tones."),

        ("traditional","wedding","hourglass,pear","modest","medium,tan,deep",
         "images/traditional/wedding/7_traditional_wedding.jpg",
         "Cream & Coral 3D Floral Lace Cape Gown",
         "A cream Ankara fitted gown with 3D coral floral appliqué and a matching lace cape. Exquisite ceremonial wear.",
         "The fitted gown defines the hourglass silhouette beautifully and the cape adds modest coverage with drama.",
         "Cream and coral florals are warm and vivid — stunning on tan and deep complexions."),

        ("traditional","wedding","hourglass,petite","balanced","medium,tan,deep",
         "images/traditional/wedding/8_traditional_wedding.jpg",
         "Sky Blue Guipure Lace Two-Piece",
         "A sky blue guipure lace structured corset top with a matching full skirt. Elegant Northern Nigerian bridal style.",
         "The corset top defines the waist and the full skirt creates an elegant A-line balance, ideal for hourglass and petite.",
         "Sky blue lace is cool and luminous, beautiful on medium to deep complexions."),

        ("traditional","wedding","hourglass,pear","bold","medium,tan,deep",
         "images/traditional/wedding/9_traditional_wedding.jpg",
         "Blue & Orange Floral Ankara Column Gown",
         "A fitted blue and orange Ankara floral column gown with a wide shimmering cape overlay. Regal and dramatic.",
         "The fitted column celebrates the figure while the cape overlay adds grandeur — perfect for weddings and owambe.",
         "The cobalt blue and warm orange Ankara is bold and electrifying on tan and deep complexions."),
    ]

    c.executemany('''
        INSERT INTO outfits
        (clothing_type, occasion, body_type, modesty, skin_tone, image, label, description, why_body, why_skin)
        VALUES (?,?,?,?,?,?,?,?,?,?)
    ''', outfits)

    conn.commit()
    conn.close()
    print(f"Database created with {len(outfits)} outfits.")

if __name__ == '__main__':
    init_db()
