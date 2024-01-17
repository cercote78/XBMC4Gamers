### URLDownloading by Rocky5.
import extract,hashlib,hmac,math,os,re,requests,socket,struct,time,traceback,xbmc,xbmcgui
dialog = xbmcgui.Dialog()
dprogress = xbmcgui.DialogProgress()
working_directory = os.getcwd() + '/'

# Updated to new location
URLDownloader_Bin='1UvxE7X485CTSLAccmpkUb8NTMoI9u7va'
DownloadList_Bin='1X_2u2-5Ace2IvLKklVAsyHDHj9pMkJw-'
URLDownloader_Zip='1zg_K10VAAn7O6KvBbCBtxGjLftmT6m9g'
ESTestBuild='1VXzu0XzekSiEuS5IxD1wMm9EeRYlcSA5'
ESBuild='16T0dUzzYQAjzp5L2CRiEa298iOTF17XK'
GSTestBuild='1K89uwM524DgyaoCLoG2c1T6Hk5vex9dP'
GSBuild='1cLG1C7_bcMtZPX8n6vXmvWh2TgYXYJLW'

if os.path.isfile('Special://skin/720p/includes.xml') and not os.path.isfile('Special://skin/xml/includes.xml'):
	skin_xml_path = '720p'
else:
	skin_xml_path = 'xml'

class GoogleDriveDownloader:
	#CHUNK_SIZE = 32768 # 32.768kb
	#CHUNK_SIZE = 65536 # 65.536kb
	CHUNK_SIZE = 512000 # 512kb
	DOWNLOAD_URL = "https://docs.google.com/uc?export=download"
	
	@staticmethod
	
	def download_file_from_google_drive(file_id,dest_path,zipsize,filename,overwrite=False,unzip=False,showsize=False):
		destination_directory = os.path.dirname(dest_path)
		
		if not os.path.exists(destination_directory):
			makedirs(destination_directory)
		
		if not os.path.exists(dest_path) or overwrite:
			
			if filename == "Update":
				xbmc.executebuiltin('Skin.SetString(DisableProgress,Disabled)')
				xbmc.executebuiltin('Skin.SetString(DisableCancel,Disabled)')
				progress_resolver = "Checking for update"
			
			else:
				xbmc.executebuiltin('Skin.SetString(DisableCancel,)')
				xbmc.executebuiltin('Skin.SetString(DisableProgress,)')
				progress_resolver = "Resolving Google Drive link"
			
			dprogress.create("URLDOWNLOADER","",progress_resolver)
			dprogress.update(0)
			current_download_size = [0]
			session = requests.Session()
			response = session.post(GoogleDriveDownloader.DOWNLOAD_URL, params={'id': file_id, 'confirm': 't'}, stream=True, verify=False)
			
			if not str(response.status_code).startswith('2'):
				global invalidlink
				global responsecode
				
				if str(response.status_code).startswith('4'):
					httperrors = ["400 Bad Request","401 Unauthorized","402 Payment Required (Experimental)","403 Forbidden","404 Not Found","405 Method Not Allowed","406 Not Acceptable","407 Proxy Authentication Required","408 Request Timeout","409 Conflict","410 Gone","411 Length Required","412 Precondition Failed","413 Request Entity Too Large","414 Request-URI Too Long","415 Unsupported Media Type","416 Requested Range Not Satisfiable","417 Expectation Failed","418 I?m a teapot (RFC 2324)","420 Enhance Your Calm (Twitter)","422 Unprocessable Entity (WebDAV)","423 Locked (WebDAV)","424 Failed Dependency (WebDAV)","425 Too Early (WebDAV)","426 Upgrade Required","428 Precondition Required","429 Too Many Requests","431 Request Header Fields Too Large","444 No Response (Nginx)","449 Retry With (Microsoft)","450 Blocked by Windows Parental Controls (Microsoft)","451 Unavailable For Legal Reasons","499 Client Closed Request (Nginx)"]
					for error in httperrors:
						if error.startswith(str(response.status_code)):
							responsecode = error
					invalidlink = 1
				
				if str(response.status_code).startswith('5'):
					httperrors = ["500 Internal Server Error","501 Not Implemented","502 Bad Gateway","503 Service Unavailable","504 Gateway Timeout","505 HTTP Version Not Supported (Experimental)","506 Variant Also Negotiates (Experimental)","507 Insufficient Storage (WebDAV)","508 Loop Detected (WebDAV)","510 Not Extended","511 Network Authentication Required"]
					for error in httperrors:
						if error.startswith(str(response.status_code)):
							responsecode = error
					invalidlink = 2
				raise Exception('download error')
			
			GoogleDriveDownloader._save_response_content(response,dest_path,showsize,current_download_size,zipsize,filename)
			
			if unzip:
				
				try:
					with zipfile.ZipFile(dest_path,'r') as z:
						z.extractall(destination_directory)
				
				except zipfile.BadZipfile:
					print 'Ignoring `unzip` since "'+file_id+'" does not look like a valid zip file'
	
	@staticmethod
	
	def _save_response_content(response,destination,showsize,current_size,zipsize,filename):
		percent = 0
		current_size = int(current_size[0])
		StartTime = time.clock()
		
		with open(destination,'wb') as f:
			for chunk in response.iter_content(GoogleDriveDownloader.CHUNK_SIZE):
				if chunk:  # filter out keep-alive new chunks
					f.write(chunk)
					
					if showsize:
						percent = current_size*101/zipsize
						current_size += GoogleDriveDownloader.CHUNK_SIZE
						# calculate time renaming
						ElapsedTime = (time.clock() - StartTime)
						ChunksPerTime = (current_size / ElapsedTime)
						EstimatedTotalTime = (zipsize / ChunksPerTime)
						TimeLeftInSeconds = (EstimatedTotalTime - ElapsedTime) * 10 / 10 + 1 # adding + 1 makes it finish on 0 instead of being 0 with 1 second left
						TimeLeftInMinutes = TimeLeftInSeconds // 60
						TimeLeftInHours = TimeLeftInMinutes // 60
						
						if TimeLeftInHours >= 1:
							TimeLeft = ("Estimated time left %s hour, %s minutes " % (int(TimeLeftInHours),int(TimeLeftInMinutes) % 60))
						elif TimeLeftInMinutes >= 1:
							TimeLeft = ("Estimated time left %s minutes, %s seconds" % (int(TimeLeftInMinutes) % 60,int(TimeLeftInSeconds) % 60))
						elif TimeLeftInSeconds < 60:
							TimeLeft = ("Estimated time left %s seconds" % (int(TimeLeftInSeconds) % 60))
						
						dprogress.update(percent,filename.replace('.zip',''),TimeLeft)
						
						if dprogress.iscanceled():
							global allowcancellation
							allowcancellation = 1
							raise Exception("User cancelled download")

def download_update_check(url):
	if not os.path.exists(update_path):
		os.makedirs(update_path)
	
	path = os.path.join(update_path,url.split('/')[-1])
	filename = updatename
	GoogleDriveDownloader.download_file_from_google_drive(file_id=str(url),dest_path=str(update_path+filename),zipsize=int(zipsize),filename="Update",unzip=False,showsize=False,overwrite=True)

def download_url(url):
	dprogress.create("DOWNLOADING","","Initializing")
	
	if not os.path.exists(download_path):
		os.makedirs(download_path)
	
	path = os.path.join(download_path,url.split('/')[-1])
	GoogleDriveDownloader.download_file_from_google_drive(file_id=str(url),dest_path=str(file),zipsize=int(zipsize),filename=filename,unzip=False,showsize=True,overwrite=True)

def extract_file(file):
	if not os.path.exists(xbmc.translatePath(install_path)):
		os.makedirs(xbmc.translatePath(install_path))
	
	dprogress.create("EXTRACTING","","Initializing")
	zippath = xbmc.translatePath(install_path)
	dprogress.update(0,filename.replace('.zip',''),"This can take some time, please be patient.")
	extract.all(file,zippath,dprogress)

def clear_X():
	try:
		dprogress.create("CACHE","","Initializing")
		
		for root,dirs,files in os.walk("X:/",topdown=False):
			
			for name in files:
				os.remove(os.path.join(root,name))
			
			for name in dirs:
				os.rmdir(os.path.join(root,name))
			dprogress.update(0,'','Preparing Cache')
			time.sleep(0.1)
	
	except Exception as error:
		traceback.print_exc()

def convert_size(size_bytes):
	
	if size_bytes == 0:
		return "0B"
	
	size_name = ("B","KB","MB")
	i = int(math.floor(math.log(size_bytes,1024)))
	p = math.pow(1024,i)
	s = round(size_bytes / p,2)
	return "%s %s" % (s,size_name[i])

def update_check():
	global updatename
	global urldinvalid
	global xmlinvalid
	xmlinvalid = 0
	urldinvalid = 0
	
	if not os.path.isfile('Z:/temp/URLDownloader.bin'):
		updatename = 'URLDownloader.bin'
		download_update_check(str(URLDownloader_Bin))
		
		with open(os.path.join(working_directory,'version.bin'),'r') as verfile:
			local_version = verfile.readline().rstrip()
		
		with open('Z:/temp/URLDownloader.bin','r') as verfile:
			urldversion = verfile.readline().rstrip()
		
		if int(local_version.replace(".","")) < int(urldversion.replace(".","")):
			os.remove('Z:/temp/URLDownloader.bin')
			urldinvalid = 1
	
	if not os.path.isfile('Z:/temp/DownloadList.bin'):
		updatename = 'DownloadList.bin'
		download_update_check(str(DownloadList_Bin))
		
		with open('Z:/temp/DownloadList.bin','r') as verfile:
			dlsversion = verfile.readline().rstrip()
		
		with open(xbmc.translatePath('Special://skin/'+skin_xml_path+'/_Script_URLDownloader.xml'),"rb") as updatefile:
			udhashlibmd5.update(updatefile.read())
		
		if udhashlibmd5.hexdigest() != dlsversion:
			os.remove('Z:/temp/DownloadList.bin')
			xmlinvalid = 1

	dprogress.close()
	
def dash_update_check():
	global updatename
			
	# Updated check files
	updatename = 'updatecheck.bin'
	if "emustation" in xbmc.getLocalizedString(31000).lower():
		if "test build" in xbmc.getLocalizedString(31000).lower():
			download_update_check(str(ESTestBuild))
		else:
			download_update_check(str(ESBuild))
	else:
		if "test build" in xbmc.getLocalizedString(31000).lower():
			download_update_check(str(GSTestBuild))
		else:
			download_update_check(str(GSBuild))

	dprogress.close()

def dlc_hashing(titleid):
	hddkeybin = os.path.join(working_directory,'hdd-key.bin')
	hddkeytxt = 'Special://xbmc/system/hdd-key.txt'
	filecount = 0
	readhddkey = 1
	countlist = 0
	dprogress.update(0)
	xbmc.executebuiltin('Skin.SetString(DisableProgress,Disabled)')
	
	# Check for a txt/bin file with the hdd key or use the eeprom.
	if os.path.isfile(hddkeybin):
		readhddkey = 0
		hddkey = None
		
		with open(hddkeybin) as hex:
			hddkey = hex.readline()
		
		if len(hddkey) == 32:
			hddkey = bytearray.fromhex(hddkey)
		else:
			dprogress.create("DLC SIGNER","Loading.","")
			readhddkey = 1
	
	while readhddkey:
		key = xbmc.getInfoLabel('system.hddlockkey')
		
		if len(key.strip()) < 32:
			dprogress.update(0,"Loading",".")
			time.sleep(.2)
			dprogress.update(0,"Loading","..")
			time.sleep(.2)
			dprogress.update(0,"Loading","...")
		else:
			with open(hddkeybin,"w") as txteeprom: txteeprom.write(key.strip())
			hddkey = key.strip().decode('hex')
			break
	
	dprogress.update(0,"Signing ContextMeta.xbx","This can take some time, please be patient.","")
	xbmc.executebuiltin('Skin.SetString(DisableProgress,)')
	
	for folder,subfolder,file in os.walk('E:/TDATA/'+titleid):
		filecount += len(file)
	
	for folder,subfolder,file in os.walk('E:/TDATA/'+titleid):
		
		for xbxfile in file:
			xbxfile = xbxfile.lower()
			
			if xbxfile == "contentmeta.xbx":
				contextmetafile = os.path.join(folder,xbxfile)
				filesize = os.path.getsize(contextmetafile)
				readxbx = open(contextmetafile,'r+b')
				# All DLC installed to HDD must have this byte set to 0x01. Must be done before signing to calculate the correct signature.
				# Credit to sinikal6969 for letting me know about this.
				readxbx.seek(32,0)
				readxbx.write(bytearray.fromhex("01").decode())							
				readxbx.seek(0,0)
				filedata = readxbx.read(filesize)
				# Check the header fields.
				headersize = struct.unpack('I',filedata[24:28])[0]
				titleid = filedata[36:40]
				# Compute the HMAC key using the title id and HDD key.
				hmacKey = hmac.new(hddkey,titleid,hashlibsha1).digest()[0:20]
				# Compute the content signature.
				contentSignature = hmac.new(hmacKey,filedata[20:headersize],hashlibsha1).digest()[0:20]
				readxbx.seek(0,0)
				readxbx.write(contentSignature)
				countlist = countlist + 1
				time.sleep(1)
			
			dprogress.update((countlist * 100) / filecount,"Signing ContextMeta.xbx","This can take some time, please be patient.")
			countlist = countlist + 1

# Some variables Set outside the loop
re_focus_download_button = "9000"

try:
	# Check for network/internet activity
	socket.setdefaulttimeout(3.0)
	socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("8.8.8.8", 53))
	xbmc.executebuiltin('Dialog.Close(1904,false)')
	global httperrors
	httperrors = None
	global allowcancellation
	allowcancellation = 0
	global responsecode
	global invalidlink
	invalidlink = 0
	extensions = [ 'zip' ]
	download_path = 'X:/downloads/'
	update_path = 'Z:/temp/'
	udhashlibmd5 = hashlib.md5()
	hashlibsha1 = hashlib.sha1
	dlcmode = 0
	xawinstal = 0
	xmlinvalid = 0
	urldinvalid = 0
	valid_arguments = 1
	
	# args passed from xml
	try:
		defaulturl = sys.argv[1:][0]
	except:
		defaulturl == ""
	
	try:
		filename = sys.argv[2:][0]
	except:
		filename == ""
	
	try:
		zipsize = sys.argv[3:][0]
	except:
		zipsize == ""
	
	try:
		zipsizecheck = sys.argv[4:][0]
	except:
		zipsizecheck == ""
	
	try:
		install_path = sys.argv[5:][0]
	except:
		install_path = ""
	
	try:
		mod_dlc_mode = sys.argv[6:][0]
	except:
		mod_dlc_mode = ""
	
	# Check consistency of args
	if defaulturl == "":
		valid_arguments = 0
	
	if filename == "":
		valid_arguments = 0
	
	if zipsize == "":
		valid_arguments = 0
	
	if zipsizecheck == "":
		valid_arguments = 0
	
	# vars
	if install_path == "Emulator_Folder_Path":
		
		if xbmc.getCondVisibility('Skin.String(Custom_Emulator_Path)'):
			install_path = xbmc.getInfoLabel('Skin.String(Custom_Emulator_Path)')
		else:
			install_path = ""
	
	if install_path == "Roms_Folder_Path":
		
		if xbmc.getCondVisibility('Skin.String(Custom_Roms_Path)'):
			install_path	= xbmc.getInfoLabel('Skin.String(Custom_Roms_Path)')
		else:
			install_path = ""
	
	if install_path == "Media_Folder_Path":
		
		if xbmc.getCondVisibility('Skin.String(Custom_Media_Path)'):
			install_path = xbmc.getInfoLabel('Skin.String(Custom_Media_Path)')
		else:
			install_path = ""
	
	if valid_arguments:
		
		# Download the check file to see if there is an update for the dashboards.
		if filename == "URLDownloader.zip":
			dash_update_check()
		
		# Download the check file to see if there is an update. Doing it this way speeds up the loading after you download 1 files and the files are kept until a reboot.
		if not filename == "URLDownloader.zip":
			update_check()
		
		# If hash doesn't match tell user to update,also if filename is the urldownloader.zip bypass.
		if xmlinvalid == 0 and urldinvalid == 0 or filename == "URLDownloader.zip" or xbmc.getInfoLabel('Control.GetLabel(1)') == "Download Assets":
			# This is here to fix compatibility issues with previous builds.
			file = os.path.join(download_path,filename)
			
			# Truncate the filename to look cleaner and also get the titleid for DLC installation.
			if install_path == "XAWI":
				xawinstal = 1
			
			if mod_dlc_mode == "DLC":
				titleid = filename[-12:]; titleid = titleid[:-4]
				filename = filename[:-13]+'.zip'
				dlcmode = 1
			
			if os.path.isfile(file):
				os.remove(file)
			
			if filename == "URLDownloader.zip" or dialog.yesno("DOWNLOAD","",filename+"[CR]Install size "+convert_size(float(zipsize))):
				
				if install_path == "":
					install_path = dialog.browse(3,"Select destination folder",'files','')
					
					if mod_dlc_mode == "MOD" and not install_path == "" and not os.path.isfile(os.path.join(install_path,'default.xbe')):
						dialog.ok("ERROR","Cant find a default.xbe","Did you select the proper folder?")
						install_path = 0							

				if xawinstal: # If Xbox Artwork Installer Files process it
					if os.path.isfile('E:\\UDATA\\09999993\\location.bin'):
						with open('E:\\UDATA\\09999993\\location.bin','r') as input:
							install_path = input.readline().strip()
					else:
						xawinstal = 2
				
				if install_path:
					
					try:
						free_space_check = install_path # Check for free space
						
						if free_space_check.startswith('Special:') or free_space_check.startswith('Q:'):
							free_space_check = xbmc.translatePath('Special://root/')[:2]
						
						partition_free_space = xbmc.getInfoLabel('System.Freespace('+free_space_check[:1]+')').replace(free_space_check[:2]+' ','').split(' ')[0]
						
						if int(partition_free_space)*1024*1024 > int(zipsizecheck)+(1024*1024*2):
							
							try:
								clear_X()
								download_url(defaulturl)
								xbmc.executebuiltin('Skin.SetString(DisableCancel,Disabled)') # Disable the cancel button
								
								try:
									extract_file(file)
									os.remove(file)
									
									if dlcmode: # If DLC process the files
										dlc_hashing(titleid)
									xbmc.executebuiltin('Skin.SetString(DisableCancel,)') # Enable the cancel button								
									
									if filename == "XBMC-Emustation-update-files.zip" or filename == "XBMC-Emustation-test-build.zip" and os.path.isfile(xbmc.translatePath('Special://xbmc/updater/default.xbe')):
										dprogress.close()
										
										if dialog.yesno("QUESTION","","Update the built-in emulators?[CR]This is optional and not required."):
											with open(os.path.join(working_directory,'skip_emus.bin'), 'w') as tmp: tmp.write('')
										
										xbmc.executebuiltin('RunXBE(' + xbmc.translatePath('Special://xbmc/updater/default.xbe') + ')')
									
									elif filename == "XBMC4Gamers-update-files.zip" or filename == "XBMC4Gamers-test-build.zip" and os.path.isfile(xbmc.translatePath('Special://xbmc/updater/default.xbe')):
										xbmc.executebuiltin('RunXBE(' + xbmc.translatePath('Special://xbmc/updater/default.xbe') + ')')
									
									elif filename == "Cache Formatter.zip" and os.path.isfile(xbmc.translatePath('Special://xbmc/Cache Formatter/default.xbe')):
										xbmc.executebuiltin('RunXBE(' + xbmc.translatePath('Special://xbmc/Cache Formatter/default.xbe') + ')')
									
									elif filename == "URLDownloader.zip" and os.path.isdir(xbmc.translatePath('Special://xbmc/system/scripts/tmp/urldownloader')):
										xbmc.executebuiltin('RunScript(' + xbmc.translatePath('Special://xbmc/system/scripts/autoexec.py') + ')')
									
									else:
										dprogress.close()
										dialog.ok("SUCCESS","",filename.replace('.zip','') + " Installed")
										xbmc.executebuiltin('Dialog.Close(1902,false)')
								
								except Exception as error:
									traceback.print_exc()
									dprogress.close()
									dialog.ok("ERROR","Issue getting file.","Google Drive could be down.","Please try again later.")
							
							except Exception as error:
								traceback.print_exc()
								
								if allowcancellation == 1:
									dprogress.close()
									dialog.ok("URLDOWNLOADER","You cancelled the download of",filename.replace('.zip',''))
								
								elif invalidlink == 1:
									dprogress.close()
									dialog.ok("4xx: Client Error",str(responsecode),"File: "+filename)
								
								elif invalidlink == 2:
									dprogress.close()
									dialog.ok("5xx: Server Error",str(responsecode),"This is googles fault.","File: "+filename)
								
								else:
									dprogress.close()
									dialog.ok("ERROR","Damn something went wrong.","Local network issue, using Insignia DNS","without a secondary DNS set?")
								xbmc.executebuiltin('Dialog.Close(1902,false)')
						else:
							dialog.ok("ERROR","","Insufficient space on "+free_space_check)
					
					except Exception as error:
						traceback.print_exc()
						
						if xawinstal == 2:
							dprogress.close()
							dialog.ok('UH-OH','','Please download and run[CR]The Xbox Artwork installer at least once.','')
							xbmc.executebuiltin('Dialog.Close(1902,false)')
				
				else:
					pass
			
			else:
				pass
		
		else:
			dialog.ok("UPDATE AVAILABLE","Press (A) to update the","[B]URLDownloader[/B]")
			xbmc.executebuiltin('ActivateWindow(1904)')
			xbmc.executebuiltin('RunScript(Special://urldownloader/default.py,'+str(URLDownloader_Zip)+',URLDownloader.zip,2247055,2822733,Q:/system/scripts/)')
	
	else:
		dialog.ok("ERROR","Corrupt _Script_URLDownloader.xml","Update URLDownloader")
		xbmc.executebuiltin('Dialog.Close(1902,false)')
	
	try: # Used to zero the progress bar after everything is done
		dprogress.update(0)
	except:
		pass
	
	xbmc.executebuiltin('SetFocus('+re_focus_download_button+')') # Set focus to download button

except socket.error as ex:
	xbmc.executebuiltin('Dialog.Close(1904,false)')
	dialog.ok("ERROR","No Interweb access","Please check your network settings")
	xbmc.executebuiltin('SetFocus('+re_focus_download_button+')')
