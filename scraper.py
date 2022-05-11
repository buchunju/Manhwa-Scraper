#!/usr/bin/env python3

# manga/manhua/manhwa scraper

import requests
from bs4 import BeautifulSoup
from sys import argv
import imghdr
from os   import path, system
from PIL  import Image

# add your own url
#https://mangatx.com/manga/the-origin/
#url = 'https://mangatx.com/manga/fist-demon-of-mount-hua' 

url = 'https://mangatx.com/manga/my-amazing-wechat'

base_url = url[url.rfind('/')+1:]

def gen_pdf(images : list, chap : str):
	images.reverse()
	hd = ""
	while len(images) > 0:
		hd = images.pop()
		ck = imghdr.what(hd)
		if ck == None:
			continue
		break

	img = Image.open(f"{hd}").convert('RGB')

	images.reverse()
	image_list = []
	print('Generating pdf')
	for i in images:
		ck = imghdr.what(i)
		if ck == None:
			continue
		im = Image.open(i).convert('RGB')
		image_list.append(im)
	img.save(f'{base_url}/{chap}/{chap}.pdf',save_all=True, append_images=image_list)


def save_images(image: list, name : str, numm: str):
	skip = True
	if numm != None:
		skip = False
	dir = base_url + '/' + name
	if path.exists(dir) != True:
		system(f'mkdir -p "{dir}"')
	img_list = []
	for img in image:
		img_list.append(dir + '/' + img[img.rfind('/')+1:])
		m_img = img[img.rfind("/")+1:img.rfind(".")]
		if not skip:
			if m_img == numm:
				skip = True
		if skip:
			img = img.strip()
			print(f'Downloading: {img}')
			response = requests.get(img)
			file = open(dir + '/' + img[img.rfind('/')+1:], "wb")
			file. write(response.content)
			file. close()

	gen_pdf(img_list, name)



def main():
	t = requests.get(url)
	begin = True
	if len(argv) > 1:
		begin = False
	args = argv
	soup = BeautifulSoup(t.text, 'html.parser')
	chapters = soup.find_all('li', class_="wp-manga-chapter")
	chapters.reverse()
	for link in chapters:
		for l in link.find_all('a'):
			c_name = l.string
			if c_name != None:
				c_name = c_name.strip()
				if not begin:
					if c_name.split(' ')[1] == argv[1]:
						begin = True
					# else:
					# 	print(f'Skiping {c_name.split(" ")[1]}')
				if begin:
					print(f'getting {c_name.strip()}')
					r = requests.get(l.get('href'))
					soup2 = BeautifulSoup(r.text, 'html.parser')
					images = []
					for im in soup2.find_all('div', class_="page-break no-gaps"):
						for img in im.find_all('img'):
							images.append(img.get('data-src'))
					if len(args) == 3:
						save_images(images, c_name, args.pop())
					else:
						save_images(images, c_name, None)



if __name__ == '__main__':
	main()
