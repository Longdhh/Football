from ultralytics import SAM
import cv2

model = SAM('sam2_t.pt')
model.info()

# input_image = "./dataset/video/00000.jpg"
# , points=[[388, 324], [232, 543], [378, 763], [607, 619], [786, 462], [958, 253], [1175, 390], [1248, 470], [1414, 871], [1152, 724], [347, 526], [551, 719], [874, 666], [890, 382], [1013, 483], [1104, 327], [1293, 414], [1333, 472], [1591, 639], [1172, 752], [1915, 400], [1875, 846], [788, 390], [315, 241]]
results = model("./dataset/video.mp4", stream=True)
results[0].show()
# results[0].show()
# for i, res in enumerate(results):
#     normalized_boxes = res.boxes.xywhn
#     with open(input_image.replace(".jpg", ".txt"), "w", encoding="UTF-8") as f:
#         j = 0
#         for nbox in normalized_boxes:
#             x, y, w, h = nbox
#             if j<10:
#                 f.write("0 {} {} {} {}".format(x, y, w, h) + '\n')
#             elif j<21:
#
#             print(nbox)