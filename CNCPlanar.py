#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  Updated 14.02.2016 10:54:36
#
#  CNCPlanar.py
#  
#  Copyright 2016 ocybr <Jeremy.Goss@weistekengineering.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
import sys, os, math

#used to store user set cord limits via settings.dat.
settings = []

#User enttered cords system.
xCordEnd = 0
xCordStart = 0
yCordEnd = 0
yCordStart = 0
zCordStart = 0
zCordEnd = 0
commands = []
Multiplier = 0

#Gcodes
MOVE = 'G0' #Linear Motion

#Mcodes
Stop = 'M30'
pause = 'M2'

#Material Definitions
DEFAULT = 0
AcrylicSlow = '$110=250'
AcrylicFast = '$110=1200'
Wood_Soft = '$110=800'
Wood_Hard = '$110=450'

#type of finish
ROUGH = 3
MEDIUM = 2
FINE = 1

REV = "CNC Surface Planer VA.2"
RET = '\r'
NEWL = '\n'

#This function checks if a default settings.dat file is found
#use this file to set your min max axis limits.
def openDefaultSettings():
	temp = ""
	global settings
	if os.path.isfile("settings.dat"):
		print "file exists"
		dfile = open("settings.dat","r")
		for index in dfile:
			temp = temp + str(index)
		settings = temp.split(RET)
		#for index in settings:
		#	print str(index)
		dfile.close()
	else:
		print "Creating settings.dat file, use this file to define min max cord settings."+NEWL
		dfile = open("settings.dat","w")
		dfile.write("each setting is on a new line, integers only. delete this line!"+RET)
		dfile.write("xmin"+RET)
		dfile.write("xmax"+RET)
		dfile.write("ymin"+RET)
		dfile.write("ymax"+RET)
		dfile.write("zmin"+RET)
		dfile.write("zmax")
		dfile.close()

#This function checks your inputs agaisnt your predefined limits
#in settings.dat, if settings.dat is missing or incorrect this will not work
def checkLimits(usr,pos):
	global goodSetting
	sCords = ""
	
	if pos == 0:
		sCords = "X"
		limit = str(settings[0])
		Min = limit[0]
		Max = limit[2:5]
	elif pos == 1:
		Min = str(settings[1])
		Max = str(settings[2])
	elif pos == 2:
		Min = str(settings[3])
		Max = str(settings[4])
		#print "pos 2"
		#print "Min : " + str(Min)
		#print "Max : " + str(Max)
	
	if not int(usr) >= int(Min):
		print "Min Max cord settings enabled, your entered value is below your Min "+sCords+" Axis settings."+RET
	elif int(usr) > int(Max):
		print "Min Max cord settings enabled, your entered value is above your Max "+sCords+"X Axis settings."+RET
	else:
		goodSetting = 1
		return usr

#This function sets the x axis feed rate based on my experiances with these materials
def materialSelect():
	commands.append("(Set the feed rate based on material.)")
	#Set feed rate of the x axis to something slower.
	response = raw_input("Please select your current working material, (1)AcrylicSlow,(2)AcrylicFast,(3)Soft Wood,(4)Hard Wood. : ")
	if response == "1":
		commands.append("(Material selected : Acrylic Slow)")
		commands.append(AcrylicSlow)
		print "Material set to : Acrylic Slow"
	elif response == "2":
		commands.append("(Material selected : Acrylic Fast)")
		commands.append(AcrylicFast)
		print "Material set to : Acrylic Fast"
	elif response == "3":
		commands.append("(Material selected : Soft Wood)")
		commands.append(Wood_Soft)
		print "Material set to : Soft Wood"
	elif response == "4":
		commands.append("(Material selected : Hard Wood)")
		commands.append(Wood_Hard)
		print "Material set to : Hard Wood"
	
#This function sets the quality of the planar, rough is 3mm wide passes
#Medium is 2mm passes and fine is 1mm passes.
def finishQuality():
	#set the finish quality
	global Multiplier
	response = raw_input("Please select the desired finish quality. (1)Rough, (2)Medium, (3)Fine. : ")
	if response == "3":
		commands.append("(Finish quality selected : Fine)")
		Multiplier = FINE
	elif response == "2":
		commands.append("(Finish quality selected : Medium)")
		Multiplier = MEDIUM
	elif response == "1":
		commands.append("(Finish quality selected : Rough)")
		Multiplier = ROUGH

#This function puts everything together and creates your Material Planar NC file
#use this file to load into your fav program and away you go.
def makeNcFile(sfile, yEnd):
	print "Multiplier : " + str(Multiplier)
	print "Start and End x Cords : " + str(xCordStart) + " | " + str(xCordEnd)
	print "Start and End y Cords : " + str(yCordStart) + " | " + str(yCordEnd)
	commands.append("(Planar code begin.)")
	counter = 0
	yCounter = 0
	while counter <= yEnd:
		print "in the loop" + str(counter)
		#z will be setup later for multipule passes
		#y
		commands.append(MOVE+'Y'+str(yCounter))
		yCounter = yCounter + int(Multiplier)
		#x
		commands.append(MOVE+'X'+str(xCordEnd))
		#y
		commands.append(MOVE+'Y'+str(yCounter))
		yCounter = yCounter + int(Multiplier)
		#x
		commands.append(MOVE+'X'+str(xCordStart))
		#print str(yCounter)
		counter = counter + int(Multiplier)*2
	
	commands.append("(Planar code end.)")
	#Tell the machine to stop the cycle.
	commands.append("(Stop the machine)")
	commands.append(Stop)
	#lift the z axis a bit.
	commands.append("(lift the z axis out of the way)")
	commands.append('G0Z10')
	#home. GRBL wont home after M30 system not IDLE
	#commands.append("(Home the device we are done.)")
	#commands.append('$H') 
	#set feed rates back to normal.
	commands.append("(Set x axis feed rates back to normal)")
	commands.append('$110='+str(DEFAULT))
	for index in commands:
		sfile.write(index+NEWL)
	sfile.close()
	return

print REV

print "Follow the directions."+NEWL

print "We are assuming that you have already homed or set new zero cords."+NEWL
print "!!!!!READ THIS!!!!!"+RET
print "We are assuming that your Y axis will be the orientation by whitch we planar the surface."+RET
print "Example, your x axis is Static meaning it only moves from xStart to Xend it does not stop it does not change."+RET
print "Your Y axis on the other hand is what changes by 1,2,or 3mm."
print "If this is confusing generate a small Surface planar code set eg xS=0,xE=20,yS=0,yE=20 Quality fine, Material any."+RET
print "move your axis to a location they will not interfere with anything. Raise your Z axis enough that it wont "+RET
print "hit anything either. This will be a test so you can see how this script works with your machine."+RET
print "Load the file generated and hit print."+NEWL

print "Set your z axis next to your starting point, .1mm below the working surface we will"+RET
print "take care of the rest."+NEWL

print "Attemping to open settings.dat for cords min and max settings."+RET

openDefaultSettings()

response = raw_input("What is your default x axis feed rate? $110 setting : ")
DEFAULT = int(response)

goodSetting = 0
while goodSetting == 0:
	response = raw_input("What is your starting x cordinate? : ")
	xCordStart = checkLimits(response,0)

goodSetting = 0
#lists are still funny to me..
while goodSetting == 0:
	response = raw_input("What is your ending x cordinate? : ")
	xCordEnd = checkLimits(response,0)
		
goodSetting = 0
while goodSetting == 0:
	response = raw_input("What is your starting Y cordinate? : ")
	yCordStart = checkLimits(response,1)

goodSetting = 0
while goodSetting == 0:
	response = raw_input("What is your ending Y cordinate? : ")
	yCordEnd = checkLimits(response,1)
	
materialSelect()
finishQuality()

print "Creating NC file now."
sfile = open("BedPlanar.nc","w")
sfile.write("("+REV+")"+NEWL)
sfile.write("(Script last updated 13.02.2016 21:26:36)"+NEWL)
sfile.write("(Created with CNC Surface Planar scipt: WeisTekEng)"+NEWL)
sfile.write("(www.weistekengineering.com | Jeremy.goss@weistekengineering.com)"+NEWL)
makeNcFile(sfile,int(yCordEnd))





