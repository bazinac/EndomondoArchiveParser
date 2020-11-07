import json
import shutil, os

# ------------CONFIG-----------------------
INPUT_FOLDER_ARCHIVE = 'ARCHIVE/'
OUTPUT_FOLDER = '_OUTPUT/'
HTML_TEMPLATE = 'template.html'
ENCODING = 'utf8' # 'cp1250' might be necessary on win
# ------------EOF CONFIG-------------------

def createHtmlSkeleton(index=1):
    output_file = OUTPUT_FOLDER + 'sheet' + str(index) + '.html'
    shutil.copyfile(HTML_TEMPLATE, output_file)
    return output_file

def appendOneImageToHtml(output_html_file, image_file, datetime, sport, name, notes):
    item_html = """
    <figure class="houba"><img alt="hovno" src="../ARCHIVE/<1IMAGE_FILE>" style="width: 350px; height: 350px;">
    <figcaption><DATETIME>(<SPORT>)<br>
      <span><b><NAME></b></span><br>
      <span><NOTES></span><br>

      <IMAGES_FOLDER>
  </figure>
    """
    item_html = item_html.replace('<1IMAGE_FILE>', image_file)
    item_html = item_html.replace('<DATETIME>', datetime)
    item_html = item_html.replace('<SPORT>', sport)
    item_html = item_html.replace('<NOTES>', notes)
    item_html = item_html.replace('<NAME>', name)
    if len(image_file) > 0:
        item_html = item_html.replace('<IMAGES_FOLDER>', '<a href=../ARCHIVE/"' + image_file[:-8] + '">=FOTKY=</a>') #strip /big.jpg
    else:
        item_html = item_html.replace('<IMAGES_FOLDER>','')

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
        img_url = ""
        sport = ""

        if file[-4:] == "json":

            with open(os.path.join(subdir, file)) as json_file:
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
                        img_url = dd[1]['picture'][0][0]['url']
            print("---")

            appendOneImageToHtml(output_file, img_url, start_time, sport, name, notes)
            fileCounter += 1
            if fileCounter % 100 == 0:
                print(str(fileCounter))
                output_file_index += 1
                output_file = createHtmlSkeleton(output_file_index)

print("Celkem napraseno " + str(fileCounter) + " cviceni")

