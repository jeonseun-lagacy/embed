from tkinter import *
import requests
from datetime import datetime

# 출퇴근 QR 요청 url
now = str(datetime.now())


# qr code 를 요청하고 저장된 qr code 이미지 경로 반환
def get_qr_code():
    print('qr code' + now)
    # url = 'http://113.198.245.107:12345/qr-code/seun'
    url = 'http://localhost:5000/qr-code/seun'
    response = requests.get(url)
    result = response.content
    image_path = 'qr_code.jpg'
    with open(image_path, 'wb') as f:
        f.write(result)
    return image_path


def start_attendance():
    global now
    now = str(datetime.now().today().date())
    print(now)
    get_qr_code()


def end_attendance():
    window.quit()


window = Tk()
window.attributes("-zoomed", True)
image = PhotoImage(file=get_qr_code()).zoom(5, 5)
label = Label(window, text="출퇴근 QR", image=image)
label.pack()
start_attendance_btn = Button(window, text="근무시작", command=start_attendance)
end_attendance_btn = Button(window, text="근무종료", command=end_attendance)
start_attendance_btn.pack()
end_attendance_btn.pack()
window.mainloop()
