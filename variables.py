from rose.common import obstacles, actions

good_obs_lst = [obstacles.PENGUIN, obstacles.WATER, obstacles.CRACK]
bad_obs_lst = [obstacles.BIKE, obstacles.BARRIER]

water_gain_score = 4
water_loss_score = -10

crack_gain_score = 5
crack_loss_score = -10

bad_obs_score = -10

penguin_gain_score = 10
penguin_loss_score = 0

none_score = 0