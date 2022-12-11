# Description: This program detects fire in a video and sends an email to the user.
# thư viện
import cv2
import numpy as np
import smtplib
import playsound
import threading
#định nghĩa các biến toàn cục
Alarm_Status = False
Email_Status = False
Fire_Reported = 0
#hàm mở âm thanh cảnh báo
def play_alarm_sound_function():
	while True:
		playsound.playsound(r'alarm-sound.mp3',True)
#hàm gửi mail
def send_mail_function():
    #định nghĩa các biến toàn cục
    recipientEmail = "Enter_Recipient_Email"
    recipientEmail = recipientEmail.lower()
    #gửi mail
    try:
        server = smtplib.SMTP('hault.cm@gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login("Enter_Your_Email (System Email)", 'Enter_Your_Email_Password (System Email')
        server.sendmail('Enter_Your_Email (System Email)', recipientEmail, "Warning A Fire Accident has been reported on ABC Company")
        print("sent to {}".format(recipientEmail))
        server.close()
    except Exception as e:
    	print(e)

#hàm chính
#đọc video
# video = cv2.VideoCapture(0) # If you want to use webcam use Index like 0,1.
video = cv2.VideoCapture(r"fire.mp4")
while True:
    #đọc từng frame
    (grabbed, frame) = video.read()
    if not grabbed:
        break
    #thay đổi kích thước video
    frame = cv2.resize(frame, (960, 540))
    #chuyển đổi từ BGR sang HSV
    blur = cv2.GaussianBlur(frame, (21, 21), 0)
    #chuyển đổi từ BGR sang HSV
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    #định nghĩa màu đỏ
    lower = [18, 50, 50]
    upper = [35, 255, 255]
    #định nghĩa màu đỏ
    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")
    #tìm màu đỏ
    mask = cv2.inRange(hsv, lower, upper)
    #tìm màu đỏ
    output = cv2.bitwise_and(frame, hsv, mask=mask)
    #đếm số pixel màu đỏ
    no_red = cv2.countNonZero(mask)
    #nếu số pixel màu đỏ lớn hơn 15000 thì báo cảnh báo
    if int(no_red) > 15000:
        Fire_Reported = Fire_Reported + 1
    #hiển thị kết quả
    cv2.imshow("output", output)

    # if Fire_Reported >= 1:
    #     if Alarm_Status == False:
    #         threading.Thread(target=play_alarm_sound_function).start()
    #         Alarm_Status = True
    #     if Email_Status == False:
    #         threading.Thread(target=send_mail_function).start()
    #         Email_Status = True
    if cv2.waitKey(1) & 0xFF == ord('q'):
            break
#đóng cửa sổ
cv2.destroyAllWindows()
#đóng video
video.release()
