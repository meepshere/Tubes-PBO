from flask import Flask, render_template, url_for, request, redirect
#from flask_sqlalchemy import SQLAlchemy
#from datetime import datetime
from . import app, db
from invent.dtbs import *
from invent.userSekarang import *

@app.route('/', methods=['POST', 'GET'])
def loginPage():
    if request.method == 'POST':
        global findPengguna
        global pengguna 
        inputID = request.form['contentUser']
        inputSandi = request.form['contentPass']
        try: 
            findPengguna = Manusia.query.filter_by(nim=inputID).first()
            if((findPengguna.sandi == inputSandi)==True):
                pengguna = userNow(findPengguna, findPengguna.nim, findPengguna.sandi, findPengguna.nama)
                return render_template('mainPage.html')
            else:
                return "Informasi login salah2"
        except:
            return "Informasi login salah"
    else: 
        return render_template('index.html')

@app.route('/mainPage', methods=['GET'])
def mainPage():
    return render_template('mainPage.html')

@app.route('/seluruhBarang', methods=['POST', 'GET'])
def mainmain():
    if request.method == 'POST':
        barang_masuk = request.form['content']
        gedung_masuk = request.form['gedungc']
        ruang_masuk = request.form['ruangc']
        tempat = Gedung.query.filter_by(namaGedung=gedung_masuk).first()
        tempatR = Ruang.query.filter_by(namaRuang=ruang_masuk).first()

        barang_baru = Barang(namaBarang=barang_masuk, ged=tempat.id, kel=tempatR.id)

        if(tempatR in tempat.kelas):
            try:    
                db.session.add(barang_baru)
                db.session.commit()
                return redirect('/')
            except:
                return str(tempat)+f'awaw'
        else:
            return f'gaada ruangan {tempatR.namaRuang} di gedung {tempat.namaGedung}'

    else:
        tasks = Barang.query.all()
        
        return render_template('seluruhBarang.html', tasks=tasks)
        
@app.route('/pinjamForm/<int:id>', methods=['POST', 'GET'])
def pinjamForm(id):
    if request.method == 'POST':
        perihal = request.form['content']
        letakFile = request.form['pathberkas']
        banyak = request.form['stokberkas']
        #pengguna += 1
        stokbarang = Barang.query.get_or_404(id)
        try:
            if stokbarang.stoksisa >= int(banyak) :
                try:
                    pengguna.setAct(pengguna.getAct()+1)
                    pinjam_baru = Peminjaman(kodePeminjaman=perihal, benda=id, banyak=banyak, peminjam=pengguna.getID(), letak=letakFile)
                    stokbarang.stoksisa -= int(banyak)
                    try:
                        db.session.add(pinjam_baru)
                        db.session.commit()
                        return redirect('/dataPinjamDiri')
                    except:
                        return 'gatau gagal'
                except:
                    return 'gatau gagal3'
            else:
                return 'stok tida cukup'
        except:
                return 'gatau gagal4'

    else:
        return render_template('pinjamForm.html', id=id)

@app.route('/inputUser', methods=['POST', 'GET'])
def masukData():
    if request.method == 'POST':
        if request.form['content3'] != "":
            kelas_masuk = request.form['content3']
            gedungnya = request.form['gedungk']

            try:
                tempat = Gedung.query.filter_by(namaGedung=gedungnya).first()
                kelas_baru = Ruang(namaRuang=kelas_masuk, ged_id=tempat.id)
            except:
                return pengguna.getNama()

            try:
                db.session.add(kelas_baru)
                db.session.commit()
                return redirect('/gedung')
            except:
                return 'gatau gagal'

        if request.form['content2'] != "":
            gedung_masuk = request.form['content2']
            gedung_baru = Gedung(namaGedung=gedung_masuk)

            try:
                db.session.add(gedung_baru)
                db.session.commit()
                return redirect('/gedung')
            except:
                return 'gatau gagal'
                
        if request.form['content'] != "":
            barang_masuk = request.form['content']
            gedung_masuk = request.form['gedungc']
            ruang_masuk = request.form['ruangc']
            jumlah = request.form['stokc']
            try:
                tempat = Gedung.query.filter_by(namaGedung=gedung_masuk).first()
                tempatR = Ruang.query.filter_by(namaRuang=ruang_masuk).first()

                barang_baru = Barang(namaBarang=barang_masuk, ged=tempat.id, kel=tempatR.id, stok=jumlah, stoksisa=jumlah)
            except:
                return "fail"

            if(tempatR in tempat.kelas):
                try:    
                    db.session.add(barang_baru)
                    db.session.commit()
                    return redirect('/gedung')
                except:
                    return str(tempat)+f'awaw'
            else:
                return f'gaada ruangan {tempatR.namaRuang} di gedung {tempat.namaGedung}'
        else:
            return "masukin inputan dong bank"

    else:
        
        return render_template('inputUser.html')

@app.route('/gedung', methods=['POST', 'GET'])
def gedungUI():
    if request.method == 'POST':
        gedung_masuk = request.form['content']
        gedung_baru = Gedung(namaGedung=gedung_masuk)

        try:
            db.session.add(gedung_baru)
            db.session.commit()
            return redirect('/gedung')
        except:
            return 'gatau gagal'

    else:
        tasks = Gedung.query.all()
        return render_template('gedung.html', tasks=tasks)

@app.route('/lihatRuang/<int:id>', methods=['POST', 'GET'])
def lihatRuang(id):
    gedungnya = Gedung.query.get_or_404(id)
    tasks = Ruang.query.filter_by(beradaPadaGedung=gedungnya)
    return render_template('lihatKelas.html', tasks=tasks, ged = gedungnya)


@app.route('/lihatBarang/<int:id>', methods=['POST', 'GET'])
def lihatBarangUI(id):
    namged = Ruang.query.filter_by(id=id).first()
    tot_barang = namged.barangsR
    return render_template('lihatBarang.html', tasks=tot_barang, namaKelas=namged.namaRuang)

@app.route('/lihatDetail/<int:id>', methods=['POST', 'GET'])
def lihatDetail(id):
    brg = Barang.query.filter_by(id=id).first()
    tasks = brg.dipinjam
    kls = brg.tempatKelas
    gdg = brg.tempatGedung
    return render_template('lihatDetail.html', tasks=tasks, brg=brg, gdg = gdg, kls = kls)


@app.route('/dataPinjamDiri', methods=['POST', 'GET'])
def dataPinjamDiri():
    if request.method == 'POST':
        return "pst"
    else:
        try:
            task = Manusia.query.filter_by(nim=pengguna.getID()).first()
            return render_template('dataPinjamDiri.html', task=task, nPinjam=pengguna.getAct())
        except:
            return redirect('/')


@app.route('/gantiDataDiri', methods=['POST', 'GET'])
def gantiDataDiri():
    if request.method == 'POST':
        addrBaru = request.form['content']
        phnumber = request.form['notelp']

        try:
            task = Manusia.query.get_or_404(pengguna.getID())
            task.alamat = addrBaru
            task.no_telp = phnumber
            db.session.commit()
            return redirect('/gantiDataDiri')
        except:
            return 'gatau gagal'
    else:
        try:
            task = Manusia.query.filter_by(nim=pengguna.getID()).first()
            return render_template('gantiDataDiri.html', task=task)
        except:
            return redirect('/')

@app.route('/peminjamanDiri/<int:id>', methods=['POST', 'GET'])
def peminjamanDiri(id):
    berkas = []
    berkasPeminjam = []
    berkasDipinjam = []
    idbarang = Barang.query.get_or_404(id)
    for i in idbarang.dipinjam:
        tempberkas = Peminjaman.query.filter_by(id=i.id).first()
        berkas.append(tempberkas)
        berkasPeminjam.append(tempberkas.peminjamBarang)
        berkasDipinjam.append(tempberkas.barangDipinjam)
    return render_template('peminjamanDiri.html', tasks=berkas, brgid=id)

@app.route('/peminjamanDiriK/<int:id>', methods=['POST', 'GET'])
def peminjamanDiriK(id):
    berkas = Peminjaman.query.filter_by(id=id).first()
    berkasPeminjam = berkas.peminjamBarang
    berkasDipinjam = berkas.barangDipinjam
    return render_template('peminjamanDiriK.html', task=berkas, orang=berkasPeminjam, brg=berkasDipinjam)

@app.route('/hapus/<int:id>')
def hapus(id):
    barang_dihapus = Barang.query.get_or_404(id)

    try:
        db.session.delete(barang_dihapus)
        db.session.commit()
        return redirect('/mainPage')
    except:
        return "sadge barang masih dipinjam"

@app.route('/hapus2/<int:id>')
def hapusG(id):
    temp = Gedung.query.get_or_404(id)
    try:
        db.session.delete(temp)
        db.session.commit()
        return redirect('/mainPage')
    except:
        return "sadge"

@app.route('/hapusK/<int:id>')
def hapusK(id):
    temp = Ruang.query.get_or_404(id)
    try:
        db.session.delete(temp)
        db.session.commit()
        return redirect('/mainPage')
    except:
        return "sadge"

@app.route('/hapusP/<int:id>')
def hapusP(id):
    temp = Peminjaman.query.get_or_404(id)
    temp.barangDipinjam.stoksisa += temp.banyak
    try:
        db.session.delete(temp)
        db.session.commit()
        return redirect('/mainPage')
    except:
        return "sadge"
    
@app.route('/logoutbye/')
def logoutbye():
    global pengguna
    try:
        del pengguna
        return redirect('/')
    except:
        return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)