import fileinput, os, shutil, time, xbmc, xbmcgui, zipfile
Root_Directory	= xbmc.translatePath("Special://root/")[:-8]
zip_file = os.path.join(Root_Directory, 'updater/Update Files/update-files.zip')
xbmc.executebuiltin('Skin.SetString(DashboardUpdatedSmall,0)')
xbmc.executebuiltin('Skin.Reset(DashboardUpdated)')
pDialog	= xbmcgui.DialogProgress()
dialog	= xbmcgui.Dialog()
cleanupafter = 0

if os.path.isfile(zip_file):
	pDialog.create('Stage 2 of 2')
	pDialog.update(0,"Download complete","Updating dashboard")
	if not os.path.isfile(Root_Directory+'system/keymaps/Enabled'): cleanupafter = 1

##############################################################
## Update folder names and remove old crap no longer needed
##############################################################
## Update older backup to backups
	if os.path.isdir(Root_Directory+'system/backups') and os.path.isdir(Root_Directory+'system/backup'):
		shutil.rmtree(Root_Directory+'system/backup')
	elif os.path.isdir(Root_Directory+'system/backup'):
		os.rename(Root_Directory+'system/backup', Root_Directory+'system/backups')
##############################################################
## Remove older .modules folder
	if os.path.isdir(Root_Directory+'system/scripts/.modules'):
		shutil.rmtree(Root_Directory+'system/scripts/.modules')
##############################################################
## Remove old folders or files that are no longer needed.
	if os.path.isdir(Root_Directory+'system/toggles'):
		shutil.rmtree(Root_Directory+'system/toggles')
	
	if os.path.isdir(Root_Directory+'skins/Manage Profiles Skin/720p'):
		shutil.rmtree(Root_Directory+'skins/Manage Profiles Skin/720p')
	
	if os.path.isdir(Root_Directory+'skins/Profile Skin/720p'):
		shutil.rmtree(Root_Directory+'skins/Profile Skin/720p')
	
	if os.path.isdir(Root_Directory+'skins/Profile Skin/media/backgrounds'):
		shutil.rmtree(Root_Directory+'skins/Profile Skin/media/backgrounds')
	
	if os.path.isdir(Root_Directory+'skins/Profile Skin/extras/splashes') and not os.path.isdir(Root_Directory+'skins/Profile Skin/extras/themes/splashes'):
		shutil.move(Root_Directory+'skins/Profile Skin/extras/splashes',Root_Directory+'skins/Profile Skin/extras/themes/splashes')
	else:
		if os.path.isdir(Root_Directory+'skins/Profile Skin/extras/splashes'):
			shutil.rmtree(Root_Directory+'skins/Profile Skin/extras/splashes')
	
	if os.path.isfile(Root_Directory+'system/scripts/XBMC4Gamers/Utilities/dialog res check.py'):
		os.remove(Root_Directory+'system/scripts/XBMC4Gamers/Utilities/dialog res check.py')
	
	if os.path.isfile(Root_Directory+'system/scripts/XBMC4Gamers/Utilities/Random Items.py'):
		os.remove(Root_Directory+'system/scripts/XBMC4Gamers/Utilities/Random Items.py')
	
	if os.path.isdir(Root_Directory+'skins/Manage Profiles Skin/xml'):
		if os.path.isfile(Root_Directory+'skins/Manage Profiles Skin/xml/Includes_Context_Buttons.xml'):
			os.remove(Root_Directory+'skins/Manage Profiles Skin/xml/Includes_Context_Buttons.xml')
		
		if os.path.isfile(Root_Directory+'skins/Manage Profiles Skin/xml/Includes_Snow.xml'):
			os.remove(Root_Directory+'skins/Manage Profiles Skin/xml/Includes_Snow.xml')
		
		if os.path.isfile(Root_Directory+'skins/Manage Profiles Skin/xml/Includes_Birthday.xml'):
			os.remove(Root_Directory+'skins/Manage Profiles Skin/xml/Includes_Birthday.xml')
		
		if os.path.isfile(Root_Directory+'skins/Manage Profiles Skin/xml/Includes_Easter.xml'):
			os.remove(Root_Directory+'skins/Manage Profiles Skin/xml/Includes_Easter.xml')
		
		if os.path.isfile(Root_Directory+'skins/Manage Profiles Skin/xml/Includes_Particles.xml'):
			os.remove(Root_Directory+'skins/Manage Profiles Skin/xml/Includes_Particles.xml')
	
	if os.path.isdir(Root_Directory+'skins/Profile Skin/xml'):
		if os.path.isfile(Root_Directory+'skins/Profile Skin/xml/Custom_View_Options.xml'):
			os.remove(Root_Directory+'skins/Profile Skin/xml/Custom_View_Options.xml')
		
		if os.path.isfile(Root_Directory+'skins/Profile Skin/xml/Includes_Recent_Played.xml'):
			os.remove(Root_Directory+'skins/Profile Skin/xml/Includes_Recent_Played.xml')
		
		for viewfile in os.listdir(os.path.join(Root_Directory,'skins/Profile Skin/xml')):
			if viewfile.startswith('Viewtype_View'):
				os.remove(os.path.join(Root_Directory,'skins/Profile Skin/xml',viewfile))
		
		if os.path.isfile(Root_Directory+'skins/Profile Skin/xml/Viewtype_54_Panel.xml'):
				os.remove(Root_Directory+'skins/Profile Skin/xml/Viewtype_54_Panel.xml')
		
		if os.path.isfile(Root_Directory+'skins/Profile Skin/xml/Viewtype_56_Card.xml'):
				os.remove(Root_Directory+'skins/Profile Skin/xml/Viewtype_56_Card.xml')
		
		if os.path.isfile(Root_Directory+'skins/Profile Skin/xml/Viewtype_61_CarouselSmaller.xml'):
				os.remove(Root_Directory+'skins/Profile Skin/xml/Viewtype_61_CarouselSmaller.xml')
		
		if os.path.isfile(Root_Directory+'skins/Profile Skin/xml/_Script_Synopsis.xml'):
				os.remove(Root_Directory+'skins/Profile Skin/xml/_Script_Synopsis.xml')	
	
	if os.path.isdir(Root_Directory+'skins/Profile Skin/media/folder fanart'):
		if os.path.isdir(Root_Directory+'skins/Profile Skin/extras/folder fanart'):
			shutil.rmtree(Root_Directory+'skins/Profile Skin/extras/folder fanart')
		shutil.copytree(Root_Directory+'skins/Profile Skin/media/folder fanart',Root_Directory+'skins/Profile Skin/extras/folder fanart')
		shutil.rmtree(Root_Directory+'skins/Profile Skin/media/folder fanart')

	if os.path.isdir('E:/TDATA/Rocky5 needs these Logs/XBMC4Gamers'):
		shutil.rmtree('E:/TDATA/Rocky5 needs these Logs/XBMC4Gamers')
		os.mkdir('E:/TDATA/Rocky5 needs these Logs/XBMC4Gamers')		
	
	if os.path.isdir(os.path.join(Root_Directory,'system/scripts/XBMC4Gamers Extras/Synopsis')):
		shutil.rmtree(os.path.join(Root_Directory,'system/scripts/XBMC4Gamers Extras/Synopsis'))
	
	if os.path.isdir('E:/UDATA/09999990'):
		shutil.rmtree('E:/UDATA/09999990')

##############################################################
## Extract the dashboard zip
	with zipfile.ZipFile(zip_file) as zip:
		Total_TXT_Files = len(zip.namelist()) or 1
		Devide = 100.0 / Total_TXT_Files
		Percent = 0
		for item in zip.namelist():
			xbmc.executebuiltin('Skin.SetString(DashboardUpdatedSmall,'+str(int(Percent))+')')
			Percent += Devide
			pDialog.update(int(Percent),"Download complete","Updating dashboard")
			try:
				zip.extract(item, Root_Directory)
			except:
				print "Failed - "+item
		pDialog.update(100,"Download complete","Updating dashboard complete")
		xbmc.executebuiltin('Skin.SetBool(DashboardUpdated)')
		time.sleep(3)
	
	if os.path.isdir(Root_Directory+'skins/DVD2Xbox Skin'):
		shutil.rmtree(Root_Directory+'skins/DVD2Xbox Skin')
		input = fileinput.input(Root_Directory+'system/userdata/profiles.xml', inplace=True)
		for line in input:
			 if '<name>DVD2Xbox</name>' in line:
				 for _ in range(19):
					 next(input, None)
			 else:
				 print line,
	
	if os.path.isfile(Root_Directory+'system/userdata/guisettings.xml'): # set the master profile to default(dashboard) for network
		for line in fileinput.input(Root_Directory+'system/userdata/guisettings.xml', inplace=1):
			line = line.replace('<assignment>1','<assignment>0')
			line = line.replace('<assignment>2','<assignment>0')
			line = line.replace('<audio>384','<audio>0')
			line = line.replace('<audiotime>8','<audiotime>0')
			line = line.replace('<video>1024','<video>0')
			line = line.replace('<timeserveraddress>time.google.com</timeserveraddress>','<timeserveraddress>pool.ntp.org</timeserveraddress>')
			line = line.replace('<timeserveraddress>time.windows.com</timeserveraddress>','<timeserveraddress>pool.ntp.org</timeserveraddress>')
			print line,
	
	for Profiles in os.listdir(os.path.join(Root_Directory,'system/userdata/profiles')):
		guisettings = os.path.join(Root_Directory,'system/userdata/profiles',Profiles,'guisettings.xml')
		if os.path.isfile(guisettings):
			for line in fileinput.input(guisettings, inplace=1):
				line = line.replace('<audio>384','<audio>0')
				line = line.replace('<audiotime>8','<audiotime>0')
				line = line.replace('<video>1024','<video>0')
				line = line.replace('<videotime>8','<videotime>0')
				line = line.replace('<videotime>8','<videotime>0')
				line = line.replace('<timeserveraddress>time.google.com</timeserveraddress>','<timeserveraddress>pool.ntp.org</timeserveraddress>')
				line = line.replace('<timeserveraddress>time.windows.com</timeserveraddress>','<timeserveraddress>pool.ntp.org</timeserveraddress>')
				if '<font>' in line and not '<font>Arial.ttf</font>' in line: 
					line = line = '<font>default.ttf</font>\n'
				if '<skincolors>' in line: 
					line = line = '<skincolors>default.xml</skincolors>\n'
				if '<skintheme>' in line: 
					line = line = '<skintheme>default.xpr</skintheme>\n'
				if ' name="Manage Profiles Skin.' in line: 
					line = line = '\n'
				print line,

##############################################################
## After extraction cleanup any files that the user didn't have enabled
	if cleanupafter:
		os.remove(Root_Directory+'system/keymaps/Enabled')
else:
	pDialog.create('Error')
	pDialog.update(0,"Download complete","Files are missing")
	time.sleep(5)

## Write the cleanup script and reload the dashboard xbe
autoexec_data = "import os, xbmcgui\ntmp = 'E:/CACHE/tmp.bin'\nif os.path.isfile(tmp):\n	if os.path.isfile('Q:/system/keymaps/Enabled'): xbmc.executebuiltin('Skin.SetBool(editmode)')\n	os.remove(tmp)\n	xbmcgui.Dialog().textviewer('Changes.txt', open('Special://root/system/SystemInfo/changes.txt').read())"
with open(os.path.join(Root_Directory,'system/scripts/autoexec.py') , 'w') as autoexec: autoexec.write(autoexec_data)
with open("E:/CACHE/tmp.bin", 'w') as tmp: tmp.write('')
time.sleep(3)
os.remove(xbmc.translatePath("Special://root/default.xbe"))
xbmc.executebuiltin('RunXBE('+ Root_Directory +'default.xbe)')