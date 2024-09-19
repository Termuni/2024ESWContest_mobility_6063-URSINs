def Calculate_Warning_Score(ppg_bpm_lv, ecg_bpm_lv, camera_lv, pedal_err, score):
    score += LV_To_Score_ppg(ppg_bpm_lv)
    score += LV_To_Score_ecg(ecg_bpm_lv)
    score += LV_To_Score_cam(camera_lv)
    if pedal_err:
        score += 20
    return score


def LV_To_Score_ppg(lv):
    if lv == 1:
        return -1
    elif lv == 2:
        return 2
    elif lv == 3:
        return 4
    elif lv == 4:
        return 8
    return 0
    
def LV_To_Score_ecg(lv):
    if lv == 1:
        return -1
    elif lv == 2:
        return 2
    elif lv == 3:
        return 4
    elif lv == 4:
        return 8
    return 0
    
def LV_To_Score_cam(lv):
    if lv == 1:
        return -1
    elif lv == 2:
        return 2
    elif lv == 3:
        return 4
    elif lv == 4:
        return 8
    return 0