from flask import Blueprint, json, Response, request
from sqlalchemy import exc, String
from sqlalchemy.sql.expression import cast
from mainmembers import db, Temperaturi, Orase, Tari
from datetime import datetime

temperaturesapi = Blueprint('temperaturesapi', __name__)

@temperaturesapi.route("/api/temperatures", methods=["POST"])
def posttemperature():
    payload = request.json
    if payload and "idOras" in payload and "valoare" in payload:
        try:
            db.session.add(Temperaturi(valoare=payload["valoare"], id_oras=payload["idOras"]))
            db.session.commit()
            ct = Temperaturi.query.order_by(Temperaturi.id.desc()).first()
        except exc.SQLAlchemyError:
            return Response(status=409)
        return Response(status=201, mimetype="application/json", response=json.dumps({'id': ct.id}))
    else:
        return Response(status=400)

@temperaturesapi.route("/api/temperatures", methods=["GET"])
def gettemperatures():
    latitudine = request.args.get('lat')
    longitudine = request.args.get('lon')
    fromd = request.args.get('from')
    untild = request.args.get('until')

    qs = []

    if latitudine:
        qs.append(cast(Orase.latitudine, String) == str("{0:.3f}".format(float(latitudine))))

    if longitudine:
        qs.append(cast(Orase.longitudine, String) == str("{0:.3f}".format(float(longitudine))))

    if fromd:
        qs.append(Temperaturi.timestamp >= datetime.strptime(fromd, "%Y-%m-%d"))

    if untild:
        qs.append(Temperaturi.timestamp <= datetime.strptime(untild, "%Y-%m-%d"))

    makeqs = []
    if not qs:
        makeqs = Temperaturi.query.all()
    else:
        makeqs = db.session.query(Temperaturi).join(Orase, Temperaturi.id_oras==Orase.id).filter(*qs).all()
    
    rsp = []
    for x in makeqs:
            rsp.append({'id': x.id, 'valoare': x.valoare, 'timestamp': str(datetime.strftime(x.timestamp, "%Y-%m-%d"))})
        
    return Response(status=200, mimetype="application/json", response=json.dumps(rsp))


@temperaturesapi.route("/api/temperatures/cities/<id_oras>", methods=["GET"])
def gettemperaturebycity(id_oras):
    fromd = request.args.get('from')
    untild = request.args.get('until')

    qs = []
    qs.append(Temperaturi.id_oras==id_oras)

    if fromd:
        qs.append(Temperaturi.timestamp >= datetime.strptime(fromd, "%Y-%m-%d"))
    if untild:
        qs.append(Temperaturi.timestamp <= datetime.strptime(untild, "%Y-%m-%d"))

    rsp = []
    makeqs = db.session.query(Temperaturi).filter(*qs).all()
    for x in makeqs:
        rsp.append({'id': x.id, 'valoare': x.valoare, 'timestamp': x.timestamp})

    return Response(status=200, mimetype="application/json", response=json.dumps(rsp))

@temperaturesapi.route("/api/temperatures/countries/<id_tara>", methods=["GET"])
def gettemperaturebycountry(id_tara):
    fromd = request.args.get('from')
    untild = request.args.get('until')

    qs = []
    qs.append(Orase.id_tara==id_tara)

    if fromd:
            qs.append(Temperaturi.timestamp >= datetime.strptime(fromd, "%Y-%m-%d"))
    if untild:
            qs.append(Temperaturi.timestamp <= datetime.strptime(untild, "%Y-%m-%d"))

    rsp = []
    makeqs = db.session.query(Temperaturi).join(Orase, Temperaturi.id_oras==Orase.id).join(Tari, Orase.id_tara==Tari.id).filter(*qs).all()
    for x in makeqs:
        rsp.append({'id': x.id, 'valoare': x.valoare, 'timestamp': x.timestamp})

    return Response(status=200, mimetype="application/json", response=json.dumps(rsp))

@temperaturesapi.route("/api/temperatures/<id>", methods=["PUT"])
def puttemperature(id):
    payload = request.json
    if payload and "idOras" in payload and "valoare" in  payload:
        try:
            extracttemperature = Temperaturi.query.get(id)
            extracttemperature.id_oras = payload["idOras"]
            extracttemperature.valoare = payload["valoare"]
            db.session.commit()
        except exc.SQLAlchemyError:
            return Response(status=404)
        return Response(status=200)
    else:
        return Response(status=400)

@temperaturesapi.route("/api/temperatures/<id>", methods=["DELETE"])
def deltemperature(id):
    try:
        extracttemperature = Temperaturi.query.get(id)
        db.session.delete(extracttemperature)
        db.session.commit()
    except exc.SQLAlchemyError:
        return Response(status=404)
    return Response(status=200)