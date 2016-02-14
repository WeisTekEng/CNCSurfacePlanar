#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  Updated 13.02.2016 20:58:24
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

x = []
y = []
z = []
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

REV = "CNC Surface Planer V0.1"
RET = '\r'
NEWL = '\n'

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

def makeNcFile(sfile, yEnd):
	print "Multiplier : " + str(Multiplier)
	print "Start and End x Cords : " + str(xCordStart) + " | " + str(xCordEnd)
	print "Start and End y Cords : " + str(yCordStart) + " | " + str(yCordEnd)
	commands.append("(Planar code begin.)")
	counter = 0
	yCounter = 0
	while counter <= yEnd:
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
	#home.
	commands.append("(Home the device we are done.)")
	commands.append('$H') 
	#set feed rates back to normal.
	commands.append("(Set x axis feed rates back to normal)")
	commands.append('$110='+str(DEFAULT))
	for index in commands:
		sfile.write(index+RET)
	return

print REV

print "Follow the directions."+NEWL

print "Set your z axis next to your starting point, .1mm below the working surface we will"+NEWL
print "take care of the rest."+NEWL

response = raw_input("What is your default x axis feed rate? $110 setting : ")
DEFAULT = int(response)

response = raw_input("What is your starting x cordinate? : ")
xCordStart = int(response)

response = raw_input("What is your ending x cordinate? : ")
xCordEnd = int(response)

response = raw_input("What is your starting Y cordinate? : ")
yCordStart = int(response)

response = raw_input("What is your ending Y cordinate? : ")
yCordEnd = int(response)

materialSelect()
finishQuality()

print "Creating NC file now."
sfile = open("BedPlanar.nc","w")
sfile.write("("+REV+")"+NEWL)
sfile.write("(Script last updated 13.02.2016 21:26:36)"+NEWL)
sfile.write("(Created with CNC Surface Planar scipt: WeisTekEng)"+NEWL)
sfile.write("(www.weistekengineering.com | Jeremy.goss@weistekengineering.com)"+NEWL)
makeNcFile(sfile,yCordEnd)





