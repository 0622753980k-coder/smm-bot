import telebot, sqlite3, requests, time, os, threading
from datetime import datetime
from telebot.types import ReplyKeyboardMarkup as RK, KeyboardButton as KB, InlineKeyboardMarkup as IK, InlineKeyboardButton as IB
from flask import Flask

TOKEN = '8904483870:AAF_O56epbVmcEkldoLO0Xdd49SALTqFYJg'
ADMIN_ID = 8467707826
GRIZZLY_API_KEY = '3335af0d250efb73bdc40ebf82fa42dd'
SMM_API_KEY = '5f44258668604a14d48bd99270c1f8f4'
SMM_API_URL = 'https://top4smm.com/api.php'

bot = telebot.TeleBot(TOKEN)
usr_st, tmp_dt = {}, {}

def init_db():
    c = sqlite3.connect('b.db')
    c.execute('CREATE TABLE IF NOT EXISTS u (id INTEGER PRIMARY KEY, b INTEGER DEFAULT 0, r INTEGER DEFAULT 0)')
    c.execute('CREATE TABLE IF NOT EXISTS o (id INTEGER PRIMARY KEY AUTOINCREMENT, u INTEGER, oid TEXT, l TEXT, q INTEGER, d TEXT, s TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS a (id INTEGER PRIMARY KEY AUTOINCREMENT, t TEXT, d TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS s (k TEXT PRIMARY KEY, v TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS ad (id INTEGER PRIMARY KEY)')
    c.execute("INSERT OR IGNORE INTO s (k,v) VALUES ('card', '8600 0000 0000 0000')")
    c.execute("INSERT OR IGNORE INTO s (k,v) VALUES ('admin', '@admin')")
    c.execute("INSERT OR IGNORE INTO s (k,v) VALUES ('m_chan', '')")
    for k, v in [('p_y1','190000'), ('p_y2','120000'), ('p_y3','60000'), ('p_1func','50000'), ('p_2func','100000'), ('p_adsense','30000'), ('m_nomer','20'), ('m_yt_sub','20'), ('m_yt_watch','20'), ('m_smm','20')]:
        c.execute("INSERT OR IGNORE INTO s (k,v) VALUES (?, ?)", (k, v))
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
        {'service': '8316', 'name': 'YT Watchtime (Arzon)', 'category': 'youtube watch', 'rate': '3.0', 'min': 100, 'max': 4000, 'description': "⚠️ Kanalda kamida 60 daqiqalik video bo'lishi shart!\n🔹 Uderjanie: 60+ daqiqa.\n🔹 Tezlik: Sekinroq (Kuniga 100-300 soat).\n🔹 Kafolat: Yo'q."},
        {'service': '8317', 'name': 'YT Watchtime (Tezkor)', 'category': 'youtube watch', 'rate': '6.0', 'min': 100, 'max': 4000, 'description': "⚠️ Kanalda kamida 60 daqiqalik video bo'lishi shart!\n🔹 Uderjanie: 60+ daqiqa to'xtovsiz.\n🔹 Tezlik: Kuniga 300-500 soat.\n🔹 Kafolat: 30 kunlik tiklash."},
        {'service': '8318', 'name': 'YT Watchtime (Premium)', 'category': 'youtube watch', 'rate': '9.0', 'min': 100, 'max': 4000, 'description': "⚠️ Kamida 15+ daqiqalik video yetarli!\n🔹 Uderjanie: 15-30 daqiqa (High Retention).\n🔹 Tezlik: Kuniga 500-1000 soat.\n🔹 Kafolat: Umrbod (Non-drop)."},
        {'service': '6597', 'name': 'YT Obunachi (Arzon)', 'category': 'youtube sub', 'rate': '5.0', 'min': 10, 'max': 1000, 'description': "🔹 Tezlik: Kuniga 30-50 ta.\n🔹 Kafolat: Yo'q."},
        {'service': '6598', 'name': 'YT Obunachi (Kafolatli)', 'category': 'youtube sub', 'rate': '10.0', 'min': 10, 'max': 1000, 'description': "🔹 Tezlik: Kuniga 50-100 ta.\n🔹 Kafolat: 30 kun tiklash."},
        {'service': '6599', 'name': 'YT Obunachi (Premium)', 'category': 'youtube sub', 'rate': '15.0', 'min': 10, 'max': 1000, 'description': "🔹 Tezlik: Tezkor.\n🔹 Kafolat: Umrbod tushmaydi."},
        {'service': '101', 'name': 'YT View (Arzon)', 'category': 'youtube view', 'rate': '1.0', 'min': 100, 'max': 100000, 'description': "🔹 Uderjanie: 1-3 daqiqa.\n🔹 Tezlik: 1K-5K."},
        {'service': '102', 'name': 'YT View (Tezkor)', 'category': 'youtube view', 'rate': '2.0', 'min': 100, 'max': 100000, 'description': "🔹 Uderjanie: High Retention (Yuqori).\n🔹 Tezlik: 10K-50K."},
        {'service': '103', 'name': 'YT View (Premium)', 'category': 'youtube view', 'rate': '3.5', 'min': 100, 'max': 100000, 'description': "🔹 Uderjanie: Maksimal.\n🔹 Tavsiyalarga (rekomendatsiya) chiqaradi."},
        {'service': '111', 'name': 'YT Like (Arzon)', 'category': 'youtube like', 'rate': '2.0', 'min': 10, 'max': 10000, 'description': "🔹 Arzon layklar."},
        {'service': '112', 'name': 'YT Like (Sifatli)', 'category': 'youtube like', 'rate': '5.0', 'min': 10, 'max': 10000, 'description': "🔹 Sifatli, 30 kun kafolat."},
        {'service': '121', 'name': 'YT Comment', 'category': 'youtube comment', 'rate': '20.0', 'min': 10, 'max': 1000, 'description': "🔹 Ijobiy izohlar."},
        {'service': '201', 'name': 'TG Obuna', 'category': 'telegram sub', 'rate': '0.8', 'min': 100, 'max': 10000, 'description': "🔹 Tezkor obunachilar."},
        {'service': '211', 'name': 'TG Prosmotr', 'category': 'telegram view', 'rate': '0.1', 'min': 100, 'max': 50000, 'description': "🔹 Ko'rishlar soni."},
        {'service': '301', 'name': 'IG Obuna', 'category': 'instagram sub', 'rate': '0.8', 'min': 100, 'max': 10000, 'description': "🔹 Instagram obuna."},
        {'service': '401', 'name': 'TT Obuna', 'category': 'tiktok sub', 'rate': '0.8', 'min': 100, 'max': 10000, 'description': "🔹 TikTok obuna."}
    ]

def get_gz_pr(sc=None, cid=None):
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
            try: bot.send_message(ref, "🔔 <b>Do'stingiz kirdi!</b> U to'lov qilsa 5% bonus olasiz.", parse_mode='HTML')
            except: pass
    c.close()
    if not c_sub(uid):
        ch = g_set('m_chan'); mk = IK().add(IB("➕ Obuna bo'lish", url=f"https://t.me/{ch.replace('@','')}"), IB("🔄 Tekshirish", callback_data="ck_sub"))
        return bot.send_message(m.chat.id, "⚠️ <b>Kanalga a'zo bo'ling!</b>", reply_markup=mk, parse_mode='HTML')
    usr_st[uid] = None
    bot.send_message(m.chat.id, f"👋 <b>Assalomu alaykum {m.from_user.first_name}!</b>\nBotga xush kelibsiz. Quyidagi menyudan kerakli bo'limni tanlang.", reply_markup=m_menu(uid), parse_mode='HTML')

@bot.callback_query_handler(func=lambda c: c.data == "ck_sub")
def ck_s(c):
    if c_sub(c.from_user.id): 
        try: bot.delete_message(c.message.chat.id, c.message.message_id)
        except: pass
        bot.send_message(c.message.chat.id, "✅ Menyuga marhamat:", reply_markup=m_menu(c.from_user.id), parse_mode='HTML')
    else: bot.answer_callback_query(c.id, "❌ Hali a'zo bo'lmadingiz!", show_alert=True)

@bot.message_handler(func=lambda m: m.text == "Bosh sahifa 🔝")
def bs(m): usr_st[m.from_user.id] = None; bot.send_message(m.chat.id, "Asosiy menyu:", reply_markup=m_menu(m.from_user.id))

@bot.message_handler(func=lambda m: m.text == "👤 Mening hisobim")
def mc(m):
    i = sqlite3.connect('b.db').cursor().execute("SELECT b, (SELECT COUNT(id) FROM u WHERE r=?) FROM u WHERE id=?", (m.from_user.id, m.from_user.id)).fetchone()
    bot.send_message(m.chat.id, f"👤 <b>ID:</b> <code>{m.from_user.id}</code>\n💵 <b>Balans:</b> <b>{i[0] if i else 0}</b> so'm\n👥 <b>Takliflar:</b> {i[1] if i else 0} ta\n🔗 <code>https://t.me/{bot.get_me().username}?start={m.from_user.id}</code>", parse_mode='HTML')

@bot.message_handler(func=lambda m: m.text in ["💬 Murojaat", "🛒 Buyurtmalarim"])
def mb(m):
    if m.text == "💬 Murojaat": bot.send_message(m.chat.id, f"✍️ <b>Admin:</b> {g_set('admin')}", parse_mode='HTML')
    else:
        r = sqlite3.connect('b.db').cursor().execute("SELECT oid, s, q, l, d FROM o WHERE u=? ORDER BY id DESC LIMIT 5", (m.from_user.id,)).fetchall()
        if not r: return bot.send_message(m.chat.id, "❌ Buyurtmalar yo'q.")
        t = "<b>Oxirgi buyurtmalar:</b>\n\n"
        for x in r: t += f"🆔 <code>{x[0]}</code> | Holat: {x[1]} | Miqdor: {x[2]}\n"
        bot.send_message(m.chat.id, t, parse_mode='HTML')

@bot.message_handler(func=lambda m: m.text == "👑 Admin Panel" and is_adm(m.from_user.id))
def ap(m): bot.send_message(m.chat.id, "👑 <b>Admin Panel:</b>", reply_markup=a_menu(), parse_mode='HTML')

@bot.message_handler(func=lambda m: is_adm(m.from_user.id) and m.text in ["👥 Statistika", "📣 Kanal ulash", "✉️ Xabarnoma", "⚙️ Narxlarni o'zgartirish", "📈 Foizlarni o'zgartirish", "👮‍♂️ Admin qo'shish", "💳 Karta o'zgartirish", "💬 Murojaat o'zgartirish"])
def adm_bts(m):
    if m.text == "👥 Statistika":
        u = sqlite3.connect('b.db').cursor().execute("SELECT COUNT(id), SUM(b) FROM u").fetchone()
        bot.send_message(m.chat.id, f"A'zolar: {u[0]} ta\nBalanslar: {u[1] or 0} so'm")
    elif m.text == "📣 Kanal ulash":
        usr_st[m.from_user.id] = "set_chan"; bot.send_message(m.chat.id, "Kanalni @bilan yuboring (O'chirish uchun 0):")
    elif m.text == "✉️ Xabarnoma":
        usr_st[m.from_user.id] = "brd_msg"; bot.send_message(m.chat.id, "Xabarni yuboring:")
    elif m.text == "⚙️ Narxlarni o'zgartirish":
        mk = IK(row_width=1).add(IB(f"06-09: {g_set('p_y1')}", callback_data="edp_p_y1"), IB(f"10-19: {g_set('p_y2')}", callback_data="edp_p_y2"), IB(f"25-26: {g_set('p_y3')}", callback_data="edp_p_y3"), IB(f"1 funksiya: {g_set('p_1func')}", callback_data="edp_p_1func"), IB(f"2 funksiya: {g_set('p_2func')}", callback_data="edp_p_2func"), IB(f"Adsense: {g_set('p_adsense')}", callback_data="edp_p_adsense"))
        bot.send_message(m.chat.id, "Tanlang:", reply_markup=mk)
    elif m.text == "📈 Foizlarni o'zgartirish":
        mk = IK(row_width=1).add(IB(f"Nomer: {g_set('m_nomer')}%", callback_data="edp_m_nomer"), IB(f"YT Sub: {g_set('m_yt_sub')}%", callback_data="edp_m_yt_sub"), IB(f"YT Watch: {g_set('m_yt_watch')}%", callback_data="edp_m_yt_watch"), IB(f"SMM: {g_set('m_smm')}%", callback_data="edp_m_smm"))
        bot.send_message(m.chat.id, "Tanlang:", reply_markup=mk)
    elif m.text == "👮‍♂️ Admin qo'shish":
        usr_st[m.from_user.id] = "add_adm"; bot.send_message(m.chat.id, "Admin ID:")
    elif m.text == "💳 Karta o'zgartirish":
        usr_st[m.from_user.id] = "set_c"; bot.send_message(m.chat.id, "Yangi karta raqami:")
    elif m.text == "💬 Murojaat o'zgartirish":
        usr_st[m.from_user.id] = "set_a"; bot.send_message(m.chat.id, "Yangi admin yuzerini yozing:")

@bot.callback_query_handler(func=lambda c: c.data.startswith("edp_"))
def ed_p(c): usr_st[c.from_user.id] = f"setp_{c.data[4:]}"; bot.send_message(c.message.chat.id, "Yangi qiymatni raqamda yuboring:")

@bot.message_handler(func=lambda m: str(usr_st.get(m.from_user.id)) in ["set_chan", "brd_msg", "add_adm", "set_c", "set_a"] or str(usr_st.get(m.from_user.id)).startswith("setp_"))
def adm_st(m):
    st = usr_st[m.from_user.id]
    if st == "set_chan":
        u_set('m_chan', "" if m.text == "0" else m.text); usr_st[m.from_user.id] = None; bot.send_message(m.chat.id, "Saqlandi!")
    elif st == "brd_msg":
        usr_st[m.from_user.id] = None; u = sqlite3.connect('b.db').cursor().execute("SELECT id FROM u").fetchall()
        for x in u:
            try: bot.copy_message(x[0], m.chat.id, m.message_id); time.sleep(0.04)
            except: pass
        bot.send_message(m.chat.id, "Xabar yuborildi!")
    elif st.startswith("setp_"):
        if not m.text.isdigit(): return bot.send_message(m.chat.id, "Raqam yozing!")
        u_set(st[5:], m.text); usr_st[m.from_user.id] = None; bot.send_message(m.chat.id, "Saqlandi!")
    elif st == "add_adm":
        if not m.text.isdigit(): return bot.send_message(m.chat.id, "Faqat raqamli ID!")
        sqlite3.connect('b.db').cursor().execute("INSERT OR IGNORE INTO ad (id) VALUES (?)", (int(m.text),)).connection.commit(); usr_st[m.from_user.id] = None; bot.send_message(m.chat.id, "Admin qo'shildi!")
    elif st == "set_c": u_set('card', m.text); usr_st[m.from_user.id] = None; bot.send_message(m.chat.id, "Karta saqlandi!")
    elif st == "set_a": u_set('admin', m.text); usr_st[m.from_user.id] = None; bot.send_message(m.chat.id, "Admin saqlandi!")

@bot.message_handler(func=lambda m: m.text in ["➕ 2006-2009", "➕ 2010-2019", "➕ 2025-2026"] and is_adm(m.from_user.id))
def adc(m): usr_st[m.from_user.id] = f"wac_{'y1' if '2006' in m.text else ('y2' if '2010' in m.text else 'y3')}"; bot.send_message(m.chat.id, "Kanal ma'lumotlarini (Login:Parol) yuboring:")

@bot.message_handler(func=lambda m: str(usr_st.get(m.from_user.id)).startswith("wac_"))
def sav_ac(m):
    sqlite3.connect('b.db').cursor().execute("INSERT INTO a (t, d) VALUES (?, ?)", (usr_st[m.from_user.id].split('_')[1], m.text)).connection.commit()
    usr_st[m.from_user.id] = None; bot.send_message(m.chat.id, "Kanal bazaga qo'shildi!")

@bot.message_handler(commands=['addbalance'])
def ad_b(m):
    if is_adm(m.from_user.id) and len(m.text.split()) > 2:
        a = m.text.split(); u_bal(int(a[1]), int(a[2])); bot.send_message(int(a[1]), f"🎁 <b>{a[2]} so'm</b> hisobingizga qo'shildi!", parse_mode='HTML'); bot.send_message(m.chat.id, "Bajarildi!")

@bot.message_handler(func=lambda m: m.text == "💳 Hisob to'ldirish")
def tu(m): bot.send_message(m.chat.id, "💵 <b>Qancha to'ldirasiz?</b> (Min: 1000 so'm):", parse_mode='HTML'); usr_st[m.from_user.id] = "wa"

@bot.message_handler(func=lambda m: usr_st.get(m.from_user.id) == "wa")
def ra(m):
    if not m.text.isdigit() or int(m.text) < 1000: return bot.send_message(m.chat.id, "Kamida 1000 so'm yozing!")
    a = int(m.text); usr_st[m.from_user.id] = None
    mk = IK().add(IB("✅ To'lov qildim", callback_data=f"dn_{a}"), IB("❌ Bekor qilish", callback_data="cancel_pay"))
    bot.send_message(m.chat.id, f"💳 Karta: <code>{g_set('card')}</code>\n💵 Summa: <b>{a} so'm</b>\nTo'lov qilib tasdiqlang!", reply_markup=mk, parse_mode='HTML')

@bot.callback_query_handler(func=lambda c: c.data == 'cancel_pay')
def cancel_pay(c):
    try: bot.delete_message(c.message.chat.id, c.message.message_id)
    except: pass
    bot.send_message(c.message.chat.id, "❌ Bekor qilindi.")

@bot.callback_query_handler(func=lambda c: c.data.startswith('dn_'))
def dn(c):
    try: bot.delete_message(c.message.chat.id, c.message.message_id)
    except: pass
    a, u = int(c.data.split('_')[1]), c.from_user.id
    bot.send_message(u, "⏳ Tekshirilmoqda...")
    adm_msg(f"🔔 To'lov kutilmoqda:\nID: <code>{u}</code>\nSumma: {a}", rm=IK().add(IB("✅ Tasdiqlash", callback_data=f"ap_{u}_{a}"), IB("❌ Rad", callback_data=f"rj_{u}_{a}")))

@bot.callback_query_handler(func=lambda c: c.data.startswith('ap_') or c.data.startswith('rj_'))
def ad_d(c):
    try: bot.delete_message(c.message.chat.id, c.message.message_id)
    except: pass
    p = c.data.split('_'); u, a = int(p[1]), int(p[2])
    if p[0] == "ap":
        u_bal(u, a); bot.send_message(u, f"✅ <b>Balans to'ldirildi:</b> {a} so'm", parse_mode='HTML')
        ref = sqlite3.connect('b.db').cursor().execute("SELECT r FROM u WHERE id=?", (u,)).fetchone()[0]
        if ref:
            bns = int(a * 0.05)
            if bns > 0:
                u_bal(ref, bns)
                try: bot.send_message(ref, f"🎁 Referal bonus: {bns} so'm!")
                except: pass
    else: bot.send_message(u, "❌ To'lov rad etildi.")

C_LIST = [("0", "Rossiya 🇷🇺"), ("1", "Ukraina 🇺🇦"), ("2", "Qozog'iston 🇰🇿"), ("3", "Xitoy 🇨🇳"), ("4", "Filippin 🇵🇭"), ("5", "Myanma 🇲🇲"), ("6", "Indoneziya 🇮🇩"), ("12", "AQSh 🇺🇸"), ("16", "Angliya 🇬🇧")]
S_LIST = [("vk", "VKontakte"), ("go", "Google"), ("fb", "Facebook"), ("ig", "Instagram"), ("dt", "TikTok"), ("wa", "WhatsApp")]

@bot.callback_query_handler(func=lambda c: c.data == "none")
def none_cb(c): bot.answer_callback_query(c.id)

@bot.message_handler(func=lambda m: m.text == "📱 Nomer olish")
def nm(m):
    mk = IK(row_width=2).add(IB("📞 Telegram", callback_data="tg_p_0"), IB("☎️ Boshqa Tarmoqlar", callback_data="ot_p_0"))
    bot.send_message(m.chat.id, "Tarmoqni tanlang:", reply_markup=mk)

@bot.callback_query_handler(func=lambda c: c.data.startswith("tg_p_"))
def tg_pg(c):
    page = int(c.data.split('_')[2]); pr = get_gz_pr(sc="tg"); mv = get_m('m_nomer'); mk = IK(row_width=2); btns = []
    for cid, cname in C_LIST[page*8 : page*8+8]:
        cost = pr.get(cid)
        if cost: btns.append(IB(f"{cname} - {int(cost * 12700 * mv)}", callback_data=f"buy_tg_{cid}_{int(cost * 12700 * mv)}"))
        else: btns.append(IB(f"{cname} (Yo'q)", callback_data="none"))
    for i in range(0, len(btns), 2): mk.row(*btns[i:i+2])
    mk.row(IB("⬅️", callback_data=f"tg_p_{page-1}") if page > 0 else IB("➖", callback_data="none"), IB(f"{page+1}/2", callback_data="none"), IB("➡️", callback_data=f"tg_p_{page+1}") if page < 1 else IB("➖", callback_data="none"))
    try: bot.edit_message_text("Davlatni tanlang:", c.message.chat.id, c.message.message_id, reply_markup=mk)
    except: pass

@bot.callback_query_handler(func=lambda c: c.data.startswith("ot_p_"))
def ot_pg(c):
    page = int(c.data.split('_')[2]); mk = IK(row_width=2); btns = []
    for cid, cname in C_LIST[page*8 : page*8+8]: btns.append(IB(f"{cname}", callback_data=f"ot_c_{cid}"))
    for i in range(0, len(btns), 2): mk.row(*btns[i:i+2])
    mk.row(IB("⬅️", callback_data=f"ot_p_{page-1}") if page > 0 else IB("➖", callback_data="none"), IB(f"{page+1}/2", callback_data="none"), IB("➡️", callback_data=f"ot_p_{page+1}") if page < 1 else IB("➖", callback_data="none"))
    try: bot.edit_message_text("Davlatni tanlang:", c.message.chat.id, c.message.message_id, reply_markup=mk)
    except: pass
@bot.callback_query_handler(func=lambda c: c.data.startswith("ot_c_"))
def ot_c_sel(c):
    cid = c.data.split('_')[2]; cname = dict(C_LIST).get(cid, "Davlat")
    pr = get_gz_pr(cid=cid); mv = get_m('m_nomer')
    if not pr: return bot.answer_callback_query(c.id, "Nomerlar yo'q", show_alert=True)
    mk = IK(row_width=2); btns = []
    for sc, sname in S_LIST:
        cost = pr.get(sc)
        if cost:
            price = int(cost * 12700 * mv)
            btns.append(IB(f"{sname} - ({price})", callback_data=f"buy_{sc}_{cid}_{price}"))
        else: btns.append(IB(f"{sname} (Yo'q)", callback_data="none"))
    for i in range(0, len(btns), 2): mk.row(*btns[i:i+2])
    mk.add(IB("🔙 Orqaga", callback_data="ot_p_0"))
    try: bot.edit_message_text(f"Tarmoqni tanlang ({cname}):", c.message.chat.id, c.message.message_id, reply_markup=mk)
    except: pass

@bot.callback_query_handler(func=lambda c: c.data.startswith("buy_"))
def pb(c):
    p = c.data.split('_'); sc, cid, pr = p[1], p[2], int(p[3])
    if g_bal(c.from_user.id) < pr: return bot.answer_callback_query(c.id, "Pul kam!", show_alert=True)
    r = req_gz(sc, cid)
    if r["s"]:
        u_bal(c.from_user.id, -pr); mk = IK().add(IB("🔎 SMS olish", callback_data=f"ck_{r['id']}_{pr}"), IB("❌ Bekor", callback_data=f"cl_{r['id']}_{pr}"))
        bot.send_message(c.message.chat.id, f"✅ Nomer olindi: <code>{r['n']}</code>\nYechildi: {pr} so'm", reply_markup=mk, parse_mode='HTML')
    else: bot.answer_callback_query(c.id, f"Xato: {r['m']}", show_alert=True)

@bot.callback_query_handler(func=lambda c: c.data.startswith("ck_") or c.data.startswith("cl_"))
def ck_cl(c):
    p = c.data.split('_')
    if p[0] == "ck":
        try: st = requests.get(f"https://api.grizzlysms.com/stubs/handler_api.php?api_key={GRIZZLY_API_KEY}&action=getStatus&id={p[1]}", timeout=5).text
        except: st = ""
        if "WAIT" in st: bot.answer_callback_query(c.id, "Kutilmoqda...", show_alert=True)
        elif "OK" in st: bot.send_message(c.message.chat.id, f"✅ SMS Kod: <code>{st.split(':')[1]}</code>", parse_mode='HTML')
        else: bot.answer_callback_query(c.id, "Bekor qilingan", show_alert=True)
    else:
        try:
            st = requests.get(f"https://api.grizzlysms.com/stubs/handler_api.php?api_key={GRIZZLY_API_KEY}&action=getStatus&id={p[1]}", timeout=5).text
            if "OK" in st: return bot.answer_callback_query(c.id, "SMS kelgan!", show_alert=True)
            requests.get(f"https://api.grizzlysms.com/stubs/handler_api.php?api_key={GRIZZLY_API_KEY}&action=setStatus&status=8&id={p[1]}", timeout=5)
            u_bal(c.from_user.id, int(p[2]))
            bot.send_message(c.message.chat.id, f"Bekor qilindi. Pul qaytdi: {p[2]} so'm")
        except: bot.answer_callback_query(c.id, "Xato yuz berdi", show_alert=True)

@bot.message_handler(func=lambda m: m.text in ["🔴 Tayyor Kanallar", "📦 Xizmatlar"])
def yt_smm(m):
    if "Kanallar" in m.text:
        mk = IK(row_width=1)
        for k, n in [("y1", "🔴 [ESKI] 2006-09"), ("y2", "🔴 [ESKI] 2010-19"), ("y3", "🔴 [YANGI] 2025-26")]: mk.add(IB(f"{n} - {g_set('p_'+k)} so'm", callback_data=f"by_{k}"))
        mk.add(IB(f"🛠 1 funksiya - {g_set('p_1func')} so'm", callback_data="by_n_1func"), IB(f"🛠 2 funksiya - {g_set('p_2func')} so'm", callback_data="by_n_2func"), IB(f"💰 Adsense - {g_set('p_adsense')} so'm", callback_data="by_n_adsense"))
        bot.send_message(m.chat.id, "YouTube Kanallar:", reply_markup=mk)
    else:
        mk = IK(row_width=2).add(IB("✈️ Telegram", callback_data="mp_tg"), IB("📸 Instagram", callback_data="mp_ig"), IB("🔴 YouTube", callback_data="mp_yt"), IB("🎵 TikTok", callback_data="mp_tt"))
        bot.send_message(m.chat.id, "Ijtimoiy tarmoqni tanlang:", reply_markup=mk)

@bot.callback_query_handler(func=lambda c: c.data.startswith("by_"))
def b_yt(c):
    t = c.data.split('_')
    if t[1] == "n":
        pr = int(g_set('p_' + t[2]))
        if g_bal(c.from_user.id) < pr: return bot.answer_callback_query(c.id, "Pul kam!", show_alert=True)
        u_bal(c.from_user.id, -pr); usr_st[c.from_user.id] = f"wn_{t[2]}"
        if t[2] in ['1func','2func']: bot.send_message(c.message.chat.id, "Ma'lumotlarni yuboring:")
        else: bot.send_message(c.message.chat.id, "💰 <b>Adsense uchun quyidagi ma'lumotlarni yuboring:</b>\n\n👤 Ism-familiya:\n📞 Telefon raqam:\n📍 To'liq manzil:\n📮 Pochta indeksi:", parse_mode='HTML')
    else:
        pr = int(g_set('p_' + t[1]))
        if g_bal(c.from_user.id) < pr: return bot.answer_callback_query(c.id, "Pul kam!", show_alert=True)
        u_bal(c.from_user.id, -pr); acc = sqlite3.connect('b.db').cursor().execute("SELECT id, d FROM a WHERE t=? LIMIT 1", (t[1],)).fetchone()
        yoriqnoma = "⚠️ <b>Foydalanish bo‘yicha yo‘riqnoma</b>\n\nBloklanib qolmaslik uchun birinchi sutkada keskin harakatlar qilmang.\n\n<b>Muhim:</b>\n• Parolni darrov o‘zgartirmang\n• Uni 24 soatdan keyin, o‘sha qurilma / IP orqali o‘zgartiring\n• Telefon raqamini darrov bog‘lamang\n• Faqat 7 kundan keyin qo‘shing\n• Zaxira pochtani darrov o‘zgartirish mumkin — bu xavfsiz\n• Birinchi soatlarda parol, IP yoki qurilmani keskin almashtirish — bloklanish xavfi"
        if acc:
            sqlite3.connect('b.db').cursor().execute("DELETE FROM a WHERE id=?", (acc[0],)).connection.commit()
            bot.send_message(c.message.chat.id, f"✅ Xarid qilindi!\n\nKanal: <code>{acc[1]}</code>\n\n{yoriqnoma}", parse_mode='HTML')
        else:
            sqlite3.connect('b.db').cursor().execute("INSERT INTO o (u,oid,l,q,d,s) VALUES (?,?,?,?,?,?)", (c.from_user.id, "YT", t[1], 1, datetime.now().strftime("%Y.%m.%d %H:%M:%S"), "Kutmoqda")).connection.commit()
            bot.send_message(c.message.chat.id, "Buyurtma qabul qilindi. Tez orada admin yetkazadi.")

@bot.message_handler(func=lambda m: str(usr_st.get(m.from_user.id)).startswith("wn_"))
def sv_nch(m):
    t = usr_st[m.from_user.id].split('_')[1]
    sqlite3.connect('b.db').cursor().execute("INSERT INTO o (u,oid,l,q,d,s) VALUES (?,?,?,?,?,?)", (m.from_user.id, t, m.text, 1, datetime.now().strftime("%Y.%m.%d %H:%M:%S"), "Kutmoqda")).connection.commit()
    usr_st[m.from_user.id] = None; bot.send_message(m.chat.id, "Qabul qilindi!")

@bot.callback_query_handler(func=lambda c: c.data.startswith("mp_"))
def smc(c):
    p = c.data.split('_')[1]; mk = IK(row_width=1)
    if p == 'yt': opts = [("watch", "⏱ Watchtime"), ("sub", "🔴 Obunachilar"), ("view", "👁 Ko'rishlar"), ("like", "👍 Layklar"), ("comment", "💬 Kommentlar")]
    else: opts = [("sub", "👥 Obunachilar"), ("view", "👁 Ko'rishlar"), ("like", "❤️ Layklar")]
    for cid, cn in opts: mk.add(IB(cn, callback_data=f"mc_{p}_{cid}"))
    try: bot.edit_message_text("Xizmat turini tanlang:", c.message.chat.id, c.message.message_id, reply_markup=mk)
    except: pass

@bot.callback_query_handler(func=lambda c: c.data.startswith("mc_"))
def n_ss(c):
    _, p, cid = c.data.split('_'); s = g_smm()
    f = [x for x in s if p in x['category'] and cid in x['category']]
    if not f: return bot.answer_callback_query(c.id, "Xizmat topilmadi", show_alert=True)
    mv = get_m('m_yt_sub') if cid == 'sub' else (get_m('m_yt_watch') if cid == 'watch' else get_m('m_smm'))
    mk = IK(row_width=1)
    for srv in f:
        pr = int(float(srv['rate']) * 12700 * mv)
        mk.add(IB(f"{srv['name']} - {pr} so'm", callback_data=f"sq_{srv['service']}"))
    mk.add(IB("🔙 Orqaga", callback_data=f"mp_{p}"))
    try: bot.edit_message_text("Xizmatni tanlang:", c.message.chat.id, c.message.message_id, reply_markup=mk)
    except: pass

@bot.callback_query_handler(func=lambda c: c.data.startswith("sq_"))
def sq_sel(c):
    sid = c.data.split('_')[1]; srv = next((x for x in g_smm() if x['service'] == sid), None)
    if not srv: return bot.answer_callback_query(c.id, "Xizmat topilmadi", show_alert=True)
    mv = get_m('m_yt_watch') if 'watch' in srv['category'] else get_m('m_smm')
    pr = int(float(srv['rate']) * 12700 * mv)
    txt = f"🛍 <b>Tanlandi:</b> {srv['name']}\n💵 <b>Narx:</b> {pr} so'm (1000 ta)\n\nℹ️ <b>Ma'lumot:</b>\n<i>{srv['description']}</i>\n\n🔗 <b>Link (Havola) yuboring:</b>"
    try: bot.edit_message_text(txt, c.message.chat.id, c.message.message_id, parse_mode='HTML')
    except: pass
    usr_st[c.from_user.id] = 'wl'; tmp_dt[c.from_user.id] = {'s': sid, 'p': pr, 'm': int(srv['min']), 'x': int(srv['max'])}

@bot.message_handler(func=lambda m: usr_st.get(m.from_user.id) == 'wl')
def pl(m): tmp_dt[m.from_user.id]['l'] = m.text; usr_st[m.from_user.id] = 'wq'; bot.send_message(m.chat.id, "🔢 <b>Qancha kerak? (Raqam yozing):</b>", parse_mode='HTML')

@bot.message_handler(func=lambda m: usr_st.get(m.from_user.id) == 'wq')
def pq(m):
    if not m.text.isdigit(): return bot.send_message(m.chat.id, "Raqam yozing!")
    q = int(m.text); d = tmp_dt.get(m.from_user.id)
    if not d: return bot.send_message(m.chat.id, "Boshqatdan kiring.")
    t = int((d['p']/1000)*q)
    if q < d['m'] or q > d['x'] or g_bal(m.from_user.id) < t:
        usr_st[m.from_user.id] = None; return bot.send_message(m.chat.id, "Pul yetarli emas yoki limit noto'g'ri!")
    u_bal(m.from_user.id, -t); bot.send_message(m.chat.id, "Top4smm saytiga buyurtma yuborilmoqda...")
    try:
        r = requests.get(SMM_API_URL, params={'key': SMM_API_KEY, 'act': 'new_order', 'service_id': d['s'], 'link': d['l'], 'count': q}, timeout=15).json()
        if type(r) is dict and ('order' in r or 'order_id' in r):
            oid = r.get('order') or r.get('order_id')
            bot.send_message(m.chat.id, f"✅ Qabul qilindi! Buyurtma ID: {oid}")
        else:
            u_bal(m.from_user.id, t); bot.send_message(m.chat.id, f"Sayt qabul qilmadi: {r}")
    except:
        u_bal(m.from_user.id, t); bot.send_message(m.chat.id, "Tarmoq xatosi yuz berdi.")
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
