import discord
from discord.ext import commands
from config import TOKEN
import sqlite3

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
@bot.command()
async def start(ctx):
    await ctx.send(
        "Merhaba! Bu bot kariyer önerilerini sizin için belirlenmiş birkaç kategori ve meslek arasından size mesleklerin açıklaması ile birlikte sunar. Eğer bir sorun yaşarsanız lütfen !yardım komutunu kullanın.(not eğer bir kariyer ve meslek öneriniz varsa !oneri komutunu kullanabilirsiniz ve eğer bir önerinizi görmek istersenis !onerileri_gor komutunu kullanabilirsiniz!)"
    )

job_categories = {
    "Sağlık": ["Doktor", "Hemşire", "Eczacı"],
    "Teknoloji": ["Yazılım Geliştirici", "Sistem Yöneticisi", "Veri Analisti"],
    "Sanat": ["Ressam", "Müzisyen", "Yazar"],
    "İnşaat": ["Mimar", "Yapı Tasarımı", "İnşaat Şantiye Sorumluluğu"]
}

job_messages = {
    "Doktor": "Doktorlar insanların sağlıklı bir hayat yaşaması için çalışır bu iş çok iyi bir el göz koordinasyonu gerektirir ve en küçük hatalar bile hastaların yaşamını kaybetmesine yol açabilir,eğer ki bu işi istiyorsanız ve el göz koordinasyonunuz iyi ise bu işi seçmelisiniz!.",
    "Hemşire": "Hemşireler hastaların bakımını sağlar ve bazı insanların hayatlarını bile kurtarabilirler,eğer bu iş size göre ise bu sizin için olan bir meslektir!Bol şanslar :D.",
    "Eczacı": "Doktorların hastalara vermiş olduğu ilaçları onlara verir,yeterli dozunda ve doğru olması gerekir,bu iş dikkat ve  öözen gerektirir,eğer bu işe uygun görüyorsanız kendinizi bu işi seçmelisiniz!.",
    "Yazılım Geliştirici": "Yazılım Geliştiricilerinin teknolojide çok büyük bir etkisi vardır,bu alanda kod dillerini bilmeniz,kod yazabilmeniz ve kodunuzu manuel veya birim testten en az bir kere geçirmeniz lazım,en küçük hata bile yazılımın çalışmamasına yol açabilir,eğer ki kod yazmayı biliyorsanız ve bu işin size göre olduğunuzu düşünüyorsanız bu işi seçebilirsiniz!   .",
    "Sistem Yöneticisi": "Bilgisayar sistemlerinde var olan sorunları çözüp olabildiğince az hata ile çalışmasını sağlamanız gerekiyor.Eğer ki bilgisayar sistemleri hakkında bilginiz varsa ve bu işin size göre olduğunu düşünoyorsanız bu işi seçebilirsiniz!",
    "Veri Analisti": "Size verilen verileri kontrol edip analiz etmeniz gerekiyor.Bu iş çok büyük bir matematiksel ve analitik bir zeka gerektirir yaptığınız kararları düşünmeniz ve doğru olup olmadığına karar vermeniz gerekiyor,bu sizin seçiminiz ve eğer bunları yapabilirim diyorsanız o zaman bu işi seçin!",
    "Ressam": "Resimlerinizle düşüncelerinizi dışarı dünyaya yansıtıyor,bundan eğleniyorsunuz ve para kazanıyorsunuz,bu işi seçerseniz çok disiplinli olmak ve düzenli olmanız lazım,bu işi yapabileceğinizi düşünüyorsanız bu işi seçin!",
    "Müzisyen": "Müzisyen: Müziğinizle insanlara ilham veriyorsunuz.",
    "Yazar": "Yazar: Kelimelerinizle dünyalar yaratıyorsunuz.",
    "Mimar": "Mimar: Binaların ve yapıların tasarımını yapıyorsunuz.",
    "Yapı Tasarımı": "Yapı Tasarımı: Yapıların planlanmasında görev alıyorsunuz.",
    "İnşaat Şantiye Sorumluluğu": "İnşaat Şantiye Sorumlusu: Şantiyede işlerin düzenli ilerlemesini sağlıyorsunuz."
}

class JobView(discord.ui.View):
    def __init__(self, jobs):
        super().__init__(timeout=None)
        for job in jobs:
            self.add_item(JobButton(job))

class JobButton(discord.ui.Button):
    def __init__(self, job):
        super().__init__(label=job, style=discord.ButtonStyle.secondary)
        self.job = job

    async def callback(self, interaction: discord.Interaction):
        message = job_messages.get(self.job, f"{self.job} mesleğini seçtin!")
        await interaction.response.send_message(message, ephemeral=True)

class CategoryView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Sağlık", style=discord.ButtonStyle.primary)
    async def saglik(self, interaction: discord.Interaction, button: discord.ui.Button):
        jobs = job_categories["Sağlık"]
        await interaction.response.edit_message(content="Bir meslek seç:", view=JobView(jobs))

    @discord.ui.button(label="Teknoloji", style=discord.ButtonStyle.primary)
    async def teknoloji(self, interaction: discord.Interaction, button: discord.ui.Button):
        jobs = job_categories["Teknoloji"]
        await interaction.response.edit_message(content="Bir meslek seç:", view=JobView(jobs))

    @discord.ui.button(label="Sanat", style=discord.ButtonStyle.primary)
    async def sanat(self, interaction: discord.Interaction, button: discord.ui.Button):
        jobs = job_categories["Sanat"]
        await interaction.response.edit_message(content="Bir meslek seç:", view=JobView(jobs))

    @discord.ui.button(label="İnşaat", style=discord.ButtonStyle.primary)
    async def insaat(self, interaction: discord.Interaction, button: discord.ui.Button):
        jobs = job_categories["İnşaat"]
        await interaction.response.edit_message(content="Bir meslek seç:", view=JobView(jobs))

@bot.command()
async def meslek(ctx):
    await ctx.send("Bir kategori seç:", view=CategoryView())




@bot.command()
async def mesleksec(ctx, kategori: str = None, *, meslek: str = None):
    if kategori is None:
        kategoriler = ', '.join([k.title() for k in job_categories.keys()])
        await ctx.send(f"Lütfen bir kategori seçin: {kategoriler}\nÖrnek: `!mesleksec sağlık`")
        return
    kategori_input = kategori.lower()

    kategori_map = {k.lower(): k for k in job_categories.keys()}
    if kategori_input not in kategori_map:
        kategoriler = ', '.join([k.title() for k in job_categories.keys()])
        await ctx.send(f"Geçersiz kategori. Kategoriler: {kategoriler}")
        return
    kategori_key = kategori_map[kategori_input]
    if meslek is None:
        meslekler = ', '.join([m.title() for m in job_categories[kategori_key]])
        await ctx.send(f"{kategori_key} kategorisindeki meslekler: {meslekler}\nBir meslek seçmek için: `!mesleksec {kategori} <meslek>`")
        return
    meslek_input = meslek.lower()
    secilen_meslek = None
    for m in job_categories[kategori_key]:
        if m.lower() == meslek_input:
            secilen_meslek = m
            break
    if not secilen_meslek:
        meslekler = ', '.join([m.title() for m in job_categories[kategori_key]])
        await ctx.send(f"Geçersiz meslek. {kategori_key} kategorisindeki meslekler: {meslekler}")
        return
    mesaj = job_messages.get(secilen_meslek, f"{secilen_meslek} mesleğini seçtiniz!")
    await ctx.send(mesaj)


@bot.command()
async def yardım(ctx):
    await ctx.send("Eğer ki metinle meslek seçmek istiyorsanız lütfen !mesleksec komutunu kullanın veya eğer butonla yapmak istiyorsanız !meslek komutunu kullanın")



@bot.command(name="oneri", aliases=["öneri"])
async def oneri(ctx, kategori: str = None, meslek: str = None, *, açıklama_ve_oneri: str = None):
    if not kategori or not meslek or not açıklama_ve_oneri:
        await ctx.send('Kullanım: `!oneri <kategori> <meslek> <açıklama> | <ek öneri>`\nÇok kelimeli kategori/meslek için tırnak ("") kullanın.')
        return

    kategori = kategori.title()
    meslek = meslek.title()

    if "|" in açıklama_ve_oneri:
        açıklama, oneri = [x.strip() for x in açıklama_ve_oneri.split("|", 1)]
    else:
        açıklama = açıklama_ve_oneri
        oneri = ""

    # Aynı öneri var mı kontrol et
    conn = sqlite3.connect("veri_tabani.db")
    c = conn.cursor()
    c.execute(
        "SELECT 1 FROM oneriler WHERE kategori=? AND meslek=? AND açıklama=? AND oneri=?",
        (kategori, meslek, açıklama, oneri)
    )
    if c.fetchone():
        await ctx.send("Bu öneri zaten mevcut, tekrar eklenmedi.")
        conn.close()
        return

    # Veritabanına kaydet
    c.execute(
        "INSERT INTO oneriler (kullanici, kategori, meslek, açıklama, oneri) VALUES (?, ?, ?, ?, ?)",
        (str(ctx.author), kategori, meslek, açıklama, oneri)
    )
    conn.commit()
    conn.close()

    # job_categories'e ekle
    if kategori in job_categories:
        if meslek not in job_categories[kategori]:
            job_categories[kategori].append(meslek)
    else:
        job_categories[kategori] = [meslek]

    # job_messages'a ekle
    job_messages[meslek] = açıklama

    await ctx.send(f"Önerin kaydedildi ve sisteme eklendi!\nKategori: {kategori}\nMeslek: {meslek}\nAçıklama: {açıklama}\nEk bilgi: {oneri}")

def db_init():
    conn = sqlite3.connect("veri_tabani.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS oneriler (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kullanici TEXT,
            kategori TEXT,
            meslek TEXT,
            oneri TEXT,
            açıklama TEXT
        )
    """)
    conn.commit()
    conn.close()

db_init() 
@bot.command()
async def onerileri_gor(ctx):
    """Veritabanındaki tüm önerileri listeler."""
    conn = sqlite3.connect("veri_tabani.db")
    c = conn.cursor()
    c.execute("SELECT kullanici, kategori, meslek, açıklama, oneri FROM oneriler")
    rows = c.fetchall()
    conn.close()
    if not rows:
        await ctx.send("Henüz öneri yok.")
    else:
        mesajlar = []
        for kullanici, kategori, meslek, açıklama, oneri in rows:
            mesajlar.append(
                f"**{kullanici}** - {kategori}/{meslek}\nAçıklama: {açıklama}\nEk: {oneri}\n"
            )
        # Discord mesaj limiti için gerekirse böl
        for i in range(0, len(mesajlar), 5):
            await ctx.send("\n".join(mesajlar[i:i+5]))


@bot.command()
async def stop(ctx):
    await ctx.send("Bu botu kullandığınız için çok teşekkür ederim,hoşçakalın!")
    await bot.close()
bot.run(TOKEN)
