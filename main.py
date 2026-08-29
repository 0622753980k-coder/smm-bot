import telebot, sqlite3, requests, time, os, threading
from datetime import datetime
from telebot.types import ReplyKeyboardMarkup as RK, KeyboardButton as KB, InlineKeyboardMarkup as IK, InlineKeyboardButton as IB
from flask import Flask

TOKEN = '8904483870:AAF_O56epbVmcEkldoLO0Xdd49SALTqFYJg'
ADMIN_ID = 8467707826
GRIZZLY_API_KEY = '3335af0d250efb73bdc40ebf82fa42dd'

SMM_API_KEY = '5f44258668604a14d48bd99270c1f8f4'
SMM_API_URL = 'https://top4smm.com/api.php'

K_C = {"RUB": {"r": 140.0, "t": 0}, "USD": {"r": 12700.0, "t": 0}}

def g_k(c, d):
    if time.time() - K_C[c]["t"] > 3600:
        try:
            r = requests.get(f"https://cbu.uz/uz/arkhiv-kursov-valyut/json/{c}/", timeout=3).json()
            K_C[c]["r"] = float(r[0]['Rate']); K_C[c]["t"] = time.time()
        except: K_C[c]["r"] = d
    return K_C[c]["r"]

bot = telebot.TeleBot(TOKEN); usr_st, tmp_dt = {}, {}

E_PHON="📱"; E_BOX="📹"; E_STAR="✨"; E_USER="👥"; E_1USR="👤"; E_OK="✅"; E_CHRT="📊"; E_PEN="✍️"; E_ERR="❌"; E_DOWN="⬇️"; E_CARD="💳"; E_CART="🛒"; E_BAG="🛍"; E_MONY="💵"; E_LINK="🔗"; E_TIME="⏳"; E_NUM="🔢"; E_DATE="📅"; E_BELL="🔔"; E_CROWN="👑"

def init_db():
    c = sqlite3.connect('b.db')
    c.execute('CREATE TABLE IF NOT EXISTS u (id INTEGER PRIMARY KEY, b INTEGER DEFAULT 0)')
    try: c.execute('ALTER TABLE u ADD COLUMN r INTEGER DEFAULT 0')
    except: pass
    c.execute('CREATE TABLE IF NOT EXISTS o (id INTEGER PRIMARY KEY AUTOINCREMENT, u INTEGER, oid TEXT, l TEXT, q INTEGER, d TEXT, s TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS a (id INTEGER PRIMARY KEY AUTOINCREMENT, t TEXT, d TEXT)') 
    c.execute('CREATE TABLE IF NOT EXISTS s (k TEXT PRIMARY KEY, v TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS ad (id INTEGER PRIMARY KEY)')
    c.execute("INSERT OR IGNORE INTO s (k,v) VALUES ('card', '8600 0000 0000 0000')")
    c.execute("INSERT OR IGNORE INTO s (k,v) VALUES ('admin', '@SizningUserneyim')")
    c.execute("INSERT OR IGNORE INTO s (k,v) VALUES ('m_chan', '')")
    for x, y in [('p_y1','190000'), ('p_y2','120000'), ('p_y3','60000'), ('p_1func','50000'), ('p_2func','100000'), ('p_adsense','30000'), ('m_nomer','20'), ('m_yt_sub','20'), ('m_yt_watch','20'), ('m_smm','20')]: 
        c.execute("INSERT OR IGNORE INTO s (k,v) VALUES (?, ?)", (x, y))
    c.commit(); c.close()
init_db()

def is_adm(uid): return uid == ADMIN_ID or (sqlite3.connect('b.db').cursor().execute("SELECT id FROM ad WHERE id=?", (uid,)).fetchone() is not None)
def g_adms(): return list(set([ADMIN_ID] + [x[0] for x in sqlite3.connect('b.db').cursor().execute("SELECT id FROM ad").fetchall()]))
def adm_msg(txt, rm=None):
    for a in g_adms():
        try: bot.send_message(a, txt, reply_markup=rm, parse_mode='HTML')
        except: pass

def g_bal(id): return (sqlite3.connect('b.db').cursor().execute("SELECT b FROM u WHERE id=?", (id,)).fetchone() or [0])[0]
def g_c(t): return (sqlite3.connect('b.db').cursor().execute("SELECT COUNT(id) FROM a WHERE t=?", (t,)).fetchone() or [0])[0]
def g_set(k): return (sqlite3.connect('b.db').cursor().execute("SELECT v FROM s WHERE k=?", (k,)).fetchone() or [""])[0]
def u_set(k, v): c=sqlite3.connect('b.db'); c.execute("UPDATE s SET v=? WHERE k=?", (v, k)); c.commit(); c.close()
def u_bal(id, amt):
    c = sqlite3.connect('b.db'); c.execute("INSERT OR IGNORE INTO u (id,b,r) VALUES (?,0,0)", (id,))
    c.execute("UPDATE u SET b=b+? WHERE id=?", (amt, id)); c.commit(); c.close()

def get_m(k):
    try: return 1.0 + (int(g_set(k)) / 100.0)
    except: return 1.20

def g_smm():
    return [
        {'service': '8316', 'name': 'YT Watchtime (Arzon)', 'category': 'youtube watch time hour', 'rate': '3.0', 'min': 100, 'max': 4000, 'description': "⚠️ DIQQAT: Kanalda kamida 60 daqiqalik (1 soatlik) video bo'lishi shart!\n\n🔹 Uderjanie: Har bir prosmotrda videoningiz 60+ daqiqa ko'riladi.\n🔹 Tezlik: Sekinroq (Kuniga 100-300 soat).\n🔹 Kafolat: Yo'q (Tushish ehtimoli bor)."},
        {'service': '8317', 'name': 'YT Watchtime (Tezkor)', 'category': 'youtube watch time hour', 'rate': '6.0', 'min': 100, 'max': 4000, 'description': "⚠️ DIQQAT: Kanalda kamida 60 daqiqalik (1 soatlik) video bo'lishi shart!\n\n🔹 Uderjanie: Har bir prosmotrda videoningiz 60+ daqiqa to'xtovsiz ko'riladi.\n🔹 Tezlik: Kuniga 300-500 soat yig'iladi.\n🔹 Kafolat: 30 kunlik tiklash kafolati bor."},
        {'service': '8318', 'name': 'YT Watchtime (Premium)', 'category': 'youtube watch time hour', 'rate': '9.0', 'min': 100, 'max': 4000, 'description': "⚠️ DIQQAT: Kanalda kamida 15+ daqiqalik video bo'lishi yetarli!\n\n🔹 Uderjanie: Videoningiz 15-30 daqiqa atrofida ko'riladi (High Retention).\n🔹 Tezlik: Tezkor (Kuniga 500-1000 soat).\n🔹 Kafolat: Umrbod (Non-drop, umuman tushmaydi)."},
        {'service': '6597', 'name': 'YT Obunachi (Arzon)', 'category': 'youtube sub follower', 'rate': '5.0', 'min': 10, 'max': 1000, 'description': "🔹 Tezlik: Kuniga 30-50 ta qo'shiladi.\n🔹 Sifat: Arzon aralash obunachilar.\n🔹 Kafolat: Yo'q (Tushish ehtimoli bor)."},
        {'service': '6598', 'name': 'YT Obunachi (Kafolatli)', 'category': 'youtube sub follower', 'rate': '10.0', 'min': 10, 'max': 1000, 'description': "🔹 Tezlik: Kuniga 50-100 ta qo'shiladi.\n🔹 Sifat: Yaxshi.\n🔹 Kafolat: 30 kun kafolat (tushsa to'ldirib beriladi)."},
        {'service': '6599', 'name': 'YT Obunachi (Premium)', 'category': 'youtube sub follower', 'rate': '15.0', 'min': 10, 'max': 1000, 'description': "🔹 Tezlik: Kuniga 100-200 ta tezkor.\n🔹 Sifat: Haqiqiy faol foydalanuvchilar.\n🔹 Kafolat: Umrbod (Tushib ketmaydi)."},
        {'service': '101', 'name': 'YT View (Arzon)', 'category': 'youtube view', 'rate': '1.0', 'min': 100, 'max': 100000, 'description': "🔹 Uderjanie: Tasodifiy (Odatda 1-3 daqiqa).\n🔹 Tezlik: Kuniga 1000-5000 ta.\n🔹 Sifat: Oddiy prosmotrlar, videoni trendga chiqarmaydi."},
        {'service': '102', 'name': 'YT View (Tezkor)', 'category': 'youtube view', 'rate': '2.0', 'min': 100, 'max': 100000, 'description': "🔹 Uderjanie: High Retention (Videoning katta qismi ko'riladi).\n🔹 Tezlik: Kuniga 10K-50K ta tezkor."},
        {'service': '103', 'name': 'YT View (Premium)', 'category': 'youtube view', 'rate': '3.5', 'min': 100, 'max': 100000, 'description': "🔹 Uderjanie: Juda baland (High Retention).\n🔹 Sifat: 100% haqiqiy, videoni tavsiyalarga (rekomendatsiya) chiqishiga yordam beradi."},
        {'service': '111', 'name': 'YT Like (Arzon)', 'category': 'youtube like', 'rate': '2.0', 'min': 10, 'max': 10000, 'description': "🔹 Sifat: Arzon layklar. Tushib ketish xavfi bor."},
        {'service': '112', 'name': 'YT Like (Sifatli)', 'category': 'youtube like', 'rate': '5.0', 'min': 10, 'max': 10000, 'description': "🔹 Sifat: Haqiqiy akkauntlardan layklar. 30 kun kafolat."},
        {'service': '113', 'name': 'YT Like (Premium)', 'category': 'youtube like', 'rate': '10.9', 'min': 10, 'max': 10000, 'description': "🔹 Sifat: Eng yuqori sifatli umrbod kafolatli layklar (Drop 0%)."},
        {'service': '121', 'name': 'YT Comment (Arzon)', 'category': 'youtube comment', 'rate': '15.0', 'min': 10, 'max': 1000, 'description': "🔹 Sifat: Oddiy inglizcha izohlar (Good, Nice video va h.k)."},
        {'service': '122', 'name': 'YT Comment (Ijobiy)', 'category': 'youtube comment', 'rate': '30.0', 'min': 10, 'max': 1000, 'description': "🔹 Sifat: Videoning mavzusiga doir maxsus ijobiy izohlar."},
        {'service': '123', 'name': 'YT Comment (Custom)', 'category': 'youtube comment', 'rate': '65.0', 'min': 10, 'max': 1000, 'description': "🔹 Sifat: Eng sifatli Premium izohlar."},
        {'service': '201', 'name': 'TG Sub (Arzon)', 'category': 'telegram sub follower', 'rate': '0.5', 'min': 100, 'max': 10000, 'description': "🔹 Sifat: Aralash obunachilar (Bot/Real). Tushish ehtimoli baland."},
        {'service': '202', 'name': 'TG Sub (Sifatli)', 'category': 'telegram sub follower', 'rate': '1.0', 'min': 100, 'max': 10000, 'description': "🔹 Sifat: O'rtacha faollikdagi foydalanuvchilar. 30 kunlik kafolat."},
        {'service': '203', 'name': 'TG Sub (Premium)', 'category': 'telegram sub follower', 'rate': '2.0', 'min': 100, 'max': 10000, 'description': "🔹 Sifat: Haqiqiy o'zbek/rus faol obunachilar. Tushmaydi."},
        {'service': '211', 'name': 'TG View (Arzon)', 'category': 'telegram view', 'rate': '0.05', 'min': 100, 'max': 50000, 'description': "🔹 Oddiy arzon ko'rishlar (prosmotr)."},
        {'service': '212', 'name': 'TG View (Tezkor)', 'category': 'telegram view', 'rate': '0.1', 'min': 100, 'max': 50000, 'description': "🔹 Tezkor ko'rishlar."},
        {'service': '213', 'name': 'TG View (Premium)', 'category': 'telegram view', 'rate': '0.2', 'min': 100, 'max': 50000, 'description': "🔹 Haqiqiy foydalanuvchilardan sifatli prosmotr."},
        {'service': '301', 'name': 'IG Sub (Arzon)', 'category': 'instagram sub follower', 'rate': '0.5', 'min': 100, 'max': 10000, 'description': "🔹 Sifat: Bot obunachilar. Kafolatsiz."},
        {'service': '302', 'name': 'IG Sub (Kafolatli)', 'category': 'instagram sub follower', 'rate': '1.0', 'min': 100, 'max': 10000, 'description': "🔹 Sifat: Yaxshi sifatli obunachilar (30 kun kafolat)."},
        {'service': '303', 'name': 'IG Sub (Premium)', 'category': 'instagram sub follower', 'rate': '1.5', 'min': 100, 'max': 10000, 'description': "🔹 Sifat: Haqiqiy profillar, umrbod kafolat (Non-Drop)."},
        {'service': '401', 'name': 'TT Sub (Arzon)', 'category': 'tiktok sub follower', 'rate': '0.5', 'min': 100, 'max': 10000, 'description': "🔹 Sifat: Aralash TikTok obunachilari."},
        {'service': '402', 'name': 'TT Sub (Sifatli)', 'category': 'tiktok sub follower', 'rate': '1.0', 'min': 100, 'max': 10000, 'description': "🔹 Sifat: Yaxshi sifat. Videoni rekomendatsiyaga olib chiqishga yordam beradi."},
        {'service': '403', 'name': 'TT Sub (Premium)', 'category': 'tiktok sub follower', 'rate': '2.0', 'min': 100, 'max': 10000, 'description': "🔹 Sifat: Eng yuqori sifat, kafolatli obunachilar."}
]def get_gz_pr(sc=None, cid=None):
    try:
        url = f"https://api.grizzlysms.com/stubs/handler_api.php?api_key={GRIZZLY_API_KEY}&action=getPrices"
        if sc: url += f"&service={sc}"
        if cid: url += f"&country={cid}"
        r = requests.get(url, timeout=10).json(); p = {}
        if sc and not cid:
            for c_id, s_data in r.items():
                if type(s_data) is dict and sc in s_data:
                    v = s_data[sc].get('cost') or s_data[sc].get('price')
                    if v: p[str(c_id)] = float(v)
        elif cid and not sc:
            target = r[str(cid)] if str(cid) in r else r
            for s_id, s_data in target.items():
                if type(s_data) is dict:
                    v = s_data.get('cost') or s_data.get('price')
                    if v: p[str(s_id)] = float(v)
        return p
    except: return {}

def req_gz(sc, cid):
    try:
        r = requests.get(f"https://api.grizzlysms.com/stubs/handler_api.php?api_key={GRIZZLY_API_KEY}&action=getNumber&service={sc}&country={cid}").text
        if "ACCESS_NUMBER" in r: return {"s": True, "id": r.split(':')[1], "n": r.split(':')[2]}
        return {"s": False, "m": r}
    except Exception as e: return {"s": False, "m": str(e)}

def c_sub(uid):
    ch = g_set('m_chan')
    if not ch or is_adm(uid): return True
    try: return bot.get_chat_member(ch, uid).status in ['member', 'administrator', 'creator']
    except: return True

def req_sub(cid, uid):
    ch = g_set('m_chan'); mk = IK(row_width=1).add(IB("➕ Obuna bo'lish", url=f"https://t.me/{ch.replace('@','')}"), IB("🔄 Tekshirish", callback_data="ck_sub"))
    try: bot.send_message(cid, f"⚠️ <b>Botdan foydalanish uchun kanalga a'zo bo'ling!</b>", reply_markup=mk, parse_mode='HTML')
    except: pass

@bot.callback_query_handler(func=lambda c: c.data == "ck_sub")
def ck_s(c):
    if c_sub(c.from_user.id): 
        try: bot.delete_message(c.message.chat.id, c.message.message_id)
        except: pass
        try: bot.send_message(c.message.chat.id, f"{E_OK} <b>Rahmat! Menyuga marhamat:</b>", reply_markup=m_menu(c.from_user.id), parse_mode='HTML')
        except: pass
    else: bot.answer_callback_query(c.id, "❌ Hali a'zo bo'lmadingiz!", show_alert=True)

def m_menu(uid):
    m = RK(resize_keyboard=True).row(KB("📦 Xizmatlar"), KB("📱 Nomer olish")).row(KB("🔴 Tayyor Kanallar"), KB("💳 Hisob to'ldirish")).row(KB("🛒 Buyurtmalarim"), KB("👤 Mening hisobim")).row(KB("💬 Murojaat"))
    if is_adm(uid): m.add(KB("👑 Admin Panel"))
    return m

def a_menu(): return RK(resize_keyboard=True).row(KB("➕ 2006-2009"), KB("➕ 2010-2019")).row(KB("➕ 2025-2026"), KB("👥 Statistika")).row(KB("💳 Karta o'zgartirish"), KB("⚙️ Narxlarni o'zgartirish")).row(KB("📈 Foizlarni o'zgartirish"), KB("📣 Kanal ulash")).row(KB("✉️ Xabarnoma"), KB("👮‍♂️ Admin qo'shish")).row(KB("💬 Murojaat o'zgartirish"), KB("Bosh sahifa 🔝"))

@bot.message_handler(commands=['start'])
def st(m):
    uid = m.from_user.id; ref = 0; args = m.text.split()
    if len(args) > 1 and args[1].isdigit():
        ref = int(args[1]); ref = 0 if ref == uid else ref
    c = sqlite3.connect('b.db'); exists = c.execute("SELECT id FROM u WHERE id=?", (uid,)).fetchone()
    if not exists:
        c.execute("INSERT INTO u (id,b,r) VALUES (?,0,?)", (uid, ref)); c.commit()
        if ref:
            try: bot.send_message(ref, f"{E_BELL} <b>Sizning havolangiz orqali do'stingiz kirdi!</b>\nU hisob to'ldirganda sizga 5% bonus.", parse_mode='HTML')
            except: pass
    c.close()
    if not c_sub(uid): return req_sub(m.chat.id, uid)
    usr_st[uid] = None
    txt = f"👋 <b>Assalomu alaykum! {m.from_user.first_name}</b>\n\n🤖 <b>@{bot.get_me().username}</b> ga xush kelibsiz!\n\n<blockquote>Ushbu bot orqali siz barcha platformalarga, shuningdek:\n✈️ Telegram,\n📸 Instagram,\n🎵 TikTok,\n🔴 YouTube\nva boshqa tarmoqlarga sifatli va hamyonbop <b>NAKRUTKA</b> va boshqa xizmatlardan foydalanishingiz mumkin 🛍\n\n<b>Bundan tashqari botda:</b>\n📱 Virtual Nomerlar xaridi\n🔴 Tayyor YouTube kanallar va Adsense ham mavjud!</blockquote>"
    try: bot.send_message(m.chat.id, txt, reply_markup=m_menu(uid), parse_mode='HTML')
    except: pass

@bot.message_handler(func=lambda m: m.text == "Bosh sahifa 🔝")
def bs(m):
    if not c_sub(m.from_user.id): return req_sub(m.chat.id, m.from_user.id)
    usr_st[m.from_user.id] = None; bot.send_message(m.chat.id, "Asosiy menyu:", reply_markup=m_menu(m.from_user.id))

@bot.message_handler(func=lambda m: m.text == "👤 Mening hisobim")
def mc(m):
    if not c_sub(m.from_user.id): return req_sub(m.chat.id, m.from_user.id)
    i = sqlite3.connect('b.db').cursor().execute("SELECT b, (SELECT COUNT(id) FROM u WHERE r=?) FROM u WHERE id=?", (m.from_user.id, m.from_user.id)).fetchone()
    bot.send_message(m.chat.id, f"{E_USER} <b>Profilingiz:</b>\n\n{E_1USR} <b>ID:</b> <code>{m.from_user.id}</code>\n{E_MONY} <b>Balans:</b> <b>{i[0] if i else 0}</b> so'm\n\n🎁 <b>Referal tizimi (5% bonus):</b>\n🔗 <code>https://t.me/{bot.get_me().username}?start={m.from_user.id}</code>\n👥 Taklif qilinganlar: <b>{i[1] if i else 0} ta</b>", parse_mode='HTML')

@bot.message_handler(func=lambda m: m.text in ["💬 Murojaat", "🛒 Buyurtmalarim"])
def mb(m):
    if not c_sub(m.from_user.id): return req_sub(m.chat.id, m.from_user.id)
    if m.text == "💬 Murojaat": bot.send_message(m.chat.id, f"{E_PEN} <b>Admin:</b>\n{g_set('admin')}", parse_mode='HTML')
    else:
        r = sqlite3.connect('b.db').cursor().execute("SELECT oid, s, q, l, d FROM o WHERE u=? ORDER BY id DESC LIMIT 5", (m.from_user.id,)).fetchall()
        if not r: return bot.send_message(m.chat.id, f"{E_ERR} Buyurtmalar yo'q.", parse_mode='HTML')
        t = f"{E_STAR} <b>Oxirgi buyurtmalar:</b>\n\n"
        for x in r: t += f"{E_1USR} <b>ID:</b> <code>{x[0]}</code>\n{E_PEN} <b>Holat:</b> {x[1]}\n{E_NUM} <b>Miqdor:</b> {x[2]}\n{E_LINK} <b>Link:</b> {x[3]}\n{E_DATE} <b>Vaqt:</b> {x[4]}\n— — —\n"
        bot.send_message(m.chat.id, t, parse_mode='HTML', disable_web_page_preview=True)

@bot.message_handler(func=lambda m: m.text == "👑 Admin Panel" and is_adm(m.from_user.id))
def ap(m): bot.send_message(m.chat.id, f"{E_CROWN} <b>Admin Panel</b>\nBalans berish: <code>/addbalance ID SUMMA</code>", reply_markup=a_menu(), parse_mode='HTML')

@bot.message_handler(func=lambda m: is_adm(m.from_user.id) and m.text in ["👥 Statistika", "📣 Kanal ulash", "✉️ Xabarnoma", "⚙️ Narxlarni o'zgartirish", "📈 Foizlarni o'zgartirish", "👮‍♂️ Admin qo'shish", "💳 Karta o'zgartirish", "💬 Murojaat o'zgartirish"])
def adm_bts(m):
    if m.text == "👥 Statistika":
        u = sqlite3.connect('b.db').cursor().execute("SELECT COUNT(id), SUM(b) FROM u").fetchone()
        bot.send_message(m.chat.id, f"{E_CHRT} <b>Statistika:</b>\nA'zolar: <b>{u[0]}</b>\nBalanslar: <b>{u[1] or 0}</b>\nKanallar: 06-09(<b>{g_c('y1')}</b>), 10-19(<b>{g_c('y2')}</b>), 25-26(<b>{g_c('y3')}</b>)", parse_mode='HTML')
    elif m.text == "📣 Kanal ulash":
        usr_st[m.from_user.id] = "set_chan"; bot.send_message(m.chat.id, f"{E_PEN} Majburiy obuna kanalini <b>@bilan</b> yuboring\n(O'chirish uchun 0 yozing)\n<i>Hozirgi: {g_set('m_chan')}</i>", parse_mode='HTML')
    elif m.text == "✉️ Xabarnoma":
        usr_st[m.from_user.id] = "brd_msg"; bot.send_message(m.chat.id, f"{E_PEN} <b>Xabarni yuboring</b> (/cancel - bekor qilish):", parse_mode='HTML')
    elif m.text == "⚙️ Narxlarni o'zgartirish":
        mk = IK(row_width=1).add(IB(f"06-09: {g_set('p_y1')}", callback_data="edp_p_y1"), IB(f"10-19: {g_set('p_y2')}", callback_data="edp_p_y2"), IB(f"25-26: {g_set('p_y3')}", callback_data="edp_p_y3"), IB(f"1 funksiya: {g_set('p_1func')}", callback_data="edp_p_1func"), IB(f"2 funksiya: {g_set('p_2func')}", callback_data="edp_p_2func"), IB(f"Adsense: {g_set('p_adsense')}", callback_data="edp_p_adsense"))
        bot.send_message(m.chat.id, "⚙️ <b>Qaysi xizmat narxini o'zgartirasiz?</b>", reply_markup=mk, parse_mode='HTML')
    elif m.text == "📈 Foizlarni o'zgartirish":
        mk = IK(row_width=1).add(IB(f"📱 Nomerlar: {g_set('m_nomer')}%", callback_data="edp_m_nomer"), IB(f"🔴 YT Obunachi: {g_set('m_yt_sub')}%", callback_data="edp_m_yt_sub"), IB(f"⏱ YT Watchtime: {g_set('m_yt_watch')}%", callback_data="edp_m_yt_watch"), IB(f"🛍 Boshqa SMM: {g_set('m_smm')}%", callback_data="edp_m_smm"))
        bot.send_message(m.chat.id, "⚙️ <b>Qaysi xizmat ustama foizini o'zgartirasiz?</b>\nFaqat foiz raqamini yozing (Masalan: 30)", reply_markup=mk, parse_mode='HTML')
    elif m.text == "👮‍♂️ Admin qo'shish":
        usr_st[m.from_user.id] = "add_adm"; bot.send_message(m.chat.id, f"{E_PEN} <b>Yangi admin ID:</b>", parse_mode='HTML')
    elif m.text == "💳 Karta o'zgartirish":
        usr_st[m.from_user.id] = "set_c"; bot.send_message(m.chat.id, f"{E_PEN} <b>Yangi karta:</b>\n<i>Hozirgi: {g_set('card')}</i>", parse_mode='HTML')
    elif m.text == "💬 Murojaat o'zgartirish":
        usr_st[m.from_user.id] = "set_a"; bot.send_message(m.chat.id, f"{E_PEN} <b>Yangi admin (@bilan):</b>\n<i>Hozirgi: {g_set('admin')}</i>", parse_mode='HTML')

@bot.callback_query_handler(func=lambda c: c.data.startswith("edp_"))
def ed_p(c): usr_st[c.from_user.id] = f"setp_{c.data[4:]}"; bot.send_message(c.message.chat.id, f"{E_PEN} <b>Yangi qiymatni raqamda yuboring:</b>", parse_mode='HTML')

@bot.message_handler(func=lambda m: str(usr_st.get(m.from_user.id)) in ["set_chan", "brd_msg", "add_adm", "set_c", "set_a"] or str(usr_st.get(m.from_user.id)).startswith("setp_"))
def adm_st(m):
    st = usr_st[m.from_user.id]
    if st == "set_chan":
        u_set('m_chan', "" if m.text == "0" else m.text); usr_st[m.from_user.id] = None; bot.send_message(m.chat.id, f"{E_OK} Kanal saqlandi!", parse_mode='HTML')
    elif st == "brd_msg":
        usr_st[m.from_user.id] = None
        if m.text == "/cancel": return bot.send_message(m.chat.id, "Bekor qilindi.")
        u = sqlite3.connect('b.db').cursor().execute("SELECT id FROM u").fetchall(); c = 0
        bot.send_message(m.chat.id, f"{E_TIME} Yuborilmoqda..."); 
        for x in u:
            try: bot.copy_message(x[0], m.chat.id, m.message_id); c += 1; time.sleep(0.05)
            except: pass
        bot.send_message(m.chat.id, f"{E_OK} Xabar {c} kishiga yuborildi!")
    elif st.startswith("setp_"):
        if not m.text.isdigit(): return bot.send_message(m.chat.id, "Raqam kiriting!")
        u_set(st[5:], m.text); usr_st[m.from_user.id] = None; bot.send_message(m.chat.id, f"{E_OK} Saqlandi!", parse_mode='HTML')
    elif st == "add_adm":
        if not m.text.isdigit(): return bot.send_message(m.chat.id, "Faqat ID!")
        sqlite3.connect('b.db').cursor().execute("INSERT OR IGNORE INTO ad (id) VALUES (?)", (int(m.text),)).connection.commit(); usr_st[m.from_user.id] = None; bot.send_message(m.chat.id, f"{E_OK} Admin qo'shildi!", parse_mode='HTML')
    elif st == "set_c": u_set('card', m.text); usr_st[m.from_user.id] = None; bot.send_message(m.chat.id, f"{E_OK} Saqlandi!", parse_mode='HTML')
    elif st == "set_a": u_set('admin', m.text); usr_st[m.from_user.id] = None; bot.send_message(m.chat.id, f"{E_OK} Saqlandi!", parse_mode='HTML')

@bot.message_handler(func=lambda m: m.text in ["➕ 2006-2009", "➕ 2010-2019", "➕ 2025-2026"] and is_adm(m.from_user.id))
def adc(m): usr_st[m.from_user.id] = f"wac_{'y1' if '2006' in m.text else ('y2' if '2010' in m.text else 'y3')}"; bot.send_message(m.chat.id, f"{E_PEN} <b>Kanal yuboring (Login:Parol):</b>", parse_mode='HTML')

@bot.message_handler(func=lambda m: str(usr_st.get(m.from_user.id)).startswith("wac_"))
def sav_ac(m):
    if m.text in ["📦 Xizmatlar", "Bosh sahifa 🔝", "👑 Admin Panel"]: usr_st[m.from_user.id] = None; return bot.send_message(m.chat.id, f"{E_ERR} Xato!", parse_mode='HTML')
    sqlite3.connect('b.db').cursor().execute("INSERT INTO a (t, d) VALUES (?, ?)", (usr_st[m.from_user.id].split('_')[1], m.text)).connection.commit(); usr_st[m.from_user.id] = None; bot.send_message(m.chat.id, f"{E_OK} Kanal qo'shildi!", parse_mode='HTML')

@bot.message_handler(commands=['addbalance'])
def ad_b(m):
    if is_adm(m.from_user.id) and len(m.text.split()) > 2: a = m.text.split(); u_bal(int(a[1]), int(a[2])); bot.send_message(int(a[1]), f"🎁 <b>{a[2]} so'm</b> qo'shildi!", parse_mode='HTML'); bot.send_message(m.chat.id, f"{E_OK} Bajarildi")

@bot.message_handler(func=lambda m: m.text == "💳 Hisob to'ldirish")
def tu(m):
    if not c_sub(m.from_user.id): return req_sub(m.chat.id, m.from_user.id)
    bot.send_message(m.chat.id, "💵 <b>Qancha to'ldirasiz?</b>\n⬇️ <b>Min: 1000 so'm</b>", parse_mode='HTML'); usr_st[m.from_user.id] = "wa"

@bot.message_handler(func=lambda m: usr_st.get(m.from_user.id) == "wa")
def ra(m):
    if not m.text.isdigit(): return bot.send_message(m.chat.id, "‼️ Raqam kiriting.", parse_mode='HTML')
    a = int(m.text)
    if a < 1000: return bot.send_message(m.chat.id, "⬇️ Min 1000 so'm.", parse_mode='HTML')
    usr_st[m.from_user.id] = None
    RASM = "https://i.postimg.cc/c4ptYvg0/IMG-20260829-155347-374.jpg" 
    txt = f"➡️ <b>Karta:</b> <code>{g_set('card')}</code>\n\n💵 Miqdor: <b>{a} so'm</b>\n✅ To'lov qilib tasdiqlang!"
    mk = IK(row_width=1).add(IB("✅ To'lov qildim", callback_data=f"dn_{a}"), IB("❌ Bekor qilish", callback_data="cancel_pay"))
    try: bot.send_photo(m.chat.id, RASM, caption=txt, reply_markup=mk, parse_mode='HTML')
    except: bot.send_message(m.chat.id, txt, reply_markup=mk, parse_mode='HTML')

@bot.callback_query_handler(func=lambda c: c.data == 'cancel_pay')
def cancel_pay(c):
    try: bot.delete_message(c.message.chat.id, c.message.message_id)
    except: pass
    bot.send_message(c.message.chat.id, "❌ <b>Bekor qilindi.</b>", parse_mode='HTML')

@bot.callback_query_handler(func=lambda c: c.data.startswith('dn_'))
def dn(c):
    try: bot.delete_message(c.message.chat.id, c.message.message_id)
    except: pass
    a, u = int(c.data.split('_')[1]), c.from_user.id
    bot.send_message(u, f"{E_TIME} Tekshirilmoqda...", parse_mode='HTML')
    adm_msg(f"{E_BELL} <b>To'lov kutilmoqda:</b>\n{E_1USR} Mijoz: <code>{u}</code>\n{E_MONY} Summa: {a}", rm=IK().add(IB("✅ Tasdiqlash", callback_data=f"ap_{u}_{a}"), IB("❌ Rad", callback_data=f"rj_{u}_{a}")))

@bot.callback_query_handler(func=lambda c: c.data.startswith('ap_') or c.data.startswith('rj_'))
def ad_d(c):
    try: bot.delete_message(c.message.chat.id, c.message.message_id)
    except: pass
    p = c.data.split('_'); u, a = int(p[1]), int(p[2])
    if p[0] == "ap":
        u_bal(u, a); bot.send_message(u, f"{E_OK} <b>Balans to'ldirildi:</b> {a} so'm", parse_mode='HTML')
        ref = sqlite3.connect('b.db').cursor().execute("SELECT r FROM u WHERE id=?", (u,)).fetchone()[0]
        if ref:
            bns = int(a * 0.05)
            if bns > 0:
                u_bal(ref, bns)
                try: bot.send_message(ref, f"🎁 <b>Referal bonus!</b>\nDo'stingiz to'lov qildi. Sizga {bns} so'm berildi!", parse_mode='HTML')
                except: pass
    else: bot.send_message(u, f"{E_ERR} To'lov rad etildi.", parse_mode='HTML')

C_LIST = [("0", "Rossiya 🇷🇺"), ("1", "Ukraina 🇺🇦"), ("2", "Qozog'iston 🇰🇿"), ("3", "Xitoy 🇨🇳"), ("4", "Filippin 🇵🇭"), ("5", "Myanma 🇲🇲"), ("6", "Indoneziya 🇮🇩"), ("7", "Malayziya 🇲🇾"), ("12", "AQSh 🇺🇸"), ("16", "Angliya 🇬🇧"), ("31", "JAR 🇿🇦"), ("34", "Estoniya 🇪🇪")]
S_LIST = [("vk", "VKontakte"), ("go", "Google"), ("fb", "Facebook"), ("ig", "Instagram"), ("dt", "TikTok"), ("wa", "WhatsApp")]

@bot.callback_query_handler(func=lambda c: c.data == "none")
def none_cb(c): bot.answer_callback_query(c.id)

@bot.message_handler(func=lambda m: m.text == "📱 Nomer olish")
def nm(m):
    if not c_sub(m.from_user.id): return req_sub(m.chat.id, m.from_user.id)
    bot.send_message(m.chat.id, f"{E_PHON} <b>Tarmoqni tanlang:</b> {E_DOWN}", reply_markup=IK(row_width=2).add(IB("📞 Telegram", callback_data="tg_p_0"), IB("☎️ Boshqa Tarmoqlar", callback_data="ot_p_0")), parse_mode='HTML')

@bot.callback_query_handler(func=lambda c: c.data.startswith("tg_p_"))
def tg_pg(c):
    page = int(c.data.split('_')[2]); pr = get_gz_pr(sc="tg"); gk = g_k("USD", 12700); mv = get_m('m_nomer'); mk = IK(row_width=2); btns = []
    for cid, cname in C_LIST[page*8 : page*8+8]:
        cost = pr.get(cid)
        if cost: btns.append(IB(f"{cname} - {int(cost * gk * mv)}", callback_data=f"buy_tg_{cid}_{int(cost * gk * mv)}"))
        else: btns.append(IB(f"{cname} (Yo'q)", callback_data="none"))
    for i in range(0, len(btns), 2): mk.row(*btns[i:i+2])
    tp = (len(C_LIST) + 7) // 8
    mk.row(IB("⬅️", callback_data=f"tg_p_{page-1}") if page > 0 else IB("➖", callback_data="none"), IB(f"{page+1}/{tp}", callback_data="none"), IB("➡️", callback_data=f"tg_p_{page+1}") if page < tp - 1 else IB("➖", callback_data="none"))
    mk.add(IB("⭐ TOP DAVLATLAR", callback_data="tg_top"))
    try: bot.edit_message_text(f"⁉️ <b>Davlatni tanlang:</b>", c.message.chat.id, c.message.message_id, reply_markup=mk, parse_mode='HTML')
    except: pass

@bot.callback_query_handler(func=lambda c: c.data == "tg_top")
def tg_top(c):
    pr = get_gz_pr(sc="tg"); gk = g_k("USD", 12700); mv = get_m('m_nomer'); valid_c = []
    for cid, cname in C_LIST:
        if cid in pr: valid_c.append((cid, cname, pr[cid]))
    mk = IK(row_width=2); btns = []
    for cid, cname, p_usd in sorted(valid_c, key=lambda x: x[2])[:6]:
        btns.append(IB(f"{cname} - {int(p_usd * gk * mv)}", callback_data=f"buy_tg_{cid}_{int(p_usd * gk * mv)}"))
    for i in range(0, len(btns), 2): mk.row(*btns[i:i+2])
    mk.add(IB("🔙 Orqaga", callback_data="tg_p_0"))
    try: bot.edit_message_text("⭐ <b>TOP 6 davlat:</b>", c.message.chat.id, c.message.message_id, reply_markup=mk, parse_mode='HTML')
    except: pass
    @bot.callback_query_handler(func=lambda c: c.data.startswith("ot_p_"))
def ot_pg(c):
    page = int(c.data.split('_')[2]); mk = IK(row_width=2); btns = []
    for cid, cname in C_LIST[page*8 : page*8+8]: btns.append(IB(f"{cname}", callback_data=f"ot_c_{cid}"))
    for i in range(0, len(btns), 2): mk.row(*btns[i:i+2])
    tp = (len(C_LIST) + 7) // 8
    mk.row(IB("⬅️", callback_data=f"ot_p_{page-1}") if page > 0 else IB("➖", callback_data="none"), IB(f"{page+1}/{tp}", callback_data="none"), IB("➡️", callback_data=f"ot_p_{page+1}") if page < tp - 1 else IB("➖", callback_data="none"))
    mk.add(IB("⭐ TOP DAVLATLAR", callback_data="ot_top"))
    try: bot.edit_message_text(f"⁉️ <b>Davlatni tanlang:</b>", c.message.chat.id, c.message.message_id, reply_markup=mk, parse_mode='HTML')
    except: pass

@bot.callback_query_handler(func=lambda c: c.data == "ot_top")
def ot_top(c):
    top_c = [("0", "Rossiya 🇷🇺"), ("1", "Ukraina 🇺🇦"), ("2", "Qozog'iston 🇰🇿"), ("12", "AQSh 🇺🇸"), ("16", "Angliya 🇬🇧"), ("6", "Indoneziya 🇮🇩")]
    mk = IK(row_width=2); btns = []
    for cid, cname in top_c: btns.append(IB(f"{cname}", callback_data=f"ot_c_{cid}"))
    for i in range(0, len(btns), 2): mk.row(*btns[i:i+2])
    mk.add(IB("🔙 Orqaga", callback_data="ot_p_0"))
    try: bot.edit_message_text("⭐ <b>TOP davlatlar:</b>", c.message.chat.id, c.message.message_id, reply_markup=mk, parse_mode='HTML')
    except: pass

@bot.callback_query_handler(func=lambda c: c.data.startswith("ot_c_"))
def ot_c_sel(c):
    cid = c.data.split('_')[2]; cname = dict(C_LIST).get(cid, "Noma'lum")
    try: bot.edit_message_text(f"{E_TIME} Yuklanmoqda...", c.message.chat.id, c.message.message_id, parse_mode='HTML')
    except: pass
    pr = get_gz_pr(cid=cid); gk = g_k("USD", 12700); mv = get_m('m_nomer')
    if not pr:
        try: bot.edit_message_text(f"{E_ERR} <b>Nomerlar yo'q.</b>", c.message.chat.id, c.message.message_id, reply_markup=IK().add(IB("🔙 Orqaga", callback_data="ot_p_0")), parse_mode='HTML')
        except: pass
        return
    txt = f"📞 <b>Tarmoqni tanlang:</b>\n♻️ <b>Davlat: {cname}</b>\n\n"; mk = IK(row_width=2); btns = []
    for sc, sname in S_LIST:
        cost = pr.get(sc)
        if cost:
            price = int(cost * gk * mv); txt += f"🔹 <b>{sname}</b> - {price} so'm\n"
            btns.append(IB(f"{sname} - ({price})", callback_data=f"buy_{sc}_{cid}_{price}"))
        else: btns.append(IB(f"{sname} (Yo'q)", callback_data="none"))
    for i in range(0, len(btns), 2): mk.row(*btns[i:i+2])
    mk.add(IB("🔙 Orqaga", callback_data="ot_p_0"))
    try: bot.edit_message_text(txt, c.message.chat.id, c.message.message_id, reply_markup=mk, parse_mode='HTML')
    except: pass

@bot.callback_query_handler(func=lambda c: c.data.startswith("buy_"))
def pb(c):
    p = c.data.split('_'); sc, cid, pr = p[1], p[2], int(p[3])
    if g_bal(c.from_user.id) < pr: return bot.answer_callback_query(c.id, "🔴 Pul kam!", show_alert=True)
    try: bot.edit_message_text(f"{E_TIME} Olinmoqda...", c.message.chat.id, c.message.message_id, parse_mode='HTML')
    except: pass
    r = req_gz(sc, cid)
    if r["s"]:
        u_bal(c.from_user.id, -pr); mk = IK().add(IB("🔎 SMS olish", callback_data=f"ck_{r['id']}_{pr}"), IB("❌ Bekor", callback_data=f"cl_{r['id']}_{pr}"))
        try: bot.edit_message_text(f"{E_OK} <b>Xarid qilindi!</b>\n{E_PHON} <code>{r['n']}</code>\nYechildi: {pr} so'm", c.message.chat.id, c.message.message_id, reply_markup=mk, parse_mode='HTML')
        except: pass
    else: 
        try: bot.edit_message_text(f"{E_ERR} Xato: {r['m']}", c.message.chat.id, c.message.message_id, parse_mode='HTML')
        except: pass

@bot.callback_query_handler(func=lambda c: c.data.startswith("ck_") or c.data.startswith("cl_"))
def ck_cl(c):
    p = c.data.split('_')
    if p[0] == "ck":
        try: st = requests.get(f"https://api.grizzlysms.com/stubs/handler_api.php?api_key={GRIZZLY_API_KEY}&action=getStatus&id={p[1]}").text
        except: st = ""
        if "WAIT" in st: bot.answer_callback_query(c.id, "⏳ Kuting...", show_alert=True)
        elif "OK" in st:
            try: bot.edit_message_text(f"{E_OK} <b>Kod:</b> <code>{st.split(':')[1]}</code>", c.message.chat.id, c.message.message_id, parse_mode='HTML')
            except: pass
        else: bot.answer_callback_query(c.id, "Bekor qilingan", show_alert=True)
    else:
        try:
            st = requests.get(f"https://api.grizzlysms.com/stubs/handler_api.php?api_key={GRIZZLY_API_KEY}&action=getStatus&id={p[1]}").text
            if "OK" in st: return bot.answer_callback_query(c.id, "SMS keldi, bekor qilib bo'lmaydi!", show_alert=True)
            cancel_req = requests.get(f"https://api.grizzlysms.com/stubs/handler_api.php?api_key={GRIZZLY_API_KEY}&action=setStatus&status=8&id={p[1]}").text
            if "ACCESS_CANCEL" in cancel_req:
                u_bal(c.from_user.id, int(p[2]))
                try: bot.edit_message_text(f"{E_OK} <b>Bekor qilindi.</b> Pul qaytdi: {p[2]}", c.message.chat.id, c.message.message_id, parse_mode='HTML')
                except: pass
            else: bot.answer_callback_query(c.id, f"Sayt xatosi: {cancel_req}", show_alert=True)
        except: bot.answer_callback_query(c.id, "Xato", show_alert=True)

@bot.message_handler(func=lambda m: m.text in ["🔴 Tayyor Kanallar", "📦 Xizmatlar"])
def yt_smm(m):
    if not c_sub(m.from_user.id): return req_sub(m.chat.id, m.from_user.id)
    if "Kanallar" in m.text:
        mk = IK(row_width=1)
        for k, n in [("y1", "🔴 [ESKI] 2006-09"), ("y2", "🔴 [ESKI] 2010-19"), ("y3", "🔴 [YANGI] 2025-26")]: mk.add(IB(f"{n} - {g_set('p_'+k)} so'm", callback_data=f"by_{k}"))
        mk.add(IB(f"🛠 1 funksiya - {g_set('p_1func')} so'm", callback_data="by_n_1func"), IB(f"🛠 2 funksiya - {g_set('p_2func')} so'm", callback_data="by_n_2func"), IB(f"💰 Adsense - {g_set('p_adsense')} so'm", callback_data="by_n_adsense"))
        bot.send_message(m.chat.id, f"🔴 <b>YouTube:</b>", reply_markup=mk, parse_mode='HTML')
    else:
        mk = IK(row_width=2).add(IB("✈️ Telegram", callback_data="mp_tg"), IB("📸 Instagram", callback_data="mp_ig"), IB("🔴 YouTube", callback_data="mp_yt"), IB("🎵 TikTok", callback_data="mp_tt"))
        bot.send_message(m.chat.id, f"{E_BOX} <b>Tarmoq:</b>", reply_markup=mk, parse_mode='HTML')

@bot.callback_query_handler(func=lambda c: c.data.startswith("by_"))
def b_yt(c):
    t = c.data.split('_')
    if t[1] == "n":
        pr = int(g_set('p_' + t[2]))
        if g_bal(c.from_user.id) < pr: return bot.answer_callback_query(c.id, "🔴 Pul kam!", show_alert=True)
        u_bal(c.from_user.id, -pr); usr_st[c.from_user.id] = f"wn_{t[2]}"
        if t[2] in ['1func','2func']: txt = "🛠 <b>Ma'lumot yuboring (Yo'nalish/Link):</b>"
        else: txt = "💰 <b>Adsense uchun quyidagi ma'lumotlarni yuboring:</b>\n\n👤 Ism-familiya:\n📞 Telefon raqam:\n📍 To'liq manzil:\n📮 Pochta indeksi:"
        try: bot.edit_message_text(txt, c.message.chat.id, c.message.message_id, parse_mode='HTML')
        except: pass
    else:
        pr = int(g_set('p_' + t[1]))
        if g_bal(c.from_user.id) < pr: return bot.answer_callback_query(c.id, "🔴 Pul kam!", show_alert=True)
        u_bal(c.from_user.id, -pr); acc = sqlite3.connect('b.db').cursor().execute("SELECT id, d FROM a WHERE t=? LIMIT 1", (t[1],)).fetchone()
        yoriqnoma = "⚠️ <b>Foydalanish bo‘yicha yo‘riqnoma</b>\n\nBloklanib qolmaslik uchun birinchi sutkada keskin harakatlar qilmang.\n\n<b>Muhim:</b>\n• Parolni darrov o‘zgartirmang\n• Uni 24 soatdan keyin, o‘sha qurilma / IP orqali o‘zgartiring\n• Telefon raqamini darrov bog‘lamang\n• Faqat 7 kundan keyin qo‘shing\n• Zaxira pochtani darrov o‘zgartirish mumkin — bu xavfsiz\n• Birinchi soatlarda parol, IP yoki qurilmani keskin almashtirish — bloklanish xavfi"
        if acc:
            sqlite3.connect('b.db').cursor().execute("DELETE FROM a WHERE id=?", (acc[0],)).connection.commit()
            try: bot.edit_message_text(f"{E_OK} <b>Xarid qilindi!</b>\n\n🎁 <b>KANAL:</b>\n<code>{acc[1]}</code>\n\n{yoriqnoma}", c.message.chat.id, c.message.message_id, parse_mode='HTML')
            except: pass
            adm_msg(f"{E_BELL} Kanal sotildi: {c.from_user.id}")
        else:
            sqlite3.connect('b.db').cursor().execute("INSERT INTO o (u,oid,l,q,d,s) VALUES (?,?,?,?,?,?)", (c.from_user.id, "YT", t[1], 1, datetime.now().strftime("%Y.%m.%d %H:%M:%S"), "Kutmoqda")).connection.commit()
            try: bot.edit_message_text(f"{E_OK} <b>Kuting! Admin yuboradi.</b>", c.message.chat.id, c.message.message_id, parse_mode='HTML')
            except: pass
            adm_msg(f"{E_BELL} <b>Kanal buyurtmasi:</b> {c.from_user.id}", rm=IK().add(IB("📤 Yuborish", callback_data=f"snd_{c.from_user.id}")))

@bot.message_handler(func=lambda m: str(usr_st.get(m.from_user.id)).startswith("wn_"))
def sv_nch(m):
    t = usr_st[m.from_user.id].split('_')[1]
    if m.text in ["📦 Xizmatlar", "Bosh sahifa 🔝"]:
        u_bal(m.from_user.id, int(g_set('p_'+t))); usr_st[m.from_user.id] = None; return bot.send_message(m.chat.id, "Bekor qildindi. Pul qaytdi.")
    sqlite3.connect('b.db').cursor().execute("INSERT INTO o (u,oid,l,q,d,s) VALUES (?,?,?,?,?,?)", (m.from_user.id, t, "Buyurtma", 1, datetime.now().strftime("%Y.%m.%d %H:%M:%S"), "Kutmoqda")).connection.commit()
    usr_st[m.from_user.id] = None; bot.send_message(m.chat.id, f"{E_OK} <b>Qabul qilindi!</b>", parse_mode='HTML')
    adm_msg(f"{E_BELL} <b>Buyurtma:</b>\n{m.from_user.id}\n{m.text}", rm=IK().add(IB("📤 Yuborish", callback_data=f"snd_{m.from_user.id}")))

@bot.callback_query_handler(func=lambda c: c.data.startswith("snd_"))
def rq_snd(c): usr_st[c.from_user.id] = f"fw_{c.data.split('_')[1]}"; bot.send_message(c.message.chat.id, f"{E_PEN} <b>Ma'lumot (Login/Parol) kiriting:</b>", parse_mode='HTML')

@bot.message_handler(func=lambda m: str(usr_st.get(m.from_user.id)).startswith("fw_"))
def fw_m(m):
    uid = usr_st[m.from_user.id].split('_')[1]; usr_st[m.from_user.id] = None
    yoriqnoma = "⚠️ <b>Foydalanish bo‘yicha yo‘riqnoma</b>\n\nBloklanib qolmaslik uchun birinchi sutkada keskin harakatlar qilmang.\n\n<b>Muhim:</b>\n• Parolni darrov o‘zgartirmang\n• Uni 24 soatdan keyin, o‘sha qurilma / IP orqali o‘zgartiring\n• Telefon raqamini darrov bog‘lamang\n• Faqat 7 kundan keyin qo‘shing\n• Zaxira pochtani darrov o‘zgartirish mumkin — bu xavfsiz\n• Birinchi soatlarda parol, IP yoki qurilmani keskin almashtirish — bloklanish xavfi"
    try: 
        bot.send_message(uid, f"🎁 <b>Tayyor:</b>\n<code>{m.text}</code>\n\n{yoriqnoma}", parse_mode='HTML'); bot.send_message(m.chat.id, "Yuborildi")
        sqlite3.connect('b.db').cursor().execute("UPDATE o SET s='Bajarildi ✅' WHERE u=?", (uid,)).connection.commit()
    except: bot.send_message(m.chat.id, "Xato!")

@bot.callback_query_handler(func=lambda c: c.data.startswith("mp_"))
def smc(c):
    p = c.data.split('_')[1]; mk = IK(row_width=1)
    if p == 'yt': opts = [("sub", "🔴 Obunachilar"), ("watch", "⏱ Watchtime (Soat)"), ("view", "👁 Ko'rishlar (Views)"), ("like", "👍 Layklar"), ("comment", "💬 Kommentariya")]
    else: opts = [("sub", "👥 Obuna (Followers)"), ("view", "👁 Ko'rish (Views)"), ("like", "❤️ Layk"), ("comment", "💬 Kommentariya")]
    for cid, cn in opts: mk.add(IB(cn, callback_data=f"mc_{p}_{cid}"))
    try: bot.edit_message_text(f"{E_DOWN} <b>Qaysi xizmat turini tanlaysiz?</b>", c.message.chat.id, c.message.message_id, reply_markup=mk, parse_mode='HTML')
    except: pass

@bot.callback_query_handler(func=lambda c: c.data.startswith("mc_"))
def n_ss(c):
    _, p, cid = c.data.split('_')
    s = g_smm()
    
    net_kws = {"yt": ["youtube", "yt"], "ig": ["instagram", "ig"], "tg": ["telegram", "tg"], "tt": ["tiktok", "tt"]}
    srv_kws = {"sub": ["sub", "follower", "obuna"], "watch": ["watch", "time", "hour"], "view": ["view", "prosmotr"], "like": ["like"], "comment": ["comment"]}
    
    nk = net_kws.get(p, [""])
    sk = srv_kws.get(cid, [""])
    
    f = []
    for x in s:
        txt = (str(x.get('name','')) + " " + str(x.get('category',''))).lower()
        if any(n in txt for n in nk) and any(k in txt for k in sk): f.append(x)
                
    if not f:
        try: bot.edit_message_text(f"⚠️ Ushbu bo'lim bo'yicha xizmat topilmadi.", c.message.chat.id, c.message.message_id, reply_markup=IK().add(IB("🔙 Orqaga", callback_data=f"mp_{p}")), parse_mode='HTML')
        except: pass
        return
    
    def safe_float(v):
        try: return float(str(v).replace(',','.'))
        except: return 0.0
        
    f = sorted(f, key=lambda x: safe_float(x.get('rate', '0')))
    sl = []
    if len(f) > 0: sl.append(("🥈 Arzon", f[0]))
    if len(f) > 1: sl.append(("🥇 Tezkor", f[1]))
    if len(f) > 2: sl.append(("💎 Premium", f[2]))
    
    mv = get_m('m_yt_sub') if cid == 'sub' else (get_m('m_yt_watch') if cid == 'watch' else get_m('m_smm'))
    gk = g_k("USD", 12700); mk = IK(row_width=1); txt = f"🛍 <b>Sifatni tanlang:</b>\n\n"
    
    for l, srv in sl:
        pr = int(safe_float(srv.get('rate', '0')) * gk * mv)
        txt += f"🔹 <b>{l}</b> - {pr} so'm (1000 ta)\nMin: {srv.get('min')} | Max: {srv.get('max')}\n\n"
        mk.add(IB(f"{l} - {pr} so'm", callback_data=f"sq_{srv['service']}_{cid}"))
    mk.add(IB("🔙 Orqaga", callback_data=f"mp_{p}"))
    
    try: bot.edit_message_text(txt, c.message.chat.id, c.message.message_id, reply_markup=mk, parse_mode='HTML')
    except Exception as e: pass

@bot.callback_query_handler(func=lambda c: c.data.startswith("sq_"))
def sq_sel(c):
    _, sid, cid = c.data.split('_'); s = g_smm()
    srv = next((x for x in s if str(x.get('service')) == sid), None)
    if not srv: return bot.answer_callback_query(c.id, "Xizmat topilmadi")
    
    mv = get_m('m_yt_sub') if cid == 'sub' else (get_m('m_yt_watch') if cid == 'watch' else get_m('m_smm'))
    def safe_float(v):
        try: return float(str(v).replace(',','.'))
        except: return 0.0
        
    pr = int(safe_float(srv.get('rate', '0')) * g_k("USD", 12700) * mv)
    
    txt = f"🛍 <b>Tanlandi:</b> {srv['name']}\n💵 <b>Narx:</b> {pr} so'm (1000 ta uchun)\n\nℹ️ <b>Ma'lumot (Tavsif):</b>\n<i>{srv['description']}</i>\n\n🔗 <b>Link (Havola) yuboring:</b>"
    
    try: bot.edit_message_text(txt, c.message.chat.id, c.message.message_id, parse_mode='HTML')
    except Exception as e: pass
    
    usr_st[c.from_user.id] = 'wl'; tmp_dt[c.from_user.id] = {'s': sid, 'p': pr, 'm': int(srv.get('min',10)), 'x': int(srv.get('max',10000))}

@bot.message_handler(func=lambda m: usr_st.get(m.from_user.id) == 'wl')
def pl(m): tmp_dt[m.from_user.id]['l'] = m.text; usr_st[m.from_user.id] = 'wq'; bot.send_message(m.chat.id, f"{E_NUM} Qancha kerak? (Raqam yozing):", parse_mode='HTML')

@bot.message_handler(func=lambda m: usr_st.get(m.from_user.id) == 'wq')
def pq(m):
    if not m.text.isdigit(): return bot.send_message(m.chat.id, "Raqam yozing!")
    q = int(m.text); d = tmp_dt.get(m.from_user.id)
    if not d: return bot.send_message(m.chat.id, "Xato! Boshqatdan kiring.")
    
    t = int((d['p']/1000)*q)
    if q < d['m'] or q > d['x'] or g_bal(m.from_user.id) < t: 
        usr_st[m.from_user.id] = None; return bot.send_message(m.chat.id, "Pul kam yoki limit xato!")
        
    u_bal(m.from_user.id, -t)
    bot.send_message(m.chat.id, f"{E_TIME} Saytga yuborilmoqda...")
    
    try:
        payload = {'key': SMM_API_KEY, 'act': 'new_order', 'service_id': d['s'], 'link': d['l'], 'count': q}
        r = requests.get(SMM_API_URL, params=payload, timeout=15).json()
        
        if type(r) is dict and ('order' in r or 'order_id' in r): 
            oid = r.get('order') or r.get('order_id')
            bot.send_message(m.chat.id, f"✅ Qabul! Buyurtma ID: {oid}")
        else: 
            u_bal(m.from_user.id, t)
            bot.send_message(m.chat.id, f"Sayt qabul qilmadi: {r}")
    except Exception as e:
        u_bal(m.from_user.id, t)
        bot.send_message(m.chat.id, f"Tarmoq xatosi yuz berdi.")
        
    usr_st[m.from_user.id] = None

app = Flask(__name__)
@app.route('/')
def home(): return "Bot 24/7 rejimida ishlamoqda!"

def run_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

t = threading.Thread(target=run_server)
t.start()

bot.infinity_polling()
    
