import cv2
import getpass
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import motion

smtp_server = "smtp.gmail.com"
port = 587
portssl = 465
userid = input("GMail ID : ")
passwd = getpass.getpass('Password:')


def sendMail(image):
    to=[userid]
    imageByte=cv2.imencode(".jpeg",image)[1].tostring()
    msg=MIMEMultipart()
    imageMime=MIMEImage(imageByte)
    msg.attach(imageMime)
    msg['From']='Me'
    msg['To']=to[0]
    msg['Subject'] = "가게 내부에 움직임이 감지되었습니다. 확인해주세요"
    server = smtplib.SMTP(smtp_server, port)
    server.ehlo_or_helo_if_needed()
    ret,m = server.starttls()
    server.ehlo_or_helo_if_needed()
    ret,m=server.login(userid, passwd)
    if (ret != 235):
        print("login fail")
        return
    print("login Success!!")
    server.sendmail('me', to, msg.as_string())
    server.quit()


if __name__ == '__main__':
    thresh=16
    cam=cv2.VideoCapture(0)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

    if cam.isOpened()==False:
        print("cam isnt opened")
        exit()
    i = [None, None, None]
    flag=False
    for n in range(3):
        i[n] = motion.getGrayCamImg(cam)
    checkFlag = 0
    while True:
        diff = motion.diffImage(i[0], i[1], i[2])
        thrimg = cv2.threshold(diff, thresh, 1, cv2.THRESH_BINARY)[1]
        count = cv2.countNonZero(thrimg)

        # if invader is checked.
        if count > 1:
            checkFlag += 1
        elif checkFlag >= 10 and flag == False:
            sendMail(i[2])
            flag=True
            print("가게 내부에 움직임이 감지되었습니다. 확인해주세요")
        elif count==0 and flag==True:
            flag=False
            checkFlag=0

        print("Check Flag : " + str(checkFlag))

        motion.updateCameraImage(cam, i)
        key = cv2.waitKey(10)
        if key == 27:
            break