from . import db
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from io import BytesIO

class Gedung(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    namaGedung = db.Column(db.String(20), unique=True, nullable=False)
    barangs = db.relationship('Peminjaman', backref='tempatGedung')
    kelas = db.relationship('Ruang', backref='beradaPadaGedung')
    mg_gedung = db.Column(db.Integer, db.ForeignKey('manusia.id'))

class Ruang(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    namaRuang = db.Column(db.String(20), nullable=False)
    barangsR = db.relationship('Peminjaman', backref='tempatKelas')
    ged_id = db.Column(db.Integer, db.ForeignKey('gedung.id'), nullable=False)
    pj_ruang = db.Column(db.Integer, db.ForeignKey('manusia.id'))

class Barang(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    namaBarang = db.Column(db.String(200), nullable=False)
    dipinjam = db.relationship('Peminjaman', backref='barangDipinjam')
    stok = db.Column(db.Integer, nullable=False)
    bastPerolehan = db.Column(db.String(300))
    bastPerolehanData = db.Column(db.LargeBinary)
    bastPMimtype = db.Column(db.Text)
    stoksisa = db.Column(db.Integer)


    def __repr__(self):
        return f"Barang('{self.id}','{self.namaBarang}')"

class Manusia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(200), nullable=False)
    sandi = db.Column(db.String(10), nullable=False)
    alamat = db.Column(db.String(200))
    no_telp = db.Column(db.String(16))
    role = db.Column(db.Boolean, nullable=False)
    meminjam = db.relationship('Peminjaman', backref='peminjamBarang')
    gedungnya = db.relationship('Gedung', backref='MG_dariGedung')
    ruangnya = db.relationship('Ruang', backref='PJ_dariRuang')
    

class Peminjaman(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kodePeminjaman = db.Column(db.String(200), nullable=False)
    benda = db.Column(db.Integer, db.ForeignKey('barang.id'), nullable=False)
    peminjam = db.Column(db.Integer, db.ForeignKey('manusia.id'), nullable=False)
    ged = db.Column(db.Integer, db.ForeignKey('gedung.id'), nullable=False)
    kel = db.Column(db.Integer, db.ForeignKey('ruang.id'), nullable=False)
    jumlah = db.Column(db.Integer)
    tgl = db.Column(db.String(200))
    tgl2 = db.Column(db.String(200))
    bast = db.Column(db.String(300))
    bastData = db.Column(db.LargeBinary)
    bastMimtype = db.Column(db.Text)
    kondisi = db.Column(db.String(200))
    
class FileContents(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(300))
    data = db.Column(db.LargeBinary)


