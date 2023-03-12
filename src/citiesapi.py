from flask import Blueprint, json, Response, request
from sqlalchemy import exc
from mainmembers import db, Orase

citiesapi = Blueprint('citiesapi', __name__)

@citiesapi.route("/api/cities", methods=["POST"])
def postcity():
    payload = request.json
    if payload and "idTara" in payload and "nume" in payload and "lat" in payload and "lon" in payload:
        try:
            db.session.add(Orase(id_tara=payload["idTara"], nume_oras=payload["nume"], latitudine=payload["lat"], longitudine=payload["lon"]))
            db.session.commit()
            ct = Orase.query.order_by(Orase.id.desc()).first()#nume
        except exc.SQLAlchemyError:
            return Response(status=409)
        return Response(status=201, mimetype="application/json", response=json.dumps({'id': ct.id}))
    else:
        return Response(status=400)

@citiesapi.route("/api/cities", methods=["GET"])
def getcities():
    rsp = []
    cities = Orase.query.all()

    for x in cities:
        rsp.append({'id': x.id, 'idTara': x.id_tara, 'nume': x.nume_oras, 'lat': float(x.latitudine), 'lon': float(x.longitudine)})

    return Response(status=200, mimetype="application/json", response=json.dumps(rsp))

@citiesapi.route("/api/cities/country/<id>", methods=["GET"])
def getcitiesbycountry(id):
    rsp = []
    cities = Orase.query.filter_by(id_tara=id)

    for x in cities:
        rsp.append({'id': x.id, 'nume': x.nume_oras, 'lat': float(x.latitudine), 'lon': float(x.longitudine)})
    
    return Response(status=200, mimetype="application/json", response=json.dumps(rsp))

@citiesapi.route("/api/cities/<id>", methods=["PUT"])
def putcity(id):
    payload = request.json
    if payload and "idTara" in payload and "nume" in payload and "lat" in payload and "lon" in payload:
        try:
            extractcity = Orase.query.get(id)
            extractcity.id_tara = payload["idTara"]
            extractcity.nume_oras = payload["nume"]
            extractcity.latitudine = payload["lat"]
            extractcity.longitudine = payload["lon"]
            db.session().commit()
        except exc.SQLAlchemyError:
            return Response(status=404)
        return Response(status=200)
    else:
        return Response(status=400)

@citiesapi.route("/api/cities/<id>", methods=["DELETE"])
def deletecity(id):
    try:
        extractcity = Orase.query.get(id)
        db.session.delete(extractcity)
        db.session.commit()
    except exc.SQLAlchemyError:
        return Response(status=404)
    return Response(status=200)
