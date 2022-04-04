from flask import Blueprint, jsonify,request
from modules.db import Attraction



att_manage = Blueprint('att_manage',__name__,template_folder="templates")



#%08 issue
@att_manage.route("/api/attractions", methods=["GET"])
def api_attr():
	page=request.args.get("page")
	keyword=request.args.get("keyword")
	#got keyword
	if keyword=="undefined":
		keyword=""
	if keyword!=None and keyword != "":
		ender=(int(page)+1)*12
		page=ender-12
		result=Attraction.attraction_key(page,ender,keyword)
		return jsonify(result)
	#no keywords
	else:
		if page==None:
			page=0
		#應改為抓13筆 判斷有無下頁
		ender=(int(page)+1)*12
		page=ender-11
		result=Attraction.attraction_no_key(page,ender)
		return jsonify(result)

		

#單一景點資料
@att_manage.route("/api/attraction/<attractionId>", methods=["GET"])
def api_atid(attractionId):
	result=Attraction.attraction_id(attractionId)
	return jsonify(result)
