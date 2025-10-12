import cv2

def read_vid(path):
    vid = cv2.VideoCapture(path)
    frame_rate = vid.get(cv2.CAP_PROP_FPS)
    frames = []
    while True:
        ret, frame = vid.read()
        if not ret:
            break
        frames.append(frame)
    return frames, frame_rate

def export_vid(frames, frame_rate, path):
    output = cv2.VideoWriter(path, cv2.VideoWriter_fourcc(*'mp4v'), frame_rate, (frames[0].shape[1], frames[0].shape[0]))
    for frame in frames:
        output.write(frame)
    output.release()
    print("Video exported successfully!!!")