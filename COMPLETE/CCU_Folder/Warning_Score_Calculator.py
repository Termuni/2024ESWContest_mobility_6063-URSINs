def Calculate_Warning_Score(ppg_bpm_lv, ecg_bpm_lv, camera_lv, belt_lv, pedal_err, score):
    score += LV_To_Score_ppg(ppg_bpm_lv)
    score += LV_To_Score_ecg(ecg_bpm_lv)
    score += LV_To_Score_cam(camera_lv)
    score += LV_To_Score_belt(belt_lv)
    if pedal_err:
        score += 10
    return score


def LV_To_Score_ppg(lv):
    if lv == 1:
        return -0.2
    elif lv == 2:
        return 0.2
    elif lv == 3:
        return 0.4
    elif lv == 4:
        return 0.6
    return 0
    
def LV_To_Score_ecg(lv):
    if lv == 1:
        return -0.2
    elif lv == 2:
        return 0.2
    elif lv == 3:
        return 0.4
    elif lv == 4:
        return 0.6
    return 0
    
def LV_To_Score_cam(lv):
    if lv == 1:
        return -0.2
    elif lv == 2:
        return 0.2
    elif lv == 3:
        return 0.4
    elif lv == 4:
        return 0.6
    return 0

def LV_To_Score_belt(lv):
    if lv==2:
        return 2
    return 0
