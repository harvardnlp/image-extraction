import os
from PIL import Image
import IPython
import glob
from math import log

os.system("mkdir dataset")
os.system("mkdir out")

for x in undone:
    for g_f in glob.glob("papers/"+ x + ".pdf"):
        g = g_f.split("/")[-1]
        os.system("rm dataset/*")
        os.system("rm out/*")
        command = "convert -background white  -alpha remove -alpha off -density 200 '" + g_f + "'[1-12]  png24:dataset/" +g +"-%04d.png"
        print(command)
        os.system(command)
        command2 = "python infer_simple.py  --cfg e2e_faster_rcnn_X-101-64x4d-FPN_1x.yaml --output-dir out --image-ext png --wts model_final.pkl dataset/ > tmp 2> tmp.err"
        os.system(command2)
        print(g)
        if not os.path.exists("out/out.csv"):
            print("failed")
            break
            continue
        d = -1e9
        for i, l in enumerate(open("out/out.csv")):
            print(i)
            f,  x0, y0, x1, y1, _ = l.strip().split(";")
            print(f)
            original = Image.open("dataset/"+ f)
            cropped_example = original.crop((int(x0)-20, int(y0)-20, int(x1)+20, int(y1)+20))
            cropped_example.save("pics/" + f + "." + str(i) + ".png")
    break

