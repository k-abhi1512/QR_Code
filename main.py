from flask import Flask, request, jsonify, make_response
from flask import render_template, request
from flask import redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
import qrcode
import main
import random, string


app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads/'

app.config['SECRET_KEY'] = 'thisissecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////mnt/c/Users/akumar/Desktop/httpmethods/qrgen.db'

db = SQLAlchemy(app)

class QRC(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50))
    image = db.Column(db.String(80))



# Generating the QR Code
@app.route('/', methods=['POST'])
def index():

    if request.method == 'POST':
        code = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(13))
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
            )
        qr.add_data(code)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        filename = ''.join(random.choice(string.ascii_lowercase) for _ in range(9))+'.png'
        pa = os.path.join(UPLOAD_FOLDER,  filename)
        img.save(pa)
        new_qr = QRC(code=code, image=pa)
        db.session.add(new_qr)
        db.session.commit()

        return jsonify({'message' : 'New QRCode Generated!'})
    else:
        return render_template('index.html')


# Getting all QR Code
@app.route('/qrlist', methods=['GET'])
def get_qr_list():
    qrlist = QRC.query.all()

    if not qrlist:
        return jsonify({'message' : 'No QR found!'})
    
    output = []
    for qr in qrlist:
        qr_data = {}
        qr_data['id'] = qr.id
        qr_data['code'] = qr.code
        qr_data['image'] = qr.image
        output.append(qr_data)

    return jsonify({'qr_list' : output})


# Getting the QR Code
@app.route('/qrlist/<int:id>', methods=['GET'])
def get_1qr_list(id):
    qrlist = QRC.query.filter_by(id=id).first()

    if not qrlist:
        return jsonify({'message' : 'No QR found!'})
    
    qr_data = {}
    qr_data['id'] = qrlist.id
    qr_data['code'] = qrlist.code
    qr_data['image'] = qrlist.image

    return jsonify({'qr_list' : qr_data})

#run the app
if __name__ == '__main__':
    app.run(debug=True) 


