This python script is used to turn a SQL Server database into a .dia diagram for use in the Dia program (see http://dia-installer.de/)  It does not produce relationship lines, though some initial work for this has been done.  To configure, you will need to set sqlDirectory and diagramDirectory paths in lines 302 and 303.


This looks for a secrets.py file in the directory 'pythonToolSettings,' parallel to the one this script is placed in.  That is:

<rootdirectory>/diagrammer/diagrammer.py
<rootdirectory>/pythonToolSettings/secrets.py

You will also need a file named diagramming_settings.py in 
<rootdirectory>/pythonToolSettings/diagramming_settings.py

These will have these forms:

secrets.py:
###################
secrets = json.loads("""
 
		{
			"serverAdminPassword":"yoursecret", 
			
			"serverAdminPassword1437":"yoursecret",
			
			"localSqlServerPassword": "yoursecret"
		} 
	""")
##############################

diagramming_settings.py:
###################
config = json.loads("""
		{
			"databaseName":"xxxxx" ,
			"databaseUser": "sa",
			"databaseServer": "yyyy",
			"tableSchema": "dbo"
		}
	""")
##############################
