#!/usr/bin/env python
#-*- coding: utf-8

import sys
import types
import math
import re
import pg
import urllib
import kmlbase
import kmldom
import kmlengine

import kmlcedric
import fed

class fedpolls():

    BLANK16 = "http://earth.smurfmatic.net/img/16px.png"
    GCHARTURL = "http://chart.apis.google.com/chart"
    
    def __init__(self, ely, fednum, nowater=True):
	self.ely = ely
	self.fednum = fednum
	self.nowater = nowater
	self.ed_namee = ""
	self.ed_namef = ""
    	self.conn = pg.connect('canada', '127.0.0.1', 5432, None, None, 'canada', 'aew2ohVu')
	self.factory = kmldom.KmlFactory_GetFactory()
	self.kml = self.factory.CreateElementById(kmldom.Type_kml)

    def DB(self):
	# polygons
	if self.nowater:
	    nowater_str = "_nowater"
	else:
	    nowater_str = ""
	sql_args = { "fednum":self.fednum, "ely": self.ely, "nowater": nowater_str }
	# fed riding
	#resgeofed = self.conn.query("SELECT * FROM fed308_a WHERE fed_num = '%d' " % sql_args).dictresult()
	sql_riding = "SELECT gid, ed_id, ed_namee, ed_namef, \
	    ST_AsKML(ST_Transform(the_geom, 4326)) AS boundary, \
	    ST_X(ST_Centroid(ST_Transform(the_geom, 4326))) AS x, ST_Y(ST_Centroid(ST_Transform(the_geom, 4326))) AS y, \
	    ST_XMax(ST_Envelope(ST_Transform(the_geom, 4326))) AS bbox_xmax, ST_YMax(ST_Envelope(ST_Transform(the_geom, 4326))) AS bbox_ymax, \
	    ST_XMin(ST_Envelope(ST_Transform(the_geom, 4326))) AS bbox_xmin, ST_YMin(ST_Envelope(ST_Transform(the_geom, 4326))) AS bbox_ymin, \
	    ST_Envelope(ST_Transform(the_geom, 4326)) AS bbox \
	    FROM fed308_a WHERE fed_num = %(fednum)d " % sql_args
	resgeofed = self.conn.query(sql_riding % sql_args).dictresult()
	self.ed_namee = resgeofed[0]["ed_namee"]
	self.ed_namef = resgeofed[0]["ed_namef"]
	if self.fednum >= 24000 & self.fednum < 25000:
	    self.ed_name = self.ed_namef
	else:
	    self.ed_name = self.ed_namee
	self.boundary = resgeofed[0]["boundary"]
	self.bbox = resgeofed[0]["bbox"]
	self.bbox_xmax = resgeofed[0]["bbox_xmax"]
	self.bbox_ymax = resgeofed[0]["bbox_ymax"]
	self.bbox_xmin = resgeofed[0]["bbox_xmin"]
	self.bbox_ymin = resgeofed[0]["bbox_ymin"]
	self.x = resgeofed[0]["x"]
	self.y = resgeofed[0]["y"]
	# area
	resgeo = self.conn.query("SELECT pd.*, ST_AsKML(the_geom%(nowater)s) boundary, ST_AsKML(ST_Centroid(the_geom%(nowater)s)) point FROM pd308_a_%(ely)d pd WHERE pd.fed_num = '%(fednum)d' ORDER BY pd_num, emrp_name " % sql_args).dictresult()
	self.geokml = dict()
	for x in resgeo:
	    if 'emrp_name' in x:
		poll_num = str(x["emrp_name"])
	    else:
		poll_num = str(x["pd_num"])
	    if poll_num not in self.geokml:
		self.geokml[poll_num] = dict()
	    if "boundary" not in self.geokml[poll_num]:
		self.geokml[poll_num]["boundary"] = list()
	    self.geokml[poll_num]["boundary"].append(x["boundary"])
	    if "point" not in self.geokml[poll_num]:
		self.geokml[poll_num]["point"] = list()
	    self.geokml[poll_num]["point"].append(x["point"])
	    boundarydata = dict()
	    for a in ["gid","pd_id","pd_num","pd_nbr_sfx","pd_type","adv_poll","ed_id","fed_num","a_updt_dte","g_updt_dte","emrp_name","poll_name","pn_updt_dt","ad_updt_dt","urban_rura","shape_leng","shape_area"]:
		if a in x:
		    boundarydata[a] = x[a]
		else:
		    boundarydata[a] = None
	    if "boundarydata" not in self.geokml[poll_num]:
		self.geokml[poll_num]["boundarydata"] = list()
	    self.geokml[poll_num]["boundarydata"].append(boundarydata)
	# point
	resgeo = self.conn.query("SELECT *, ST_AsKML(the_geom) point FROM pd308_p_%(ely)d WHERE fed_num = %(fednum)d ORDER BY pd_num, emrp_name " % sql_args).dictresult()
	for x in resgeo:
	    if 'emrp_name' in x:
		poll_num = str(x["emrp_name"])
	    else:
		poll_num = str(x["pd_num"])
	    if poll_num not in self.geokml:
		self.geokml[poll_num] = dict()
	    if "point" not in self.geokml[poll_num]:
		self.geokml[poll_num]["point"] = list()
	    self.geokml[poll_num]["point"].append(x["point"])
	    pointdata = dict()
	    for a in ["gid","pd_id","pd_num","pd_nbr_sfx","pd_type","adv_poll","ed_id","fed_num","a_updt_dte","g_updt_dte","emrp_name","mobile_pol","sbpd_addre","address_id","st_adr_nbr","st_adr_n_1","street_id","st_nme","st_typ_cde","st_drctn_c","from_ste_n","to_ste_nbr","from_floor","to_floor","bldg_namee","bldg_namef","old_pd_id","poll_name","pn_updt_dt","ad_updt_dt","urban_rura"]:
		if a in x:
		    pointdata[a] = x[a]
		else:
		    pointdata[a] = None
	    if "pointdata" not in self.geokml[poll_num]:
		self.geokml[poll_num]["pointdata"] = list()
	    self.geokml[poll_num]["pointdata"].append(pointdata)
	    # results
	rescols = ["pd_num", "pd_name", "nb_votes", "nb_rejected", "nb_electors", "cand_firstname", "cand_middlename", "cand_lastname", "party_namee", "party_namef", "incumbent", "elected", "void", "nopoll", "mergedwith"]
	resres = self.conn.query("SELECT " + ", ".join(rescols) + " FROM fed_res_%(ely)d WHERE fed_num = %(fednum)d ORDER BY pd_num, nb_votes DESC" % sql_args).dictresult()
	self.res = dict()
	for x in resres:
	    if x["pd_num"] is not None:
    		pid = x["pd_num"]
	    else:
		pid = 0
	    if not re.match('S/R', x['pd_num']) and not re.match('Jan', x['pd_num']) and len(x['pd_num']) > 0:
		try:
		    #real_pid = re.match(r'(\d{1,3})-?(\d*)', x['pd_num']).group(1)
		    real_pid = re.match('\d{1,3}-?\d*', x['pd_num']).group(0)
		except:
		    real_pid = '0'
	    else:
		real_pid = '0'
	    # initialize result slot for this pd
	    if not real_pid in self.res:
		self.res[real_pid] = dict()
	    if not x['pd_num'] in self.res[real_pid]: # init for sub-pd
		self.res[real_pid][x['pd_num']] = list()
	    self.res[real_pid][x['pd_num']].append(x) # append for each candidate in the pd
	    '''
	    for a in res_cols:
		if a.startswith("nb_"):
		    self.nb[pid][a.replace("nb_", "")] = x[a]
		else:
		    self.res[pid][a] = x[a]
	    '''
    	self.combineRes()
	#for x in self.res:
	#    print x
	#    print self.res[x]

    def genGoogleChart1(self, id):
	res = self.rescombined[id]
	#nb = self.nb[id]
	inChart = 0
	qs = list()
	arr = dict()
	arr['cht'] = 'p'
	arr['chs'] = '500x150'
	arr['chp'] = str(math.radians(180))
	arr['chl'] = ''
	arr['chd'] = 't:'
	arr['chco'] = ''
	chl = list()
	chd = list()
	chco = list()
	for x in res:
	    if x["votes_nb"] > 0.01:
		inChart += 1
		chl.append(x["party_name_bi"])
		chd.append(str(int(round(x["votes_percent"]))))
		if kmlcedric.getHtmlHexFromGEHex(kmlcedric.partyColor(x["party_namee"]), False) == 'FFFFFF':
		    chco.append('CCCCCC')
		else:
		    chco.append(kmlcedric.getHtmlHexFromGEHex(kmlcedric.partyColor(x["party_namee"]), False))
	arr['chl'] += "|".join(chl)
	arr['chd'] += ",".join(chd)
	arr['chco'] += "|".join(chco)
	#for arrKeys in arr.keys():
	#    qs.append(arrKeys + '=' + arr[arrKeys])
	if inChart > 0:
	    return self.GCHARTURL + "?" + urllib.urlencode(arr)
	else:
	    return None

    def combineRes(self):
	self.rescombined = dict()
	for pd_num in self.res: # each poll in the riding
	    for key in self.res[pd_num]: # each sub-poll (A,B,C,etc.) in a polling div
		combined_res = dict()
		onesubpoll = self.res[pd_num][key]
		totalVotes = 0
		for x in onesubpoll:
		    thisParty = x['party_namee']
		    thisPartyInfo = fed.partyInfo(thisParty)
		    if thisParty == "No Affiliation" or thisParty == "Independent":
			thisParty += " | " + x["cand_lastname"]
		    if not thisParty in combined_res:
			combined_res[thisParty] = dict()
			combined_res[thisParty]['votes_nb'] = 0
			combined_res[thisParty]['electors_nb'] = 0
			combined_res[thisParty]['rejected_nb'] = 0
			combined_res[thisParty]['party_name'] = x['party_namee']
			combined_res[thisParty]['party_namee'] = x['party_namee']
			combined_res[thisParty]['party_namef'] = x['party_namef']
			combined_res[thisParty]['party_logo'] = thisPartyInfo['logo']
			combined_res[thisParty]['party_color'] = thisPartyInfo['color_hex']
			combined_res[thisParty]['party_name_bi'] = thisPartyInfo['name_bi']
			combined_res[thisParty]['candidate_firstname'] = x['cand_firstname']
			combined_res[thisParty]['candidate_middlename'] = x['cand_middlename']
			combined_res[thisParty]['candidate_lastname'] = x['cand_lastname']
			combined_res[thisParty]['mergedwith'] = x['mergedwith']
			if combined_res[thisParty]['candidate_middlename'] <> None:
			    combined_res[thisParty]['candidate_firstmiddlename'] = x['cand_firstname'] + ' ' + x['cand_middlename']
			else:
			    combined_res[thisParty]['candidate_firstmiddlename'] = x['cand_firstname']
			if len(combined_res[thisParty]['party_logo']) > 0:
			    combined_res[thisParty]['party_logo_html'] = '<img src="' + thisPartyInfo['logo'] + '" alt="' + thisParty + '" border="0"/>'
			else:
			    combined_res[thisParty]['party_logo_html'] = thisParty
		    combined_res[thisParty]['electors_nb'] += x['nb_electors']
		    combined_res[thisParty]['rejected_nb'] += x['nb_rejected']
		    combined_res[thisParty]['votes_nb'] += x['nb_votes']
		    totalVotes += x['nb_votes']
		for thisParty in combined_res:
		    if totalVotes <> 0:
			combined_res[thisParty]['votes_percent'] = combined_res[thisParty]['votes_nb'] * 100 / float(totalVotes)
			combined_res[thisParty]['votes_prop'] = combined_res[thisParty]['votes_nb'] / float(totalVotes)
		    else:
			combined_res[thisParty]['votes_percent'] = 0.0
			combined_res[thisParty]['votes_prop'] = 0.0
		#cmp = lambda x, y: cmp(y['votes_nb'], x['votes_nb'])
		combined_list = combined_res.values()
		combined_list.sort(key = lambda foo:(foo['votes_nb']), reverse = True)
		self.rescombined[str(pd_num)] = combined_list
	
    def genPollStyle(self, id, style_state):
	kmlid = "poll-" + str(id) 
	if style_state == kmldom.STYLESTATE_HIGHLIGHT:
	    kmlid += "-on"
	elif style_state == kmldom.STYLESTATE_NORMAL:
	    kmlid += "-off"
	style = kmlcedric.genBasicStyle(kmlid)
	if id not in self.rescombined:
	    return style
	res = self.rescombined[id]
	# Set styles
	iconStyle = style.get_iconstyle()
	labelStyle = style.get_labelstyle()
	lineStyle = style.get_linestyle()
	polyStyle = style.get_polystyle()
	balloonStyle = style.get_balloonstyle()
	listStyle = style.get_liststyle()
	res = self.rescombined[id]
	#nb = self.nb[id]
	allnone = True
	for x in res:
	    if x["votes_nb"] > 0:
		allnone = False
		break
	if allnone:
	    '''
    	    iconStyle.set_scale(0.5)
	    icon = self.factory.CreateIconStyleIcon()
	    icon_href = self.GCHARTURL + "?chst=d_map_pin_letter&chld=|CCCCCC|000000"
    	    icon.set_href(icon_href)
	    iconStyle.set_icon(icon)
	    labelStyle.set_scale(0.5)
	    if style_state == kmldom.STYLESTATE_HIGHLIGHT:
		labelStyle.set_scale(1)
		iconStyle.set_scale(1)
	    return style
	    '''
	#pos = sorted(res, key=lambda k: -k["votes_nb"])
	if allnone:
	    firstcolor = 0xffcccccc
	else:
	    firstcolor = kmlcedric.partyColor(res[0]["party_name"])
	    if res[0]["electors_nb"] > 0:
		margin = 1.0 * (res[0]["votes_nb"] - res[1]["votes_nb"]) / res[0]["electors_nb"]
		alpha = int(round(margin ** 0.25 * 256)) * 0x1000000
		firstcolor += alpha
	    else:
		margin = 0.0
		alpha = 1
	if "boundary" in self.geokml[id]:
	    if style_state == kmldom.STYLESTATE_HIGHLIGHT:
		lineStyle.set_width(2)
		polyStyle.set_color(kmlbase.Color32(0x00000000))
		labelStyle.set_scale(1.5)
		iconStyle.set_scale(0)
		icon = self.factory.CreateIconStyleIcon()
		icon.set_href(self.BLANK16)
		iconStyle.set_icon(icon)
	    elif style_state == kmldom.STYLESTATE_NORMAL:
		try:
		    polyStyle.set_color(kmlbase.Color32(firstcolor))
		except NotImplementedError:
		    polyStyle.set_color(kmlbase.Color32(0xffffffff))
		polyStyle.set_colormode(kmldom.COLORMODE_NORMAL)
		labelStyle.set_scale(0.5)
		icon_color = kmlcedric.getHtmlHexFromGEHex(firstcolor, False)
		iconStyle.set_scale(0)
		icon = self.factory.CreateIconStyleIcon()
		icon.set_href(self.BLANK16)
		iconStyle.set_icon(icon)
	else:# type(self.geokml[x]["point"]) is types.ListType: # Point polls
    	    iconStyle.set_scale(0.5)
	    icon_color = kmlcedric.getHtmlHexFromGEHex(firstcolor, False)
	    icon = self.factory.CreateIconStyleIcon()
	    icon_href = self.GCHARTURL + "?chst=d_map_pin_letter&chld=|" + icon_color + "|000000"
    	    icon.set_href(icon_href)
	    iconStyle.set_icon(icon)
	    labelStyle.set_scale(0.5)
	    if style_state == kmldom.STYLESTATE_HIGHLIGHT:
		labelStyle.set_scale(1)
		iconStyle.set_scale(1)
	return style

    def genInfoWindowHTML(self, id):
	if id not in self.rescombined:
	    return "<em>Results unavailable for this polling division / Résultats non disponibles pour ce bureau de scrutin</em>"
	res = self.rescombined[id]
	'''
	if nb["valid"] is None:
	    return "<div>" + str(nb["electors"]) + " registered voters</div><div>This poll was merged with another one.</div>"
	turnout_txt = "Turnout: " + str(round((nb["valid"] + nb["rejected"]) * 1.0 / nb["electors"] * 100,2)) + " % "
	if nb["rejected"] > 0:
	    turnout_txt += " = (" + str(nb["valid"]) + " votes + " + str(nb["rejected"]) + " rejected) / " + str(nb["electors"]) + " registered voters "
	else:
	    turnout_txt += " = " + str(nb["valid"]) + " votes / " + str(nb["electors"]) + " registered voters "
	'''
	desc = '<table border="1" width="500">'
	desc += '<tr><th>candidate / candidat</th><th>party / parti</th><th>votes</th></tr>'
	votesTotal = 0
	for x in res:
	    votesTotal += x["votes_nb"] 
	    desc += '<tr><td>%(candidate_lastname)s, %(candidate_firstmiddlename)s</td><td>%(party_logo_html)s</td><td>%(votes_nb)s (%(votes_percent).2f%%)</td></tr>' % x
	    #desc += '<tr><td>%(party)s</td><td>%(votes)d</td><td>%(percent).2f%%</td></tr>' % { "party": x.upper(), "votes": res[x], "percent": 100 * float(res[x]) / nb["valid"] }
	desc += '</table>'
	rejected_nb = res[0]["rejected_nb"]
    	electors_nb = res[0]["electors_nb"]
	if votesTotal + rejected_nb == 0 or electors_nb == 0:
	    turnout_txt = "No votes compiled / Pas de votes calculés "
	else:
	    turnout_txt = "Turnout / participation: (%(votestotal)d votes + %(rejected)d rej.) / %(electors)d elect. = %(percent)s%%" % {"votestotal": votesTotal, "rejected": rejected_nb, "electors": electors_nb, "percent": str(round((votesTotal + rejected_nb) * 1.0 / electors_nb * 100,2)) }
	desc = '<div>' + turnout_txt + '</div>' + desc
	if "mergedwith" in res[0] and res[0]["mergedwith"] is not None:
	    merged = res[0]["mergedwith"]
	    try:
		merged_txt = re.match('\d{1,3}-?\d*', merged).group(0)
	    except:
		merged_txt = res[0]["mergedwith"]
    	    desc = '<a href="#pd-%(merged)s;balloon">Merged with poll <strong>%(merged_txt)s</strong> / Fusionné avec le bureau de scrutin <strong>%(merged)s</strong></a>' % { "merged_txt": merged_txt, "merged": merged }
	# Google Chart
	googleChart = self.genGoogleChart1(id)
	if googleChart is not None:
	    desc += '<div><img src="' + googleChart + '" alt="chart"/></div>'
	return desc

    def genKml(self):
	docu = self.factory.CreateDocument()
	docu.set_name(str(self.fednum) + " " + self.ed_name)
	#kml = factory.CreateKml()
	self.kml = self.factory.CreateElementById(kmldom.Type_kml)
	kmlfile = kmlengine.KmlFile.CreateFromImport(self.kml)
	self.kml = kmldom.AsKml(kmlfile.get_root())
	self.kml.set_feature(docu)
	geokmlkeys = self.geokml.keys()
	geokmlkeys.sort()
	for x in geokmlkeys:
	    pl = self.factory.CreatePlacemark()
	    pl.set_name(x)
	    pl.set_id("pd-"+x)
	    point_kml = self.geokml[x]["point"]
	    point_text = ''
	    if type(point_kml) is types.ListType:
		try:
		    point_kml = "".join(point_kml)
		except TypeError:
		    point_kml = ""
	    if "boundary" in self.geokml[x]:
		bounds_kml = self.geokml[x]["boundary"]
		if type(bounds_kml) is types.ListType:
		    try:
			bounds_kml = "".join(bounds_kml)
		    except:
			continue
			'''
			bounds_to_use = list()
			for b in bounds_kml:
			    if b <> None:
				bounds_to_use.append(b)
			bounds_kml = ""
			'''
		if bounds_kml.startswith('<Polygon>'):
		    bounds_kml = '<MultiGeometry>' + bounds_kml + '</MultiGeometry>'
		try:
		    bounds_kml = bounds_kml.replace("</MultiGeometry><MultiGeometry>", "")
		    bounds_points_kml = bounds_kml.replace("<MultiGeometry>", "<MultiGeometry>" + point_kml)
		    kmlfile,errors = kmlengine.KmlFile.CreateFromParse(bounds_points_kml)
		except:
		    bounds_kml = self.geokml[x]["boundary"][0]
		    bounds_points_kml = bounds_kml.replace("<MultiGeometry>", "<MultiGeometry>" + point_kml)
		    kmlfile,errors = kmlengine.KmlFile.CreateFromParse(bounds_points_kml)
		if "boundarydata" in self.geokml[x]:
		    for boundarydata in self.geokml[x]['boundarydata']:
			if 'poll_name' in boundarydata and boundarydata["poll_name"] is not None:
			    point_text += "<strong>%s</strong><br/>" % boundarydata["poll_name"]
			    break
		mg = kmldom.AsMultiGeometry(kmlfile.get_root())
	    #if point_kml <> None and point_kml.startswith('<Point>'):
	    else:
		kmlfile,errors = kmlengine.KmlFile.CreateFromParse("<MultiGeometry>"+point_kml+"</MultiGeometry>")
		mg = kmldom.AsMultiGeometry(kmlfile.get_root())
		if "pointdata" in self.geokml[x]:
		    for pointdata in self.geokml[x]['pointdata']:
			this_point_kml = ""
			if 'emrp_name' in pointdata:
			    if feduid >= 24000 and feduid < 25000:
				this_point_text = pointdata['bldg_namef'] # au Quebec, c'est en francais
			    else:
				this_point_text = pointdata['bldg_namee']
			    if this_point_text == None or len(this_point_text) <= 0:
				this_point_text = ''
				if pointdata['st_adr_nbr'] <> None and len(pointdata['st_adr_nbr']) > 0:
				    this_point_text += pointdata['st_adr_nbr']
				if pointdata['st_nme'] <> None and len(pointdata['st_nme']) > 0:
				    if len(this_point_text) > 0:
					this_point_text += ' '
				    this_point_text += pointdata['st_nme']
				if pointdata['st_drctn_c'] <> None and len(pointdata['st_drctn_c']) > 0:
				    if len(this_point_text) > 0:
					this_point_text += ' '
				    this_point_text += pointdata['st_drctn_c']
			    point_text += "<strong>%s</strong><br/>" % this_point_text
	    pl.set_geometry(mg)
	    pl.set_styleurl('#poll-' + str(x))
	    docu.add_feature(pl)
	    #snippet = self.factory.CreateSnippet()
	    #snippet.set_text(point_text)
	    #pl.set_snippet(snippet)
	    pl.set_description(point_text + self.genInfoWindowHTML(x))
	    # Styles
	    style_map = self.factory.CreateStyleMap()
	    style_map.set_id('poll-' + str(x))
	    style_on = self.genPollStyle(x, kmldom.STYLESTATE_HIGHLIGHT)
	    style_off = self.genPollStyle(x, kmldom.STYLESTATE_NORMAL)
	    pair_on = self.factory.CreatePair()
	    pair_on.set_key(kmldom.STYLESTATE_HIGHLIGHT)
	    pair_on.set_styleselector(style_on)
	    pair_off = self.factory.CreatePair()
	    pair_off.set_key(kmldom.STYLESTATE_NORMAL)
	    pair_off.set_styleselector(style_off)
	    style_map.add_pair(pair_on)
	    style_map.add_pair(pair_off)
	    docu.add_styleselector(style_map)
	# Riding
	'''
	pl = factory.CreatePlacemark()
	pl.set_name(self.riding_geom['edabbr'] + ' ' + self.riding_geom['edname'])
	kmlfile,errors = kmlengine.KmlFile.CreateFromParse(self.riding_geom['boundary'])
	mg = kmldom.AsMultiGeometry(kmlfile.get_root())
	pl.set_geometry(mg)
	pl.set_styleurl('#riding-' + self.edabbr.lower())
	docu.add_feature(pl)
	ridingStyle = kmlcedric.genBasicStyle('riding-' + self.edabbr.lower(), None, None)
	ls = ridingStyle.get_linestyle()
	'''
	#ls.set_color(kmlbase.Color32(partyColor(global_res['party_name']) + 0x7f000000))
	#ls.set_color(kmlbase.Color32(0xff00ffff))
	#docu.add_styleselector(ridingStyle)
	lookat = self.factory.CreateLookAt()
	lookat.set_longitude(self.x)
	lookat.set_latitude(self.y)
	lookat.set_tilt(15)
	lookat.set_altitudemode(kmldom.ALTITUDEMODE_ABSOLUTE)
	if (self.fednum >= 24000 and self.fednum < 25000) or (self.fednum >= 35000 and self.fednum < 36000):
	    lookat.set_heading(-30)
	bbox_x_km = (self.bbox_xmax - self.bbox_xmin) * 80.0
	bbox_y_km = (self.bbox_ymax - self.bbox_ymin) * 111.0
	if bbox_y_km > bbox_x_km:
	    max_side_km = bbox_y_km
	else:
	    max_side_km = bbox_x_km
	lookat.set_altitude(0)
	lookat.set_range(max_side_km)
	lookat.set_range(max_side_km*1000*1.4)
	docu.set_abstractview(lookat)

    def printKml(self):
	print kmldom.SerializePretty(self.kml)
	
if __name__ == '__main__':
    water = False
    year = 2011
    feduid = sys.argv[1]
    try:
	feduid = int(feduid)
    except:
	print "Invalid feduid %s " % feduid
	sys.exit()
    for i in range(2,len(sys.argv)):
	if sys.argv[i] == "-ww":
	    water = True
	if sys.argv[i] == "-el":
	    year = int(sys.argv[i+1])
    if water:    
	can = fedpolls(year, feduid, nowater=False)
    else:
	can = fedpolls(year, feduid)
    can.DB()
    can.genKml()
    #sys.exit()
    can.printKml()
