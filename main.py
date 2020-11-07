import json
import shutil, os

# ------------CONFIG-----------------------
INPUT_FOLDER_ARCHIVE = 'ARCHIVE/'
OUTPUT_FOLDER = '_OUTPUT/'
HTML_TEMPLATE = 'template.html'
ENCODING = 'utf-8'
# ------------EOF CONFIG-------------------

def createHtmlSkeleton(index=1):
    output_file = OUTPUT_FOLDER + 'sheet' + str(index) + '.html'
    shutil.copyfile(HTML_TEMPLATE, output_file)
    return output_file

def appendOneImageToHtml(output_html_file, images, datetime, sport, name, notes):
    item_html = """
    <figure class="houba"><img alt="hovno" src="../ARCHIVE/<1IMAGE_FILE>" style="width: 350px; height: 350px;">
    <figcaption><DATETIME>(<SPORT>)<br>
      <span><b><NAME></b></span><br>
      <span><NOTES></span><br>

      <IMAGES>
  </figure>
    """
    if len(images) > 0:
        item_html = item_html.replace('<1IMAGE_FILE>', images[0])
    item_html = item_html.replace('<DATETIME>', datetime)
    item_html = item_html.replace('<SPORT>', sport)
    item_html = item_html.replace('<NOTES>', notes)
    item_html = item_html.replace('<NAME>', name)
    
    if len(images) == 0:
        item_html = item_html.replace('<IMAGES>','')
    elif len(images) == 1:     
        item_html = item_html.replace('<IMAGES>', '<a href="../ARCHIVE/' + images[0] + '">FOTO1</a>')
    elif len(images) == 2:     
        item_html = item_html.replace('<IMAGES>', '<a href="../ARCHIVE/' + images[0] + '">FOTO1</a><a href="../ARCHIVE/' + images[1] + '">FOTO2</a>')
    elif len(images) == 3:     
        item_html = item_html.replace('<IMAGES>', '<a href="../ARCHIVE/' + images[0] + '">FOTO1</a><a href="../ARCHIVE/' + images[1] + '">FOTO2</a><a href="../ARCHIVE/' + images[2] + '">FOTO3</a>')    
    elif len(images) == 4:     
        item_html = item_html.replace('<IMAGES>', '<a href="../ARCHIVE/' + images[0] + '">FOTO1</a><a href="../ARCHIVE/' + images[1] + '">FOTO2</a><a href="../ARCHIVE/' + images[2] + '">FOTO3</a><a href="../ARCHIVE/' + images[3] + '">FOTO4</a>')  
    elif len(images) == 5:     
        item_html = item_html.replace('<IMAGES>', '<a href="../ARCHIVE/' + images[0] + '">FOTO1</a><a href="../ARCHIVE/' + images[1] + '">FOTO2</a><a href="../ARCHIVE/' + images[2] + '">FOTO3</a><a href="../ARCHIVE/' + images[3] + '">FOTO4</a><a href="../ARCHIVE/' + images[4] + '">FOTO5</a>')  
    else:
       item_html = item_html.replace('<IMAGES>', '<a href="../ARCHIVE/' + images[0] + '">FOTO1</a><a href="../ARCHIVE/' + images[1] + '">FOTO2</a><a href="../ARCHIVE/' + images[2] + '">FOTO3</a><a href="../ARCHIVE/' + images[3] + '">FOTO4</a><a href="../ARCHIVE/' + images[4] + '">FOTO5</a>')

    f = open(output_html_file, "r", encoding=ENCODING)
    contents = f.readlines()
    f.close()

    contents.insert(52, item_html)

    f = open(output_html_file, "w", encoding=ENCODING)
    contents = "".join(contents)
    f.write(contents)
    f.close()

# MAIN

# Clear output
if os.path.exists(OUTPUT_FOLDER):
    shutil.rmtree(OUTPUT_FOLDER)
os.mkdir(OUTPUT_FOLDER)

# Prepare steering vars
fileCounter = 0
output_file_index = 1
output_file = createHtmlSkeleton(output_file_index)

# Process workouts one by one
for subdir, dirs, files in os.walk(INPUT_FOLDER_ARCHIVE + "/Workouts"):
    for file in sorted(files):

        start_time = ""
        name = ""
        notes = ""
        images = []
        sport = ""

        if file[-4:] == "json":

            with open(os.path.join(subdir, file), "r",encoding=ENCODING) as json_file:
                data = json.load(json_file)

            for d in data:
                if 'start_time' in d:
                    print(d['start_time'])
                    start_time=d['start_time']
                if 'name' in d:
                    print(d['name'])
                    name=d['name']
                if 'sport' in d:
                    print(d['sport'])
                    sport=d['sport']
                if 'notes' in d:
                    print(d['notes'])
                    notes = d['notes']
                if 'pictures' in d:
                    for dd in d['pictures']:
                        print(dd[1]['picture'][0][0]['url'])
                        images.append (dd[1]['picture'][0][0]['url'])
                        
                        if len(d) > 3 :
                            print(dd[3]['picture'][0][0]['url'])
                            images.append (dd[3]['picture'][0][0]['url'])
                        if len(d) > 5 :
                            print(dd[3]['picture'][0][0]['url'])
                            images.append (dd[5]['picture'][0][0]['url'])
                        if len(d) > 7 :
                            print(dd[3]['picture'][0][0]['url'])
                            images.append (dd[7]['picture'][0][0]['url'])
                        if len(d) > 9 :
                            print(dd[3]['picture'][0][0]['url'])
                            images.append (dd[9]['picture'][0][0]['url'])   
            print("---")            

            appendOneImageToHtml(output_file, images, start_time, sport, name, notes)
            fileCounter += 1
            if fileCounter % 100 == 0:
                print(str(fileCounter))
                output_file_index += 1
                output_file = createHtmlSkeleton(output_file_index)

print("Celkem napraseno " + str(fileCounter) + " cviceni")

