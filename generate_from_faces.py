import os
import pyperclip
from tqdm import tqdm

Sleep = 1
fil = "faces"
fil_f = fil + ".png"
where = fil + "/"

Files = os.listdir(where)
Names = []
Out = ""
loop = 0

for File in tqdm(Files) :
    loop = loop + 1
    if len(File) < 11:
        continue
    if "X" in File:
        continue

Out = Out + "total_faces = {}".format(loop) + "\n"

loop = 0

for File in tqdm(Files) :
    loop = loop + 1
    if len(File) < 11:
        continue
    if "X" in File:
        continue
    Path = where + File
    Name = File[:-1]
    Name = Name[:-1]
    Name = Name[:-1]
    Name = Name[:-1]
    Names.append(Name)

    Full = '{} = img("{}")'.format(Name, Path)

    Out = Out + "\n" + Full



known_fn = "known_face_names = {}".format(Names)

known_fe = "known_face_encodings = {}".format(Names)
known_fe = known_fe.replace("'", "")

final = Out + "\n" + known_fe + "\n" + known_fn
pyperclip.copy(final)

