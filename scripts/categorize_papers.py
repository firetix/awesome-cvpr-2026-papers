from __future__ import annotations

import csv
import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
INPUT_CSV = DATA / "cvpr2026_papers_with_abstracts.csv"
OUTPUT_CSV = DATA / "cvpr2026_papers_categorized.csv"
OUTPUT_JSON = DATA / "cvpr2026_papers_categorized.json"
STATS_JSON = DATA / "category_stats.json"

AREA_KEYWORDS = {
    "Vision-Language & Multimodal Intelligence": {
        "vision-language": 7, "vision language": 7, "vlm": 7, "mllm": 7, "multimodal large language": 8,
        "large language model": 5, "llm": 3, "visual question answering": 6, "vqa": 5, "caption": 4,
        "referring expression": 5, "visual grounding": 5, "language-guided": 5, "text-image": 4,
        "image-text": 4, "multimodal": 4, "open-vocabulary": 4, "open vocabulary": 4,
        "prompt": 2, "instruction": 2, "reasoning": 3, "spatial understanding": 3,
    },
    "Generative Models, Editing & Creative Vision": {
        "diffusion": 7, "generative": 6, "generation": 6, "text-to-image": 8, "text to image": 8,
        "text-to-video": 8, "text to video": 8, "image generation": 7, "video generation": 8,
        "editing": 6, "stylization": 6, "style": 3, "inversion": 4, "flow matching": 5,
        "denoising": 3, "sampling": 3, "autoregressive": 4, "controlnet": 4, "lora": 3,
        "synthesis": 5, "novel view synthesis": 5, "avatar": 3, "3d generation": 8,
        "audio generation": 8, "music": 5, "image-to-image": 7, "text-guided": 4,
    },
    "3D Vision, Geometry & Neural Rendering": {
        "3d": 7, "4d": 5, "multi-view": 7, "multiview": 7, "view synthesis": 6, "novel view": 6,
        "reconstruction": 6, "geometry": 6, "geometric": 5, "depth": 5, "stereo": 5,
        "sfm": 5, "structure-from-motion": 6, "camera pose": 5, "pose estimation": 4,
        "point cloud": 6, "pointcloud": 6, "mesh": 5, "neural rendering": 6, "nerf": 7,
        "gaussian splatting": 8, "3dgs": 8, "radiance field": 7, "slam": 6, "lidar": 5,
        "surface": 4, "scene reconstruction": 7, "metric-scale": 5,
    },
    "Video, Motion & Temporal Understanding": {
        "video": 7, "temporal": 6, "motion": 6, "tracking": 5, "action recognition": 6,
        "event": 3, "dynamic scene": 6, "spatio-temporal": 6, "spatiotemporal": 6, "long-form": 4,
        "frame": 3, "trajectory": 4, "forecasting": 4, "scene flow": 5, "optical flow": 5,
    },
    "Embodied AI, Robotics & Autonomous Driving": {
        "robot": 8, "robotic": 8, "embodied": 8, "manipulation": 7, "navigation": 6,
        "autonomous driving": 8, "driving": 6, "humanoid": 7, "loco-manipulation": 8,
        "world model": 6, "vla": 7, "vision-language-action": 8, "agent": 4,
        "policy": 4, "planning": 5, "sim-to-real": 7, "reinforcement learning": 5,
    },
    "Recognition, Detection & Segmentation": {
        "classification": 5, "recognition": 6, "detection": 7, "detector": 6, "segmentation": 7,
        "semantic segmentation": 8, "instance segmentation": 8, "panoptic": 7, "mask": 4,
        "object": 2, "open-set": 5, "zero-shot": 3, "few-shot": 3, "anomaly detection": 6,
        "tracking-by-detection": 5, "localization": 4,
    },
    "Low-Level Vision & Computational Photography": {
        "super-resolution": 8, "super resolution": 8, "restoration": 7, "denoising": 6,
        "deblurring": 7, "deblur": 7, "deraining": 7, "dehazing": 7, "low-light": 7,
        "hdr": 6, "raw": 4, "isp": 6, "computational photography": 8, "image quality": 5,
        "compression": 5, "inpainting": 5, "colorization": 5, "camera": 3, "noise": 3,
    },
    "Learning, Optimization & Efficient Foundation Models": {
        "pre-training": 7, "pretraining": 7, "self-supervised": 7, "unsupervised": 4, "semi-supervised": 4,
        "training": 3, "distillation": 6, "teacher": 4, "student": 4, "optimization": 5,
        "efficient": 5, "efficiency": 5, "acceleration": 6, "compression": 5, "quantization": 7,
        "pruning": 7, "sparse": 4, "adapter": 4, "fine-tuning": 4, "finetuning": 4,
        "attention": 3, "transformer": 3, "foundation model": 5, "representation learning": 6,
        "continual": 5, "federated": 5, "test-time": 5, "domain adaptation": 5,
    },
    "Datasets, Benchmarks & Evaluation": {
        "dataset": 8, "benchmark": 8, "evaluation": 7, "metric": 6, "protocol": 4,
        "challenge": 4, "leaderboard": 5, "corpus": 5, "annotation": 4, "labels": 3,
        "large-scale dataset": 9, "survey": 5, "taxonomy": 4,
    },
    "Safety, Robustness, Privacy & Trustworthy CV": {
        "robust": 5, "robustness": 6, "adversarial": 7, "jailbreak": 8, "attack": 6,
        "defense": 6, "privacy": 7, "membership inference": 8, "watermark": 7, "bias": 6,
        "fairness": 7, "trustworthy": 7, "uncertainty": 5, "out-of-distribution": 7,
        "ood": 5, "backdoor": 7, "safety": 7, "hallucination": 5, "alignment": 4,
    },
    "Medical, Scientific, Remote-Sensing & Domain Vision": {
        "medical": 8, "clinical": 7, "mri": 8, "ct": 7, "pathology": 8, "histology": 8,
        "cell": 5, "bio": 4, "molecule": 6, "remote sensing": 8, "satellite": 7, "aerial": 6,
        "hyperspectral": 7, "agriculture": 6, "industrial": 5, "defect": 6, "traffic": 4,
        "earth observation": 8, "scientific": 4,
    },
    "Human-Centric Vision, Biometrics & Behavior": {
        "human": 6, "person": 5, "face": 7, "facial": 7, "body": 5, "hand": 5,
        "pose": 4, "gait": 7, "re-identification": 8, "reid": 7, "biometric": 8,
        "gaze": 6, "emotion": 6, "gesture": 6, "avatar": 5, "motion capture": 6,
        "talking head": 6, "human-object": 6, "hoi": 6,
    },
    "Document, OCR & Visual Information Extraction": {
        "document": 8, "ocr": 8, "scene text": 8, "text recognition": 8, "table": 6,
        "layout": 7, "chart": 5, "formula": 5, "receipt": 7, "form": 4,
        "visual information extraction": 8, "reading order": 6, "document parsing": 8,
    },
}

NOVELTY_KEYWORDS = {
    "New Representation": ["representation", "latent", "codebook", "embedding", "token", "primitive", "gaussian", "field", "structure", "decomposition"],
    "Model Architecture": ["architecture", "network", "transformer", "encoder", "decoder", "module", "adapter", "attention", "backbone"],
    "Training / Pretraining Objective": ["pre-training", "pretraining", "self-supervised", "training objective", "loss", "distillation", "fine-tuning", "curriculum", "contrastive", "reward"],
    "Data, Dataset or Synthetic-Data Engine": ["dataset", "benchmark", "synthetic", "data engine", "annotation", "corpus", "generated data", "simulation"],
    "Efficiency / Acceleration / Compression": ["efficient", "efficiency", "speed", "faster", "acceleration", "cache", "compression", "quantization", "pruning", "lightweight", "real-time", "one-step"],
    "Multimodal Fusion / Grounding": ["multimodal", "vision-language", "language", "grounding", "fusion", "text", "audio", "cross-modal"],
    "Reasoning, Planning or Agentic Control": ["reasoning", "planning", "agent", "policy", "chain", "scratchpad", "decision", "control"],
    "Editing, Control or Compositionality": ["editing", "control", "controllable", "style", "compositional", "attribute", "layout", "decompose", "layer"],
    "Geometry or Physical Prior": ["geometry", "geometric", "3d", "depth", "pose", "camera", "physics", "rendering", "calibration", "ray"],
    "Robustness, Safety or Privacy Method": ["robust", "adversarial", "privacy", "jailbreak", "attack", "defense", "watermark", "bias", "uncertainty", "safety"],
    "Evaluation, Benchmark or Metric": ["evaluation", "benchmark", "metric", "protocol", "leaderboard", "measure", "diagnose"],
    "Application or System Integration": ["system", "pipeline", "application", "framework", "deployment", "real-world", "integrated", "end-to-end"],
    "Theoretical or Analytical Insight": ["theory", "analysis", "theoretical", "principled", "proof", "bound", "investigate", "rethinking"],
}

AXIS_KEYWORDS = {
    "Accuracy / Quality": ["accuracy", "quality", "performance", "state-of-the-art", "sota", "outperform", "improve", "better"],
    "Efficiency / Speed": ["efficient", "speed", "faster", "acceleration", "real-time", "cost", "lightweight", "memory", "latency"],
    "Generalization / Robustness": ["generalization", "robust", "diverse", "domain", "out-of-distribution", "challenging", "real-world"],
    "Scalability": ["scale", "large-scale", "scalable", "long", "many", "ultra-large"],
    "Controllability / Editability": ["control", "controllable", "editing", "editability", "compositional", "attribute", "style"],
    "Temporal Consistency": ["temporal", "coherent", "consistency", "motion", "trajectory", "video"],
    "3D / Physical Consistency": ["3d", "geometry", "geometric", "pose", "depth", "multi-view", "camera", "physical"],
    "Safety / Trustworthiness": ["safety", "privacy", "adversarial", "attack", "defense", "watermark", "bias", "trustworthy"],
    "Data Efficiency": ["few-shot", "zero-shot", "data-efficient", "unlabeled", "self-supervised", "annotation"],
    "Evaluation Clarity": ["benchmark", "evaluation", "metric", "protocol", "diagnose", "measure"],
}

APPLICATION_KEYWORDS = {
    "autonomous driving": ["autonomous driving", "driving", "traffic", "vehicle"],
    "robotics": ["robot", "robotic", "embodied", "manipulation", "navigation", "humanoid"],
    "creative media": ["generation", "editing", "stylization", "avatar", "animation"],
    "medical or biological imaging": ["medical", "mri", "ct", "pathology", "histology", "cell", "bio"],
    "remote sensing": ["remote sensing", "satellite", "aerial", "earth observation", "hyperspectral"],
    "documents and OCR": ["document", "ocr", "scene text", "layout", "table", "chart"],
    "human understanding": ["human", "face", "body", "hand", "gait", "re-identification", "emotion"],
    "3D content and reconstruction": ["3d", "reconstruction", "gaussian splatting", "nerf", "novel view"],
    "foundation model training": ["foundation model", "pre-training", "pretraining", "self-supervised", "distillation"],
}


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def keyword_pattern(kw: str) -> str:
    """Match phrases as terms instead of arbitrary substrings.

    This prevents short scientific abbreviations such as ``CT`` from matching
    inside unrelated words such as ``object`` or ``architecture``.
    """
    kw = kw.lower()
    escaped = re.escape(kw)
    if re.match(r"^[a-z0-9]", kw) and re.search(r"[a-z0-9]$", kw):
        return rf"(?<![a-z0-9]){escaped}(?![a-z0-9])"
    return escaped


def score_weighted(text: str, mapping: dict[str, dict[str, int]]) -> dict[str, float]:
    scores: dict[str, float] = {}
    for label, kws in mapping.items():
        score = 0.0
        for kw, weight in kws.items():
            hits = len(re.findall(keyword_pattern(kw), text))
            if hits:
                score += weight * min(hits, 3)
        scores[label] = score
    return scores


def score_list(text: str, mapping: dict[str, list[str]]) -> dict[str, float]:
    scores: dict[str, float] = {}
    for label, kws in mapping.items():
        score = 0.0
        for kw in kws:
            hits = len(re.findall(keyword_pattern(kw), text))
            if hits:
                score += min(hits, 3)
        scores[label] = score
    return scores


def choose_top(scores: dict[str, float], default: str) -> tuple[str, str, float]:
    ordered = sorted(scores.items(), key=lambda x: (-x[1], x[0]))
    primary, pscore = ordered[0]
    secondary, sscore = (ordered[1] if len(ordered) > 1 else ("", 0.0))
    if pscore <= 0:
        return default, "", 0.35
    margin = pscore - sscore
    confidence = min(0.96, 0.45 + 0.08 * math.log1p(pscore) + 0.04 * margin)
    return primary, (secondary if sscore > 0 else ""), round(confidence, 2)


def split_sentences(text: str) -> list[str]:
    text = normalize(text)
    if not text:
        return []
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9])", text)
    return [p.strip() for p in parts if len(p.strip()) > 20]


def find_sentence(sentences: list[str], patterns: list[str]) -> str:
    for pat in patterns:
        rx = re.compile(pat, re.I)
        for sent in sentences:
            if rx.search(sent):
                return sent
    return sentences[0] if sentences else ""


def trim_sentence(sentence: str, max_len: int = 320) -> str:
    sentence = normalize(sentence)
    if len(sentence) <= max_len:
        return sentence
    return sentence[: max_len - 1].rsplit(" ", 1)[0] + "…"


def tags_from_scores(text: str, primary_area: str, secondary_area: str, novelty: str, axis: str) -> str:
    tags = []
    for candidate in [primary_area, secondary_area, novelty, axis]:
        if candidate:
            tags.append(candidate)
    extra = []
    for kw in ["diffusion", "3d", "video", "vision-language", "robotics", "autonomous driving", "segmentation", "gaussian splatting", "benchmark", "dataset", "safety", "medical", "document", "self-supervised"]:
        if kw in text:
            extra.append(kw)
    seen = []
    for t in tags + extra:
        t = t.replace(" & ", " and ")
        if t and t not in seen:
            seen.append(t)
    return "; ".join(seen[:8])


def classify(row: dict) -> dict:
    title = normalize(row.get("title", ""))
    abstract = normalize(row.get("abstract", ""))
    text = f"{title}. {abstract}".lower()
    title_text = title.lower()

    area_scores = score_weighted(text, AREA_KEYWORDS)
    # Give title hits extra influence because CVPR titles are concise topic descriptors.
    title_scores = score_weighted(title_text, AREA_KEYWORDS)
    for k, v in title_scores.items():
        area_scores[k] += 1.5 * v

    # If a paper is explicitly a dataset/benchmark, keep that visible unless another topic dominates heavily.
    if re.search(r"\b(dataset|benchmark|evaluation suite|challenge)\b", title_text):
        area_scores["Datasets, Benchmarks & Evaluation"] += 8

    primary_area, secondary_area, confidence = choose_top(area_scores, "General Computer Vision")

    novelty_scores = score_list(text, NOVELTY_KEYWORDS)
    novelty_angle, _, _ = choose_top(novelty_scores, "Application or System Integration")

    axis_scores = score_list(text, AXIS_KEYWORDS)
    improvement_axis, _, _ = choose_top(axis_scores, "Accuracy / Quality")

    application = "general computer vision"
    best_app_score = 0
    for app, kws in APPLICATION_KEYWORDS.items():
        app_score = sum(1 for kw in kws if kw in text)
        if app_score > best_app_score:
            application = app
            best_app_score = app_score

    sentences = split_sentences(abstract)
    approach_sentence = find_sentence(sentences, [r"\bwe (propose|introduce|present|develop|design)\b", r"\bour (method|approach|framework|model|system)\b", r"\bto address\b", r"\bin this paper\b"])
    evidence_sentence = find_sentence(sentences, [r"\b(outperform|achieve|improve|faster|efficient|robust|state-of-the-art|superior|reduce|increase|enable|scalable)\b", r"\bexperiments?\b"])

    approach_summary = trim_sentence(approach_sentence)
    evidence_sentence = trim_sentence(evidence_sentence)

    why = f"Targets {improvement_axis.lower()} in {primary_area.lower()} by using {novelty_angle.lower()}."
    if evidence_sentence:
        why += f" Evidence: {evidence_sentence}"
    why = trim_sentence(why, 520)

    row = dict(row)
    row.update(
        {
            "primary_area": primary_area,
            "secondary_area": secondary_area,
            "novelty_angle": novelty_angle,
            "improvement_axis": improvement_axis,
            "application_context": application,
            "approach_summary": approach_summary,
            "improvement_rationale": why,
            "evidence_sentence": evidence_sentence,
            "taxonomy_confidence": confidence,
            "research_tags": tags_from_scores(text, primary_area, secondary_area, novelty_angle, improvement_axis),
        }
    )
    return row


def main() -> None:
    with INPUT_CSV.open("r", newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    categorized = [classify(row) for row in rows]

    base_fields = list(rows[0].keys())
    new_fields = [
        "primary_area",
        "secondary_area",
        "novelty_angle",
        "improvement_axis",
        "application_context",
        "approach_summary",
        "improvement_rationale",
        "evidence_sentence",
        "taxonomy_confidence",
        "research_tags",
    ]
    fieldnames = base_fields + [f for f in new_fields if f not in base_fields]
    with OUTPUT_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(categorized)
    OUTPUT_JSON.write_text(json.dumps(categorized, indent=2, ensure_ascii=False), encoding="utf-8")

    area_counter = Counter(r["primary_area"] for r in categorized)
    novelty_counter = Counter(r["novelty_angle"] for r in categorized)
    axis_counter = Counter(r["improvement_axis"] for r in categorized)
    code_by_area = defaultdict(lambda: {"papers": 0, "with_code_or_resource": 0, "with_github": 0})
    for r in categorized:
        bucket = code_by_area[r["primary_area"]]
        bucket["papers"] += 1
        if str(r.get("code_resource_found", "")).lower() in {"true", "1", "yes"}:
            bucket["with_code_or_resource"] += 1
        if r.get("github"):
            bucket["with_github"] += 1
    stats = {
        "paper_count": len(categorized),
        "abstract_count": sum(1 for r in categorized if r.get("abstract")),
        "areas": dict(area_counter.most_common()),
        "novelty_angles": dict(novelty_counter.most_common()),
        "improvement_axes": dict(axis_counter.most_common()),
        "code_by_area": dict(sorted(code_by_area.items(), key=lambda kv: (-kv[1]["papers"], kv[0]))),
        "taxonomy_note": "Automated title+abstract taxonomy. Use as a navigation layer, not as a peer-reviewed label.",
    }
    STATS_JSON.write_text(json.dumps(stats, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"papers": len(categorized), "areas": len(area_counter), "output": str(OUTPUT_CSV)}, indent=2))


if __name__ == "__main__":
    main()
