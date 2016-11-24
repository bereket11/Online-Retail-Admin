import os, re

for file in os.listdir(r'C:\Users\Brian\Downloads\Product Images\Product Images'):
    pattern = '\W'
    newfile = file[:file.rfind('.')]
    newfile = re.sub(pattern, '_', newfile)
    os.rename(r"C:\\Users\\Brian\\Downloads\\Product Images\\Product Images\\" + file, newfile + ".jpg")