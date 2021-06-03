from flask import Flask, render_template, url_for, request, redirect, flash, send_file, session, json, jsonify, Response
#from flask_sqlalchemy import SQLAlchemy
#from datetime import datetime
from . import app, db
from invent.dtbs import *
from invent.userSekarang import *
from invent.inputroutes import *
from io import BytesIO

global findPengguna
global pengguna 

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        session.pop('user', None)
        getID = request.form['namaa']
        getPass = request.form['sandi']

        try:
            orang = Manusia.query.filter_by(id=getID).first()
            if(orang):
                if(orang.sandi == getPass):
                    global jabatan
                    if(orang.role == 0):
                        session['user'] = getID
                        jabatan = 0
                    elif(orang.role == 1):   
                        session['admin'] = getID
                        jabatan = 1
                    global pengguna
                    pengguna = userNow(orang, orang.id, orang.sandi, orang.nama)
                    halo = str(pengguna.getNama())
                    return redirect('/menu')
                else:
                    return 'pass salah'
            else:
                return 'no id'
        except:
            return redirect('/')
    else:
        return render_template('index2.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/menu', methods=['POST', 'GET'])
def menu():
    try:
        if 'user' in session or 'admin' in session:
            try:
                halo = str(pengguna.getNama())
                return render_template('menu.html', halo=halo)
            except:
                return redirect('/')
        else:
            return redirect('/')
    except:
        return redirect('/')

@app.route('/inputMenu', methods=['POST', 'GET'])
def inputMenu():
    try:
        if 'admin' in session:
            return render_template('inputSemua.html')
        elif 'user' in session:
            return render_template('adminduls.html')
        else:
            return redirect('/')
    except:
        return redirect('/')
    
@app.route('/lihatRuang', methods=['POST', 'GET'])
def lihatRuang():
    try:
        if 'user' in session or 'admin' in session:
            if request.method == 'POST':
                building = request.form['gedungnya']
                if int(building)==0:
                    return redirect('/lihatRuang')
                else:
                    dafGedung = Gedung.query.all()
                    allRuang = Ruang.query.filter_by(ged_id=int(building))
                    gedungObj = Gedung.query.get_or_404(int(building))
                    gedungName = gedungObj.namaGedung
                    semuaRuang = []
                    banyakBarang = []
                    brg = Barang.query.all()
                    dataPinjam = []
                    for task in brg:
                        # e = Ruang.query.order_by(Ruang.id.desc()).filter_by(ged_id=2).first()
                        pinjam = Peminjaman.query.order_by(Peminjaman.id.desc()).filter_by(benda=task.id).first()
                        dataPinjam.append(pinjam)
                    for i in allRuang:
                        hitung = 0
                        for j in i.barangsR:
                            if j in dataPinjam:
                                hitung += 1
                        banyakBarang.append(hitung) 
                        semuaRuang.append(i)
                    return render_template('lihatRuang.html', ruangnya=semuaRuang, banyakBarang=banyakBarang, dafGedung=dafGedung, judul=f'Gedung {gedungName}', jabatan=jabatan)

            else:
                semuaRuang = Ruang.query.all()
                dafGedung = Gedung.query.all()
                banyakBarang = []
                brg = Barang.query.all()
                dataPinjam = []
                for task in brg:
                    # e = Ruang.query.order_by(Ruang.id.desc()).filter_by(ged_id=2).first()
                    pinjam = Peminjaman.query.order_by(Peminjaman.id.desc()).filter_by(benda=task.id).first()
                    dataPinjam.append(pinjam)
                for i in semuaRuang:
                    hitung = 0
                    for j in i.barangsR:
                        if j in dataPinjam:
                            hitung += 1
                    banyakBarang.append(hitung) 
                return render_template('lihatRuang.html', ruangnya=semuaRuang, banyakBarang=banyakBarang, dafGedung=dafGedung, jabatan=jabatan, judul="Seluruh Ruang")
        else:
            return redirect('/')
    except:
        return redirect('/')

@app.route('/lihatGedung', methods=['POST', 'GET'])
def lihatGedung():
    try:
        if 'user' in session or 'admin' in session:
            if request.method == 'POST':
                pass
            else:
                semuaGedung = Gedung.query.all()
                semuaRuang = Ruang.query.all()
                banyakBarang = []
                banyakRuang = []
                brg = Barang.query.all()
                dataPinjam = []
                for task in brg:
                    pinjam = Peminjaman.query.order_by(Peminjaman.id.desc()).filter_by(benda=task.id).first()
                    dataPinjam.append(pinjam)
                # for i in semuaRuang:
                #     hitung = 0
                #     for j in i.barangsR:
                #         if j in dataPinjam:
                #             hitung += 1
                #     banyakBarangT.append(hitung) 
                for i in semuaGedung:
                    hitung = 0
                    hitungR = 0
                    for j in i.kelas:
                        for k in j.barangsR:
                            if k in dataPinjam:
                                hitung += 1
                        hitungR += 1
                    banyakBarang.append(hitung)
                    banyakRuang.append(hitungR)
                return render_template('lihatGedung.html', gedungnya=semuaGedung, banyakBarang=banyakBarang, banyakRuang=banyakRuang, judul="Seluruh Gedung")
        else:
            return redirect('/')
    except:
        return redirect('/')

@app.route('/lihatBarang', methods=['POST', 'GET'])
def lihatBarang():
    try:
        if 'user' in session or 'admin' in session:
            if request.method == 'POST':
                building = request.form['gedungnya']
                room = request.form['ruangnya']
                if int(room) != 0:
                    roomName = Ruang.query.filter_by(id=int(room)).first()
                    roomName = roomName.namaRuang
                    
                    brg = Barang.query.all()
                    dataPinjam = []
                    dataPinjam2 = []
                    stats = []
                    dafGedung = Gedung.query.all()
                    dafKelas = Ruang.query.all()
                    for task in brg:
                        # e = Ruang.query.order_by(Ruang.id.desc()).filter_by(ged_id=2).first()
                        pinjam = Peminjaman.query.order_by(Peminjaman.id.desc()).filter_by(benda=task.id).first()
                        if pinjam:
                            dataPinjam.append(pinjam)
                    
                    for i in dataPinjam:
                        if i.kel == int(room):
                            dataPinjam2.append(i)
                            stats.append(1)
                
                    # for i in dataPinjam:
                    #     pinjam = Peminjaman.query.filter_by(kel=room, id=i.id).first()            
                    #     dataPinjam2.append(pinjam)

                    return render_template('lihatBarang.html', brg=brg, pinjam=dataPinjam2, stats=stats, dafGedung=dafGedung, dafKelas=dafKelas, judul=f"Ruang {roomName}")
                elif int(building) !=0:
                    roomName = Gedung.query.filter_by(id=int(building)).first()
                    roomName = roomName.namaGedung
                    
                    brg = Barang.query.all()
                    dataPinjam = []
                    dataPinjam2 = []
                    stats = []
                    dafGedung = Gedung.query.all()
                    dafKelas = Ruang.query.all()
                    for task in brg:
                        # e = Ruang.query.order_by(Ruang.id.desc()).filter_by(ged_id=2).first()
                        pinjam = Peminjaman.query.order_by(Peminjaman.id.desc()).filter_by(benda=task.id).first()
                        if pinjam:
                            dataPinjam.append(pinjam)
                    
                    for i in dataPinjam:
                        if i.ged == int(building):
                            dataPinjam2.append(i)
                            stats.append(1)
                
                    # for i in dataPinjam:
                    #     pinjam = Peminjaman.query.filter_by(kel=room, id=i.id).first()            
                    #     dataPinjam2.append(pinjam)

                    return render_template('lihatBarang.html', brg=brg, pinjam=dataPinjam2, stats=stats, dafGedung=dafGedung, dafKelas=dafKelas, judul=f"Gedung {roomName}")
                else:
                    return redirect('/lihatBarang')

            else:
                brg = Barang.query.all()
                dataPinjam = []
                stats = []
                dafGedung = Gedung.query.all()
                dafKelas = Ruang.query.all()
                for task in brg:
                    # e = Ruang.query.order_by(Ruang.id.desc()).filter_by(ged_id=2).first()
                    pinjam = Peminjaman.query.order_by(Peminjaman.id.desc()).filter_by(benda=task.id).first()
                    if pinjam :
                        stats.append(1)
                    else :
                        stats.append(0)
                    dataPinjam.append(pinjam)

                return render_template('lihatBarang.html', brg=brg, pinjam=dataPinjam, stats=stats, dafGedung=dafGedung, dafKelas=dafKelas, judul="Seluruh Barang")
        else:
            return redirect('/')
    except:
        return redirect('/')

@app.route('/lihatPegawai', methods=['POST', 'GET'])
def lihatPegawai():
    try:
        if 'user' in session or 'admin' in session:
            dafPegawai = Manusia.query.all()
            return render_template('lihatPegawai.html', pegawainya=dafPegawai)
        else:
            return redirect('/')
    except:
        return redirect('/')
        
@app.route('/lihatPeminjaman', methods=['POST', 'GET'])
def lihatPeminjaman():
    #try:
        if 'user' in session or 'admin' in session:
            if request.method == 'POST':
                barangnya = request.form['barangnya']
                ruangnya = request.form['ruangnya']
                gedungnya = request.form['gedungnya']
                dafGedung = Gedung.query.all()
                dafKelas = []
                if int(barangnya) != 0:
                    keyword = Barang.query.get_or_404(int(barangnya))
                    keyword = keyword.namaBarang
                    dafBarang = Barang.query.all()
                    dafBarang2 = []
                    for i in dafBarang:
                        temp = Peminjaman.query.filter_by(benda=i.id).first()
                        if temp:
                            dafBarang2.append(i)
                    dafPinjam = Peminjaman.query.filter_by(benda=int(barangnya))
                    dafPinjam2 = []
                    for i in dafPinjam:
                        dafPinjam2.append(i)
                    return render_template('lihatPeminjaman.html', dafPinjam=dafPinjam2, dafBarang=dafBarang2, judul=f"Riwayat Peminjaman Barang {keyword}", dafGedung=dafGedung, dafKelas=dafKelas)
                elif int(ruangnya) != 0:
                    keyword = Ruang.query.get_or_404(int(ruangnya))
                    keyword = keyword.namaRuang
                    dafBarang = Barang.query.all()
                    dafBarang2 = []
                    for i in dafBarang:
                        temp = Peminjaman.query.filter_by(benda=i.id).first()
                        if temp:
                            dafBarang2.append(i)
                    dafPinjam = Peminjaman.query.filter_by(kel=int(ruangnya))
                    dafPinjam2 = []
                    for i in dafPinjam:
                        dafPinjam2.append(i)
                    return render_template('lihatPeminjaman.html', dafPinjam=dafPinjam2, dafBarang=dafBarang2, judul=f"Riwayat Peminjaman Ruang {keyword}", dafGedung=dafGedung, dafKelas=dafKelas)
                elif int(gedungnya) != 0:
                    keyword = Gedung.query.get_or_404(int(gedungnya))
                    keyword = keyword.namaGedung
                    dafBarang = Barang.query.all()
                    dafBarang2 = []
                    for i in dafBarang:
                        temp = Peminjaman.query.filter_by(benda=i.id).first()
                        if temp:
                            dafBarang2.append(i)
                    dafPinjam = Peminjaman.query.filter_by(ged=int(gedungnya))
                    dafPinjam2 = []
                    for i in dafPinjam:
                        dafPinjam2.append(i)
                    return render_template('lihatPeminjaman.html', dafPinjam=dafPinjam2, dafBarang=dafBarang2, judul=f"Riwayat Peminjaman Gedung {keyword}", dafGedung=dafGedung, dafKelas=dafKelas)

                else:
                    return redirect('/lihatPeminjaman')
            else:
                dafGedung = Gedung.query.all()
                dafKelas = []
                dafPinjam = Peminjaman.query.all()
                dafBarang = Barang.query.all()
                dafBarang2 = []
                for i in dafBarang:
                    temp = Peminjaman.query.filter_by(benda=i.id).first()
                    if temp:
                        dafBarang2.append(i)
                return render_template('lihatPeminjaman.html', dafPinjam=dafPinjam, dafBarang=dafBarang2, judul="Seluruh Peminjaman", dafGedung=dafGedung, dafKelas=dafKelas)
        else:
            return redirect('/')
    #except:
        #return redirect('/')

@app.route('/inputPinjam', methods=['POST', 'GET'])
def inputPinjam():
    try:
        if 'user' in session or 'admin' in session:
            dafGedung = Gedung.query.all()
            dafBarang = Barang.query.all()
            dafKelas = Ruang.query.all()
            if request.method == 'POST':
                if request.form['ruangnya'] != '':
                    global pengguna
                    nama = request.form['nama']
                    barangnya = request.form['barangnya']
                    ruangnya = request.form['ruangnya']
                    gedungnyat = Ruang.query.filter_by(id=ruangnya).first()
                    gedungnya = gedungnyat.ged_id
                    file = request.files['inputFile']
                    kondisi = request.form['kondisi']
                    tgl = request.form['tgl']

                    # global mimtipe
                    mimtipe = file.mimetype
                    #try:
                    newFile = Peminjaman(kodePeminjaman=nama, benda=barangnya, peminjam=pengguna.getID(), ged=gedungnya, kel=ruangnya, bast=file.filename, bastData=file.read(), bastMimtype=mimtipe, tgl=tgl, kondisi=kondisi)
                    db.session.add(newFile)
                    db.session.commit()
                    return "noice"
                    #except:
                        #return 'gatau gagal'
                else:
                    return "masukin ngab"
                # elif request.form['gedungnya'] != '':
                #     gedungnya = request.form['gedungnya']
                #     gedungo = Gedung.query.get_or_404(gedungnya)

                #     try:
                #         if(dafKelas == Ruang.query.all()):
                #             dafKelas = Ruang.query.filter_by(beradaPadaGedung = gedungo)
                #             return render_template('', dafGedung=gedungo, dafKelas=dafKelas)
                #     except:
                #         return 'ngatau gagal'
            else:
                return render_template('inputPinjam.html', dafGedung=dafGedung, dafKelas=dafKelas, dafBarang=dafBarang)
        else:
            return redirect('/')
    except:
        return redirect('/')

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    try:
        if 'user' in session or 'admin' in session:
            if request.method == 'POST':
                nama = request.form['nama']
                file = request.files['inputFile']

                newFile = FileContents(name=file.filename, data=file.read())
                db.session.add(newFile)
                db.session.commit()

                return 'Saved ' + file.filename + ' success.'
            
            else:
                return render_template('upld.html')
        else:
            return redirect('/')
    except:
        return redirect('/')


@app.route('/logoutbye', methods=['POST', 'GET'])
def logoutbye():
    try:
        global pengguna
        global jabatan
        
        if 'user' in session:
            session.pop('user', None)

        if 'admin' in session:
            session.pop('admin', None)

        try:
            del pengguna
            del jabatan
            return redirect('/')
        except:
            return redirect('/')
         
        return 'not done'
    except:
        return redirect('/')
    
# @app.route('/clears', methods=['POST', 'GET'])
# def clears():
#     if 'user' in session:
#         session.pop('user', None)
#         return 'done user'

#     if 'admin' in session:
#         session.pop('admin', None)
#         return 'done admin'
    
#     return 'not done'

@app.route('/writefile', methods=['POST', 'GET'])
def writefile():
    namasaya = "SAYYID GENGS"
    f = open("invent/ini.txt", "w")
    f.write(f"""Let's go!!
I am {namasaya}
Yooourssss""")
    f.close()
    f = open("invent/ini.txt", "a")
    f.write(f"\n{namasaya}")
    f.close()
    
    return send_file(filename_or_fp="ini.txt", attachment_filename="ehehe.txt", as_attachment=True, cache_timeout=0)

@app.route('/walao', methods=['POST', 'GET'])
def walao():
    return render_template('menu.html')

@app.route('/donlotBast/<namaFile>')
def donlotBast(namaFile):
    try:
        if 'user' in session or 'admin' in session:
            file_data = Peminjaman.query.filter_by(id=namaFile).first()

            return send_file(BytesIO(file_data.bastData), attachment_filename=file_data.bast, as_attachment=True, cache_timeout=0)
        else:
            return redirect('/')
    except:
        return redirect('/')

@app.route('/viewBast/<namaFile>')
def viewBast(namaFile):
    try:
        if 'user' in session or 'admin' in session:
            file_data = Peminjaman.query.filter_by(id=namaFile).first()

            return Response(file_data.bastData, mimetype=file_data.bastMimtype)
        else:
            return redirect('/')
    except:
        return redirect('/')

@app.route('/donlotBastP/<namaFile>')
def donlotBastP(namaFile):
    try:
        if 'user' in session or 'admin' in session:
            file_data = Barang.query.filter_by(id=namaFile).first()

            return send_file(BytesIO(file_data.bastPerolehanData), attachment_filename=file_data.bastPerolehan, as_attachment=True, cache_timeout=0)
        else:
            return redirect('/')
    except:
        return redirect('/')

@app.route('/viewBastP/<namaFile>')
def viewBastP(namaFile):
    try:
        if 'user' in session or 'admin' in session:
            file_data = Barang.query.filter_by(id=namaFile).first()

            return Response(file_data.bastPerolehanData, mimetype=file_data.bastPMimtype)
        else:
            return redirect('/')
    except:
        return redirect('/')

@app.route('/detailRuang/<int:id>', methods=['POST', 'GET'])
def detailRuang(id):
    try:
        if 'user' in session or 'admin' in session:
            ruangnya = Ruang.query.filter_by(id=id).first()

            brg = Barang.query.all()
            dataPinjam = []
            dataPinjam2 = []
            banyakBarang = 0
            banyakPinjam = 0
            for task in brg:
                # e = Ruang.query.order_by(Ruang.id.desc()).filter_by(ged_id=2).first()
                pinjam = Peminjaman.query.order_by(Peminjaman.id.desc()).filter_by(benda=task.id).first()
                if pinjam:
                    dataPinjam.append(pinjam)
            
            for i in dataPinjam:
                if i.kel == int(id):
                    dataPinjam2.append(i)
                    banyakBarang += 1
            
            listPinjam2 = Peminjaman.query.filter_by(kel=id)
            listPinjam = []

            for i in listPinjam2:
                banyakPinjam += 1
                listPinjam.append(i)
            
            return render_template('detailRuang.html', id=id, dafPinjam=dataPinjam2, ruangnya=ruangnya, banyakBarang=banyakBarang, listPinjam=listPinjam, banyakPinjam=banyakPinjam)
        else:
            return redirect('/')
    except:
        return redirect('/')


@app.route('/detailGedung/<int:id>', methods=['POST', 'GET'])
def detailGedung(id):
    try:
        if 'user' in session or 'admin' in session:
            gedungnya = Gedung.query.filter_by(id=id).first()
            
            brg = Barang.query.all()
            dataPinjam = []
            dataPinjam2 = []
            banyakBarang = 0
            banyakPinjam = 0
            for task in brg:
                # e = Ruang.query.order_by(Ruang.id.desc()).filter_by(ged_id=2).first()
                pinjam = Peminjaman.query.order_by(Peminjaman.id.desc()).filter_by(benda=task.id).first()
                if pinjam:
                    dataPinjam.append(pinjam)
            
            for i in dataPinjam:
                if i.ged == int(id):
                    dataPinjam2.append(i)
                    banyakBarang += 1
            
            dataPinjam = Ruang.query.filter_by(ged_id=id)
            listRuang = []
            banyakRuang = 0
            for i in dataPinjam:
                listRuang.append(i)
                banyakRuang += 1
            
            listPinjam2 = Peminjaman.query.filter_by(ged=id)
            listPinjam = []

            for i in listPinjam2:
                banyakPinjam += 1
                listPinjam.append(i)
            
            return render_template('detailGedung.html', id=id, dafPinjam=dataPinjam2, gedungnya=gedungnya, banyakBarang=banyakBarang, listPinjam=listPinjam, banyakPinjam=banyakPinjam, listRuang=listRuang, banyakRuang=banyakRuang)
        else:
            return redirect('/')
    except:
        return redirect('/')

@app.route('/detailBarang/<int:id>', methods=['POST', 'GET'])
def detailBarang(id):
    try:
        if 'user' in session or 'admin' in session:
            barangnya = Barang.query.filter_by(id=id).first()
            pinjam = Peminjaman.query.order_by(Peminjaman.id.desc()).filter_by(benda=id).first()
            listPinjam2 = Peminjaman.query.filter_by(benda=id)
            banyakPinjam = 0
            listPinjam = []
            stat = 0

            for i in listPinjam2:
                banyakPinjam += 1
                listPinjam.append(i)

            if pinjam:
                stat = 1

            return render_template('detailBarang.html', id=id, barangnya=barangnya, pinjam=pinjam, listPinjam=listPinjam, banyakPinjam=banyakPinjam, stat=stat)
        else:
            return redirect('/')
    except:
        return redirect('/')

@app.route('/detailPeminjaman/<int:id>')
def detailPeminjaman(id):
    try:
        if 'user' in session or 'admin' in session:
            pinjamnya = Peminjaman.query.filter_by(id=id).first()

            return render_template('detailPeminjaman.html', id=id, pinjamnya=pinjamnya)

    except:
        return redirect('/')

@app.route('/detailPegawai/<int:id>')
def detailPegawai(id):
    try:
        if 'user' in session or 'admin' in session:
            pegawainya = Manusia.query.filter_by(id=id).first()
            pinjam = Peminjaman.query.filter_by(peminjam=id)
            listPinjam = []
            banyakPinjam = 0

            for i in pinjam:
                listPinjam.append(i)
                banyakPinjam += 1

            return render_template('detailPegawai.html', id=id, pegawainya=pegawainya, banyakPinjam=banyakPinjam, listPinjam=listPinjam)
    except:
        return redirect('/')

@app.route('/barang/<get_brg>')
def findBarang(get_brg):
    try:
        if 'user' in session or 'admin' in session:
            roomName = Ruang.query.filter_by(id=int(get_brg)).first()
            roomName = roomName.namaRuang
            
            brg = Barang.query.all()
            dataPinjam = []
            dataPinjam2 = []
            stats = []
            dafGedung = Gedung.query.all()
            dafKelas = Ruang.query.filter_by(ged_id=1)
            for task in brg:
                # e = Ruang.query.order_by(Ruang.id.desc()).filter_by(ged_id=2).first()
                pinjam = Peminjaman.query.order_by(Peminjaman.id.desc()).filter_by(benda=task.id).first()
                if pinjam:
                    dataPinjam.append(pinjam)
            
            for i in dataPinjam:
                if i.kel == int(get_brg):
                    dataPinjam2.append(i)
                    stats.append(1)
            
            brgArray = []
            for i in dataPinjam2:
                rObj = {}
                rObj['id'] = i.barangDipinjam.id
                rObj['name'] = i.barangDipinjam.namaBarang
                brgArray.append(rObj)
            return jsonify({'brgarray' : brgArray})
            
        else:
            return redirect('/')
    except:
        return redirect('/')

        
@app.route('/barangG/<get_brg>')
def findBarangG(get_brg):
    try:
        if 'user' in session or 'admin' in session:
            roomName = Ruang.query.filter_by(id=int(get_brg)).first()
            roomName = roomName.namaRuang
            
            brg = Barang.query.all()
            dataPinjam = []
            dataPinjam2 = []
            stats = []
            dafGedung = Gedung.query.all()
            dafKelas = Ruang.query.filter_by(ged_id=1)
            for task in brg:
                # e = Ruang.query.order_by(Ruang.id.desc()).filter_by(ged_id=2).first()
                pinjam = Peminjaman.query.order_by(Peminjaman.id.desc()).filter_by(benda=task.id).first()
                if pinjam:
                    dataPinjam.append(pinjam)
            
            for i in dataPinjam:
                if i.ged == int(get_brg):
                    dataPinjam2.append(i)
                    stats.append(1)
            
            brgArray = []
            for i in dataPinjam2:
                rObj = {}
                rObj['id'] = i.barangDipinjam.id
                rObj['name'] = i.barangDipinjam.namaBarang
                brgArray.append(rObj)
            return jsonify({'brgarray' : brgArray})
            
        else:
            return redirect('/')
    except:
        return redirect('/')