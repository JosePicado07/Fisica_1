# Simulador de Leyes de Newton — Física I

Proyecto de curso: simulador interactivo de las Leyes de Newton (fuerza, masa, aceleración, fricción, MRU/MRUA), desarrollado en Python con pygame.

**Equipo:** Matías Lutz · Antonio Mora Blotta · José Andrés Picado Corrales · Juan Pablo Solano Esquivel
**Profesor:** Kevin Eduardo Cervantes Melgar

## Contenido del repositorio

| Archivo / carpeta | Descripción |
|---|---|
| `physics_playground.py` | El simulador. Dos modos: **Rebote** (caída libre y colisiones) y **Fuerza Newton** (F=m·a, fricción, MRU/MRUA, DCL). |
| `Avance #1 Física 1.pdf` | Documento del Avance #1 (planteamiento y marco teórico). |
| `Avance Final - Física 1.md` | Informe técnico completo del Avance Final (exportar a PDF antes de entregar). |
| `Guion Exposicion.md` | Guión de la exposición oral, con tiempos y partes por integrante. |
| `figuras/` | Capturas del simulador usadas en el informe. |
| `videos/VIDEOS.md` | Enlaces a los videos de respaldo grabados por cada integrante (ver instrucciones ahí). |
| `requirements.txt` | Dependencias de Python (`pygame`). |
| `run.bat` | Doble clic para instalar dependencias y correr el simulador en Windows. |
| `gamma_prompt_apertura.md` | Prompt listo para pegar en Gamma y generar las diapositivas de apertura (clip de José Andrés). |

## Cómo correr el simulador

Requiere Python 3.11+. Las dependencias están en `requirements.txt` (solo `pygame`).

**Opción rápida (Windows, doble clic):** ejecuta `run.bat` — instala lo que falte y abre el simulador.

**Opción manual (cualquier sistema):**
```
pip install -r requirements.txt
python physics_playground.py
```

## Cómo colaborar / enviar tu parte (sin necesidad de git)

Si solo necesitas actualizar un archivo (por ejemplo, agregar el enlace de tu video en `videos/VIDEOS.md`):

1. Abre el archivo en GitHub.
2. Clic en el ícono de lápiz (✎) arriba a la derecha ("Edit this file").
3. Haz tu cambio.
4. Baja al final y da clic en **"Commit changes"**.

No necesitas instalar nada — se guarda directo en el repositorio.

## Cómo colaborar con git (para quien lo prefiera)

```
git clone <URL-del-repo>
cd Proyecto
# ...hacer cambios...
git add <archivo>
git commit -m "Descripción del cambio"
git push
```

## Estado del proyecto

- [x] Avance #1 — planteamiento y marco teórico.
- [x] Avance Final — simulador funcional (modo Fuerza Newton) + informe técnico.
- [ ] Exposición oral — 13 de agosto de 2026.
- [ ] Videos de respaldo por integrante — ver [`videos/VIDEOS.md`](./videos/VIDEOS.md).
