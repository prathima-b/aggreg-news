from django.shortcuts import render,redirect
from .models import Article
import requests
from bs4 import BeautifulSoup
from collections import OrderedDict
from .forms import Post_article
def homepage(request):
    urls=requests.get("https://www.bbc.com/news")
    soup=BeautifulSoup(urls.text,'html.parser')
    t=soup.find("div",{'class':'gel-layout gel-layout--no-flex nw-c-top-stories--standard nw-c-top-stories--international'})
    f=t.select('h3')
    content=[]
    for l in f[2:]:
        content.append(l.text)
    content=list(OrderedDict.fromkeys(content))
    an=t.find_all('a',{'class':'gs-c-promo-heading gs-o-faux-block-link__overlay-link gel-pica-bold nw-o-link-split__anchor'})
    links=[]
    for ik in an:
        link=ik.get('href')
        if "https://www.bbc.co.uk" not in link:
            link="https://www.bbc.co.uk"+link
        links.append(link)
    links=list(OrderedDict.fromkeys(links))
    im=t.select('img')
    images=[]
    for i in im[1:]:
        tu=i.get('data-src')
        tu=str(tu)
        tu=tu.replace('{width}','800')
        images.append(tu)
    images=list(OrderedDict.fromkeys(images))
    conima=tuple(zip(links,content,images))
    
    url=requests.get('https://abcnews.go.com/International')
    soup=BeautifulSoup(url.text,'html.parser')
    t=soup.find_all('div',class_='band__lead')
    contents=[]
    titles=[]
    for i in t:
        content=i.find_all('section')
        for j in content[0:1]:
            pp=j.select('a')
            for kk in pp:
                contents.append(kk.get('href'))
                titles.append(kk.text)
    articles=tuple(zip(contents,titles))

    db=Article.objects.all()

    urls=requests.get("https://edition.cnn.com/entertainment")
    soup=BeautifulSoup(urls.text,'html.parser')
    r=soup.find_all('div',{'class':'zn__containers'})
    entlinks=[]
    entimages=[]
    entitles=[]
    for i in r:
        se=i.find_all('li',{'class':'cn__listitem'})
        for j in se:
            it=j.find('div',{'class','media'})
            it=it.find('a')
            entlinks.append('https://edition.cnn.com/'+it.get('href')[1:])
            it=it.find('img')
            entimages.append('https:'+it.get('data-src-medium'))
            it=j.find('span',{'class','cd__headline-text'})
            entitles.append(it.text)
    content_ent=zip(entlinks,entimages,entitles)

    urls=requests.get("https://www.firstpost.com/category/sports")
    soup=BeautifulSoup(urls.text,'html.parser')
    r=soup.find_all('ul',{'class':'list side-img two-column'})
    splinks=[]
    spimages=[]
    sptitles=[]
    for i in r:
        se=i.find_all('li')
        for j in se:
            it=j.find('a')
            splinks.append(it.get('href'))
            it=it.find('img')
            image='https:'+it.get('src')
            image=image.replace('142','300')
            image=image.replace('106','300')
            spimages.append(image)
            it=j.find('a')
            it=it.find('h3')
            sptitles.append(it.text.strip())
    content_spt=zip(splinks,spimages,sptitles)
    
    contexts={
        'conima':conima,
        'content_ent':content_ent,
        'content_spt':content_spt,
        'articles':articles,
        'db':db 
    }
   
    return render(request,'News_aggregator/homepage.html',contexts)

def post_article(request):
	if request.method=="POST":
		form=Post_article(request.POST)
		if(form.is_valid()):
			form.save()
			return redirect("homepage")
	else:
		form=Post_article()
		return render (request,"News_aggregator/form.html",{'form':form})


def search(request):
    if request.method == 'GET':
        search_query = request.GET.get('q')
        art_url=[]
        urls=requests.get("https://www.google.com/search?q={0}".format(search_query))
        soup=BeautifulSoup(urls.text,'html.parser')
        r=soup.select('.kCrYT a')
        print("Related links: ")
        title_list=[]
        for l in r[1:7]:
            link=l.get('href')
            title=l.find_all('div',{'class':'BNeawe vvjwJb AP7Wnd'})
            if title==[]:
                title=l.find_all('span',{'class':'XLloXe AP7Wnd'})
            for i in title:
                title_list.append(i.text)
            if(link.find('https://www.google.com')==-1):
                art_url.append('http://www.google.com'+link)
        links_list=zip(title_list,art_url)
        context={
        'search_query':search_query,
        "links_list": links_list
        }
        return render(request,'News_aggregator/searchresults.html',context)
    else:
        return redirect("homepage")

