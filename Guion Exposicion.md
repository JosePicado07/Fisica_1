# Guión de Exposición — Física I
## Simulador de Leyes de Newton (Physics Playground)

**Fecha de exposición:** Jueves 13 de agosto de 2026
**Duración objetivo:** 10–15 minutos (repartidos entre los 4 integrantes)
**Integrantes:** Matías Lutz · Antonio Mora Blotta · José Andrés Picado Corrales · Juan Pablo Solano Esquivel

> Este guión es una guía de contenido y tiempos, **no un texto para leer palabra por palabra**. Cada integrante debe apropiarse de su parte y explicarla con sus propias palabras. Antes de la exposición: **ensayar completo al menos 2 veces** con cronómetro, y dejar el simulador abierto y probado de antemano (no confiar en que arrancará bien la primera vez en vivo).

**Preparación técnica previa (antes de entrar al salón):**
- Tener `physics_playground.py` corriendo y probado en la laptop que se usará.
- Tener el modo Newton ya seleccionado (pestaña "🧲 Fuerza Newton") para no perder tiempo buscándolo en vivo.
- Tener valores de ejemplo ya decididos de antemano (ver sugerencias en cada sección).
- Tener el informe final (PDF) y este simulador accesibles sin depender de internet.

---

## 0. Apertura (≈ 1 min) — Todo el equipo

**Quién habla:** los 4, uno a la vez, muy breve.

Cada integrante dice su nombre y su rol en el proyecto:

- **Matías Lutz** — "Investigación y documentación: planteamiento del proyecto y marco teórico."
- **Antonio Mora Blotta** — "Desarrollador principal del simulador."
- **José Andrés Picado Corrales** — "Soporte de desarrollo: pruebas, fricción y diagrama de cuerpo libre."
- **Juan Pablo Solano Esquivel** — "Investigación y documentación: análisis de resultados y conclusiones."

Uno de los cuatro (sugerido: Matías, ya que abre la siguiente sección) dice una frase de transición:
> "Hoy les mostramos un simulador interactivo de las Leyes de Newton, que desarrollamos y verificamos durante las últimas semanas. Vamos a explicar el fenómeno físico, mostrar la simulación funcionando en vivo, y cerrar con el análisis de los resultados."

---

## 1. Planteamiento y diseño — Avance 1 (≈ 2.5–3 min) — Matías Lutz

**Qué mostrar en pantalla:** portada/diapositiva simple o el documento del Avance 1 (opcional), no es obligatorio usar diapositivas.

**Contenido a cubrir:**
1. **Fenómeno físico elegido:** Dinámica — Leyes de Newton (fuerza, masa, aceleración, equilibrio, movimiento).
2. **Motivación/justificación:** permitir experimentar con las leyes de Newton sin laboratorio físico, reforzando F=m·a, diagramas de cuerpo libre y fuerza neta de forma visual e interactiva.
3. **Objetivo general:** diseñar e implementar un simulador que permita visualizar la relación entre fuerza neta, masa y aceleración.
4. **Modelo matemático (mencionar las 3 ecuaciones clave, sin entrar en el detalle de código todavía):**
   - Segunda ley de Newton: ∑F = m·a
   - Fricción cinética: fk = μk·N
   - Integración de Euler: v(t+Δt) = v(t) + a·Δt ; r(t+Δt) = r(t) + v·Δt
5. Mencionar brevemente el diagrama de cuerpo libre como herramienta central de visualización (se mostrará en vivo más adelante).

**Frase de cierre / transición a Antonio:**
> "Con ese marco teórico definido, Antonio y José Andrés van a mostrarles cómo se implementó y cómo funciona en la práctica."

**Tiempo:** apuntar a no pasar de 3 minutos — esta parte es contexto, el peso fuerte de la exposición está en la demo y el análisis.

---

## 2. Implementación y demostración en vivo — Avance 2 (≈ 4–4.5 min) — Antonio Mora Blotta (principal) + José Andrés Picado Corrales (apoyo)

Esta es la sección de mayor peso en la rúbrica (25 pts) — practicar la demo hasta que salga fluida.

### 2.1. Arquitectura técnica (Antonio, ~1 min)

**Qué decir:**
- El simulador está hecho en Python con pygame.
- Tiene dos modos seleccionables por pestañas: un modo de rebote (previo) y el modo "Fuerza Newton", que es el que responde a los objetivos del proyecto.
- El modo Newton separa la física (clase `NewtonState`, sin nada de interfaz) de la parte visual — esto permitió probar la física de forma aislada, sin necesidad de abrir la ventana gráfica cada vez.
- La física usa integración de Euler con el mismo Δt del framerate (~1/60 s), tal como se planteó en el Avance 1.

### 2.2. Demo en vivo — parte 1: F = m·a (Antonio, ~1.5 min)

**Qué hacer en pantalla:**
1. Mostrar el simulador en modo 1D, sin fricción.
2. Poner Fa = 10 N, masa = 2 kg. Iniciar. Señalar la lectura de aceleración en vivo (≈5.0 m/s²).
3. Pausar, subir la masa a 5 kg (sin tocar la fuerza), reiniciar e iniciar de nuevo. Señalar que la aceleración baja a ≈2.0 m/s² — **la misma fuerza, más masa, menos aceleración**, a=Fneta/m en vivo.
4. Señalar el diagrama de cuerpo libre: los vectores de Fa, peso (W), normal (N) y fricción (fk si está activa), y explicar que se escalan proporcionalmente a su magnitud.

### 2.3. Demo en vivo — parte 2: fricción y modo 2D (José Andrés, ~1.5 min)

**Qué hacer en pantalla:**
1. Activar la fricción, poner μk en un valor visible (p. ej. 0.25) y dejar Fa constante. Señalar en el panel derecho el mensaje que indica si "Fa>fk: acelera" o "Fa=fk: equilibrio (MRU)".
2. Quitar la fuerza aplicada (Fa=0) con el objeto en movimiento y mostrar cómo desacelera hasta detenerse limpiamente, sin rebotar de signo.
3. Cambiar a modo 2D, aplicar la fuerza con un ángulo (p. ej. 45°), e iniciar — mostrar cómo el objeto traza una trayectoria diagonal y cómo el DCL rota junto con la fuerza aplicada.
4. Mencionar brevemente las pruebas realizadas: se verificó F=m·a, MRU, MRUA, el frenado por fricción sin oscilaciones, y el comportamiento correcto al reiniciar y cambiar de modo.

**Frase de cierre / transición:**
> "Con la simulación funcionando y probada, Juan Pablo va a mostrarles qué dicen estos resultados desde el punto de vista físico."

---

## 3. Análisis de resultados y comparación teórica (≈ 2.5–3 min) — Juan Pablo Solano Esquivel

**Qué mostrar en pantalla:** el gráfico de posición vs. tiempo del simulador (curva simulada vs. curvas ideales MRU/MRUA), idealmente con el mismo caso Fa=10N, m=1kg, sin fricción usado en las pruebas.

**Contenido a cubrir:**
1. **MRU:** cuando la fuerza neta es cero, el simulador reproduce una línea perfectamente recta en el gráfico de posición — velocidad constante, sin ningún error numérico (la integración de una constante es exacta).
2. **MRUA:** con fuerza neta constante, tras 5 segundos con Fa=10N y m=1kg se obtuvo x≈124.5 m frente al valor analítico exacto de 125 m — una desviación de apenas 0.4%, explicada por el error de truncamiento propio del método de Euler, no por un error de modelado físico.
3. **Hallazgo clave sobre la fricción:** el equipo esperaba, según el planteamiento del Avance 1, que la fricción produjera una "velocidad terminal". Al implementar la fórmula exacta fk=μk·N (constante, no depende de la velocidad), se comprobó que **no hay velocidad terminal con fricción cinética pura** — la aceleración se mantiene constante mientras Fa>fk. La velocidad terminal sí aparece en el otro modo del simulador (rebote), donde la resistencia del aire depende de v² — es un contraste que ayuda a entender la diferencia entre fricción de Coulomb y arrastre aerodinámico.
4. **Modo 2D:** cuando la fuerza tiene una componente perpendicular a la velocidad inicial, la trayectoria simulada se aparta ligeramente de la curva MRUA ideal, porque la fricción se opone a la velocidad instantánea (que va rotando) y no a la dirección fija de la fuerza aplicada.

**Frase de transición:**
> "Estos resultados también nos permiten hablar de los límites del modelo que construimos."

---

## 4. Limitaciones y alcance (≈ 1.5–2 min) — Juan Pablo Solano Esquivel (continúa)

**Contenido a cubrir (elegir 3–4, no es necesario leerlas todas):**
- El método de Euler introduce un error numérico pequeño pero medible (visto en el caso MRUA).
- No se modela fricción estática: en el modelo, cualquier Fa≠0 mueve el objeto, aunque sea diminuta — en la realidad existe un umbral mínimo.
- El objeto es puntual: no hay rotación ni tamaño real.
- El plano es siempre horizontal: no se modelan planos inclinados.
- El modo Newton no tiene colisiones (a diferencia del modo rebote): el objeto puede desplazarse indefinidamente.
- El modelo es válido solo para mecánica clásica, a velocidades muy por debajo de la luz — consistente con el alcance planteado desde el Avance 1.

---

## 5. Conclusiones (≈ 1–1.5 min) — Matías Lutz o Juan Pablo (a definir según ensayo)

**Contenido a cubrir:**
1. Se cumplió el objetivo general: el simulador representa fielmente F=m·a con controles interactivos de masa, fuerza y fricción, verificado cuantitativamente con menos de 1% de error atribuible únicamente a la integración numérica.
2. Se reprodujeron correctamente los casos límite MRU y MRUA, comparando visualmente con las curvas ideales.
3. El proceso de implementación llevó a un hallazgo físico relevante no anticipado en el Avance 1: la diferencia entre fricción de Coulomb (constante) y arrastre aerodinámico (cuadrático en v) respecto a la existencia de una velocidad terminal.
4. Como mejora futura: incorporar un integrador de mayor orden (Runge-Kutta 4) para reducir el error numérico, y modelar fricción estática y planos inclinados.

**Cierre:**
> "Con esto cerramos la presentación. Quedamos atentos a sus preguntas."

---

## 6. Defensa — posibles preguntas y quién responde

Repasar esto en el ensayo; cualquier integrante debe poder responder lo básico, pero se sugiere una primera línea de respuesta por tema:

| Pregunta probable | Responde primero | Puntos clave de la respuesta |
|---|---|---|
| ¿Por qué usaron el método de Euler y no uno más preciso (RK4)? | Antonio | Simplicidad de implementación y suficiente precisión para el propósito educativo del simulador; el error medido fue de solo 0.4% en 5 s. Se identifica como mejora futura. |
| ¿Por qué no hay velocidad terminal con fricción? | Juan Pablo | fk=μk·N es constante, no depende de v; la velocidad terminal requiere una fuerza que crezca con la velocidad (como el arrastre aerodinámico del otro modo del simulador). |
| ¿Cómo decidieron los rangos de los sliders (masa, fuerza, μk)? | José Andrés | Rangos elegidos para cubrir casos pedagógicamente interesantes (desde casi sin masa hasta objetos pesados) sin volver la simulación numéricamente inestable. |
| ¿Qué pasaría si aumentan mucho el Δt? | Antonio | El error de Euler crece proporcionalmente a Δt; con pasos muy grandes la simulación se volvería visiblemente imprecisa o inestable. |
| ¿Por qué extendieron el código existente en vez de reescribirlo? | Antonio o José Andrés | El sandbox de rebote ya era funcional y correcto; extenderlo evitó duplicar trabajo y permitió reutilizar los widgets de interfaz ya probados. |
| ¿Qué mejorarían del simulador? | Cualquiera (ver sección 5) | Integrador de mayor orden, fricción estática, planos inclinados, colisiones en modo Newton. |

---

## Resumen de tiempos (objetivo: 12–13 min, dentro del rango 10–15)

| Sección | Responsable(s) | Tiempo aprox. |
|---|---|---|
| 0. Apertura | Todos | 1 min |
| 1. Planteamiento y diseño | Matías | 3 min |
| 2. Implementación y demo en vivo | Antonio + José Andrés | 4.5 min |
| 3. Análisis de resultados | Juan Pablo | 3 min |
| 4. Limitaciones | Juan Pablo | 1.5 min |
| 5. Conclusiones | Matías / Juan Pablo | 1.5 min |
| **Total** | | **~13 min** |

*(La sección de preguntas/defensa no cuenta en el tiempo de exposición formal, pero hay que estar preparados para extenderse unos minutos más.)*
