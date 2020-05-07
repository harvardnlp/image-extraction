import os
from PIL import Image
import IPython
import glob
from math import log
import argparse

os.system("mkdir dataset")
os.system("mkdir out")


def get_histogram_dispersion(histogram):
    log2 = lambda x:log(x)/log(2)
    
    total = len(histogram)
    counts = {}
    for item in histogram:
        counts.setdefault(item,0)
        counts[item]+=1
        
    ent = 0
    for i in counts:
        p = float(counts[i])/total
        ent-=p*log2(p)
    return -ent*log2(1/ent)
        

def main(args):
    for g_f in glob.glob(args.data_dir + "/*.pdf"):
        g = g_f.split("/")[-1]
        os.system("rm dataset/*")
        os.system("rm out/*")
        command = (
            "convert -background white  -alpha remove -alpha off -density 200 '"
            + g_f
            + "'[1-12]  png24:dataset/"
            + g
            + "-%04d.png"
        )
        print(command)
        os.system(command)
        command2 = (
            "python infer_simple.py "
            + " --cfg e2e_faster_rcnn_X-101-64x4d-FPN_1x.yaml "
            + " --output-dir out "
            + " --image-ext png "
            + " --wts model_final.pkl dataset/ > tmp 2> tmp.err"
        )
        os.system(command2)
        print(g)
        if not os.path.exists("out/out.csv"):
            print("failed")
            continue
        best = -1e9
        for i, l in enumerate(open("out/out.csv")):
            print(i)
            f, x0, y0, x1, y1, _ = l.strip().split(";")
            print(f)
            original = Image.open("dataset/" + f)
            cropped_example = original.crop(
                (int(x0) - 20, int(y0) - 20, int(x1) + 20, int(y1) + 20)
            )
        
            disp = get_histogram_dispersion(im.histogram())
            if disp > best:
                disp = size
                cropped_example.save(out_dir + "/" + f + ".png")


if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()

    # Required positional argument
    parser.add_argument("data_dir", help="Dataset path with pdfs")
    parser.add_argument("out_dir", help="Output path with pngs")
    args = parser.parse_args()
    main(args)
