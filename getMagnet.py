#-*- encoding: utf-8 -*- 
import sys
import re
from html.parser import HTMLParser
import urllib
import zlib
from pip._vendor.requests.packages import urllib3
from lib2to3.fixer_util import String
class BTSMain_Parser(HTMLParser):
	def __init__(self):
		self.table_start=False;
		self.body_start=False;
		self.tr_start=False;
		self.td_start=False;
		self.title=[];
		self.url=[];
		self.textarea_start=False;
		self.magnet='';
		HTMLParser.__init__(self);
	def handle_starttag(self, tag, attrs):
		if tag=='table' and 'table magnet-list' in attrs[0]:
			self.table_start=True;
		if tag=='tbody' and self.table_start:
			self.body_start=True;
		if tag=='td' and self.body_start:
			self.td_start=True;
		if tag=='a' and self.td_start and 'btn' in attrs[1]:
			self.title.append(attrs[2][1]);
			self.url.append(attrs[0][1]);
		if tag=='textarea' and 'magnetLink' in attrs[0]:
			self.textarea_start=True;
	def handle_endtag(self, tag):
		if self.table_start and tag=='table':
			self.table_start=False;
		if self.body_start and tag=='tbody':
			self.body_start=False;
		if self.td_start and tag=='td':
			self.td_start=False;
		if self.textarea_start and tag=='textarea':
			self.textarea_start=False;
	def handle_data(self, data):
		if self.textarea_start:
			self.magnet+=data;
	def getURL(self):
		if len(self.url)==0:
			return '';
		else:
			return self.url[0];
	def getMagnet(self):
		return self.magnet;
	
def GetFromBTSpread(designation):
	urlbase="http://www.btspread.com/search/";
	url=urlbase+designation;
	response=urllib.request.urlopen(url);
	html=response.read();
	print(response.info());
	
	if response.info().get('Content-Encoding')=='gzip':
		html=zlib.decompress(html, 16+zlib.MAX_WBITS);
	btsmp=BTSMain_Parser();
	btsmp.feed(html.decode());
	subpageurl=btsmp.getURL();
	if len(subpageurl)==0:
		return designation;
	html=urllib.request.urlopen(subpageurl).read();
	htmlTEXT=html.decode('utf-8');
	mp=re.compile('magnet\:\?.*</textarea>')
	magList=mp.findall(htmlTEXT);
	if len(magList)>0:
		return magList[0].strip('</textarea>');
	else:
		return '';

# for i in range(1,10):
# 	print(GetFromBTSpread('CWP48'));