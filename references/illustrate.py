#!/usr/bin/env python3
"""illustrate.py - 수능특강식 문항 삽화 파이프라인 (작은 로컬 모델 → 선화 SVG)

도식(그래프, 좌표, 실험 장치 배치, 흐름)은 이 스크립트를 쓰지 않고 SVG를 직접 쓴다
(references/illustration.md). 이 스크립트는 사물·장면 그림에만 쓴다.

단계
  1. gen        텍스트 → PNG (기본 SANA-Sprint 0.6B, 대체 SD-Turbo)       [torch, diffusers]
  2. clean      흑백 이진화 → 잡티 제거 → 내용 영역으로 잘라내기              [Pillow]
  3. vectorize  PNG → SVG path                                               [vtracer]
  4. normalize  색을 먹색 하나로, viewBox 정리, 클래스 부여                    [표준 라이브러리]
  5. label      라벨 JSON(A, B, ㄱ …)을 SVG <text>로 덧씌움                   [표준 라이브러리]

사용법
  python3 illustrate.py setup                       # 설치 명령만 출력한다(실행하지 않는다)
  <venv>/bin/python illustrate.py run --prompt "a microscope" --out assets/fig-microscope.svg [--labels labels.json] [--seed 7] [--model sana|sdturbo]
  python3 illustrate.py from-png in.png --out fig.svg [--labels labels.json]   # 직접 그린 스케치·사진 선화도 같은 후처리
  python3 illustrate.py label fig.svg --labels labels.json --out fig-labeled.svg

라벨 JSON 형식 (좌표는 결과 SVG의 viewBox 기준 0~1 비율)
  [{"text": "A", "x": 0.18, "y": 0.42}, {"text": "ㄱ", "x": 0.7, "y": 0.2, "accent": true}]

출력 SVG 옆에 같은 이름의 .json(모델, 시드, 프롬프트, 단계 수)을 남겨 같은 결과를 다시 만들 수 있게 한다.
"""
import argparse, json, os, re, sys, time
import xml.etree.ElementTree as ET

VENV = os.path.expanduser("~/.cache/paper-to-course/venv")
MODELS = {
    "sana": {"id": "Efficient-Large-Model/Sana_Sprint_0.6B_1024px_diffusers", "steps": 2, "size": 1024},
    "sdturbo": {"id": "stabilityai/sd-turbo", "steps": 2, "size": 512},
}
STYLE = (", simple black line drawing, textbook illustration, flat, no shading, no gradient, "
         "white background, clean closed outlines, no text, no letters")
INK = "#1F2328"
SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)


def die(msg):
    sys.exit("illustrate.py: " + msg)


def need_pil():
    """Pillow를 가져온다. 없으면 설치 안내와 함께 종료."""
    try:
        from PIL import Image, ImageFilter, ImageOps
    except ImportError:
        die(f"Pillow가 없다. `python3 {sys.argv[0]} setup`의 명령으로 만든 {VENV}의 파이썬으로 실행하시오.")
    return Image, ImageFilter, ImageOps


def load_labels(path):
    """라벨 JSON을 읽고 형식을 검사한다: [{"text": str, "x": 0~1, "y": 0~1, "accent": bool?}]"""
    try:
        with open(path, encoding="utf-8") as f:
            labels = json.load(f)
    except (OSError, ValueError) as e:
        die(f"라벨 JSON을 읽지 못했다({path}): {e}")
    if not isinstance(labels, list):
        die("라벨 JSON은 객체의 배열이어야 한다.")
    for i, L in enumerate(labels):
        if not isinstance(L, dict):
            die(f"라벨 #{i + 1}: 객체가 아니다.")
        miss = [k for k in ("text", "x", "y") if k not in L]
        if miss:
            die(f"라벨 #{i + 1}: 키 {', '.join(miss)}가 없다 (필요: text, x, y).")
        if not isinstance(L["text"], str) or any(isinstance(L[k], bool) or not isinstance(L[k], (int, float)) for k in ("x", "y")):
            die(f"라벨 #{i + 1}: text는 문자열, x·y는 숫자(0~1 비율)여야 한다.")
    return labels


# ── 1. 생성 ───────────────────────────────────────────────────────────
def generate(model, prompt, seed, size=None):
    try:
        import torch
        from diffusers import AutoPipelineForText2Image
    except ImportError:
        die(f"torch/diffusers가 없다. `python3 {sys.argv[0]} setup`의 명령으로 {VENV}를 만든 뒤 그 파이썬으로 실행하시오.")
    m = MODELS[model]
    dev = "mps" if torch.backends.mps.is_available() else ("cuda" if torch.cuda.is_available() else "cpu")
    dtype = torch.float32 if dev == "cpu" else (torch.bfloat16 if model == "sana" else torch.float16)
    if model == "sana":
        from diffusers import SanaSprintPipeline
        pipe = SanaSprintPipeline.from_pretrained(m["id"], torch_dtype=dtype)
    else:
        pipe = AutoPipelineForText2Image.from_pretrained(m["id"], torch_dtype=dtype)
    pipe = pipe.to(dev)
    g = torch.Generator("cpu").manual_seed(seed)
    s = size or m["size"]
    kw = dict(prompt=prompt + STYLE, num_inference_steps=m["steps"], generator=g, height=s, width=s)
    if model == "sdturbo":
        kw["guidance_scale"] = 0.0
    t = time.time()
    img = pipe(**kw).images[0]
    return img, {"model": m["id"], "device": dev, "dtype": str(dtype), "steps": m["steps"],
                 "size": s, "seed": seed, "prompt": prompt, "style": STYLE, "seconds": round(time.time() - t, 2)}


# ── 2. 정리 ───────────────────────────────────────────────────────────
def clean(img, threshold=160, pad=8):
    Image, ImageFilter, ImageOps = need_pil()
    g = ImageOps.grayscale(img.convert("RGB"))
    bw = g.point(lambda v: 0 if v < threshold else 255, mode="L")
    bw = bw.filter(ImageFilter.MedianFilter(3))          # 작은 점 제거
    box = ImageOps.invert(bw).getbbox()
    if not box:
        die("그림에서 선을 찾지 못했다(이진화 결과가 비어 있음).")
    l, t, r, b = box
    bw = bw.crop((max(0, l - pad), max(0, t - pad), min(bw.width, r + pad), min(bw.height, b + pad)))
    return bw.convert("RGB")


# ── 3. 벡터화 ─────────────────────────────────────────────────────────
def vectorize(png_path, svg_path):
    try:
        import vtracer
    except ImportError:
        die(f"vtracer가 없다. {VENV}/bin/pip install vtracer")
    vtracer.convert_image_to_svg_py(png_path, svg_path, colormode="binary", filter_speckle=8,
                                    mode="spline", corner_threshold=60, length_threshold=4.0, path_precision=1)


# ── 4. 정규화 ─────────────────────────────────────────────────────────
def normalize(svg_path, out_path, label=""):
    tree = ET.parse(svg_path)
    root = tree.getroot()
    w = float(re.sub(r"[^\d.]", "", root.get("width", "0")) or 0)
    h = float(re.sub(r"[^\d.]", "", root.get("height", "0")) or 0)
    if not root.get("viewBox") and w and h:
        root.set("viewBox", f"0 0 {w:g} {h:g}")
    for k in ("width", "height"):
        root.attrib.pop(k, None)
    root.set("role", "img")
    if label:
        root.set("aria-label", label)
    removed = 0
    for parent in root.iter():
        for el in list(parent):
            fill = (el.get("fill") or "").lower()
            if fill in ("#fff", "#ffffff", "white"):        # 흰 배경 조각 제거
                parent.remove(el); removed += 1
                continue
            if el.tag.endswith("path"):
                el.set("fill", INK)
                el.set("class", "ink-fill")
                el.attrib.pop("stroke", None)
    tree.write(out_path, encoding="unicode")
    return removed


# ── 5. 라벨 ───────────────────────────────────────────────────────────
def label(svg_path, labels, out_path, accent="#1F6FB2"):
    tree = ET.parse(svg_path)
    root = tree.getroot()
    vb = [float(v) for v in re.split(r"[\s,]+", root.get("viewBox", "0 0 100 100").strip())]
    if len(vb) != 4:
        die(f"viewBox가 네 값이 아니다: {root.get('viewBox')!r}")
    fs = max(12.0, vb[3] * 0.06)
    for L in labels:
        t = ET.SubElement(root, f"{{{SVG_NS}}}text")
        t.set("x", f"{vb[0] + L['x'] * vb[2]:.1f}")
        t.set("y", f"{vb[1] + L['y'] * vb[3]:.1f}")
        t.set("font-size", f"{fs:.0f}")
        t.set("font-weight", "700")
        t.set("text-anchor", "middle")
        t.set("dominant-baseline", "middle")
        t.set("paint-order", "stroke")
        t.set("stroke", "#FFFFFF")                         # 선 위에 올라가도 읽히게 흰 테두리
        t.set("stroke-width", f"{fs * 0.25:.1f}")
        t.set("fill", accent if L.get("accent") else INK)   # <img>로 넣으면 페이지 CSS가 닿지 않으므로 색을 직접 쓴다
        if L.get("accent"):
            t.set("class", "accent-text")
        t.text = L["text"]
    tree.write(out_path, encoding="unicode")


def postprocess(img, out, labels, meta, accent="#1F6FB2"):
    base = os.path.splitext(out)[0]
    png, raw = base + ".clean.png", base + ".raw.svg"
    d = os.path.dirname(os.path.abspath(out))
    os.makedirs(d, exist_ok=True)
    try:
        clean(img).save(png)
        vectorize(png, raw)
        normalize(raw, out, meta.get("prompt", ""))
        if labels:
            label(out, labels, out, accent)
        paths = sum(1 for _ in ET.parse(out).getroot().iter(f"{{{SVG_NS}}}path"))
        meta.update({"paths": paths, "bytes": os.path.getsize(out)})
        with open(base + ".json", "w", encoding="utf-8") as f:
            json.dump(meta, f, ensure_ascii=False, indent=2)
    finally:
        for p in (png, raw):    # 중간 산출물은 실패해도 남기지 않는다
            if os.path.exists(p):
                os.remove(p)
    print(f"{out}  (path {paths}개, {meta['bytes'] // 1024}KB)")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("setup")
    r = sub.add_parser("run"); r.add_argument("--prompt", required=True); r.add_argument("--out", required=True)
    r.add_argument("--seed", type=int, default=7); r.add_argument("--model", choices=MODELS, default="sana")
    r.add_argument("--size", type=int); r.add_argument("--labels")
    r.add_argument("--accent", default="#1F6FB2", help="강의의 교과 색(--color-accent)")
    f = sub.add_parser("from-png"); f.add_argument("png"); f.add_argument("--out", required=True); f.add_argument("--labels")
    f.add_argument("--accent", default="#1F6FB2")
    l = sub.add_parser("label"); l.add_argument("svg"); l.add_argument("--labels", required=True); l.add_argument("--out", required=True)
    l.add_argument("--accent", default="#1F6FB2")
    a = ap.parse_args()
    if a.cmd == "run" and a.size is not None:
        mult = 32 if a.model == "sana" else 8       # SANA는 32, SD-Turbo(VAE)는 8의 배수여야 한다
        if a.size <= 0 or a.size % mult:
            die(f"--size는 {a.model}에서 {mult}의 배수여야 한다 (받은 값: {a.size}).")
    labels = load_labels(a.labels) if getattr(a, "labels", None) else []

    if a.cmd == "setup":
        print(f"""# 한 번만 실행한다. 저장소 밖에 설치하고, 생성된 강의에는 SVG 파일만 들어간다.
uv venv --python 3.12 {VENV}
uv pip install --python {VENV}/bin/python torch diffusers transformers accelerate sentencepiece protobuf pillow vtracer
# 모델 가중치는 첫 실행 때 Hugging Face 캐시(~/.cache/huggingface)로 내려받는다.""")
    elif a.cmd == "run":
        img, meta = generate(a.model, a.prompt, a.seed, a.size)
        postprocess(img, a.out, labels, meta, a.accent)
    elif a.cmd == "from-png":
        Image = need_pil()[0]
        postprocess(Image.open(a.png), a.out, labels, {"source": os.path.basename(a.png)}, a.accent)
    elif a.cmd == "label":
        os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
        label(a.svg, labels, a.out, a.accent)
        print(a.out)


if __name__ == "__main__":
    main()
