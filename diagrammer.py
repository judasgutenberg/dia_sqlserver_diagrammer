import subprocess	   
import os
import pyodbc
import json
import sys
import requests
import math
import re
from past.builtins import execfile




def newColumn(name, type, size, isPrimary, isNullable, isUnique, comment):
	#print(name, isNullable)
	nameToUse = name
	typeToUse = type
	takesLength = ['varchar', 'nvarchar']
	if isPrimary:
		nameToUse = "#" + nameToUse + "#"
	if type in takesLength:
		typeToUse = type + '(' + str(size) + ')'
	elif type== "decimal":
		typeToUse = type + '(19,2)'
	elif type== "float":
		typeToUse = type + '(53)'
	out = """
	<dia:composite type="table_attribute">
		<dia:attribute name="name">
		<dia:string>#""" + nameToUse + """#</dia:string>
		</dia:attribute>
		<dia:attribute name="type">
		<dia:string>#""" + typeToUse + """#</dia:string>
		</dia:attribute>
		<dia:attribute name="comment">
		<dia:string>##</dia:string>
		</dia:attribute>
		<dia:attribute name="primary_key">
		<dia:boolean val=""" + '"' + str(isPrimary).lower() + '"' +  """/>
		</dia:attribute>
		<dia:attribute name="nullable">
		<dia:boolean val=""" + '"' +str(isNullable).lower() + '"' + """/>
		</dia:attribute>
		<dia:attribute name="unique">
		<dia:boolean val=""" + '"' + str(isUnique).lower() + '"' + """/>
		</dia:attribute>
	</dia:composite>
	"""
	return out
	
def newTable(name, columns, northwestCorner, id):
	out = """
		<dia:object type="Database - Table" version="0" id=""" + '"' + str(id) + '"' + """>
		  <dia:attribute name="obj_pos">
			<dia:point val=""" + '"' + str(northwestCorner.lon) + """,""" + str(northwestCorner.lat) + '"' +  """/>
		  </dia:attribute>
		  <dia:attribute name="obj_bb">
			<dia:rectangle val=""" + '"' +  str(northwestCorner.lon) + """,""" + str(northwestCorner.lat) + """;44.675,30.44"/>
		  </dia:attribute>
		  <dia:attribute name="meta">
			<dia:composite type="dict"/>
		  </dia:attribute>
		  <dia:attribute name="elem_corner">
			<dia:point val=""" + '"' +  str(northwestCorner.lon) + """,""" + str(northwestCorner.lat) + '"' +  """/>
		  </dia:attribute>
		  <dia:attribute name="elem_width">
			<dia:real val="14.004999999999999"/>
		  </dia:attribute>
		  <dia:attribute name="elem_height">
			<dia:real val="11.500000000000002"/>
		  </dia:attribute>
		  <dia:attribute name="text_colour">
			<dia:color val="#000000"/>
		  </dia:attribute>
		  <dia:attribute name="line_colour">
			<dia:color val="#000000"/>
		  </dia:attribute>
		  <dia:attribute name="fill_colour">
			<dia:color val="#ffffff"/>
		  </dia:attribute>
		  <dia:attribute name="line_width">
			<dia:real val="0.10000000000000001"/>
		  </dia:attribute>
		  <dia:attribute name="name">
			<dia:string>#""" + name + """#</dia:string>
		  </dia:attribute>
		  <dia:attribute name="comment">
			<dia:string>##</dia:string>
		  </dia:attribute>
		  <dia:attribute name="visible_comment">
			<dia:boolean val="false"/>
		  </dia:attribute>
		  <dia:attribute name="tagging_comment">
			<dia:boolean val="false"/>
		  </dia:attribute>
		  <dia:attribute name="underline_primary_key">
			<dia:boolean val="false"/>
		  </dia:attribute>
		  <dia:attribute name="bold_primary_keys">
			<dia:boolean val="true"/>
		  </dia:attribute>
		  <dia:attribute name="normal_font">
			<dia:font family="monospace" style="0" name="Courier"/>
		  </dia:attribute>
		  <dia:attribute name="name_font">
			<dia:font family="sans" style="80" name="Helvetica-Bold"/>
		  </dia:attribute>
		  <dia:attribute name="comment_font">
			<dia:font family="sans" style="0" name="Helvetica"/>
		  </dia:attribute>
		  <dia:attribute name="normal_font_height">
			<dia:real val="0.80000000000000004"/>
		  </dia:attribute>
		  <dia:attribute name="name_font_height">
			<dia:real val="0.69999999999999996"/>
		  </dia:attribute>
		  <dia:attribute name="comment_font_height">
			<dia:real val="0.69999999999999996"/>
		  </dia:attribute>
		  <dia:attribute name="attributes">"""

	for column in columns:
		#print(column.name, column.isNullable)

		out = out + newColumn(column.name, column.type, column.size, column.isPrimary, column.isNullable, column.isUnique, "")
	out = out + """
		

	</dia:attribute>
		"""
	out = out + "</dia:object>"

	return out
	
def diaHeader():
	out = """<?xml version="1.0" encoding="UTF-8"?>
	<dia:diagram xmlns:dia="http://www.lysator.liu.se/~alla/dia/">
	"""
	return out
def diaFooter():
	out = """
	</dia:diagram>
	
	"""
	return out


def xxdiaLine(beginLat, beginLon, endLat, endLon):
	out="""
		<dia:object type="Database - Reference" version="0" id="O0">
			<dia:attribute name="obj_pos">
			<dia:point val="""  + '"' + str(beginLat)+ ',' + str(beginLon) + '"' + """/>
			</dia:attribute> 
	
			<dia:attribute name="meta">
			<dia:composite type="dict"/>
			</dia:attribute>
			<dia:attribute name="orth_points">
			<dia:point val=""" + '"' + str(beginLat) + "," +  str(beginLon) + '"' + """/>
			<dia:point val=""" + '"' + str(endLat) + "," +  str(endLon )+ '"' + """/>
			</dia:attribute>
			<dia:attribute name="orth_orient">
			<dia:enum val="0"/>
			<dia:enum val="1"/>
			<dia:enum val="0"/>
			</dia:attribute>
			<dia:attribute name="orth_autoroute">
			<dia:boolean val="false"/>
			</dia:attribute>
			<dia:attribute name="text_colour">
			<dia:color val="#000000"/>
			</dia:attribute>
			<dia:attribute name="line_colour">
			<dia:color val="#ff0000"/>
			</dia:attribute>
			<dia:attribute name="line_width">
			<dia:real val="0.10000000000000001"/>
			</dia:attribute>
			<dia:attribute name="line_style">
			<dia:enum val="0"/>
			<dia:real val="1"/>
			</dia:attribute>
			<dia:attribute name="corner_radius">
			<dia:real val="0"/>
			</dia:attribute>
			<dia:attribute name="end_arrow">
			<dia:enum val="0"/>
			</dia:attribute>
			<dia:attribute name="start_point_desc">
			<dia:string>#1#</dia:string>
			</dia:attribute>
			<dia:attribute name="end_point_desc">
			<dia:string>#n#</dia:string>
			</dia:attribute>
			<dia:attribute name="normal_font">
			<dia:font family="monospace" style="0" name="Courier"/>
			</dia:attribute>
			<dia:attribute name="normal_font_height">
			<dia:real val="0.59999999999999998"/>
			</dia:attribute>
		    <dia:connections>
				<dia:connection handle="0" to="O2" connection="13"/>
			  </dia:connections>
		</dia:object>
	"""
	return out
 

def diaLine(beginLat, beginLon, endLat, endLon):
	out="""
		<dia:object type="Database - Reference" version="0" id="O0">
		 	<dia:attribute name="obj_pos">
			<dia:point val="""  + '"' + str(beginLat)+ ',' + str(beginLon) + '"' + """/>
			</dia:attribute> 
	
			<dia:attribute name="meta">
			<dia:composite type="dict"/>
			</dia:attribute>
 
			<dia:attribute name="orth_orient">
			<dia:enum val="0"/>
			<dia:enum val="1"/>
			<dia:enum val="0"/>
			</dia:attribute>
			<dia:attribute name="orth_autoroute">
			<dia:boolean val="false"/>
			</dia:attribute>
			<dia:attribute name="text_colour">
			<dia:color val="#000000"/>
			</dia:attribute>
			<dia:attribute name="line_colour">
			<dia:color val="#009900"/>
			</dia:attribute>
			<dia:attribute name="line_width">
			<dia:real val="0.10000000000000001"/>
			</dia:attribute>
			<dia:attribute name="line_style">
			<dia:enum val="0"/>
			<dia:real val="1"/>
			</dia:attribute>
			<dia:attribute name="corner_radius">
			<dia:real val="0"/>
			</dia:attribute>
			<dia:attribute name="end_arrow">
			<dia:enum val="0"/>
			</dia:attribute>
			<dia:attribute name="start_point_desc">
			<dia:string>#1#</dia:string>
			</dia:attribute>
			<dia:attribute name="end_point_desc">
			<dia:string>#n#</dia:string>
			</dia:attribute>
			<dia:attribute name="normal_font">
			<dia:font family="monospace" style="0" name="Courier"/>
			</dia:attribute>
			<dia:attribute name="normal_font_height">
			<dia:real val="0.59999999999999998"/>
			</dia:attribute>
		    <dia:connections>
				<dia:connection handle="0" to="O2" connection="13"/>
				<dia:connection handle="0" to="O4" connection="14"/>
			  </dia:connections>
		</dia:object>
	"""
	return out

def getTablesFromSqlCreate(path):
	sqlFile = open(path)
	sql = sqlFile.read()
	sqlFile.close()
	lines = sql.split("\n")
	tables = []
	for line in lines:
		#print(line)
		table = find_between(line, "[dbo].[", "]")
		
		#print(table.group(1))
		if table and not table in tables:
			print(table)
			tables.append(table)
	return tables
	
def find_between(s, first, last):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

class Object(object):
	pass

execfile("../pythonToolSettings/secrets.py")
execfile("../pythonToolSettings/diagramming_settings.py")

odbcConn = pyodbc.connect('DRIVER={SQL Server};SERVER=' + config["databaseServer"] + ';DATABASE=' + config["databaseName"] + ';UID=' + config["databaseUser"] + ';PWD=' + secrets["localSqlServerPassword"] )
 
schemaCursor = odbcConn.cursor()


sqlDirectory = "K:\pas\schema3"
diagramDirectory = "K:\pas\schema3"


for filename in os.listdir(sqlDirectory):
	if filename.endswith(".sql"):  #all the .sql files
		#print(filename, sqlDirectory)
		path = sqlDirectory + "\\" + filename
		tableList = getTablesFromSqlCreate(path)
		print(tableList)

		timesThrough = 0
		out = ""
		out = out  + '<dia:layer name="Background" visible="true" active="true">'
		#out = out + diaLine(13, 14, 23, 30)
		for tableName in tableList:
			 
			
			sql = """SELECT KU.table_name as TABLENAME,column_name as PRIMARYKEYCOLUMN
			FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS AS TC
			INNER JOIN
				INFORMATION_SCHEMA.KEY_COLUMN_USAGE AS KU
					  ON TC.CONSTRAINT_TYPE = 'PRIMARY KEY' AND
						 TC.CONSTRAINT_NAME = KU.CONSTRAINT_NAME AND 
						 KU.table_name='""" + tableName + """'
			ORDER BY KU.TABLE_NAME, KU.ORDINAL_POSITION;
			"""

			schemaCursor.execute(sql)
			#print(sql)
			pks = []
			pkRecords = schemaCursor.fetchall()
			pkResults = []
			pkColumns = [column[0] for column in schemaCursor.description]
			for schemaRecord in pkRecords:
					x = dict(zip(pkColumns, schemaRecord))
					pks.append(x["PRIMARYKEYCOLUMN"])
					pkResults.append(x)
					
					
			#print(pkResults)

			sql = ''
			sql += "SELECT  COLUMN_NAME AS MixedCaseName, LOWER(COLUMN_NAME) AS Name, DATA_TYPE AS Type, CHARACTER_MAXIMUM_LENGTH AS Length, ";
			sql += " COLLATION_NAME AS Collation, ";
			sql += " IS_NULLABLE AS Nullable ";
			sql += " FROM INFORMATION_SCHEMA.COLUMNS " 
			sql += " WHERE TABLE_NAME = '" + tableName + "' "
			sql += "  ";
			sql += "   ";
				

			schemaCursor.execute(sql)
			schemaRecords = schemaCursor.fetchall()
			results = []
			columns = [column[0] for column in schemaCursor.description]
			for schemaRecord in schemaRecords:
					x = dict(zip(columns, schemaRecord))
					results.append(x)
					

			#if tableName == "Inventory":
				#print(results )



			#print(tableName, pks)
			columns = []
			id = "O" + str(timesThrough + 1)
			for record in results:
				#print(record)
				#print("---------")
				column = Object()

				column.type= record["Type"]
				column.name = record["MixedCaseName"]
				column.size = record["Length"]
				column.isPrimary = False
				if column.name in pks:
					
					column.isPrimary = True
				
				column.isUnique = False
				if record["Nullable"] == "YES":
					column.isNullable = True
				else:
					#print(column.name)
					column.isNullable = False
				columns.append(column)
			northwestCorner = Object()
			northwestCorner.lat = 19 
			northwestCorner.lon = 12 * timesThrough
			out = out + newTable(tableName, columns, northwestCorner, id)
			#print(out)
			timesThrough = timesThrough + 1

		out = out + "</dia:layer>"
		#out = out + diaLine(13, 14, 23, 30)
		out = diaHeader() + out + diaFooter()
			
		fileObject  = open(sqlDirectory + "\\" + filename + ".dia", "w") 
		fileObject.write(out)
		fileObject.close()
	 
		continue
	else:
		continue