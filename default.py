#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,xbmcaddon,base64,socket
import CommonFunctions, urlparse, os
try:
  import StorageServer
except:
  import storageserverdummy as StorageServer
cache = StorageServer.StorageServer("cinemassacre_com", 24)
common = CommonFunctions
##common.plugin = plugin
    
socket.setdefaulttimeout(30)
pluginhandle = int(sys.argv[1])
xbox = xbmc.getCondVisibility("System.Platform.xbox")
addon = xbmcaddon.Addon(id='plugin.video.cinemassacre')
translation = addon.getLocalizedString

forceViewMode=addon.getSetting("forceViewMode")
if forceViewMode=="true":
  forceViewMode=True
else:
  forceViewMode=False
viewMode=str(addon.getSetting("viewMode"))

baseUrl = "http://cinemassacre.com"
dontShowTheseUrls = []
dontShowTheseUrls.append("/fanstuff/")
dontShowTheseUrls.append("/full-list-of-avgn-videos/")
dontShowTheseUrls.append("/fan-art-page")
dontShowTheseUrls.append("/2011/01/19/avgn-iphone-game-texting-of-the-bread/")
dontShowTheseUrls.append("/2010/03/10/avgn-game-over-2-by-gavin-maclean/")
dontShowTheseUrls.append("/2009/08/17/avgn-ko-boxing/")
dontShowTheseUrls.append("/2009/01/19/11909-avgn-game-over-by-gavin-maclean/")
dontShowTheseUrls.append("/2008/08/03/the-avgn-in-pixel-land-blast-by-kevin-berryman/")
dontShowTheseUrls.append("/2008/02/25/the-angry-video-game-by-eric-ruth/")
dontShowTheseUrls.append("/fan-songs-page")
#dontShowTheseUrls.append("")

#def writeLineToFile(lineToWrite):
#        f = open('C:\\Users\\Demon\\AppData\\Roaming\\XBMC\\addons\\plugin.video.cinemassacre_com\\log.file','a')
#        ##f.write(lineToWrite+'\n')
#        print(lineToWrite, file=f)
#        f.close()

def index():
        addDir("Angry Video Game Nerd","/category/avgn/","listCategories",os.path.join(addon.getAddonInfo('path'),"avgn.png"))
        addDir("Board James","/category/boardjames/","listCategories",os.path.join(addon.getAddonInfo('path'),"boardJ.png"))
        addDir("Movie Reviews","/category/moviereviews/","listCategories",os.path.join(addon.getAddonInfo('path'),"icon.png"))
        addDir("You Know What's BullShit","/category/ykwb/","listCategories",os.path.join(addon.getAddonInfo('path'),"ykwbs.png"))
        addDir("Films","/category/films/","listCategories",os.path.join(addon.getAddonInfo('path'),"icon.png"))
        xbmcplugin.endOfDirectory(pluginhandle)
        if forceViewMode==True:
          xbmc.executebuiltin('Container.SetViewMode('+viewMode+')')

def excludeUrl(url):
        for notUrl in dontShowTheseUrls:
          if notUrl in url:
            return True
        return False
        
def listCategories(url):
        getThisUrl = baseUrl+url
        if baseUrl in url:
          getThisUrl = url
        tmpContent = getUrl(getThisUrl)
        navList = common.parseDOM(tmpContent, "div", attrs={"id": "nav"})
        navList = common.parseDOM(navList, "ul", attrs={"id": "navlist"})
        liList = common.parseDOM(navList, "li", ret="class")
        curCat = ""
        for i in range(0,len(liList)):
          if "current-cat" in liList[i]:
            curCat = liList[i]
            break
        liList = common.parseDOM(navList, "li", attrs={"class": curCat})
        liList = common.parseDOM(liList, "ul", attrs={"class": "children"})
        if len(liList)>0:
          liList = liList[0]
        else:
          listVideos(url)
          return
        addDir("All Videos",getThisUrl,'listVideos',"")
        navUrls = re.compile('<a(?:.+?)href=(?:[\'|\"]*)([^\'|\"]*)(?:[\'|\"]*)(?:[^\>]*)>([^\<]*)</a>', re.DOTALL).findall(liList)
        for i in range(0,len(navUrls)):
          if excludeUrl(navUrls[i][0]):
            continue
          addDir(cleanTitle(navUrls[i][1].encode('ascii', 'ignore')),navUrls[i][0],'listVideos',"")
        xbmcplugin.endOfDirectory(pluginhandle)

def listVideos(url):
        getThisUrl = baseUrl+url
        if baseUrl in url:
          getThisUrl = url
        content = ""
        nextPage = 1
        curPage = 1
        ##cache.delete(url)
        linkList = []
        while (nextPage > 0):
            tmpContent = getUrl(getThisUrl)
            
            midContent = common.parseDOM(tmpContent, "div", attrs={"id": "mid-inner"})
            linksContent = common.parseDOM(midContent, "div", attrs={"id": "content"})
            theLinks = common.parseDOM(linksContent, "div", attrs={"class": "video archive"})
            for i in range(0,len(theLinks)):
              linkh3 = common.parseDOM(theLinks[i], "h3")
              linkUrl = common.parseDOM(linkh3, "a", ret="href")[0]
              if excludeUrl(linkUrl):
                continue
              
              linkTitle = common.parseDOM(linkh3, "a")[0]
              linkDate = common.parseDOM(theLinks[i], "div", attrs={"class": "video-date"})[0]
              
              linkImage = common.parseDOM(theLinks[i], "div", attrs={"class": "video-tnail"})
              linkImage = common.parseDOM(linkImage, "img", ret="src")
              linkImageTmp = re.compile('src=([^&]*)', re.DOTALL).findall(linkImage[0])
              if len(linkImageTmp)>0:
                if linkImageTmp[0][:1] != "/":
                  linkImageTmp[0] = "/" + linkImageTmp[0]
                linkImage = baseUrl+linkImageTmp[0]
              else:
                if len(linkImage[0])>0 and baseUrl in linkImage[0]:
                  linkImage = linkImage[0]
                else:
                  linkImage = ""
              
              
              linkDate = re.compile('(.+?)<span>|</span>', re.DOTALL).findall(linkDate)[0]
              linkTitle = linkTitle+" ("+linkDate.strip()+")"
              linkTitle = linkTitle.encode('ascii', 'ignore')
              linkTitle = cleanTitle(linkTitle)
              
              linkItem = {"title":linkTitle, "url":linkUrl, "thumb":linkImage}
              linkList.append(linkItem)

            ##Check Cache
            if curPage == 1:
              curPage += 1
              storedList = cache.get(url)
              if len(storedList) > 0:
                storedList = eval(storedList)
              if len(storedList) >= len(linkList):
                itMatches = 1
                for i in range(0,len(linkList)):
                  if linkList[i] != storedList[i]:
                    itMatches = 0 #First page doesn't match cached page
                    break
                if itMatches == 1:
                  linkList = storedList
                  break #Matches cache, so break out of while loop
                
            wpPageNav = common.parseDOM(linksContent, "div", attrs={"class": "wp-pagenavi"})
            nextPageUrl = common.parseDOM(wpPageNav, "a", attrs={"class": "nextpostslink"}, ret="href")
            if len(nextPageUrl)>0:
              getThisUrl = nextPageUrl[0]
            else:
              nextPage = 0
              
        cache.set(url, repr(linkList)) #update cache
        
        for i in range(0,len(linkList)):
            addLink(linkList[i]['title'],linkList[i]['url'],'playVideo',linkList[i]['thumb'])
            
        xbmcplugin.endOfDirectory(pluginhandle)
        if forceViewMode==True:
          xbmc.executebuiltin('Container.SetViewMode('+viewMode+')')

def playVideo(url):
        tmpContent = getUrl(url)
        vidContent = common.parseDOM(tmpContent, "div", attrs={"id": "video-content"})
        iframeUrls = common.parseDOM(vidContent, "iframe", ret="src")
        embedUrls = common.parseDOM(vidContent, "embed", ret="src")
        
        vidUrl = ""
        for i in range(0,len(iframeUrls)):
          if "bit.ly" in iframeUrls[i]:
            vidUrl = iframeUrls[i]
            break
          if "springboardplatform.com/embed_iframe/" in iframeUrls[i]:
            vidUrl = iframeUrls[i]
            break
            
        if len(vidUrl)>0:
          tmpContent = getUrl(vidUrl)
          metaUrl = common.parseDOM(tmpContent, "meta", attrs={"property": "og:video"}, ret="content")
          listitem = xbmcgui.ListItem(path=metaUrl[0])
          return xbmcplugin.setResolvedUrl(pluginhandle, True, listitem)
        
        for i in range(0,len(iframeUrls)):
          if "blip.tv" in iframeUrls[i]:
            vidUrl = iframeUrls[i]
            break
            
        if len(vidUrl)==0:
          for i in range(0,len(embedUrls)):
            if "blip.tv" in embedUrls[i]:
              vidUrl = embedUrls[i]
              break
        
        if len(vidUrl)>0:
          redirectedUrl = urllib.unquote_plus(getRedirectedUrl(vidUrl))
          parsed = urlparse.urlparse(redirectedUrl)
          fileParam = urlparse.parse_qs(parsed.fragment)['file'][0]
          match=re.compile('/rss/flash/([^/?]*)', re.DOTALL).findall(fileParam)
          id=match[0]
          if xbox==True:
            listitem = xbmcgui.ListItem(path="plugin://video/BlipTV/?path=/root/video&action=play_video&videoid="+id)
          else:
            listitem = xbmcgui.ListItem(path="plugin://plugin.video.bliptv/?path=/root/video&action=play_video&videoid="+id)
          return xbmcplugin.setResolvedUrl(pluginhandle, True, listitem)
          
        for i in range(0,len(iframeUrls)):
          if "youtube.com" in iframeUrls[i]:
            vidUrl = iframeUrls[i]
            break
        
        if len(vidUrl)>0:
          match=re.compile('/embed/([^/?]*)', re.DOTALL).findall(vidUrl)
          id=match[0]
          if xbox==True:
            listitem = xbmcgui.ListItem(path="plugin://video/Youtube/?path=/root/video&action=play_video&videoid="+id)
          else:
            listitem = xbmcgui.ListItem(path="plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid="+id)
          return xbmcplugin.setResolvedUrl(pluginhandle, True, listitem)
        
        for i in range(0,len(iframeUrls)):
          if "springboardplatform.com/mediaplayer" in iframeUrls[i]:
            vidUrl = iframeUrls[i]
            break
            
        for i in range(0,len(embedUrls)):
          if "springboardplatform.com/mediaplayer" in embedUrls[i]:
            vidUrl = embedUrls[i]
            break
            
        if len(vidUrl)>0:
          match=re.compile('springboardplatform.com/mediaplayer/springboard/video/([^/]*)/([^/]*)/([^/]*)/', re.DOTALL).findall(vidUrl)
          newUrl = "http://cms.springboardplatform.com/xml_feeds_advanced/index/"+match[0][1]+"/rss3/"+match[0][2]+"/"
          tmpContent = getUrl(newUrl)
          metaUrl = common.parseDOM(tmpContent, "media:content", attrs={"medium": "video"}, ret="url")
          listitem = xbmcgui.ListItem(path=metaUrl[0])
          return xbmcplugin.setResolvedUrl(pluginhandle, True, listitem)
        
        ## How To RTMP stream:
        ## swfVfy = "http://player.screenwavemedia.com/play/jwplayer/player.swf"
        ## rtmpurl = 'rtmp://video1.screenwavemedia.com/Cinemassacre/mp4:Cinemassacre-13623_high.mp4'
        ## pageurl = 'http://cinemassacre.com/2012/01/25/board-james-doggie-doo/'
        ## playpath = 'mp4:Cinemassacre-13623_high.mp4'
        ## segmentUrl = rtmpurl + " playpath=" + playpath + " pageurl=" + pageurl + " swfVfy=" + swfVfy
        ## item = xbmcgui.ListItem('RTMP Stream',path=segmentUrl)
        ## item.setInfo( type="Video", infoLabels={ "Title": "RTMP Stream" } )
        ## return xbmcplugin.setResolvedUrl(pluginhandle, True, item)
        
        objectDataUrl = common.parseDOM(vidContent, "script", attrs={"type": "text/javascript"}, ret="src")

        for i in range(0,len(objectDataUrl)):
          if "screenwavemedia.com" in objectDataUrl[i] and "embed.php" in objectDataUrl[i]:
            vidUrl = objectDataUrl[i]
            break

        if len(vidUrl)>0:
          tmpContent = getUrl(vidUrl)
          
          streamerVal = re.compile('streamer(?:[\'|\"]*):(?:[\s|\'|\"]*)([^\']*)', re.DOTALL).findall(tmpContent)
          flashplayerVal = re.compile('flashplayer(?:[\'|\"]*):(?:[\s|\'|\"]*)([^\']*)', re.DOTALL).findall(tmpContent)
          levelsVal = re.compile('levels(?:[\'|\"]*): \[(.*)\],', re.DOTALL).findall(tmpContent)
          files = ""
          if len(levelsVal)>0:
            filesVal = re.compile('file(?:[\'|\"]*):(?:[\s|\'|\"]*)([^\'|\"]*)', re.DOTALL).findall(levelsVal[0])
            for i in range(0,len(filesVal)):
              if "high" in filesVal[i]:
                files = filesVal[i]
                break
              
          if len(streamerVal)>0 and len(flashplayerVal)>0 and len(files)>0:
            rtmpurl = streamerVal[0]
            swfVfy = flashplayerVal[0]
            
            fileExt = re.compile('\.([^.]+)$', re.DOTALL).findall(files)
            if len(fileExt)>0:
              files = fileExt[0] + ":" + files
              
            if rtmpurl[-1:] != "/":
              rtmpurl = rtmpurl + "/"
            rtmpurl = rtmpurl + files
            
            segmentUrl = rtmpurl + " playpath=" + files + " pageurl=" + url + " swfVfy=" + swfVfy
            
            listitem = xbmcgui.ListItem(path=segmentUrl)
            return xbmcplugin.setResolvedUrl(pluginhandle, True, listitem)
        
        xbmc.executebuiltin("Notification(ERROR - No Video Found,No Video found on page: "+url+",10000)")
        ##common.log("Could not load video from url " + url)

def cleanTitle(title):
        title=title.replace("&lt;","<").replace("&gt;",">").replace("&amp;","&").replace("&#039;","'").replace("&quot;","\"").replace("&szlig;","ß").replace("&ndash;","-")
        title=title.replace("&Auml;","Ä").replace("&Uuml;","Ü").replace("&Ouml;","Ö").replace("&auml;","ä").replace("&uuml;","ü").replace("&ouml;","ö")
        title=title.replace("&#038;", "&").replace("&#8217;", "’").replace("&#8211;", "–")
        title=title.strip()
        return title

def getRedirectedUrl(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:14.0) Gecko/20100101 Firefox/14.0.1')
        response = urllib2.urlopen(req)
        response.close()
        return str(response.geturl())

def getUrl(url,data=None):
        if data!=None:
          req = urllib2.Request(url,data)
          req.add_header('Content-Type', 'application/x-www-form-urlencoded')
        else:
          req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:14.0) Gecko/20100101 Firefox/14.0.1')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        return link

def parameters_string_to_dict(parameters):
        ''' Convert parameters encoded in a URL to a dict. '''
        paramDict = {}
        if parameters:
            paramPairs = parameters[1:].split("&")
            for paramsPair in paramPairs:
                paramSplits = paramsPair.split('=')
                if (len(paramSplits)) == 2:
                    paramDict[paramSplits[0]] = paramSplits[1]
        return paramDict

def addLink(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty('IsPlayable', 'true')
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
        return ok

def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
         
params=parameters_string_to_dict(sys.argv[2])
mode=params.get('mode')
url=params.get('url')
if type(url)==type(str()):
  url=urllib.unquote_plus(url)

if mode == 'listVideos':
    listVideos(url)
elif mode == 'playVideo':
    playVideo(url)
elif mode == 'listCategories':
    listCategories(url)
else:
    index()
