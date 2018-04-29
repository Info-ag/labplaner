from datetime import date
from flask import Blueprint, request, jsonify
from models.date import Date, DateSchema
from app import db

bp = Blueprint("date_api", __name__)

date_schema = DateSchema()
dates_schema = DateSchema(many=True)



@bp.route("/id/<dtid>", methods=["GET"])   #REVIEW Is the date/ neccessary? Same question for events.py
def get_date_by_id(dtid):
    fdate = Date.query.get(dtid)
    return date_schema.jsonify(fdate)


@bp.route("/name/<rdate>", methods=["GET"])
def get_date_by_date(rdate):
    odate = date(int(rdate[4:]), int(rdate[2:4]), int(rdate[:2]))
    fdate = Date.query.filter_by(day=odate).scalar()
    return date_schema.jsonify(fdate)


@bp.route("/", methods=["GET"])
def get_all_dates():
    all_dates = Date.query.all()
    result = date_schema.dump(all_dates)
    return jsonify(result)
