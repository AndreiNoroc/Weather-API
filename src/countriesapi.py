from flask import Blueprint, json, Response, request
from sqlalchemy import exc
from mainmembers import db, Tari

countriesapi = Blueprint('countriesapi', __name__)

@countriesapi.route("/api/countries", methods=["POST"])
def postcountry():
    payload = request.json
    if payload and "nume" in payload and "lat" in payload and "lon" in payload:
        try:
            db.session.add(Tari(nume_tara=payload["nume"], latitudine=payload["lat"], longitudine=payload["lon"]))
            db.session.commit()
            ct = Tari.query.order_by(Tari.id.desc()).first()
        except exc.SQLAlchemyError:
            return Response(status=409)
        
        return Response(status=201, mimetype="application/json", response=json.dumps({'id': ct.id}))
    else:
        return Response(status=400)

@countriesapi.route("/api/countries", methods=["GET"])
def getcountries():
    resp = []
    countries = Tari.query.all()
    
    for x in countries:
        resp.append({'id': x.id, 'nume': x.nume_tara, 'lat': float(x.latitudine), 'lon': float(x.longitudine)})

    return Response(status=200, mimetype="application/json", response=json.dumps(resp))

@countriesapi.route("/api/countries/<id>", methods=["PUT"])
def putcountry(id):
    payload = request.json
    if "nume" in payload and "lat" in  payload and "lon" in payload:
        try:
            extractcountry = Tari.query.get(id)
            extractcountry.nume_tara = payload["nume"]
            extractcountry.latitudine = payload["lat"]
            extractcountry.longitudine = payload["lon"]
            db.session.commit()
        except (AttributeError, exc.SQLAlchemyError):
            return Response(status=404)
        return Response(status=200)
    else:
        return Response(status=400)

@countriesapi.route("/api/countries/<id>", methods=["DELETE"])
def delcountry(id):
    try:
        extractcountry = Tari.query.get(id)
        db.session.delete(extractcountry)
        db.session.commit()
    except exc.SQLAlchemyError:
        return Response(status=404)
    return Response(status=200)
