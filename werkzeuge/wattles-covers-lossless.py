import sys, os, subprocess, json, img2pdf
from PIL import Image
Image.MAX_IMAGE_PIXELS=None
d, kdp, n = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2]), int(sys.argv[3])
B=json.load(open(f"{d}/book.json")); NAME=B["slug"]; T=B["trim"]
PAPER,BLEED=0.002252,0.125; HX,HY,HH,HB=0.591,0.709,0.197,0.189
dpi=600; os.makedirs(f"{d}/output/print",exist_ok=True)
for kind,(sp,ex,ey,hg) in {"paperback":(n*PAPER,BLEED,BLEED,0.0),"hardcover":(n*PAPER+HB,HX,HY,HH)}.items():
    w=2*(T[0]+ex+hg)+sp; h=T[1]+2*ey
    png=f"{d}/output/print/{NAME}-cover-{kind}.png"
    subprocess.run(["node",f"{d}/tools/build_wrap.mjs",png,str(w),str(h),str(sp),str(ex),str(ey),str(hg),str(dpi)],check=True,stdout=subprocess.DEVNULL)
    im=Image.open(png).convert("RGB")
    W,H=round(w*dpi),round(h*dpi)
    if im.size!=(W,H): im=im.resize((W,H),Image.LANCZOS)
    im.save(png,optimize=False,compress_level=6)
    if kind=="paperback": im.save(f"{d}/output/print/{NAME}-cover-paperback-preview.png") if False else None
    lay=img2pdf.get_layout_fun((img2pdf.in_to_pt(w),img2pdf.in_to_pt(h)))
    open(f"{kdp}/{NAME}-cover-{kind}.pdf","wb").write(img2pdf.convert(png,layout_fun=lay))
    if kind=="paperback": im.copy().resize((W//4,H//4),Image.LANCZOS).save(f"{d}/output/print/pb-preview.png")
    os.remove(png); print(kind,n,f"{w:.3f}x{h:.3f}",f"spine {sp:.3f}")
env=dict(os.environ,COVER_SCALE="3.90625",COVER_Q="100")
subprocess.run(["node",f"{d}/tools/build_cover.mjs",f"{kdp}/{NAME}-cover-10000px.jpg"],check=True,env=env,stdout=subprocess.DEVNULL)
print(Image.open(f"{kdp}/{NAME}-cover-10000px.jpg").size)
