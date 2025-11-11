from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = 'supersecretkey123'

# Konfigurasi email untuk form kritik dan saran (ganti password dengan yang valid)
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME='lagrangianss@gmail.com',
    MAIL_PASSWORD='tugasTIK24',  # Ganti dengan password atau app password Gmail yang valid
)

mail = Mail(app)

# Data artikel untuk Perpustakaan
articles = [
    {
        'title': 'Manfaat Olahraga Rutin untuk Kesehatan Mental',
        'content': 'Olahraga rutin adalah intervensi yang kuat dan terbukti secara ilmiah untuk meningkatkan kesehatan mental, bertindak sebagai antidepresan alami dengan menyeimbangkan kimia otak. Secara biokimia, aktivitas fisik meningkatkan pelepasan neurotransmiter penting seperti serotonin dan dopamin, yang mengatur suasana hati dan motivasi, serta membantu mengurangi tingkat hormon stres kortisol yang tinggi akibat tekanan kronis. Lebih jauh lagi, olahraga memberikan manfaat struktural jangka panjang dengan meningkatkan produksi Brain-Derived Neurotrophic Factor (BDNF), sering disebut "pupuk otak," yang mendukung pertumbuhan sel-sel saraf baru (neurogenesis) di Hippocampus—area yang penting untuk memori dan sering menyusut pada depresi. Selain manfaat biologis ini, olahraga juga meningkatkan fungsi kognitif (seperti fokus dan perencanaan), meningkatkan rasa efikasi diri melalui pencapaian rutin, dan membantu meregulasi siklus tidur, menjadikannya komponen integral dalam membangun ketahanan mental yang tangguh.'    
    },
    {
        'title': 'Pentingnya Nutrisi Seimbang untuk Remaja',
        'content': 'Masa remaja merupakan periode lonjakan pertumbuhan kedua tercepat dalam hidup setelah bayi, sehingga kebutuhan nutrisi seimbang sangatlah vital. Asupan makanan yang tepat—meliputi protein, karbohidrat kompleks dari biji-bijian utuh, lemak sehat, serta beragam buah dan sayuran—adalah sumber energi utama yang mendukung tingginya tingkat aktivitas fisik dan tuntutan belajar. Secara spesifik, mineral seperti kalsium dan vitamin D harus diprioritaskan karena remaja sedang membangun hingga 90% dari total massa tulang dewasa, yang sangat menentukan kekuatan tulang mereka di masa depan. Lebih dari sekadar fisik, nutrisi yang baik berperan langsung pada kesehatan mental dan kognitif; zat besi dan Omega-3, misalnya, mendukung fungsi otak, meningkatkan kemampuan konsentrasi dan memori. Dengan fondasi nutrisi yang kuat, remaja tidak hanya tumbuh sehat secara fisik, tetapi juga memiliki suasana hati yang lebih stabil, fokus yang lebih baik, dan pertahanan yang lebih kuat untuk menghadapi tantangan perkembangan dan stres akademik.'
    },
    {
        'title': 'Cara Memulai Pola Hidup Sehat di Usia Dewasa',
        'content': 'Memulai pola hidup sehat di usia dewasa tidak harus dilakukan secara drastis, tetapi fokus pada perubahan kecil yang berkelanjutan. Langkah pertama adalah menetapkan tujuan realistis—seperti tidur 7-8 jam per malam secara konsisten, bukan hanya sesekali. Dalam hal nutrisi, mulailah dengan menambahkan satu porsi sayuran atau buah pada setiap kali makan dan mengurangi minuman manis, daripada langsung menghilangkan semua makanan favorit. Untuk aktivitas fisik, tetapkan target minimal 150 menit olahraga intensitas sedang per minggu; ini bisa dicapai hanya dengan berjalan kaki cepat selama 30 menit, lima hari seminggu. Kunci sukses di usia dewasa adalah manajemen stres, yang dapat diatasi dengan menemukan hobi yang menenangkan atau memasukkan latihan kesadaran (mindfulness) singkat ke dalam rutinitas harian. Dengan mengintegrasikan kebiasaan-kebiasaan kecil ini, pola hidup sehat akan terasa lebih mudah dipertahankan dan menjadi bagian alami dari keseharian.'
    },
    {
        'title': 'Tips Mengelola Stres dengan Meditasi',
        'content': 'Mengelola stres dengan meditasi dapat dimulai dari langkah-langkah yang sangat sederhana. Inti dari meditasi adalah latihan kesadaran (mindfulness), di mana Anda membawa fokus penuh pada momen saat ini. Mulailah dengan hanya lima menit sehari di tempat yang tenang. Duduklah dengan nyaman, pejamkan mata atau tatap satu titik, dan fokuskan perhatian Anda sepenuhnya pada sensasi napas Anda—rasakan udara masuk dan keluar. Saat pikiran Anda mulai berkelana (yang pasti akan terjadi!), jangan menghakimi; akui pikiran tersebut ("Ah, aku memikirkan PR"), lalu dengan lembut kembalikan fokus Anda ke napas. Konsistensi lebih penting daripada durasi. Dengan berlatih secara rutin, Anda melatih otak untuk tidak langsung bereaksi terhadap stres, memberikan Anda jarak mental yang diperlukan untuk merespons tantangan hidup dengan lebih tenang dan bijaksana.'
    },
    {
        'title': 'Kaitan antara Tidur Cukup dan Kesehatan Jantung',
        'content': 'Tidur yang cukup adalah fondasi penting untuk menjaga kesehatan jantung optimal, karena selama tidur tubuh menjalani proses perbaikan dan regulasi krusial. Ketika kita tidur, tekanan darah dan detak jantung akan turun secara alami, memberikan kesempatan bagi sistem kardiovaskular untuk beristirahat dan memulihkan diri. Kurang tidur kronis (biasanya kurang dari 7-8 jam per malam) mengganggu proses pemulihan ini, menyebabkan peningkatan kadar hormon stres seperti kortisol. Peningkatan hormon stres ini membuat jantung bekerja lebih keras, menjaga tekanan darah tetap tinggi dan memicu peradangan di pembuluh darah, yang dalam jangka panjang dapat meningkatkan risiko hipertensi (tekanan darah tinggi), serangan jantung, dan stroke. Dengan memprioritaskan tidur berkualitas, kita secara aktif membantu jantung bekerja lebih efisien, mengurangi ketegangan pada sistem vaskular, dan menjaga kesehatan kardiovaskular tetap prima.'
    },
    {
        'title': 'Panduan Diet Sehat untuk Menjaga Berat Badan Ideal',
        'content': 'Menjaga berat badan ideal melalui diet sehat adalah strategi jangka panjang yang didasarkan pada keseimbangan nutrisi dan pengontrolan porsi, sebagaimana ditekankan oleh banyak ahli gizi klinis. Untuk mencapai hal ini, prinsip utama yang direkomendasikan adalah menggunakan metode piring sehat yang mengalokasikan sekitar 50% dari piring Anda untuk buah-buahan dan sayuran non-pati. Sayuran dan buah yang kaya serat ini memberikan volume yang mengenyangkan, membantu menjaga asupan kalori tetap terkontrol, dan mendukung kesehatan pencernaan. Sisa piring harus dibagi antara 25% protein tanpa lemak—termasuk ikan (sumber Omega-3 yang baik), dada ayam tanpa kulit, atau sumber nabati seperti kacang-kacangan dan biji-bijian—dan 25% karbohidrat kompleks seperti gandum utuh, quinoa, atau ubi. Para profesional kesehatan juga menyarankan untuk membatasi asupan gula tambahan harian hingga kurang dari 10% dari total kalori yang dikonsumsi, karena gula berlebih adalah salah satu kontributor utama penambahan berat badan dan penyakit metabolik. Selain komposisi makanan, lemak sehat dari alpukat atau minyak zaitun tetap penting untuk penyerapan vitamin A, D, E, dan K. Dengan menerapkan panduan porsi ini secara konsisten dan memastikan hidrasi yang optimal, diet sehat akan bertransformasi dari sekadar upaya sementara menjadi gaya hidup yang terukur dan berkelanjutan.'
    }
]

# Fakta kesehatan di Beranda
facts = [
    'Kesehatan mental sama pentingnya dengan kesehatan fisik.',
    'Remaja disarankan untuk berolahraga minimal 60 menit per hari.',
    'Konsumsi sayur dan buah setiap hari dapat meningkatkan sistem kekebalan tubuh.',
    'Berat badan ideal membantu mencegah berbagai penyakit kronis.',
    'Hindari konsumsi gula berlebih untuk mencegah diabetes.'
]

# Kutipan inspirasional
quotes = [
    {'author': 'Ade Rai', 'quote': 'Sehat itu murah, yang mahal itu sakit.'},
    {'author': 'Jim Rohn', 'quote': 'Jaga tubuhmu. Itu adalah satu-satunya tempat tinggalmu sepanjang hidup.'},
    {'author': 'Thich Nhat Hanh', 'quote': 'Kesehatan adalah anugerah terbesar, kepuasan adalah kekayaan terbesar.'}
]

@app.route('/')
def home():
    from random import choice
    quote = choice(quotes)
    return render_template('home.html', facts=facts, quote=quote)

@app.route('/perpustakaan')
def perpustakaan():
    return render_template('perpustakaan.html', articles=articles, enumerate=enumerate)

@app.route('/perpustakaan/<int:id>')
def article_detail(id):
    if 0 <= id < len(articles):
        article = articles[id]
        return render_template('article_detail.html', article=article)
    else:
        return 'Artikel tidak ditemukan', 404

@app.route('/kalkulator', methods=['GET', 'POST'])
def kalkulator():
    result = None
    advice = None
    if request.method == 'POST':
        try:
            umur = int(request.form.get('umur'))
            tinggi = float(request.form.get('tinggi'))
            berat = float(request.form.get('berat'))
            gender = request.form.get('gender')
            bmi = berat / ((tinggi / 100) ** 2)
            if gender == 'male':
                bmr = 10 * berat + 6.25 * tinggi - 5 * umur + 5
            else:
                bmr = 10 * berat + 6.25 * tinggi - 5 * umur - 161
            
            if bmi < 18.5:
                advice = 'Anda kekurangan berat badan. Konsumsi makanan bergizi dan olahraga ringan untuk menaikkan berat badan secara sehat.'
            elif 18.5 <= bmi < 25:
                advice = 'Berat badan Anda normal. Pertahankan pola hidup sehat dengan nutrisi seimbang dan olahraga teratur.'
            elif 25 <= bmi < 30:
                advice = 'Anda mengalami kelebihan berat badan. Disarankan mengatur pola makan dan tingkatkan aktivitas fisik.'
            else:
                advice = 'Anda masuk kategori obesitas. Segera konsultasikan ke dokter dan lakukan perubahan gaya hidup yang terstruktur.'
            result = {
                'bmi': round(bmi, 2),
                'bmr': round(bmr, 2),
            }
        except Exception:
            flash('Mohon isi data dengan benar.')
            return redirect(url_for('kalkulator'))

    return render_template('kalkulator.html', result=result, advice=advice)

@app.route('/kritik', methods=['GET', 'POST'])
def kritik():
    if request.method == 'POST':
        nama = request.form.get('nama')
        email = request.form.get('email')
        pesan = request.form.get('pesan')

        if not nama or not email or not pesan:
            flash('Mohon isi semua kolom dengan lengkap.')
            return redirect(url_for('kritik'))

        try:
            msg = Message(
                subject=f'Kritik dan Saran dari {nama}',
                sender=email,
                recipients=[app.config['MAIL_USERNAME']]
            )
            msg.body = pesan
            mail.send(msg)
            flash('Terima kasih atas kritik dan sarannya!')
        except Exception as e:
            flash(f'Gagal mengirim email: {e}')
        return redirect(url_for('kritik'))
    return render_template('kritik.html')

if __name__ == '__main__':
    app.run(debug=True)
