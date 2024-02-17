from flask import Flask, jsonify, redirect, render_template, url_for, session
from flask import request as rq
from clienteServicio import ClienteServicio
from forms import Tarjeta, Nip, Pago


app = Flask(__name__)

app.secret_key = "2451456769873"


@app.route("/")
def formulario():
    form = Tarjeta()
    return render_template("formularios/ingresar.html", form = form)


@app.route('/tarjeta', methods = ['POST'])
def getTajeta():
    trajeta_form = Tarjeta()
    if rq.method == 'POST':
        cl = ClienteServicio()
        mensaje = ""
        num = rq.form['num_tarjeta']
        session['num'] = num
        respuesta = cl.validate_terjet(num)

        if trajeta_form.validate_on_submit():
            if respuesta['verificada']:
                return redirect(url_for("formNip"))
            else:
                mensaje = respuesta['mensaje']
                return render_template("formularios/ingresar.html", form = trajeta_form, mensaje = mensaje)
    return jsonify({"respuesta":num})


@app.route('/formNip/', methods = ['GET'])
def formNip():
    nip_form = Nip()
    intentos = 0
    mensaje = ""
    if 'intentos' in session and 'mensaje'in session:
        intentos = session['intentos']
        intentos = 0
    return render_template("formularios/nip.html", form = nip_form, mensaje = mensaje, intentos = intentos)


@app.route('/nip', methods = ['POST'])
def getNip():
    nip_form = Nip()
    cl = ClienteServicio()
    pago_form = Pago()
    
    if rq.method == 'POST':        
        mensaje = ""
        mensaje_retiro= ""
        if nip_form.validate_on_submit():
            if 'num' in session:
                num = session['num']
                num_nip = rq.form['num_nip']
                respuesta = cl.validate_nip(num, num_nip)
                saldo = cl.verifica_saldo(num)
                limite = cl.verifica_limite(num)
                if respuesta['verificada']:
                    
                    return render_template("formularios/cliente.html", form= pago_form, saldo = saldo, limite = limite, mensaje = mensaje_retiro)
                else:
                    if respuesta['intentos'] >= 3:
                        return redirect(url_for("formulario"))
                    session['intentos'] = respuesta['intentos']
                    mensaje = respuesta['mensaje']
            else:
                return redirect(url_for(formulario))
    return render_template("formularios/nip.html", form = nip_form, mensaje = mensaje, intentos=respuesta['intentos'])
    
@app.route('/retiro', methods = ['POST'])
def retiro():
    cl = ClienteServicio()
    pago_form = Pago()
    cantidad = float(rq.form['pago'])
    print('Vista retiro/ cantidad -> ' + str(cantidad))
    mensaje = ""
    if rq.method == 'POST':
        if 'num' in session:
            num = session['num']
            saldo = cl.verifica_saldo(num)
            limite = cl.verifica_limite(num)
            if cantidad <= 0:
                mensaje = "La cantidad debe ser mayor a cero 😒"
            if pago_form.validate_on_submit():
                respuesta = cl.realiza_retiro(num, cantidad)
                #print("ACantidad ", respuesta)
                return render_template("formularios/cliente.html", form= pago_form, saldo = respuesta['saldo'], limite = limite, mensaje = respuesta['mensaje'])
            else:
                redirect(url_for("formNip"))
    return render_template("formularios/cliente.html", form= pago_form, saldo = saldo, limite = limite, mensaje = mensaje)

            
if __name__ == '__main__':
    app.run(debug = True, port = 5000)




