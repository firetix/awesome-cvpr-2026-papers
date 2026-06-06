# CVPR 2026 taxonomy source notes

These notes ground the category taxonomy used for `awesome-cvpr-2026-papers`.

## Sources reviewed

1. Bohrium, “CVPR 2026 Accepted Papers: Trends, Big Tech Bets & Top Highlights.” The page reports 4,090 accepted papers and describes the shift from classic CV toward multimodal, generative, and embodied work. It states that multimodal/VLM papers grew strongly in a highlighted sample, video generation and world models rose, and classic detection/segmentation/tracking received less highlight attention. URL: https://www.bohrium.com/en/blog/research-notes/cvpr-2026-accepted-papers-highlights/
2. Paper Digest, “CVPR 2026 Papers & Highlights.” The page states CVPR 2026 has more than 4,000 papers, provides generated highlights for 500 selected papers, and links to a separate CVPR 2026 code page that lists roughly 1,000 accepted papers with public code, data, or demo links. URL: https://www.paperdigest.org/2026/04/cvpr-2026-papers-highlights/
3. CVPR 2026 virtual site, “Highlighted Papers.” The official virtual program lists 575 highlighted events and includes abstracts. Early visible examples emphasize multi-view 3D reconstruction acceleration, multi-view matching, feed-forward 4D reconstruction, scalable test-time training, omni-modality visual geometry, and 3D-aware pretraining. URL: https://cvpr.thecvf.com/virtual/2026/events/Highlights2026
4. CVPR 2026 virtual site, “2026 Award Candidates.” The official virtual program lists 74 award candidate events and includes abstracts. Visible examples include datasets for reflective/transparent/low-texture 3D reconstruction, VLM jailbreaks, code-to-style image generation, membership inference for image-generation models, fast image editing, and 3D Gaussian scene encoding. URL: https://cvpr.thecvf.com/virtual/2026/events/AwardCandidates2026

## Taxonomy implications

The category system should avoid only classical CV buckets and should make the 2026 shift explicit. It should distinguish research **area** from **improvement mechanism**, because papers often contribute to one application area through a different methodological angle. Recommended top-level areas are: vision-language and multimodal intelligence; generative image/video/audio/3D; 3D, geometry, reconstruction and neural rendering; video, motion and temporal understanding; embodied AI, robotics and autonomous driving; recognition, detection and segmentation; low-level image restoration and computational photography; learning, optimization and efficient foundation-model training; datasets, benchmarks and evaluation; safety, robustness, privacy and trustworthy CV; medical/scientific/remote-sensing and domain applications; and human-centric vision, biometrics and behavior.

Recommended novelty/improvement mechanisms are: new representation; architecture/model design; training/pretraining objective; data/dataset/synthetic-data engine; efficiency/acceleration/compression; multimodal fusion/grounding; reasoning/planning/agentic control; evaluation/benchmark/metric; robustness/generalization/safety; editing/control/compositionality; geometry/physical prior; and application/system integration.
