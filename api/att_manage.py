

from flask import Blueprint, jsonify,request
from modules.db import Attraction

att_manage = Blueprint('att_manage',__name__,template_folder="templates")

@att_manage.route("/api/attractions", methods=["GET"])
def api_attr():
	page=request.args.get("page")
	keyword=request.args.get("keyword")
	if keyword=="undefined":
		keyword=""
	if keyword!=None and keyword != "":
		ender=(int(page)+1)*12
		page=ender-12
		result=Attraction.attraction_key(page,ender,keyword)
		return jsonify(result)
	else:
		if page==None:
			page=0
		ender=(int(page)+1)*12
		page=ender-11
		result=Attraction.attraction_no_key(page,ender)
		return jsonify(result)


@att_manage.route("/api/attraction/<attractionId>", methods=["GET"])
def api_atid(attractionId):
	result=Attraction.attraction_id(attractionId)
	return jsonify(result)
