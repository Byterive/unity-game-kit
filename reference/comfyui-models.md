---
title: ComfyUI model download list for 2D game art
summary: Curated, link-verified set of ComfyUI models, LoRAs, ControlNet, IP-Adapter, upscalers and nodes for making 2D game art on an RTX 3060 12 GB.
keywords: [comfyui, sdxl, flux.2 klein, z-image, lora, controlnet, ip-adapter, upscaler, licenses, game art]
status: draft
updated: 2026-10-18
---

# ComfyUI models for 2D game art (RTX 3060 12 GB, 32 GB RAM)

Every link below was opened on 2026-10-18. Sizes are from the Hugging Face or Civitai file listings. SDXL (6-7 GB per checkpoint) is the main workhorse at 12 GB. Two newer models also fit: FLUX.2 [klein] 4B and Z-Image Turbo. Both are Apache 2.0, so their outputs are fine for a game you sell. Paths are relative to the ComfyUI Desktop models folder, by default under `%LOCALAPPDATA%\Comfy-Desktop\ComfyUI-Shared`. ComfyUI reads both `models/diffusion_models` and the older name `models/unet`.

## Start here (8 files, about 29 GB)

| Name | Type | Folder | Size | Link | Why |
|---|---|---|---|---|---|
| Juggernaut XL Ragnarok (`JuggernautXL_Ragnarok_ByRunDiffusion.safetensors`) | SDXL checkpoint | models/checkpoints | 6.62 GB | [Civitai](https://civitai.com/models/133005/juggernaut-xl) | Strongest all-round SDXL model. Good at glossy, rendered gems and backgrounds. VAE is baked in. |
| DynaVision XL 0.6.1.0 (`DynaVisionXL_0.6.1.0.fp16.safetensors`) | SDXL checkpoint | models/checkpoints | 6.46 GB | [Civitai](https://civitai.com/models/122606) | Stylized "3D cartoon" look that suits chunky puzzle blocks and chess pieces. Do not use the refiner with it. |
| SDXL-Lightning 8-step LoRA (`sdxl_lightning_8step_lora.safetensors`) | LoRA (speed) | models/loras | 394 MB | [HF ByteDance](https://huggingface.co/ByteDance/SDXL-Lightning/tree/main) | Makes any SDXL finetune run in 8 steps: Euler + sgm_uniform, CFG 1. Use it for fast batch exploration. |
| ControlNet Union SDXL ProMax (`diffusion_pytorch_model_promax.safetensors`, rename e.g. `xinsir-union-promax-sdxl.safetensors`) | ControlNet | models/controlnet | 2.51 GB | [HF xinsir](https://huggingface.co/xinsir/controlnet-union-sdxl-1.0/tree/main) | One file covers canny, depth and lineart. Use it to lock chess-piece silhouettes and block shapes. Apache 2.0. |
| FLUX.2 [klein] 4B distilled fp8 (`flux-2-klein-4b-fp8.safetensors`) | Diffusion model | models/diffusion_models | 4.07 GB | [HF BFL](https://huggingface.co/black-forest-labs/FLUX.2-klein-4b-fp8/tree/main) | Newer model with much better prompt following. Runs in 4 steps. BFL lists it for a 3060 12 GB + 32 GB RAM. Apache 2.0. May need a Hugging Face login and accepting the terms. |
| Qwen3-4B text encoder (`qwen_3_4b.safetensors`) | Text encoder | models/text_encoders | 8.04 GB | [HF Comfy-Org flux2-klein-4B](https://huggingface.co/Comfy-Org/flux2-klein-4B/tree/main/split_files/text_encoders) | Required by klein 4B. Z-Image lists the same filename at the same size, so you probably only need one copy. Check the hash to be sure. |
| FLUX.2 VAE (`flux2-vae.safetensors`) | VAE | models/vae | 336 MB | [HF Comfy-Org flux2-dev](https://huggingface.co/Comfy-Org/flux2-dev/tree/main/split_files/vae) | Required by klein. |
| RealESRGAN x4plus anime 6B (`RealESRGAN_x4plus_anime_6B.pth`) | Upscaler | models/upscale_models | ~18 MB | [GitHub release v0.2.2.4](https://github.com/xinntao/Real-ESRGAN/releases) | Clean edges on flat and illustrated art. BSD-3, so it is safe for commercial use. |

Custom nodes to install with ComfyUI Manager (ComfyUI Desktop already includes the Manager, so there is nothing to install for it):

- [comfyui_controlnet_aux](https://github.com/Fannovel16/comfyui_controlnet_aux): Canny, Depth Anything and Lineart preprocessors. It downloads its own small models on first use.
- [ComfyUI_IPAdapter_plus](https://github.com/cubiq/ComfyUI_IPAdapter_plus): only if you add IP-Adapter (see Optional). It has been in maintenance-only mode since 2025-04-14.
- [ComfyUI-GGUF](https://github.com/city96/ComfyUI-GGUF): only if you use the FLUX.1 or Qwen-Image GGUF files. It adds the "Unet Loader (GGUF)" and "CLIPLoader (gguf)" nodes.

## Optional

| Name | Type | Folder | Size | Link | Why / note |
|---|---|---|---|---|---|
| Z-Image Turbo bf16 (`z_image_turbo_bf16.safetensors`) | Diffusion model | models/diffusion_models | 12.3 GB | [HF Comfy-Org](https://huggingface.co/Comfy-Org/z_image_turbo/tree/main/split_files/diffusion_models) | Apache 2.0, 8-step, renders text well. It is larger than 12 GB VRAM, so ComfyUI offloads part of it to RAM and it runs slower. An `int8_convrot` file (6.2 GB) also exists, but we have not checked whether it works on a 3060. Skip the `nvfp4` file: NVFP4 is a Blackwell-GPU format. |
| Z-Image VAE (`ae.safetensors`) | VAE | models/vae | 335 MB | [HF Comfy-Org](https://huggingface.co/Comfy-Org/z_image_turbo/tree/main/split_files/vae) | This is the FLUX.1 VAE, also used by FLUX.1 schnell/dev. Text encoder: reuse `qwen_3_4b.safetensors`. A lighter `qwen_3_4b_fp8_mixed` (5.63 GB) is in the same [repo](https://huggingface.co/Comfy-Org/z_image_turbo/tree/main/split_files/text_encoders). |
| Animagine XL 4.0 (`animagine-xl-4.0.safetensors`; an `-opt` file is also listed) | SDXL checkpoint | models/checkpoints | 6.94 GB | [HF cagliostrolab](https://huggingface.co/cagliostrolab/animagine-xl-4.0) | Flat, clean 2D illustration. Its anime bias can be useful for icons. OpenRAIL++, and the card says commercial use is allowed. |
| Playground v2.5 (`playground-v2.5-1024px-aesthetic.fp16.safetensors`) | SDXL-arch checkpoint | models/checkpoints | 6.94 GB | [HF playgroundai](https://huggingface.co/playgroundai/playground-v2.5-1024px-aesthetic/tree/main) | Very saturated, glossy colours. Uses an EDM sampler internally. SDXL LoRAs mostly do not transfer. Community license (see Licenses). |
| DreamShaper XL Lightning (`DreamShaperXL_Turbo-Lightning.safetensors`) | SDXL checkpoint | models/checkpoints | 6.46 GB | [Civitai](https://civitai.com/models/112902/dreamshaper-xl) | Fast all-rounder (4-6 steps). The page says the *Turbo* variant needs Stability permission for commercial use, and it is unclear whether that also covers this Lightning file. Fine for comparing, not ideal for shipped art. |
| SDXL base 1.0 (`sd_xl_base_1.0.safetensors`) | SDXL checkpoint | models/checkpoints | 6.94 GB | [HF stabilityai](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/tree/main) | Reference point only. The finetunes above beat it. |
| SDXL refiner 1.0 (`sd_xl_refiner_1.0.safetensors`) | SDXL checkpoint | models/checkpoints | 6.08 GB | [HF stabilityai](https://huggingface.co/stabilityai/stable-diffusion-xl-refiner-1.0/tree/main) | **Not worth it.** It only helps the base model, and the DynaVision page says it lowers quality. Use an upscale plus a low-denoise second pass instead. |
| SDXL VAE fp16 fix (`sdxl_vae.safetensors`) | VAE | models/vae | 335 MB | [HF madebyollin](https://huggingface.co/madebyollin/sdxl-vae-fp16-fix/tree/main) | Only for checkpoints without a baked VAE, or if you get black or NaN images in fp16. MIT. |
| FLUX.1 schnell Q5_K_S (`flux1-schnell-Q5_K_S.gguf`) | GGUF diffusion model | models/unet | 8.26 GB | [HF city96](https://huggingface.co/city96/FLUX.1-schnell-gguf/tree/main) | Apache 2.0, 4 steps. Needs `t5xxl_fp8_e4m3fn.safetensors` (4.89 GB) and `clip_l.safetensors` (246 MB) from [flux_text_encoders](https://huggingface.co/comfyanonymous/flux_text_encoders/tree/main), plus `ae.safetensors`. Q6_K (9.83 GB) also fits. |
| FLUX.1 dev Q5_K_S / Q6_K (`flux1-dev-Q5_K_S.gguf`) | GGUF diffusion model | models/unet | 8.29 / 9.86 GB | [HF city96](https://huggingface.co/city96/FLUX.1-dev-gguf/tree/main) | Best FLUX.1 quality and the largest set of LoRAs. Same encoders and VAE as schnell. The license text is mixed (see Licenses), so klein 4B is the safer pick. A T5 GGUF such as Q5_K_M (3.39 GB, [city96](https://huggingface.co/city96/t5-v1_1-xxl-encoder-gguf/tree/main)) saves RAM. |
| SD3.5 Medium (`sd3.5_medium.safetensors`) | Checkpoint (MMDiT) | models/checkpoints | 5.11 GB | [HF stabilityai (gated)](https://huggingface.co/stabilityai/stable-diffusion-3.5-medium/tree/main) | Fits easily, but has fewer finetunes and LoRAs. Needs `clip_g` (1.39 GB), `clip_l` and `t5xxl_fp8` in models/text_encoders. Stability Community License: free under $1M annual revenue. |
| Qwen-Image Q3_K_M (`qwen-image-Q3_K_M.gguf`) | GGUF diffusion model | models/unet | 9.68 GB | [HF city96](https://huggingface.co/city96/Qwen-Image-gguf/tree/main) | Apache 2.0 and excellent at text, but 20B and heavy. Needs `qwen_2.5_vl_7b_fp8_scaled.safetensors` (9.38 GB, [Comfy-Org](https://huggingface.co/Comfy-Org/Qwen-Image_ComfyUI/tree/main/split_files/text_encoders)) and `qwen_image_vae.safetensors` (254 MB). Slow on 12 GB, so not recommended. **Skip Qwen-Image 2.1**: it uses the Qwen Research License, which is non-commercial. |
| Game-Icons.net Style SDXL | LoRA | models/loras | 435 MB | [Civitai 637160](https://civitai.com/models/637160) | Flat game-UI icons. No trigger word, weight 1. Example tag `G4m31c0n5`. |
| IconsRedmond V2 (`IconsRedmondV2-Icons.safetensors`) | LoRA | models/loras | 171 MB | [HF artificialguybr](https://huggingface.co/artificialguybr/IconsRedmond-IconsLoraForSDXL-V2) | App-style icons. Trigger `icredm` (+ "ios icon app"), weight 0.7-0.8. |
| 3D Render Style XL (`3d_render_style_xl.safetensors`) | LoRA | models/loras | 85.5 MB | [HF goofyai](https://huggingface.co/goofyai/3d_render_style_xl/tree/main) | Glossy 3D-render look for gem blocks. Trigger "3d style", weight 0.7-1. Apache 2.0. |
| Supergiant Isometric Landscapes SDXL (`supgiantisosdxl-000002.safetensors`) | LoRA | models/loras | 870 MB | [Civitai 431825](https://civitai.com/models/431825) | Painterly game-concept backgrounds. Trigger `supgiantisosdxl`, weight 0.6-1. |
| IP-Adapter Plus SDXL ViT-H (`ip-adapter-plus_sdxl_vit-h.safetensors`) | IP-Adapter | models/ipadapter | 848 MB | [HF h94](https://huggingface.co/h94/IP-Adapter/tree/main/sdxl_models) | Keeps a whole set of pieces in one style by using a reference image. |
| CLIP-ViT-H image encoder (`models/image_encoder/model.safetensors`, rename to `CLIP-ViT-H-14-laion2B-s32B-b79K.safetensors`) | CLIP vision | models/clip_vision | 2.53 GB | [HF h94](https://huggingface.co/h94/IP-Adapter/tree/main/models/image_encoder) | Required by the vit-h IP-Adapter. The Unified Loader needs this exact name. |
| 4x-UltraSharp (`4x-UltraSharp.safetensors`) | Upscaler | models/upscale_models | 66.9 MB | [HF Kim2091](https://huggingface.co/Kim2091/UltraSharp/tree/main) | Popular and sharp, but licensed **CC BY-NC-SA 4.0**. Use RealESRGAN for shipped art. |
| RealESRGAN x4plus (`RealESRGAN_x4plus.pth`) | Upscaler | models/upscale_models | ~67 MB | [GitHub release v0.1.0](https://github.com/xinntao/Real-ESRGAN/releases) | General-purpose upscaler. BSD-3. |
| ComfyUI-RMBG node (BiRefNet, BiRefNet_toonOut, RMBG-2.0, BEN2) | custom_nodes | custom_nodes | models auto-fetched | [GitHub 1038lab](https://github.com/1038lab/ComfyUI-RMBG) | Background removal inside ComfyUI, as an alternative to your Python rembg step. Node code is GPL-3.0. Check each model's own license; RMBG-2.0's licence is not verified. BiRefNet_toonOut suits stylized art. |

Optional total if you take everything: about 99 GB. A sensible first add-on is Z-Image Turbo, the four LoRAs, IP-Adapter + CLIP-ViT-H, and Animagine: about 24 GB.

## Settings per checkpoint

| Checkpoint | Family | Sampler | Scheduler | Steps | CFG | Notes |
|---|---|---|---|---|---|---|
| JuggernautXL_Ragnarok | SDXL | dpmpp_2m_sde | karras | 30-40 | 3-6 | From the Civitai page. 832x1216 portrait. Few or no negatives. |
| DynaVisionXL 0.6.1.0 | SDXL | dpmpp_2m | karras | 30 | 6 | The page lists no settings, so these are SDXL defaults. No refiner. |
| + SDXL-Lightning 8-step LoRA | SDXL | euler | sgm_uniform | 8 | 1 | LoRA at 1.0 on any SDXL finetune (from ByteDance README). |
| animagine-xl-4.0 | SDXL | euler_ancestral | normal | 28 | 5 | From the HF card. 832x1216 OK. Avoid 1536+. |
| playground-v2.5 fp16 | SDXL (EDM) | dpmpp_2m | karras | 30 | 3 | Card: EDM DPM solver at guidance 3 (or EDM Euler at 5). SDXL LoRAs mostly incompatible. |
| DreamShaperXL_Turbo-Lightning | SDXL | dpmpp_sde | karras | 4-6 | 2 | From the Civitai page. Keep the first pass at 1024 px or below. |
| sd_xl_base_1.0 | SDXL | dpmpp_2m | karras | 30 | 7 | Baseline. The refiner is not worth it. |
| flux-2-klein-4b-fp8 | FLUX.2 | euler | simple | 4 | 1 | HF example: 4 steps, guidance 1.0. Distilled, so do not raise steps much. SDXL and FLUX.1 LoRAs do not apply. |
| z_image_turbo_bf16 | Z-Image (other) | res_multistep | simple | 9 | 1 | Card: 8-9 steps, guidance 0 (CFG 1 in ComfyUI), shift 3. Alternative: dpmpp_sde + beta at 5 steps. |
| flux1-schnell-Q5_K_S | FLUX.1 | euler | simple | 4 | 1 | Apache 2.0. No negative prompt. |
| flux1-dev-Q5_K_S | FLUX.1 | euler | simple | 20-25 | 1 | Use FluxGuidance 3.5 instead of CFG. Common defaults, not from the page. |
| sd3.5_medium | SD3.5 | euler | sgm_uniform | 40 | 4.5 | Steps and CFG from the card. The sampler is the kit's default. |
| qwen-image-Q3_K_M | Qwen-Image | euler | simple | 20 | 2.5 | Typical ComfyUI defaults. Not checked on this page. |

## Licenses (what matters for a sold game)

- **SDXL base/refiner, SDXL-Lightning, Animagine 4.0:** CreativeML OpenRAIL++-M. You can sell outputs, subject to the use-based restrictions.
- **Juggernaut XL:** OpenRAIL++-M plus an addendum. The Civitai page says you can sell image outputs. The older v9 HF card asks for a license only for paid API hosting.
- **DynaVision:** OpenRAIL++-M plus an addendum. The page does not cover selling images; we did not read the addendum.
- **DreamShaper XL Turbo:** commercial use needs Stability permission (Civitai page). The Lightning variant's status is unclear.
- **FLUX.2 klein 4B, Z-Image Turbo, FLUX.1 schnell, Qwen-Image (v1), ControlNet Union:** Apache 2.0. Commercial use is fine.
- **FLUX.1 dev (Non-Commercial License v1.1.1):** §2(d) says "You may use Output for any purpose (including for commercial purposes)", but §4(a) restricts data produced by the model "for any commercial or production purposes". This is ambiguous, so avoid it for shipped art or ask a lawyer. Any LoRA trained on dev inherits this. FLUX.2 klein 9B is also non-commercial.
- **Qwen-Image 2.1:** Qwen Research License, "for research or evaluation purposes only". Do not use it.
- **SD3.5 Medium:** Stability Community License. Free under $1M total annual revenue.
- **Playground v2.5:** commercial use allowed. You need a separate license only if image generation is your core product *and* you have more than 1M monthly users. You may not use outputs to improve other text-to-image models.
- **Upscalers:** 4x-UltraSharp and UltraSharpV2 are CC BY-NC-SA 4.0. RealESRGAN is BSD-3.
- **Civitai LoRAs:** licensed per model (mostly OpenRAIL++-M plus an addendum). Check each "Permissions" box before shipping.

## Sources (opened 2026-10-18)

- https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/tree/main ; https://huggingface.co/stabilityai/stable-diffusion-xl-refiner-1.0/tree/main ; https://huggingface.co/madebyollin/sdxl-vae-fp16-fix/tree/main
- https://civitai.com/models/133005/juggernaut-xl ; https://huggingface.co/RunDiffusion/Juggernaut-XL-v9 ; https://civitai.com/models/122606 ; https://civitai.com/models/112902/dreamshaper-xl ; https://huggingface.co/Lykon/dreamshaper-xl-v2-turbo
- https://huggingface.co/cagliostrolab/animagine-xl-4.0 ; https://huggingface.co/playgroundai/playground-v2.5-1024px-aesthetic (+ /tree/main, /blob/main/LICENSE.md)
- https://huggingface.co/ByteDance/SDXL-Lightning (+ /tree/main)
- https://bfl.ai/blog/flux2-klein-towards-interactive-visual-intelligence ; https://help.bfl.ai/articles/7108141705-can-i-run-or-fine-tune-flux-2-klein-locally ; https://docs.comfy.org/tutorials/flux/flux-2-klein ; https://huggingface.co/black-forest-labs/FLUX.2-klein-4b-fp8 ; https://huggingface.co/black-forest-labs/FLUX.2-klein-4B ; https://huggingface.co/Comfy-Org/flux2-klein-4B/tree/main/split_files/text_encoders ; https://huggingface.co/Comfy-Org/flux2-dev/tree/main/split_files/vae
- https://docs.comfy.org/tutorials/image/z-image/z-image-turbo ; https://huggingface.co/Tongyi-MAI/Z-Image-Turbo ; https://huggingface.co/Comfy-Org/z_image_turbo (diffusion_models, text_encoders, vae) ; https://huggingface.co/unsloth/Z-Image-Turbo-ComfyUI ; https://www.runflow.io/blog/comfyui-z-image
- https://huggingface.co/black-forest-labs/FLUX.1-dev/blob/main/LICENSE.md ; https://huggingface.co/city96/FLUX.1-dev-gguf/tree/main ; https://huggingface.co/city96/FLUX.1-schnell-gguf/tree/main ; https://huggingface.co/comfyanonymous/flux_text_encoders/tree/main ; https://huggingface.co/city96/t5-v1_1-xxl-encoder-gguf/tree/main
- https://huggingface.co/stabilityai/stable-diffusion-3.5-medium (+ /tree/main, text_encoders) ; https://huggingface.co/city96/Qwen-Image-gguf/tree/main ; https://huggingface.co/Comfy-Org/Qwen-Image_ComfyUI (text_encoders, vae) ; https://huggingface.co/Qwen/Qwen-Image-2.1 (+ LICENSE) ; https://openclawdc.com/blog/can-i-run-qwen-image-2-1-locally/
- https://civitai.com/models/637160 ; https://huggingface.co/artificialguybr/IconsRedmond-IconsLoraForSDXL-V2 (+ tree) ; https://huggingface.co/goofyai/3d_render_style_xl (+ tree) ; https://civitai.com/models/431825 ; https://civitai.com/models/2750829 (FLUX-dev crystal LoRA; rejected, non-commercial)
- https://huggingface.co/xinsir/controlnet-union-sdxl-1.0/tree/main ; https://huggingface.co/h94/IP-Adapter/tree/main/sdxl_models ; https://huggingface.co/h94/IP-Adapter/tree/main/models/image_encoder ; https://github.com/cubiq/ComfyUI_IPAdapter_plus
- https://huggingface.co/Kim2091/UltraSharp/tree/main ; https://huggingface.co/Kim2091/UltraSharpV2/tree/main ; https://openmodeldb.info/models/4x-UltraSharp ; https://github.com/xinntao/Real-ESRGAN/releases ; https://huggingface.co/AEmotionStudio/ai-upscale-models
- https://github.com/city96/ComfyUI-GGUF ; https://github.com/Fannovel16/comfyui_controlnet_aux ; https://github.com/1038lab/ComfyUI-RMBG ; https://docs.comfy.org/manager/install ; https://docs.comfy.org/installation/desktop/windows
