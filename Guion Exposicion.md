# Guión de Exposición — Física I
## Simulador de Leyes de Newton (Physics Playground)

**Fecha de exposición:** Jueves 13 de agosto de 2026
**Duración objetivo:** 10–15 minutos
**Integrantes:** José Andrés Picado Corrales · Matías Lutz · Antonio Mora Blotta · Juan Pablo Solano Esquivel

> **Cada integrante graba su propio clip por separado** (no es una presentación en vivo conjunta), así que este documento trae el **texto palabra por palabra** que cada quien debe decir en su video. Cada clip es independiente: empieza con tu propio saludo/presentación y cierra señalando a quién sigue, para que al unir los 4 videos en orden se sienta como una sola exposición continua.
>
> Igual pueden ajustar alguna palabra si no les sale natural al hablarlo — lo importante es no cambiar los datos ni los números (están verificados). Practiquen leyéndolo en voz alta 2–3 veces antes de grabar la toma final.

**Preparación técnica previa (antes de grabar):**
- Tener `physics_playground.py` corriendo y probado (usar `run.bat` para instalar dependencias y abrirlo directo).
- Tener el modo Newton ya seleccionado (pestaña "FUERZA NEWTON") para no perder tiempo buscándolo en cámara.
- Ensayar la secuencia de clics de tu demo (si tu parte la tiene) antes de grabar la toma final, para no dudar en video.
- Grabar en un lugar silencioso, con buena luz si es cámara, y probar el audio antes de la toma final.

**Especificaciones y proceso de envío del video:** ver [`videos/VIDEOS.md`](./videos/VIDEOS.md) en el repositorio — ahí se sube el enlace de cada clip (no el archivo, pesa demasiado) y se explica cómo editarlo desde el navegador sin instalar nada.

**Orden final de los clips al editar:** José Andrés → Matías → Antonio → Juan Pablo.

---

## Clip 1 — José Andrés Picado Corrales (≈ 3–3.5 min)
### Apertura del proyecto (diapositivas) + demo en vivo: fricción y modo 2D

Este clip abre el video. Tiene dos partes: unas diapositivas rápidas de resumen (generadas con Gamma, ver [`gamma_prompt_apertura.md`](./gamma_prompt_apertura.md)) y, sin cortar, tu demo en vivo del simulador.

### Parte A — Diapositivas (≈ 60–90 seg)

**Qué mostrar en pantalla:** las diapositivas generadas en Gamma (modo "Present" o exportadas), en pantalla completa.

> Hola, buenas tardes. Mi nombre es José Andrés Picado Corrales, y junto con mis compañeros Matías Lutz, Antonio Mora Blotta y Juan Pablo Solano Esquivel, desarrollamos para el curso de Física I un simulador interactivo de las Leyes de Newton.
>
> [**Aquí narras siguiendo tus diapositivas de Gamma:** el problema que resolvimos, qué construimos —un simulador con dos modos, uno de rebote y uno de Fuerza Newton—, cómo está hecho por encima, y los roles de cada integrante. Mantenlo breve, esto es solo el resumen antes de entrar en detalle.]
>
> Ya con esa idea general, vamos a ver el simulador funcionando en vivo.

### Parte B — Demo en vivo: fricción cinética y modo 2D (≈ 2 min)

**Qué mostrar en pantalla:** grabación de pantalla completa (`Win + Alt + R`), sin cortar desde las diapositivas. Preparar antes: modo 1D, fricción activada, μk = 0.25, Fa = 15 N.

> Mi parte en el desarrollo fue apoyar la implementación, sobre todo las pruebas, la fricción y el diagrama de cuerpo libre. Les muestro eso ahora.
>
> [**Mostrar el simulador en pantalla completa, pestaña Fuerza Newton, fricción ya activada en 0.25.**] Aquí tengo la fricción activada, con un coeficiente de 0.25. Fíjense en este mensaje del panel derecho: nos dice si la fuerza aplicada es mayor, menor o igual a la fricción. Cuando Fa es mayor que la fricción, el objeto acelera de forma constante — no se frena solo, porque la fricción cinética no depende de la velocidad, solo depende de la normal y de mu-k.
>
> Ahora, con el objeto en movimiento, le voy a quitar la fuerza aplicada. [**Bajar Fa a 0 mientras el objeto se mueve.**] Miren cómo desacelera de forma constante hasta detenerse completamente, sin rebotar ni oscilar — eso lo probamos a fondo en el código para asegurarnos de que no hubiera errores numéricos ahí.
>
> Por último, les muestro el modo 2D. [**Clic en el botón 2D, poner el ángulo de Fa en 45 grados, iniciar.**] Ahora la fuerza tiene un ángulo, y el objeto traza una trayectoria diagonal. Noten cómo el diagrama de cuerpo libre rota junto con la dirección de la fuerza aplicada, en tiempo real.
>
> Con esta vista general del simulador funcionando, le paso la palabra a Matías, que les va a explicar con más detalle la teoría detrás de todo esto.

**Duración estimada, sin contar diapositivas ni pausas de demo:** ~1 min 45 seg de narración + tiempo de slides y demo.

---

## Clip 2 — Matías Lutz (≈ 3 min)
### Marco teórico en detalle

**Qué mostrar en pantalla:** tu cara (cámara), o el documento del Avance 1 / el informe si preferís mostrar texto mientras hablás.

> Hola, soy Matías Lutz. Mi parte en el equipo fue la investigación y documentación: el planteamiento del proyecto y el marco teórico, que les voy a explicar con más detalle.
>
> El fenómeno físico que elegimos trabajar fue la dinámica de Newton: la relación entre fuerza, masa, aceleración, y cómo estos conceptos producen equilibrio o movimiento. Elegimos este tema porque nos permitía construir algo interactivo, donde uno pudiera realmente experimentar con las leyes de Newton sin necesidad de un laboratorio físico.
>
> La motivación detrás del proyecto es reforzar, de forma visual, tres ideas centrales: el diagrama de cuerpo libre, el concepto de fuerza neta, y la relación fuerza-masa-aceleración, es decir, F igual a m por a. Nuestro objetivo general fue diseñar e implementar un simulador que permitiera visualizar en tiempo real cómo cambia la aceleración de un objeto cuando se modifica la fuerza neta o la masa.
>
> Para lograrlo, el simulador se apoya en tres ecuaciones principales. La primera es la segunda ley de Newton: la sumatoria de fuerzas es igual a masa por aceleración. La segunda es la fórmula de la fricción cinética: fk es igual a mu-k, el coeficiente de fricción, multiplicado por la fuerza normal. Y la tercera es el método de integración numérica que usamos para calcular el movimiento paso a paso, llamado método de Euler: en cada instante, la velocidad nueva es la velocidad anterior más la aceleración por el paso de tiempo, y la posición nueva es la posición anterior más la velocidad por ese mismo paso de tiempo.
>
> Una herramienta central del simulador es el diagrama de cuerpo libre, que dibuja todas las fuerzas que actúan sobre el objeto como vectores, en tiempo real — ya se los mostró José Andrés hace un momento.
>
> Con ese marco teórico definido, le paso la palabra a Antonio, que les va a mostrar la arquitectura técnica y una demostración de la segunda ley de Newton en acción.

**Duración estimada leyendo a ritmo normal:** ~2 min 40 seg.

---

## Clip 3 — Antonio Mora Blotta (≈ 2.5 min)
### Arquitectura técnica + demo en vivo de F = m·a

**Qué mostrar en pantalla:** grabación de pantalla completa (`Win + Alt + R`) con el simulador ya abierto en la pestaña "FUERZA NEWTON", modo 1D, sin fricción activada.

**Preparar antes de grabar:** masa en 2 kg, fuerza aplicada (Fa) en 10 N, fricción desactivada.

> Hola, soy Antonio Mora Blotta, y fui el desarrollador principal del simulador. Les voy a mostrar la arquitectura técnica y después una demostración en vivo de la segunda ley de Newton.
>
> El simulador está hecho en Python, usando la librería pygame. Tiene dos modos, que se seleccionan con las pestañas de arriba: un modo de rebote, que ya existía de un proyecto anterior, y el modo Fuerza Newton, que es el que construimos específicamente para responder a los objetivos de este proyecto — el que ya les mostró José Andrés.
>
> Internamente, el modo Newton separa completamente la física de la interfaz: toda la lógica de fuerzas, aceleración, velocidad y posición vive en una clase que no depende para nada de la ventana gráfica. Eso nos permitió probar la física de forma aislada y automatizada antes de siquiera preocuparnos por cómo se veía en pantalla. Para el cálculo del movimiento usamos integración de Euler, con el mismo paso de tiempo del framerate, aproximadamente un sesentavo de segundo, tal como lo planteamos en el Avance uno.
>
> Ahora sí, vamos a la demostración. [**Mostrar el simulador en pantalla completa, modo 1D, sin fricción.**] Como ven, tengo la fuerza aplicada en 10 newtons y la masa en 2 kilogramos. Le doy iniciar. [**Clic en Iniciar.**] Fíjense en el panel de la derecha: la aceleración marca 5 metros por segundo al cuadrado. Eso es exactamente lo que predice la fórmula: 10 newtons entre 2 kilogramos, da 5.
>
> Ahora voy a pausar [**Clic en Pausar**], y sin tocar la fuerza, voy a subir la masa a 5 kilogramos [**Mover el slider de masa a 5**]. Reinicio [**Clic en Reset**] e inicio de nuevo [**Clic en Iniciar**]. Miren cómo cambió la aceleración: ahora marca 2 metros por segundo al cuadrado. Misma fuerza, más masa, menos aceleración — la relación inversa de a igual fuerza neta entre masa, en tiempo real.
>
> Con la simulación funcionando y probada, le paso la palabra a Juan Pablo, que les va a explicar qué dicen estos resultados desde el punto de vista físico.

**Duración estimada leyendo a ritmo normal, sin contar las pausas de la demo:** ~2 min 15 seg + tiempo de demo.

---

## Clip 4 — Juan Pablo Solano Esquivel (≈ 4.5–5 min)
### Análisis de resultados, limitaciones y conclusiones

**Qué mostrar en pantalla:** el gráfico de posición vs. tiempo del simulador (curva simulada vs. curvas ideales MRU/MRUA) — puede ser una captura de pantalla, o el informe final mostrando la Figura 1. Caso de referencia: Fa=10N, m=1kg, sin fricción.

> Hola, soy Juan Pablo Solano Esquivel. Mi parte en el equipo fue la documentación, y en esta sección les voy a compartir el análisis de resultados, las limitaciones del modelo, y las conclusiones del proyecto.
>
> Empecemos con los resultados. Cuando la fuerza neta es cero, el simulador reproduce un movimiento rectilíneo uniforme perfecto: una línea recta en el gráfico de posición, sin ningún error numérico, porque integrar una velocidad constante es matemáticamente exacto.
>
> Cuando la fuerza neta es constante y distinta de cero, probamos el caso de 10 newtons aplicados sobre 1 kilogramo, sin fricción, durante 5 segundos. El valor teórico esperado era una posición de 125 metros. El simulador nos dio 124.5 metros — una diferencia de apenas 0.4 por ciento. Esa pequeña diferencia no es un error de física, es el error numérico propio del método de integración de Euler que usamos, y lo dejamos documentado en el informe.
>
> Ahora, el hallazgo que más nos llamó la atención durante el desarrollo: en el planteamiento inicial del proyecto, esperábamos que la fricción produjera una "velocidad terminal", como cuando cae un objeto en el aire. Pero al implementar la fórmula exacta de la fricción cinética, que es constante y no depende de la velocidad, nos dimos cuenta de que eso no ocurre. Mientras la fuerza aplicada sea mayor que la fricción, la aceleración se mantiene constante indefinidamente. La velocidad terminal sí aparece, pero en el otro modo del simulador, el modo de rebote, donde la resistencia del aire sí depende de la velocidad al cuadrado. Ese contraste nos ayudó a entender mejor la diferencia real entre fricción de Coulomb y arrastre aerodinámico — algo que el planteamiento original no distinguía con tanta claridad.
>
> También notamos que en el modo 2D, cuando la fuerza tiene una componente perpendicular a la velocidad inicial, la trayectoria simulada se separa un poco de la curva ideal, porque la fricción se opone a la velocidad instantánea, que va rotando, y no a la dirección fija de la fuerza aplicada.
>
> Pasando a las limitaciones del modelo: primero, el método de Euler introduce un pequeño error numérico, como ya mencioné. Segundo, no modelamos fricción estática, así que en el simulador cualquier fuerza aplicada, por pequeña que sea, mueve el objeto — en la realidad existe un umbral mínimo antes de que algo empiece a moverse. Tercero, el objeto es puntual: no tiene rotación ni tamaño real. Y cuarto, el plano siempre es horizontal, no modelamos planos inclinados, y el modo Newton no tiene colisiones, así que el objeto se puede desplazar indefinidamente.
>
> Para cerrar, nuestras conclusiones. Cumplimos el objetivo general del proyecto: el simulador representa fielmente la relación F igual a m por a, con controles interactivos de masa, fuerza y fricción, y lo verificamos cuantitativamente con un margen de error menor al uno por ciento, atribuible únicamente a la integración numérica. Reprodujimos correctamente los dos casos límite de la cinemática, el MRU y el MRUA, comparándolos visualmente contra las curvas ideales. Y, como les comenté, el proceso de construir el simulador nos llevó a un hallazgo físico que no habíamos anticipado: la diferencia entre la fricción de Coulomb y el arrastre aerodinámico respecto a la velocidad terminal. Como mejora futura, proponemos incorporar un método de integración más preciso, como Runge-Kutta de cuarto orden, y modelar fricción estática y planos inclinados para ampliar el alcance educativo del simulador.
>
> Con esto cerramos la presentación de nuestro proyecto. Muchas gracias por su atención, y quedamos atentos a sus preguntas.

**Duración estimada leyendo a ritmo normal:** ~4 min 30 seg.

---

## Defensa — posibles preguntas y quién responde

Aunque los clips se graban por separado, todos deben poder responder preguntas en vivo el día de la exposición. Repasar esta tabla antes:

| Pregunta probable | Responde primero | Puntos clave de la respuesta |
|---|---|---|
| ¿Por qué usaron el método de Euler y no uno más preciso (RK4)? | Antonio | Simplicidad de implementación y suficiente precisión para el propósito educativo del simulador; el error medido fue de solo 0.4% en 5 s. Se identifica como mejora futura. |
| ¿Por qué no hay velocidad terminal con fricción? | Juan Pablo | fk=μk·N es constante, no depende de v; la velocidad terminal requiere una fuerza que crezca con la velocidad (como el arrastre aerodinámico del otro modo del simulador). |
| ¿Cómo decidieron los rangos de los sliders (masa, fuerza, μk)? | José Andrés | Rangos elegidos para cubrir casos pedagógicamente interesantes (desde casi sin masa hasta objetos pesados) sin volver la simulación numéricamente inestable. |
| ¿Qué pasaría si aumentan mucho el Δt? | Antonio | El error de Euler crece proporcionalmente a Δt; con pasos muy grandes la simulación se volvería visiblemente imprecisa o inestable. |
| ¿Por qué extendieron el código existente en vez de reescribirlo? | Antonio o José Andrés | El sandbox de rebote ya era funcional y correcto; extenderlo evitó duplicar trabajo y permitió reutilizar los widgets de interfaz ya probados. |
| ¿Qué mejorarían del simulador? | Cualquiera | Integrador de mayor orden, fricción estática, planos inclinados, colisiones en modo Newton. |

---

## Resumen de tiempos

| Clip | Integrante | Contenido | Tiempo aprox. |
|---|---|---|---|
| 1 | José Andrés Picado Corrales | Apertura (slides) + demo fricción y modo 2D | ~3–3.5 min |
| 2 | Matías Lutz | Marco teórico en detalle | ~3 min |
| 3 | Antonio Mora Blotta | Arquitectura + demo F=m·a | ~2.5 min |
| 4 | Juan Pablo Solano Esquivel | Análisis, limitaciones y conclusiones | ~4.5–5 min |
| **Total (video editado)** | | | **~13–15 min** |

*(Los tiempos de demo en vivo dentro de los clips 1 y 3 se suman aparte del tiempo de habla — al editar, dejar que la acción en pantalla respire un par de segundos antes de seguir hablando. Si el total se pasa de 15 min, lo primero que se puede recortar es la parte de diapositivas del Clip 1, ya que Matías cubre la teoría con más detalle después.)*

---

## Cómo grabar y enviar tu clip

1. Repasa tu texto (arriba) en voz alta un par de veces antes de la toma final.
2. Si tu parte incluye demo en vivo (clips 1 y 3): graba la pantalla completa con `Win + Alt + R` (Xbox Game Bar, viene incluido en Windows) mientras hablás y usás el simulador. Ten el simulador ya abierto y en el estado inicial correcto (ver la sección "Preparar antes de grabar" de tu clip) antes de darle a grabar.
3. Si tu parte es solo explicación (clips 2 y 4): puede ser cámara/webcam hablando directo, o pantalla mostrando el informe/gráfico mientras explicás.
4. Sube tu archivo a Google Drive y compártelo como "Cualquier persona con el enlace — Lector".
5. Agrega tu enlace en [`videos/VIDEOS.md`](./videos/VIDEOS.md) dentro del repositorio del proyecto — instrucciones detalladas ahí, incluyendo cómo hacerlo desde el navegador sin instalar nada.
