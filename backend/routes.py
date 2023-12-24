from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))


######################################################################
# RETURN HEALTH OF THE APP
######################################################################

@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200


######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################

@app.route("/count")
def count():
    if not data:
        return {"message": "internal server error"}, 500
    return jsonify(length=len(data)), 200


######################################################################
# GET ALL PICTURES
######################################################################

@app.route("/picture", methods=["GET"])
def get_pictures():
    if not data:
        return {"message": "internal server error"}, 500
    return data


######################################################################
# GET A PICTURE
######################################################################

@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    if not data:
        return {"message": "internal server error"}, 500
    for picture in data:
        if picture["id"] == id:
            return picture, 200
    return {"message": "picture not found"}, 404


######################################################################
# CREATE A PICTURE
######################################################################

@app.route("/picture", methods=["POST"])
def create_picture():
    if not data:
        return {"message": "internal server error"}, 500
    new_picture = request.get_json()
    for picture in data:
        if picture["id"] == new_picture["id"]:
            return {"message": f"picture with id {picture['id']} already present"}, 302
    data.append(new_picture)
    return new_picture, 201


######################################################################
# UPDATE A PICTURE
######################################################################

@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    if not data:
        return {"message": "internal server error"}, 500
    new_picture_data = request.get_json()
    for picture in data:
        if picture["id"] == new_picture_data["id"]:
            picture.update(new_picture_data)
            return picture, 201
    return {"message": "picture not found"}, 404


######################################################################
# DELETE A PICTURE
######################################################################

@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    if not data:
        return {"message": "internal server error"}, 500
    for picture in data:
        if picture["id"] == id:
            data.remove(picture)
            return "", 204
    return {"message": "picture not found"}, 404
