from flask import Flask, render_template, url_for, request, redirect, flash, send_file, session, json, jsonify
#from flask_sqlalchemy import SQLAlchemy
#from datetime import datetime
from . import app, db
from invent.dtbs import *
from invent.userSekarang import *
from io import BytesIO


@app.route('/inputBarang', methods=['POST', 'GET'])
def inputBarang():
    try:
        if 'user' in session or 'admin' in session:
            if request.method == 'POST':
                nama = request.form['nama']
                stok = request.form['stokc']
                file = request.files['inputFile']

                mimtipe = file.mimetype
                try:
                    newFile = Barang(namaBarang=nama, stok=stok, bastPerolehan=file.filename, bastPerolehanData=file.read(), bastPMimtype=mimtipe)
                    db.session.add(newFile)
                    db.session.commit()
                    return "noice"
                except:
                    return "false"
            else:
                return render_template('inputBarang.html')
        else:
            return redirect('/')
    except:
        return redirect('/')

@app.route('/inputManusia', methods=['POST', 'GET'])
def inputManusia():
    try:
        if 'user' in session or 'admin' in session:
            if request.method == 'POST':
                id = request.form['id']
                nama = request.form['nama']
                sandi = request.form['sandi']
                alamat = request.form['alamat']
                notelp = request.form['notelp']

                try:
                    newFile = Manusia(id=id, nama=nama, sandi=sandi, alamat=alamat, no_telp=notelp, role=0)
                    db.session.add(newFile)
                    db.session.commit()
                    return "noice"
                except:
                    return "false"
            else:
                return render_template('inputManusia.html')
        else:
            return redirect('/')
    except:
        return redirect('/')

@app.route('/inputGedung', methods=['POST', 'GET'])
def inputGedung():
    try:
        if 'user' in session or 'admin' in session:
                if request.method == 'POST':
                    nama = request.form['nama']
                    pegawainya = request.form['pegawainya']
                    
                    try:
                        newFile = Gedung(namaGedung=nama, mg_gedung=int(pegawainya))
                        db.session.add(newFile)
                        db.session.commit()
                        return "noice"
                    except:
                        return "gagal"
                else:
                    dafPegawai = Manusia.query.all()
                    return render_template('inputGedung.html', dafPegawai=dafPegawai)
        else:
            return redirect('/')
    except:
        return redirect('/')

@app.route('/inputRuang', methods=['POST', 'GET'])
def inputRuang():
    try:
        if 'user' in session or 'admin' in session:
            if request.method == 'POST':
                if request.method == 'POST':
                    nama = request.form['nama']
                    gedungnya = request.form['gedungnya']
                    pegawainya = request.form['pegawainya']

                    try:
                        tempat = Gedung.query.filter_by(id=gedungnya).first()
                        kelas_baru = Ruang(namaRuang=nama, ged_id=tempat.id, pj_ruang=int(pegawainya))
                        db.session.add(kelas_baru)
                        db.session.commit()
                        return "noice"
                    except:
                        return 'gatau gagal'
            else:
                dafPegawai = Manusia.query.all()
                dafGedung = Gedung.query.all()
                return render_template('inputRuang.html', dafGedung=dafGedung, dafPegawai=dafPegawai)
        else:
            return redirect('/')
    except:
        return redirect('/')

@app.route('/ruang/<get_ruang>')
def findRuang(get_ruang):
    try:
        if 'user' in session or 'admin' in session:
            if(int(get_ruang) != 0):
                ruang = Ruang.query.filter_by(ged_id=get_ruang)
            else:
                ruang = Ruang.query.all()
            ruangArray = []
            for i in ruang:
                rObj = {}
                rObj['id'] = i.id
                rObj['name'] = i.namaRuang
                ruangArray.append(rObj)
            return jsonify({'ruangarray' : ruangArray})
        else:
            return redirect('/')
    except:
        return redirect('/')

@app.route('/tesdownload', methods=['POST', 'GET'])
def download():
    try:
        if 'user' in session or 'admin' in session:
            file_data = FileContents.query.filter_by(id=1).first()

            return send_file(BytesIO(file_data.data), attachment_filename=file_data.name, as_attachment=True, cache_timeout=0)
        else:
            return redirect('/')
    except:
        return redirect('/')