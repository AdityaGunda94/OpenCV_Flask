from flask import Flask,redirect,url_for,render_template,request, Response
import cv2
app = Flask(__name__)
camera = cv2.VideoCapture(0)

def gen_frames():
    while True:
        success, frame = camera.read() # read the capture frames

        #if unable to read the frames i am breaking
        if not success:
            break
        else:
            detector = cv2.CascadeClassifier('HaarCascades/haarcascade_frontalface_default.xml')
            eye_cascade = cv2.CascadeClassifier('HaarCascades/haarcascade_eye.xml')
            faces = detector.detectMultiScale(frame,1.1,7)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            #Draw rectangle boxes around the faces
            for(x, y, w, h) in faces:
                cv2.rectangle(frame, (x,y), (x+w, y+h), (255, 0, 0), 2)
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = frame[y:y+h, x:x+w]
                eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 3)

                for(ex, ey, ew, eh) in eyes:
                    cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)   

            ret, buffer = cv2.imencode('.jpg', frame)
            #convert the frames to the buffer bytes.
            frame = buffer.tobytes()
            yield(b'--frame\r\n'
                  b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('myindex.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)

            