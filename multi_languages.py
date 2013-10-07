#-*-coding:utf-8-*-
import re,sys,os
import codecs,locale
import xdrlib,xlrd
import getopt
import glob
from shutil import copytree, ignore_patterns
from fdshutil import FileBak

lang = {}
def set_global_languages():
	lang['EN']="english"
	lang["Polish"]="polish"
	lang["Korean"]="korean"
	lang["French"]="france"
	lang["Spanish"]="spanish"
	lang["German"]="germany"
	lang["Italian"]="italian"
	lang["Portuguese"]="portugal"
	lang["Japanese"]="japanese"
	lang["Russian"]="russian"
	lang["Dutch"]="nederlands"
	lang["Norwegian"]="norwegian"
	lang["Danish"]="danish"
	lang["Swedish"]="swedish"
	lang["Finnish"]="finnish"

	lang["Hebrew"]="hebrew"
	lang["Polish"]="polish"
	lang["CZ"]="czech"
	lang["TR"]="turkish"
	lang["RO"]="romanian"
	lang["HU"]="hungarian"
	lang["Arabic"]="arabic"

	lang["GR"]="greek"
	lang["HR"]="polish"
	lang["CZ"]="czech"
	lang["TR"]="turkish"
	lang["RO"]="romanian"
	lang["HU"]="hungarian"

	lang["ID"]="indonesian"
	lang["TH"]="thai"
	lang["MS"]="malay" 

class FileHandler(object):	
	def write_file(self,filename,str):
	 	with open(filename,"rb+") as file:
	 		end = 0
	 		lines = []
	 		for line in file:
	 			if not line:
	 				break
	 			elif line.find("?>".encode())!=-1:
	 				end = 1
	 			else:
	 		 		lines.append(line)
	 	with open(filename,'wb+') as file:
	 		for line in lines:
	 			file.write(line)
	 		file.write(str.encode())
	 		file.write('\n'.encode())
	 		if end:
	 			file.write("?>".encode())
				
	def edit_file(self,filename,str,value):
	 	with open(filename,"rb+") as file:
	 		end = 0
	 		lines = []
	 		for line in file:
	 			if not line:
	 				break
	 			elif line.find("?>".encode())!=-1:
	 				end = 1	 				
	 			elif line.find(value.encode())!=-1:
	 				edit_str = "define('"+str+"', \""+value+"\")"
	 				lines.append(edit_str.encode())
	 			else:
	 		 		lines.append(line)
	 	with open(filename,'wb+') as file:
	 		for line in lines:
	 			file.write(line)
	 		file.write('\n'.encode())
	 		if end:
	 			file.write("?>".encode())

class LanguageHandler(object):
	file_handler = FileHandler()
	languages = {}	
	tag = []
	file_change = ""
	excel_name = ""
	input_dir = ""
	output_dir = ""

	def __init__(self,lang,tag,file_change,excel,output_dir):		
		self.languages = lang
		self.tag = tag
		self.file_change = file_change
		self.excel_name = excel
		self.output_dir = output_dir
		
	# @classmethod
	# @staticmethod
	# def __new__(clr, *args, **kwds):
	# 	cls.languages = lang
	# 	pass

	def get_languages(self):
		return sef.languages	

	def open_excel(self):
	    try:
	        data = xlrd.open_workbook(self.excel_name)
	        return data
	    except Exception:
	        print("open excel error")

	# 添加tag
	def append_tags(self):
	    data = self.open_excel()
	    table = data.sheets()[0]
	    nrows = table.nrows
	    ncols = table.ncols
	    
	    language_output_files = []
	    for j in range(0,ncols):
		    lang_str = str(table.cell(0,j))
		    lang_str = lang_str.split("'")[1].split("\\")[0]
		    language_output_file_name = self.output_dir + "/" + self.languages[lang_str]+"/"+self.file_change
		    language_output_files.append(language_output_file_name)
		    #language_output_files.append(lang_str)
	    #new_tags = self.get_new_tags('/encoding/language-test.txt',self.tag)

	    tags_flags = []
	    for i in range(1,nrows):
	    	flags = self.has_tags(language_output_files[j],self.tag[i-1])
	    	tags_flags.append(flags)            

	    #注意编码问题
	    for i in range(1,nrows):
	    	flags = 0
	    	for j in range(0,ncols):
		    	lang_str = table.cell(i,j).value.encode("utf-8")
		    	output_string = "define('"+self.tag[i-1]+"', \""+lang_str.decode("utf-8")+"\")"
		    	output_string = output_string + "\n"
		    	try:
		    		flags = self.has_tags(language_output_files[j],self.tag[i-1])
		    	except Exception:
		    		print('open file error')
		    	if  flags == 0:		    		
		    		try:
		    			self.file_handler.write_file(language_output_files[j],output_string)		    			
		    		except Exception:
		    			raise "write file error"
		    	else:
		    		print("Tag '"+self.tag[i-1]+"' is already in file=> "+language_output_files[j]+"!!!")
	    print("append successful!\n")
	    return True

	# 编辑tag
	def edit_tags(self,tag,value):
	    data = self.open_excel()
	    table = data.sheets()[0]
	    nrows = table.nrows
	    ncols = table.ncols
	    
	    language_output_files = []
	    for j in range(0,ncols):
		    lang_str = str(table.cell(0,j))
		    lang_str = lang_str.split("'")[1].split("\\")[0]
		    language_output_file_name = self.output_dir + "/" + self.languages[lang_str]+"/"+self.file_change
		    language_output_files.append(language_output_file_name)
        
	    #编码问题
	    for j in range(0,ncols):
	    	lang_str = table.cell(1,j).value
		    flags = self.has_tags(language_output_files[j],tag)		    	
			if  flags == 1:				
				try:					
					self.file_handler.edit_file(language_output_files[j],tag,value)
					print("Tag '"+tag+"' edit successful in file e=> "+language_output_files[j])#self.file_handler.edit_file(language_output_files[j],tag,value)  
				except BaseException:
					raise "edit file error"
			else:
				print("Tag '"+tag+"' must append to file=> "+language_output_files[j]+"!!!")
	    print("edit successful!\n")
	    return True

	# 是否存在tag
	def has_tags(self,filename,tag):
		exsit = 0
		with open(filename,'rb') as file:
			for line in file:
				if line.find(tag.encode())!=-1:
					exsit = 1
					break
				else:
					continue
			return exsit		
	
	# 在进行剔除，获得新的需要添加的tag	
	def get_new_tags(self,filename,tags):
		new_tags = []
		print("length:%i",len(tags))
		for i in range(0,len(tags)):
			exsit = 0
			with open(filename,'r') as file:
				for line in file:
					if line.find(tags[i])!=-1:
						exsit = 1
						break
					else:
						continue
			if exsit == 0:
				new_tags.append(tags[i])		
		return new_tags

#################################################################
excel_name = "encoding/excel.xls" #打开的excel文件
tags =['TXT_EMAIL']
#tags = ["APPEND_NEW_TAGS_11","APPEND_NEW_TAGS_12"] #新添加的tag字段
file_change = "lang.txt" #修改的file文件
output_dir = "encoding/languages"
bak_dir = 'encoding/tmp'

if __name__ == '__main__':
	print(sys.getdefaultencoding())
	set_global_languages()
	bak = FileBak(output_dir,bak_dir)
	try:
		bak.copy()
	except WindowsError:
		print('copy error')
	lang_handler = LanguageHandler(lang,tags,file_change,excel_name,output_dir)	
	lang_handler.edit_tags('TXT_EMAIL','TXT_EMAIL')
	ret = lang_handler.append_tags()
	if ret == False:
		bak.rm()
	
	#print(lang_handler.has_tags('encoding/language-test.txt','APPEND_NEW_TAGS_32'))
	#print(lang_handler.has_tags('encoding/language-test.txt','APPEND_NEW_TAGS_42'))
	#print(lang_handler.get_new_tags('encoding/language-test.txt',tags))
	#lang_handler.get_languages()
	#lang_handler.open_excel()