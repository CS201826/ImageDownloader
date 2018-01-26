#Coding: utf-8

#Import Libraries
import os
import requests
import re
import urllib
from selenium import webdriver
from threading import Thread
from bs4 import BeautifulSoup

#Define base url to download images
BASE_URL1 = 'http://all-free-download.com/wallpapers/nature-flowers-wallpaper-nature.html'
BASE_URL2 = 'http://all-free-download.com/wallpapers/cars-wallpapers.html'

#Get directory path of current file
root_path = os.path.dirname(os.path.abspath(__file__))

class ImageThread(Thread):
	"""
	This class is inherited from thread class       
	"""
	def __init__(self, name, folder, url, size):
		super().__init__()
		self.name = name
		self.folder = folder
		self.url = url
		self.size = size	

	def run(self):
		_dir = root_path+"\\"+self.folder
		
		#Create directory folder if not exists
		if not os.path.exists(_dir):
			os.makedirs(self.folder)
			
		#Get category url
		data = requests.get(self.url)
		html = BeautifulSoup(data.content, 'html5lib')
		img_container = html.find('div', class_ = 'imgcontainer')
		
		for img in img_container.find_all('div',class_='item'):
			link = img.find('a', href=re.compile('^http://all-free-download.com/wallpapers/download'))

			if link is not None:
				href_link = link['href']
				
				#Get image url to download image
				response = requests.get(href_link)
				detail_container = BeautifulSoup(response.content, 'html5lib')

				details = detail_container.find('div', id='detail_content')
				
				#Get specific size image
				for img in details.find_all('a', href=lambda href: href and str(self.size) in href):
					size_dir = _dir+"\\"+str(self.size)
					folder_path = self.folder+"\\"+self.size
					
					#Create image size directory if not exists
					if not os.path.exists(size_dir):
						os.makedirs(folder_path)

					img_link = img['href'];
					img_name = urllib.parse.urlparse(img_link)
					img_full_name = os.path.basename(img_name.path)

					print('Running', self.name,': downloading image', img_full_name)
					urllib.request.urlretrieve(img_link, folder_path+"\\"+img_full_name)
							
		
#Default categories and sizes
categories = ['nature', 'car']
sizes = ['1024_768', '1280_960', '1366_768', '1600_900', '1920_1080']

#---------Start of main program---------#
def main():
    #Print size with input value
	for k, v in enumerate(sizes):
		print(k+1, v)

	#Choose any size to download image
	size = int(input("choose any size \n"))
	if size <= 0 and size >= len(sizes):
		print('invalid size')
		exit()

	#Create and initialize ImageThread class
	thread1 = ImageThread("Thead-1", categories[0], BASE_URL1, sizes[size-1])
	thread2 = ImageThread("Thead-2", categories[1], BASE_URL2, sizes[size-1])

	#Start the thread	
	thread1.start()
	thread2.start()

#Call main function	
if __name__ == '__main__':
	main()
	
#---------End of main program---------#
