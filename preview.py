#!/usr/bin/python3
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
import subprocess


try:
	os.mkdir("tapes")
	os.mkdir("media")
except:
	pass

def process_font(font):
	file_name = "tapes/" + font + ".tape"

	with open(file_name, "w+") as f:
		data = f"""
Output "media/{font.replace(' ', '_')}.gif"

Set FontSize 38
Set Width 1280
Set Height 720
Set FontFamily "{font}"
Set Theme Afterglow

Type "treefetch"

Enter
Sleep 20s
		"""
		f.write(data)

	os.system(f"vhs < '{file_name}'")
	file_name = file_name.split("/")[-1].replace(" ", "-")

	with open("README.md", "a+") as f:
		f.writelines(
			f"### {file_name.split('/')[-1].split('.')[0]}\n![](media/{file_name.split('/')[-1].split('.')[0]}.gif)\n"
		)


#process_font("ubuntu mono nerd font mono")

def get_fonts():
	try:
		output = subprocess.check_output(["fc-list"]).decode("utf-8")
		fonts = output.strip().split("\n")
		return fonts
	except subprocess.CalledProcessError as e:
		print("Error:", e)

def extract_font_names(font_info=get_fonts()) -> list:
	font_names = []
	# Define a regular expression pattern to extract font names
	for font_name in font_info:
		font = font_name.split(': ')[1]
		
		if "nerd" in font.lower():
			if ',' in font:
				font_names.append(font.split(',')[0])
			else:
				if ':' in font:
					font = font.split(':')[0]

				font_names.append(font)
	return font_names
		

fonts = extract_font_names(get_fonts())

#print(fonts)

# for i in range(len(fonts)):
# 	process_font(fonts[i])
# 	if i % 100 == 0:
# 		print(i)

#print(*fonts, end="\n")

with ThreadPoolExecutor(max_workers=2) as executor:
	futures = []
	for font in fonts:
		future = executor.submit(process_font, font)
		futures.append(future)

	for future in as_completed(futures):
		try:
			result = future.result()
		except Exception as e:
			print(f"Exception occurred: {e}")