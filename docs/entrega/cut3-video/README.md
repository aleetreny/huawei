# Vídeo y paquete del corte 3 (mv-3)

Leah, 1 nov 2026. Interno, en español. El encargo está en [ENCARGO.md](ENCARGO.md).

## Qué se entregó

**Entregado por Alejandro el 1 nov (antes de las 24:00 UK): el paquete ligero.**

| | Paquete entregado (ligero) | Alternativa (no entregada) |
|---|---|---|
| ZIP | `~/careerlab-data/entrega-ligero/cut3/gradient-depression-mv-3-cut3.zip` (Mac de Leah) | `~/careerlab-data/entrega/cut3/gradient-depression-mv-3-cut3.zip` (Mac de Leah) |
| Tamaño | 86.255.153 bytes | 291.394.810 bytes |
| Vídeo | el original de Leah reempaquetado en `.mp4` sin recomprimir: HEVC + AAC, 1920×1080, 513,2 s (8 min 33 s) | el mismo vídeo pasado a H.264 + AAC, 1920×1080, 513,2 s |
| Contenido sin el vídeo (`content_sha256`) | `e632d7fe869a8876f965b36976fffe7f19c80f55caea6894d0b842617532a69b` | igual |

- **El contenido sin el vídeo es idéntico al paquete validado por Alejandro** (el mismo `e632d7fe…`): el Skill `mv-3` y su manifest copiados byte a byte, `docs/entrega/cut3-mv3/` como `design/` y su README.
- **Las dos versiones pasan todas las comprobaciones de `scripts/entrega/build_cut.py`**: lint sin errores, validador oficial con salida 0, inglés, ningún `TODO`, Skill y versión nombrados en los documentos, ningún título de evento y vídeo de menos de 10 minutos.
- **Riesgo conocido del entregado:** HEVC podría no abrirse en algún Windows antiguo. La versión H.264 queda en el Mac de Leah por si hiciera falta.

## Cómo se construyó (Mac de Leah)

`build_cut.py` busca el programa oficial en `~/huawei/local-runs/official-runner` y mide el vídeo con `ffprobe`. En el Mac de Leah:
- el programa oficial está en `~/techarena-career-sim`, en la versión fijada `00b084a`;
- `ffprobe` es un binario de otra arquitectura que no arranca.

Se ejecutó sin tocar el script, cambiando esas dos cosas desde fuera:

```bash
uv run python - <<'EOF'
import sys, subprocess
from pathlib import Path
H = Path.home()
sys.argv = ["build_cut.py", "--policy", "lab/policies-src/mejora/mv-3", "--cut", "cut3",
            "--design", "docs/entrega/cut3-mv3",
            "--video", str(H / "careerlab-data/entrega-ligero/cut3-video/presentation.mp4"),
            "--out", str(H / "careerlab-data/entrega-ligero")]
sys.path.insert(0, "scripts/entrega")
import build_cut
build_cut.RUNNER = H / "techarena-career-sim"
build_cut.video_seconds = lambda v: float(subprocess.run(["mdls", "-raw", "-name", "kMDItemDurationSeconds", str(v)],
                                                          capture_output=True, text=True, check=True).stdout.strip())
sys.exit(build_cut.main())
EOF
```

Vídeos:
- **ligero:** `avconvert --preset PresetPassthrough --source "Gradient Depression.mov" --output presentation.mp4`;
- **H.264:** `avconvert --preset Preset1920x1080 …`.

## Guion

| Archivo | Qué es |
|---|---|
| [speaker-notes-final.md](speaker-notes-final.md) | Guion final para las 18 diapositivas de Alejandro: 1.206 palabras, ~8,5 min, con el minuto de inicio de cada diapositiva |
| [speaker-notes-leah.md](speaker-notes-leah.md) | Versión ampliada (~9 min), con la tabla de fuentes de cada afirmación y la guía para grabar en el Mac |

Todo lo que dice el guion del Skill coincide con `lab/policies-src/mejora/mv-3/bundle/` y `docs/entrega/cut3-mv3/`. Se corrigieron dos simplificaciones:
- la protección antes de la evaluación es de Network y Output dos meses, y de Skill sólo el último mes;
- el trimestre va en una respuesta a partir del segundo.

Las cifras salen de `ENCARGO.md` §4. No se dice el puesto, que era 13 tras el corte 1 y 28 ahora.

## Relevo

1. **Hecho:** guion ampliado y guion final; paquete del corte 3 en dos versiones, las dos válidas; entregado el ligero.
2. **Datos:** los ZIP y los vídeos están fuera de Git (NORMAS §1.6), en `~/careerlab-data/entrega*/` del Mac de Leah. El vídeo original es `~/Documents/Gradient Depression.mov`.
3. **A medias:** nada.
4. **Siguiente:** juntar esta rama con `main`.
