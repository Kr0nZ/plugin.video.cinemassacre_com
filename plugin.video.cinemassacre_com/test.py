import urllib,urllib2,re,sys,base64,socket
import urlparse
str="You Know What&#8217;s Bullsh!t?"
list1 = [{"url":"heya","title":"byya"},{"url":"some","title":"none"}]
list2 = [{"url":"hey","title":"byy"},{"url":"some","title":"none"}]
print list1 == list2

##def cleanTitle(title):
##        title=title.replace("&lt;","<").replace("&gt;",">").replace("&amp;","&").replace("&#039;","'").replace("&quot;","\"").replace("&szlig;","ß").replace("&ndash;","-")
##        title=title.replace("&Auml;","Ä").replace("&Uuml;","Ü").replace("&Ouml;","Ö").replace("&auml;","ä").replace("&uuml;","ü").replace("&ouml;","ö")
##        title=title.replace("&#038;", "&").replace("&#8217;", "’").replace("&#8211;", "–")
##        title=title.strip()
##        return title
##
##print cleanTitle(str)

##vidUrl = 'http://cinemassacre.springboardplatform.com/mediaplayer/springboard/video/ciin001/865/476333/'
##match=re.compile('springboardplatform.com/mediaplayer/springboard/video/([^/]*)/([^/]*)/([^/]*)/', re.DOTALL).findall(vidUrl)
##print match
##parsed = urlparse.urlparse(url)
##print parsed.fragment
##defParam = urlparse.parse_qs(parsed.fragment)['file'][0]
##print defParam
##match=re.compile('/rss/flash/([^/?]*)', re.DOTALL).findall(defParam)
##print match

##testVar = ""
##print str(len(testVar))
##testVar = "http://bit.ly/RdUZ0W"
##print str(len(testVar))
##if "bit.ly" in testVar:
##  print "Its there"


##socket.setdefaulttimeout(30)
##baseUrl = "http://cinemassacre.com"
##
##def getUrl(url,data=None):
##        if data!=None:
##          req = urllib2.Request(url,data)
##          req.add_header('Content-Type', 'application/x-www-form-urlencoded')
##        else:
##          req = urllib2.Request(url)
##        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:14.0) Gecko/20100101 Firefox/14.0.1')
##        response = urllib2.urlopen(req)
##        link=response.read()
##        response.close()
##        return link
##
##def cleanTitle(title):
##        title=title.replace("&lt;","<").replace("&gt;",">").replace("&amp;","&").replace("&#039;","'").replace("&quot;","\"").replace("&szlig;","ß").replace("&ndash;","-")
##        title=title.replace("&Auml;","Ä").replace("&Uuml;","Ü").replace("&Ouml;","Ö").replace("&auml;","ä").replace("&uuml;","ü").replace("&ouml;","ö")
##        title=title.strip()
##        return title
##
##url = "http://cinemassacre.com/2004/05/07/castlevania-2-simons-quest/"
##tmpContent = getUrl(url)
##match=re.compile('<iframe id="([^"]*)" src="([^"]*)"', re.DOTALL).findall(tmpContent)
##url = match[0][1]
##tmpContent = getUrl(url)
##match=re.compile('<meta property="og:video" content="([^"]*)" />', re.DOTALL).findall(tmpContent)
##listitem = xbmcgui.ListItem(path=match[0])
##return xbmcplugin.setResolvedUrl(pluginhandle, True, listitem)

#print tmpContent

##getThisUrl = baseUrl+"/category/avgn/"
##content = ""
##nextPage = 1
##while (nextPage > 0):
##        tmpContent = getUrl(getThisUrl)
##        spl = tmpContent.split('<!-- content -->')
##        tmpContent = spl[1]
##        spl = tmpContent.split('<!-- /content -->')
##        tmpContent = spl[0]
##        content = content + tmpContent
##
##        spl = tmpContent.split('wp-pagenavi')
##        pagenav = spl[1]
##        print "\n"
##        print spl[1]
##        match=re.compile('<a href="([^"]*)" class="nextpostslink">', re.DOTALL).findall(pagenav)
##        print "\n"
##        print match
##        if len(match)>0:
##          getThisUrl = match[0]
##        else:
##          nextPage = 0
##
##
##spl = content.split('<div class="video archive">')
##
##for i in range(1,len(spl),1):
##	entry=spl[i]
##	print "\nNEXT "+str(i)+"\n"
##	#print entry
##	
##	match=re.compile('<h3><a href="(.+?)">(.+?)</a></h3>', re.DOTALL).findall(entry)
##	url=match[0][0]
##	title=match[0][1]
##	title=cleanTitle(title)
##
##	match=re.compile('<div class="video-date">(.+?)<span>|</span>', re.DOTALL).findall(entry)
##	date=""
##	if len(match)>0:
##	  date=" ("+match[0].strip()+")"
##	print title+date+"\n"
##	print url+"\n"
##	#addLink(title+date,url,'playVideo',"")
##
##
##print spl[0]
##sys.stdout.write(spl+"\r\n")
