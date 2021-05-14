############google_play_parsing.py############
import re

re_app_attributes = [
re.compile(r' itemprop\=\"name\"\>\<span\>(?P<app__app_name__app_name>[^\<\>]*?)\<\/span\>\<\/h1\>', flags=re.DOTALL),
re.compile(r'\<a href\=\"\/store\/apps\/dev\?[^\<\>]*?\>(?P<app__app_developer_name__developer_name>[^\<\>]*?)\<\/a\>', flags=re.DOTALL),
re.compile(r'\<a itemprop\=\"genre\" href\=\"\/store\/apps\/category\/[^\\\/]*?\" class\=\"[^\"]*?\"\>(?P<app__app_category__app_category>[^\<\>]*?)\<\/a\>', flags=re.DOTALL),
re.compile(r'\"image\"\:\"(?P<app__app_icon_url__photo_url>http[^\"]*?)\"\,', flags=re.DOTALL),
]


re_review_block = re.compile(r'\]\s*\,(?P<review__review_rate_score__rate_score>\d+)\,null\,\"(?P<review__review_content__text>[^\"]*?)\"\,\[\d+\,\d+\]\s*\,(?P<review__review_helpful_score__helpful_score>\d+)\,null\,null\,\[\"\d+\"\,\"(?P<review__review_user_name__user_name>[^\"]*?)\"\,null\,\[\[null\,\d+\,null\,\[null\,null\,\"(?P<review__review_user_profile_photo_url__photo_url>[^\"]*?)\"\]', flags=re.DOTALL)

re_url = [
re.compile(r'details\?id\=(?P<app__app_id__app_id>[^\&\\\/]*?)($|\&)', flags=re.DOTALL),
]



re_similar_app_block = re.compile(r'\<a href\=\"\/store\/apps\/details.*?stars out of five stars\" role\=\"img\"', flags=re.DOTALL)
re_similar_app_attributes = [
re.compile(r'details\?id\=(?P<similar_app__app_id__app_id>[^\"]*?)\"', flags=re.DOTALL),
re.compile(r' title\=\"[^\<\>]*?\>(?P<similar_app__app_name__app_name>[^\<\>]*?)\<\/div\>', flags=re.DOTALL),
re.compile(r'developer\?id\=[^\<\>]*?\>\<div [^\<\>]*?\>(?P<similar_app__app_developer_name__developer_name>[^\<\>]*?)\<\/div\>', flags=re.DOTALL),
re.compile(r'Rated (?P<similar_app__app_rate_score__rate_score>[\d\.]*?) stars out', flags=re.DOTALL),
]


def page_parsing(
	page_html,
	page_url,
	):
	output = []
	####
	for r in re_url:
		for m in re.finditer(r, page_url):
			output.append(m.groupdict())
	###
	for r in re_app_attributes:
		for m in re.finditer(r, page_html):
			output.append(m.groupdict())
	###
	for m in re.finditer(re_review_block,page_html):
		output.append(m.groupdict())
	###
	for m in re.finditer(re_similar_app_block, page_html):
		g = m.group()
		similar_app = {}
		for r in re_similar_app_attributes:
			for m1 in re.finditer(r, g):
				similar_app.update(m1.groupdict())
		output.append(similar_app)
	###
	for e in output:
		if 'app__app_id__app_id' in e:
			output.append({'app':'gp:{}'.format(e['app__app_id__app_id'])})
		if 'review__review_content__text' in e:
			review_text = ' '.join([e[k] for k in e])
			e['review'] = review_text
			output.append({'app__app_review__review':review_text})
		if 'similar_app__app_id__app_id' in e:
			similar_app = 'gp:{}'.format(e['similar_app__app_id__app_id'])
			e['similar_app'] = similar_app
			output.append({'app__similar_app__similar_app':similar_app})
	###
	return output


'''
import yan_web_page_download 
page_url = 'https://play.google.com/store/apps/details?id=com.zhiliaoapp.musically.go&showAllReviews=true'
page_html = yan_web_page_download.download_page_from_url(page_url)

o = page_parsing(
	page_html,
	page_url,
	)

for e in o:
	print(e)
'''
############google_play_parsing.py############