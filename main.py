import utils.video_utils
from distance_and_speed_estimator import DistanceAndSpeedEstimator
from tracker import Tracker
from team_assign import TeamAssigner
from player_ball_assigner import PlayerBallAssigner
from camera_movement import CameraMovementEstimator
from view_transformer import ViewTransformer
import numpy as np
import argparse

def get_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str, default='./dataset/test4.mp4', help="Path to input video")
    parser.add_argument('-o', '--output', type=str, help="Path to where the output will be stored")
    args = parser.parse_args()
    return args
def main(args):
    frames, frame_rate = utils.read_vid(args.input)

    tracker = Tracker("runs/detect/downloaded/best.pt")
    tracks = tracker.object_tracks(frames, read_from_stub=False, stub_path='stubs/track_stubs.pkl')

    # Get object positions
    tracker.add_position_to_tracks(tracks)

    # Camera movement estimator
    camera_movement_estimator = CameraMovementEstimator(frames[0])
    camera_movement_per_frame = camera_movement_estimator.get_camera_movement(frames)

    camera_movement_estimator.adjust_position(tracks, camera_movement_per_frame)

    # View transformer
    view_transformer = ViewTransformer()
    view_transformer.add_transformed_position_to_tracks(tracks)

    # Speed and Distance
    speed_and_distance_estimator = DistanceAndSpeedEstimator()
    speed_and_distance_estimator.add_distance_and_speed_to_tracks(tracks)

    # Ball interpolate
    tracks['ball'] = tracker.ball_interpolation(tracks["ball"])

    # Assign player team and ball acquisition
    team_assigner = TeamAssigner()
    team_assigner.assign_team_color(frames[0], tracks['player'][0])
    player_assigner = PlayerBallAssigner()
    team_ball_control = [None]
    for frame_num, player_track in enumerate(tracks['player']):
        # Assign player team
        for player_id, track in player_track.items():
            team = team_assigner.get_player_team(frames[frame_num], track['bbox'], player_id)
            tracks['player'][frame_num][player_id]['team'] = team
            tracks['player'][frame_num][player_id]['team_color'] = team_assigner.team_colors[team]

        # Assign ball control
        ball_box = tracks['ball'][frame_num][1]['bbox']
        assigned_player = player_assigner.assign_ball_to_player(player_track, ball_box)

        if assigned_player != -1:
            tracks['player'][frame_num][assigned_player]['has_ball'] = True
            team_ball_control.append(tracks['player'][frame_num][assigned_player]['team'])
        else:
            team_ball_control.append(team_ball_control[-1])
    team_ball_control = np.array(team_ball_control)
    output_video_frames = tracker.draw_annotation(frames, tracks, team_ball_control)
    speed_and_distance_estimator.draw_information(output_video_frames, tracks)
    utils.export_vid(output_video_frames, frame_rate, args.output)

if __name__ == "__main__":
    args = get_parse()
    main(args)