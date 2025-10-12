import utils

class PlayerBallAssigner():
    def __init__(self):
        self.max_player_ball_distance = 50

    def assign_ball_to_player(self, players, ball_bbox):
        ball_position = utils.get_box_center(ball_bbox)

        minimum_distance = 9999
        assigned_player = -1

        for player_id, player in players.items():
            player_bbox = player['bbox']

            distance_left = utils.measure_distance((player_bbox[0], player_bbox[-1]), ball_position)
            distance_right = utils.measure_distance((player_bbox[2], player_bbox[-1]), ball_position)
            distance = min(distance_left, distance_right)

            if distance < self.max_player_ball_distance:
                if distance < minimum_distance:
                    minimum_distance = distance
                    assigned_player = player_id
        return assigned_player