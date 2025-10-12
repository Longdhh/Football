from ultralytics import SAM

model = SAM('sam2_t.pt')
model.info()

'''
Data annotation process is done by using SAM2 and PolygonZone
You should annotate data by following class: 'goalkeeper', 'player', 'referee' and 'ball'
Edit 'input_image', 'points' parameter accordingly and run this code each time you annotate data
'''

input_image = "./dataset/images/val/00004.jpg"
results = model(input_image,
    points=[[560, 434], [588, 564], [924, 348], [990, 528], [1031, 439], [1073, 319], [1117, 462], [1160, 518], [1314, 496], [1323, 366], [1223, 271], [1846, 462], [1811, 610], [1269, 850], [444, 485], [1572, 487], [1367, 147], [1130, 680]])
results[0].show()
for i, res in enumerate(results):
    normalized_boxes = res.boxes.xywhn
    with open(input_image.replace(".jpg", ".txt"), "w", encoding="UTF-8") as f:
        j = 0
        for nbox in normalized_boxes:
            x, y, w, h = nbox

            #Change j accordingly to the frame to annotate the class correctly
            if j<14:
                f.write("2 {} {} {} {}".format(x, y, w, h) + '\n')
            elif j<15:
                f.write("1 {} {} {} {}".format(x, y, w, h) + '\n')
            elif j<17:
                f.write("3 {} {} {} {}".format(x, y, w, h) + '\n')
            else:
                f.write("0 {} {} {} {}".format(x, y, w, h) + '\n')
            j+=1