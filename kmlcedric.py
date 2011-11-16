#-*- coding: utf-8
import kmlbase
import kmldom
import kmlengine

"""
@factory - libkml factory
@id - id of style to use
"""
def genBasicStyle(id):
    factory = kmldom.KmlFactory_GetFactory()
    style = factory.CreateStyle()
    style.set_id(id)
    # Create style objects
    iconStyle = factory.CreateIconStyle()
    labelStyle = factory.CreateLabelStyle()
    lineStyle = factory.CreateLineStyle()
    polyStyle = factory.CreatePolyStyle()
    balloonStyle = factory.CreateBalloonStyle()
    listStyle = factory.CreateListStyle()
    # Set styles
    style.set_iconstyle(iconStyle)
    style.set_labelstyle(labelStyle)
    style.set_linestyle(lineStyle)
    style.set_polystyle(polyStyle)
    style.set_balloonstyle(balloonStyle)
    style.set_liststyle(listStyle)
    return style

def customPolyStyle(polyStyle, color):
    polyStyle.set_color(kmlbase.Color32(color))
    polyStyle.set_colormode(kmldom.COLORMODE_NORMAL)
    return polyStyle

def standardBalloonStyle(balloonStyle):
    balloonStyleText = '<h1>$[name]</h1><h2>$[Snippet]</h2>$[description]'
    balloonStyle.set_text(balloonStyleText)
    return balloonStyle

def noTitleBalloonStyle(balloonStyle):
    balloonStyleText = '$[description]'
    balloonStyle.set_text(balloonStyleText)
    return balloonStyle

def get_gradient_color(colorA, colorB, val):
    # 'val' must be between 0 and 1
    color = [0, 0, 0]
    for i in range(len(color)):
	color[i] = colorA[i] + val * (colorB[i] - colorA[i])
    return color

def partyColor(partyName):
    if partyName == 'Liberal' or partyName.startswith("liberal"):
	color = 0x0000ff
    elif partyName == 'Conservative' or partyName.startswith("conservative"):
	color = 0xff0000
    elif partyName == 'NDP-New Democratic Party' or partyName == 'N.D.P.' or partyName.startswith("ndp"):
	color = 0x008cff
    elif partyName == 'Bloc Québécois' or partyName.startswith("bloc"):
	color = 0x808000
    elif partyName == 'Green Party' or partyName.startswith("green"):
	color = 0x006400
    else:
	color = 0xffffff
    return color

def getPartyIdByName(partyName):
    if partyName == 'Liberal':
	partyId = 2
    elif partyName == 'Conservative':
	partyId = 3
    elif partyName == 'NDP-New Democratic Party' or partyName == 'N.D.P.':
	partyId = 4
    elif partyName == 'Bloc Québécois':
	partyId = 5
    elif partyName == 'Green Party':
	partyId = 6
    else:
	partyId = 0
    return partyId

def getPartyNameById(partyId):
    if partyId == 2:
	partyName = 'Liberal'
    elif partyId == 3:
       	partyName = 'Conservative'
    elif partyId == 4:
   	partyName = 'NDP-New Democratic Party'
    elif partyId == 5:
  	partyName = 'Bloc Québécois'
    elif partyId == 6:
 	partyName = 'Green Party'
    else:
	partyName = None
    return partyName

def getPartyNameByCommonPartyName(commonPartyName, year=None, lang="en"):
    commonPartyName = commonPartyName.lower()
    if commonPartyName == 'liberal':
	partyName = 'Liberal'
    elif commonPartyName == 'conservative':
	partyName = 'Conservative'
    elif commonPartyName == 'ndp':
	partyName = 'NDP-New Democratic Party'
	if year is not None and year == 2006:
	    partyName = 'N.D.P.'
    elif commonPartyName == 'bloc':
	partyName = 'Bloc Québécois'
    elif commonPartyName == 'green':
	partyName = 'Green Party'
    else:
	partyName = None
    return partyName

def getPartyIdByName(partyName):
    if partyName == 'Liberal':
	partyId = 2
    elif partyName == 'Conservative':
	partyId = 3
    elif partyName == 'NDP-New Democratic Party' or partyName == 'N.D.P.':
	partyId = 4
    elif partyName == 'Bloc Québécois':
	partyId = 5
    elif partyName == 'Green Party':
	partyId = 6
    else:
	partyId = 0
    return partyId

def getHtmlHexFromGEHex(GEHex, hashmark=True):
    if GEHex > 0x1000000:
	i = 2
    else:
	i = 0
    B = hex(GEHex)[2+i:4+i]
    G = hex(GEHex)[4+i:6+i]
    R = hex(GEHex)[6+i:8+i]
    if not len(B):
	R = "00"
	G = "00"
	B = "00"
    elif not len(G):
	R = B
	G = "00"
	B = "00"
    elif not len(R):
	R = G
	G = B
	B = "00"
    if hashmark:
	return "#" + R + G + B
    else:
	return R + G + B

def getHtmlHexFromGEHex(GEHex, hashmark=True):
    if GEHex > 0x1000000:
	i = 2
    else:
	i = 0
    B = hex(GEHex)[2+i:4+i]
    G = hex(GEHex)[4+i:6+i]
    R = hex(GEHex)[6+i:8+i]
    if not len(B):
	R = "00"
	G = "00"
	B = "00"
    elif not len(G):
	R = B
	G = "00"
	B = "00"
    elif not len(R):
	R = G
	G = B
	B = "00"
    if hashmark:
	return "#" + R + G + B
    else:
	return R + G + B

