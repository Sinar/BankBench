import subprocess, os, glob
from concurrent.futures import ProcessPoolExecutor

pages = sorted(glob.glob("ocr_pages/page_*.png"))

def ocr(path):
    out = os.path.splitext(path)[0]
    txt = out + ".txt"
    if os.path.exists(txt):
        return txt
    subprocess.run(["tesseract", path, out, "-l", "eng+msa", "--psm", "6"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return txt

if __name__ == "__main__":
    with ProcessPoolExecutor(max_workers=6) as ex:
        res = list(ex.map(ocr, pages))
    print("OCR done:", len(res), "pages")
