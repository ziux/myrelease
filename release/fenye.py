
def fenYe(request,fenyeno,objects):

    try:
        curPage = int(request.GET.get('curPage','1'))
        allPage = int(request.GET.get('allPage','1'))
        pageType = str(request.GET.get('pageType',''))
    except ValueError:
        curPage = 1
        allPage = 1
        pageType = ''
    if pageType == 'pageDown':
        curPage += 1
    elif pageType == 'pageUp':
        curPage -= 1
    startPos = (curPage - 1) * fenyeno
    endPos = startPos + fenyeno
    posts = objects[startPos:endPos]


    if curPage == 1 and allPage == 1:
        allPostCounts = objects.count()
        allPage = allPostCounts / fenyeno
        remainPost = allPostCounts % fenyeno
        if remainPost > 0:
            allPage += 1
    return posts,allPage,curPage
