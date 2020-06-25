# 웹 스트리밍에 대한 인터넷 예제를 참고하였습니다. 움직임을 탐지하면 탐지된 부분에 바운딩 박스를 그려줍니다.
from pyimagesearch.motion_detection import SingleMotionDetector

from imutils.video import VideoStream
from flask import Response
from flask import Flask
from flask import render_template
import threading
import argparse
import datetime
import imutils
import time
import cv2

outputFrame = None
lock = threading.Lock()

app = Flask(__name__)

vs = VideoStream(src=0).start()
time.sleep(2.0)

# 테스트용 페이지
@app.route("/")
def index():
	return render_template("index.html")


# 
def detect_motion(frameCount):
	global vs, outputFrame, lock
	# 가중치 파일을 사용한 움직임 검출 클래스 
	md = SingleMotionDetector(accumWeight=0.1)
	total = 0

	while True:
		frame = vs.read()
		frame = imutils.resize(frame, width=400)
		
		# 영상 처리가 용이한 Gray 스케일로 변환
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		
		# 엣지 검출을 통한 빠른 모션 감지를 위해 선형 필터인 가우시안 필터 적용.
		gray = cv2.GaussianBlur(gray, (7, 7), 0)
		
		# 타임 스탬프를 화면 좌측 하단에 출력
		timestamp = datetime.datetime.now()
		cv2.putText(frame, timestamp.strftime(
			"%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10),
			cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

		if total > frameCount:
			motion = md.detect(gray)

			if motion is not None:
				(thresh, (minX, minY, maxX, maxY)) = motion
				cv2.rectangle(frame, (minX, minY), (maxX, maxY),
					(0, 0, 255), 2)
		
		md.update(gray)
		total += 1

		with lock:
			outputFrame = frame.copy()
		

# 예제 참고, 제너레이터 함수 함수 작성
def generate():
	# 쓰레드 활용을 위한 lock 선언
	global outputFrame, lock

	while True:
		with lock:
			if outputFrame is None:
				continue

			(flag, encodedImage) = cv2.imencode(".jpg", outputFrame)

			if not flag:
				continue
		
		# yield 키워드를 사용해 웹 페이지 스트리밍
		yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
			bytearray(encodedImage) + b'\r\n')


@app.route("/video_feed")
def video_feed():
	return Response(generate(),
		mimetype = "multipart/x-mixed-replace; boundary=frame")


if __name__ == '__main__':
	ap = argparse.ArgumentParser()
	ap.add_argument("-f", "--frame-count", type=int, default=32, help="# of frames used to construct the background model")
	args = vars(ap.parse_args())

	t = threading.Thread(target=detect_motion, args=(args["frame_count"],))
	t.daemon = True
	t.start()

	app.run(host="0.0.0.0", port=8080, debug=True,	threaded=True, use_reloader=False)

vs.stop()
