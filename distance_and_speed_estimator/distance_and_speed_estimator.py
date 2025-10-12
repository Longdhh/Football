import cv2
import utils

class DistanceAndSpeedEstimator():
    def __init__(self):
        self.frame_window = 5
        self.frame_rate = 30

    def add_distance_and_speed_to_tracks(self, tracks):
        player_distances = {}
        for object, object_tracks in tracks.items():
            if object == 'ball' or object == 'referee':
                continue
            number_of_frames = len(object_tracks)
            for frame_num in range(0, number_of_frames, self.frame_window):
                last_frame = min(frame_num+self.frame_window, number_of_frames-1)

                for track_id, _ in object_tracks[frame_num].items():
                    if track_id not in object_tracks[last_frame]:
                        continue

                    start_position = object_tracks[frame_num][track_id]['position_transformed']
                    end_position = object_tracks[last_frame][track_id]['position_transformed']

                    if start_position is None or end_position is None:
                        continue

                    distance_covered = utils.measure_distance(start_position, end_position)
                    time_elapse = (last_frame - frame_num)/self.frame_rate
                    speed_mps = distance_covered / time_elapse
                    speed_kph = speed_mps*3.6

                    if object not in player_distances:
                        player_distances[object] = {}

                    if track_id not in player_distances[object]:
                        player_distances[object][track_id] = 0

                    player_distances[object][track_id] += distance_covered

                    for frame_num_batch in range(frame_num, last_frame):
                        if track_id not in tracks[object][frame_num_batch]:
                            continue
                        tracks[object][frame_num_batch][track_id]['speed'] = speed_kph
                        tracks[object][frame_num_batch][track_id]['distance'] = player_distances[object][track_id]

    def draw_information(self, frames, tracks):
        output_frames = []
        for frame_num, frame in enumerate(frames):
            for object, object_tracks in tracks.items():
                if object == 'ball' or object == 'referee':
                    continue
                for _, track_info in object_tracks[frame_num].items():
                    if 'speed' not in track_info:
                        continue
                    speed = track_info.get('speed', None)
                    distance = track_info.get('distance', None)
                    if speed is None or distance is None:
                        continue
                    bbox = track_info['bbox']
                    position = utils.get_foot_position(bbox)
                    position = list(position)
                    position[1]+=40

                    position = tuple(map(int, position))
                    cv2.putText(frame, f"Speed: {speed:.2f} km/h", position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0),2)
                    cv2.putText(frame, f"Distance: {distance:.2f} m", (position[0], position[1]+20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
            output_frames.append(frame)
