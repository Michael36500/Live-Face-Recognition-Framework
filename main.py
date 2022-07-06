# imports
import face_recognition
import cv2
import numpy as np
import time

# define some variables
Start = time.time()
act_face = 0

# define funuction for loading images and printing some info
def img(where):
    global total_faces
    global act_face
    act_face = act_face + 1
    print("picture loaded ", where, "\t\t\t\t", act_face, "of", total_faces)
    image = face_recognition.load_image_file(where)
    
    face_encoding = face_recognition.face_encodings(image)
    if str(face_encoding) == "[]":
        print("NO FINDABLE FACES!!!")

    return face_encoding [0]

# funuction for stopwatch when loading images
def time_convert(sec):
    mins = sec // 60
    sec = sec % 60
    hours = mins // 60
    mins = mins % 60
    print("Time Lapsed = {0}:{1}:{2}".format(int(hours),int(mins),sec))


print("GO!")

# setting camera input, usually 0
camera = 0
video_capture = cv2.VideoCapture(camera, cv2.CAP_DSHOW)
time.sleep(1)
video_capture.release()

total_faces = 3

ChrisHemsworth = img("faces/ChrisHemsworth.jpg")
TomHolland = img("faces/TomHolland.jpg")
TonyStark = img("faces/TonyStark.jpg")
known_face_encodings = [ChrisHemsworth, TomHolland, TonyStark]
known_face_names = ['ChrisHemsworth', 'TomHolland', 'TonyStark']print("pictures loaded")



print(time.time() - Start)

# setting video camera
video_capture = cv2.VideoCapture(camera, cv2.CAP_DSHOW)
# video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
# video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
print("video captured")

# Initialize some variables
multipl = 1
resize = 1 / multipl
face_locations = [] 
face_encodings = []
face_names = []
process_this_frame = True
print("variables")
loop_noob = 0
while True:
    loop_noob = loop_noob + 1
    # Grab a single frame of video
    ret, frame = video_capture.read()
    if "None" in str(frame):
        print("dont have frame, skiping it")
        continue
    # frame = cv2.resize(frame, (960, 540))     # optional if runs slower
    print(ret, loop_noob)

    # Resize frame of video to 1/4 size for faster face recognition processing
    # small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
    if "None" in str(frame):
        print("frame = None, => skip")
        continue
    small_frame = cv2.resize(frame, (0, 0), fx=resize, fy=resize)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(rgb_small_frame)
    print("debuging is fun")
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    face_names = []
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        # found face with smallest distance (difference) against known face encodings

        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]

        face_names.append(name)



    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= multipl
        right *= multipl
        bottom *= multipl
        left *= multipl

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (255, 0, 0), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1, (255, 255, 255 ), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()

 