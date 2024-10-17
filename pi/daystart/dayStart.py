import sys
import os
import json
import subprocess
import paho.mqtt.client as mqtt
refValue = {"활발":130,"친근":150,"도도":90,"소심":110}

def read_allinfo(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def write_allinfo(file_path, data):
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Data has been written to {file_path}")
    except Exception as e:
        print(f"Error writing to JSON file: {e}")


def main():
    allinfo_data = read_allinfo("/home/pi/allinfo.json")
    global refValue
    serialNum=allinfo_data['robot']['serialNumber']
    userid=allinfo_data['user']['userID']
    intimacy=allinfo_data['friendship']['current']
    personality=allinfo_data['robot']['personality']
    diaryContinuity=allinfo_data['interaction']['diaryContinuity']
    todayTotalintimacy=0
    
    #쓰다듬기 calculate
    todayTouching=read_allinfo("/home/pi/touchingNum.json")
    todayTouchingNum=todayTouching['touchingNum']
    
    #쓰다듬기 횟수 최대 100번으로 고정
    if todayTouchingNum>100: todayTouchingNum=100
    
    if todayTouchingNum==0:
        if intimacy<5000:
            todayTotalintimacy=todayTotalintimacy-refValue[personality]*0.5
        elif intimacy<8000:
            todayTotalintimacy=todayTotalintimacy-refValue[personality]*0.3
        else:
            todayTotalintimacy=todayTotalintimacy-refValue[personality]*0.1
    else:
        if intimacy<5000:
            todayTotalintimacy=todayTotalintimacy+refValue[personality]*0.5*todayTouchingNum/100
        elif intimacy<8000:
            todayTotalintimacy=todayTotalintimacy+refValue[personality]*0.3*todayTouchingNum/100
        else:
            todayTotalintimacy=todayTotalintimacy+refValue[personality]*0.1*todayTouchingNum/100
            
    todayTouching['touchingNum']=0
    write_allinfo("/home/pi/touchingNum.json", todayTouching)
    print("after cal touching : " + str(todayTotalintimacy))
    
    #다이어리 calculate
    todayDiary=read_allinfo("/home/pi/diaryDone.json")
    todayDiaryDone=todayDiary['todayDiary']
    if todayDiaryDone=="False":
        if intimacy<5000:
            todayTotalintimacy=todayTotalintimacy-refValue[personality]*0.5
        elif intimacy<8000:
            todayTotalintimacy=todayTotalintimacy-refValue[personality]*0.3
        else:
            todayTotalintimacy=todayTotalintimacy-refValue[personality]*0.1
            
        # 연속 diary -> 0
        diaryContinuity=0
    else:
        if intimacy<5000:
            todayTotalintimacy=todayTotalintimacy+refValue[personality]*0.5
        elif intimacy<8000:
            todayTotalintimacy=todayTotalintimacy+refValue[personality]*0.3
        else:
            todayTotalintimacy=todayTotalintimacy+refValue[personality]*0.1
        # 연속 diary += 1
        diaryContinuity=diaryContinuity+1
            
    todayDiary['todayDiary']="False"
    write_allinfo("/home/pi/diaryDone.json", todayDiary)
    print("after cal diary : " + str(todayTotalintimacy))
    
    #대화 횟수 calculate
    todayTalking=read_allinfo("/home/pi/talkingNum.json")
    todayTalkingNum=todayTalking['talkingNum']
    
    #대화 횟수에 따른 호감도 최대 50번으로 제한
    if todayTalkingNum>50: todayTalkingNum=50
        
    if todayTalkingNum==0:
        if intimacy<5000:
            todayTotalintimacy=todayTotalintimacy-refValue[personality]
        elif intimacy<8000:
            todayTotalintimacy=todayTotalintimacy-refValue[personality]*0.7
        else:
            todayTotalintimacy=todayTotalintimacy-refValue[personality]*0.5
    else:
        if intimacy<5000:
            todayTotalintimacy=todayTotalintimacy+refValue[personality]*1*todayTalkingNum/50
        elif intimacy<8000:
            todayTotalintimacy=todayTotalintimacy+refValue[personality]*0.7*todayTalkingNum/50
        else:
            todayTotalintimacy=todayTotalintimacy+refValue[personality]*0.5*todayTalkingNum/50
            
    todayTalking['talkingNum']=0
    write_allinfo("/home/pi/talkingNum.json", todayTalking)
    print("after cal talking : " + str(todayTotalintimacy))
    
    #연속 다이어리 작성 일수에 따른 호감도 증가
    if diaryContinuity>5: diaryContinuity=5
    if diaryContinuity>1:
        if intimacy<5000:
            todayTotalintimacy=todayTotalintimacy+refValue[personality]*0.3*(diaryContinuity-1)
        elif intimacy<8000:
            todayTotalintimacy=todayTotalintimacy+refValue[personality]*0.2*(diaryContinuity-1)
        else:
            todayTotalintimacy=todayTotalintimacy+refValue[personality]*0.1*(diaryContinuity-1)
    
    print("after cal continuity : " + str(todayTotalintimacy))
    # 친밀도 최종 계산
    intimacy=intimacy+todayTotalintimacy
    
    # 친밀도 최대 10000 제한
    if intimacy>10000: intimacy=10000
    if intimacy<0: intimacy=0
    
    # rpi 내부 data 갱신
    allinfo_data['interaction']['diaryContinuity']=diaryContinuity
    allinfo_data['friendship']['current'] = intimacy
    print(intimacy)
    print(userid)
    print(serialNum)
    subprocess.run(["mosquitto_pub", "-h", serverIP, "-t", serialNum+"/web/friendship", "-m", userid+"/"+str(intimacy)])
    write_allinfo("/home/pi/allinfo.json", allinfo_data)
    
if __name__ == "__main__":

    private_data=read_allinfo("/home/pi/private.json")
    
    serverIP = private_data["server"]["ip"]
    main()

