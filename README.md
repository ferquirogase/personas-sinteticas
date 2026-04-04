# Panel de Usuarios Sintéticos — Saldoar

Un sistema de personas simuladas por IA para hacer pruebas de UX, validar copy y priorizar features cuando no hay tiempo o recursos para investigación con usuarios reales.

---

## Qué es esto

Cuando el equipo necesita saber cómo reaccionaría un usuario a un cambio, un mensaje o un flujo nuevo, normalmente hay dos opciones: esperar a tener usuarios disponibles, o asumir. Este sistema ofrece una tercera opción: consultarle al panel.

El panel está compuesto por cuatro personas sintéticas que representan los segmentos principales de Saldoar. Cada una tiene su propia voz, sus prioridades y sus miedos. Cuando el equipo hace una consulta, cada persona responde en primera persona — no como analista que describe al usuario, sino como el usuario hablando.

**Lo que esto no es:** no reemplaza hablar con usuarios reales. Complementa cuando no hay acceso. Las respuestas son orientativas, no predictivas.

---

## Cómo funciona

El sistema tiene dos capas:

### Capa 1 — Datos empíricos (compartida por todas las personas)

Los archivos en `/datos/` contienen lo que los usuarios realmente dijeron: respuestas de NPS, tickets de soporte, resúmenes de entrevistas. Son la evidencia base del panel. Antes de responder cualquier consulta, el modelo revisa estos archivos e identifica los patrones relevantes: fricciones más mencionadas, elogios recurrentes, vocabulario real.

### Capa 2 — Personas (filtros interpretativos)

Cada persona procesa esa evidencia desde sus propias prioridades y miedos. Los mismos datos de NPS los lee Martín con ansiedad por la espera, Carlos con preocupación por la consistencia, y Ana con el peso emocional de lo que le llega a su familia.

```
/datos/nps/ + /datos/soporte/ + /datos/entrevistas/
              ↓  leer siempre antes de responder
      patrones reales: quejas, elogios, vocabulario
              ↓
    cada persona filtra con su propia lente
              ↓
  Martín → ansiedad por la espera
  Carlos → preocupación por la consistencia
  Ana    → peso emocional del envío
  Diego  → criterio técnico sobre spreads
```

**Cuando no hay datos cargados:** el modelo responde desde el perfil de cada persona y aclara que la respuesta es orientativa, no empírica.

---

## Las personas del panel

| Persona | Segmento | Volumen | Prioridades |
|---|---|---|---|
| **Martín / Laura** | Freelancer argentino/a — convierte USD a ARS | 40% | Velocidad, tasa clara, sin sorpresas |
| **Carlos** | Comerciante boliviano — compra USD para su negocio | 30% | Consistencia, soporte real, sin burocracia |
| **Ana** | Venezolana en el exterior — envía remesas a su familia | 20% | Certeza de que llega, monto completo, método accesible |
| **Diego** | Usuario crypto — convierte USDT/BTC a moneda local | 10% | Sin KYC largo, spread transparente, proceso simple |

Ver `/personas/personas.md` para el índice completo, incluyendo segmentos en lista de espera.

---

## Dos formas de usar este repositorio

### Opción A — Claude Code (recomendada)

Si tenés Claude Code instalado:

1. Abrir la carpeta `usuarios-sinteticos/` en Claude Code
2. Escribir la consulta directamente — el sistema responde desde las personas relevantes
3. No hace falta configurar nada más

El archivo `CLAUDE.md` configura el comportamiento del orquestador automáticamente.

### Opción B — Claude Projects (sin instalación)

Para usar desde [claude.ai](https://claude.ai) sin acceso técnico:

1. Crear un nuevo Project en Claude → `Projects → New Project`
2. Copiar el contenido de `INSTRUCCIONES_CLAUDE.md` en el campo *Project instructions*
3. Subir como documentos del proyecto:
   - Todos los `personas/persona_*.md`
   - `contexto/audiencia.md`
   - `contexto/prueba-social.md`
   - Los archivos de `/datos/` más recientes (cuando estén disponibles)
4. Compartir el Project con el equipo

> **Nota:** en la Opción B, cuando se actualicen datos o personas, hay que re-subir los archivos modificados al Project manualmente.

---

## Ejemplos de consultas

El archivo `/consultas/_TIPOS_DE_CONSULTA.md` tiene plantillas listas para usar con ejemplos de output esperado. Algunos tipos:

- **Reacción a un feature nuevo** — cómo reaccionaría cada persona al verlo por primera vez
- **Revisar un flujo o pantalla** — dónde se trabarían, qué no entenderían, si llegarían al final
- **Evaluar copy o mensajes** — qué entienden, si genera acción o confusión
- **Priorización de features** — cuál les cambiaría más el día a día
- **Fricción en onboarding** — en qué momento perderían motivación o abandonarían

---

## Estructura del repositorio

```
personas/
  _PLANTILLA_PERSONA.md      ← usar para crear nuevas personas
  personas.md                ← índice del panel y segmentos en lista de espera
  persona_freelancer_argentino.md
  persona_comerciante_boliviano.md
  persona_venezolano_remesas.md
  persona_usuario_crypto.md

prompts/
  panel_completo.md          ← orquestador del panel (uso general)
  martin_freelancer.md       ← Martín en modo standalone
  laura_freelancer.md        ← Laura en modo standalone (misma persona, voz femenina)
  carlos_comerciante.md
  ana_remesas.md
  diego_crypto.md

contexto/
  audiencia.md               ← segmentación, jobs to be done, casos de uso
  prueba-social.md           ← métricas de credibilidad y testimonios

datos/
  nps/                       ← respuestas de NPS por período
  soporte/                   ← tickets y comentarios de soporte
  entrevistas/               ← resúmenes de sesiones de investigación

consultas/
  _TIPOS_DE_CONSULTA.md      ← guía de preguntas útiles con ejemplos de output

decisiones/
  _FORMATO_DECISION.md       ← formato para registrar decisiones tomadas con el panel
```

---

## Cómo mantener el panel actualizado

El panel es tan bueno como los datos que lo alimentan. Estas son las acciones que más mejoran la calidad de las respuestas:

### Actualizaciones periódicas (mensuales)

| Qué cargar | Dónde | Formato |
|---|---|---|
| Respuestas de NPS del período | `datos/nps/nps_YYYY-MM.md` | Ver `datos/nps/_FORMATO_NPS.md` |
| Tickets de soporte relevantes | `datos/soporte/soporte_YYYY-MM.md` | Ver `datos/soporte/_FORMATO_SOPORTE.md` |
| Resúmenes de entrevistas | `datos/entrevistas/entrevista_YYYY-MM.md` | Ver `datos/entrevistas/_FORMATO_ENTREVISTA.md` |

### Después de cargar datos nuevos

Actualizar el campo `Estado de datos` en cada persona que esos datos cubran. Cambiar:

```
> Estado de datos: Sin datos reales cargados — perfil basado en audiencia.md y prueba-social.md.
```

por algo como:

```
> Estado de datos: Fundamentada en NPS Q1-2026 (89 respuestas), soporte marzo 2026 (34 tickets).
```

Esto le indica al modelo exactamente qué archivos buscar y qué tan respaldada está la persona.

### Cuando cambie algo significativo en el producto o el mercado

Si hay un cambio grande — nueva feature, cambio de precios, evento de mercado (devaluación, nueva regulación) — actualizar las fricciones y el contexto de las personas afectadas. Un perfil desactualizado puede generar respuestas que ya no reflejan la realidad del segmento.

### Después de cada decisión tomada con el panel

Registrar en `/decisiones/` usando el formato de `_FORMATO_DECISION.md`. Incluir:
- Qué se decidió
- Qué dijeron las personas
- Si la decisión se validó después con usuarios reales

Esto cierra el loop entre el panel sintético y la investigación real, y ayuda al equipo a detectar cuándo el panel acertó o no.

---

## Agregar una persona nueva

Si una consulta implica un segmento no cubierto, el sistema lo detecta y ofrece crearlo. También se puede pedir manualmente:

1. Copiar `personas/_PLANTILLA_PERSONA.md` y completar el perfil
2. Crear el prompt standalone en `/prompts/` siguiendo el formato de los existentes
3. Agregar la persona al índice en `personas/personas.md`
4. Agregar la persona a la tabla de `CLAUDE.md` y `INSTRUCCIONES_CLAUDE.md`

> **Nota:** una persona nueva sin datos reales es un perfil hipotético. Aclararlo en el campo `Estado de datos` y enriquecerlo cuando haya evidencia disponible.

---

## Límites del sistema

- **No predice comportamiento:** las personas pueden decir qué les preocupa o qué les interesa, pero no cuánto pagarían, si van a churnar, o cuál es su probabilidad de recomendar. Eso requiere datos reales.
- **No reemplaza investigación:** cuando hay acceso a usuarios reales, usarlo. El panel es para cuando no lo hay.
- **No para decisiones de alto riesgo:** precios, pivots de negocio o eliminar features core requieren validación real.
- **La calidad depende de los datos:** sin datos cargados, las respuestas son orientativas. Con datos actualizados, son mucho más confiables.
