# Panel de Usuarios Sintéticos — Saldoar

![Panel de Usuarios Sintéticos — Saldoar](cover.svg)

Un sistema de personas simuladas por IA para testear hipótesis, validar copy y priorizar features cuando no hay tiempo o recursos para investigación con usuarios reales.

---

## Qué es esto

Cuando el equipo necesita saber cómo reaccionaría un usuario a un cambio, un mensaje o un flujo nuevo, normalmente hay dos opciones: esperar a tener usuarios disponibles, o asumir. Este sistema ofrece una tercera: consultarle al panel.

El panel está compuesto por cinco personas sintéticas que representan los segmentos principales de Saldoar. Cada una tiene su propio worldview, su forma de razonar y sus miedos. Cuando el equipo hace una consulta, cada persona responde en primera persona — no como analista que describe al usuario, sino como el usuario hablando.

**Lo que esto no es:** no reemplaza hablar con usuarios reales. Complementa cuando no hay acceso. Las respuestas son orientativas, no predictivas.

---

## Arquitectura

El sistema tiene separación estricta entre dos componentes. Esto es lo que lo hace escalable.

### Personas (`/personas/`) — fuente primaria

Cada persona define su **worldview completo**: quién es, qué le importa, qué le da miedo y, fundamentalmente, **cómo razona**. Esta última parte es la clave: con un patrón de razonamiento definido, la persona puede responder a cualquier situación nueva — una feature que no existe todavía, un copy hipotético, un flujo que nunca se probó — sin necesitar que alguien se haya quejado de eso antes.

Los perfiles **no cambian cuando llegan datos nuevos**. Son definiciones de worldview, no repositorios de citas.

### Datos (`/datos/`) — evidencia que calibra

Los archivos en `/datos/` contienen lo que usuarios reales dijeron: NPS, tickets de soporte, entrevistas, encuestas. Se agregan en cualquier momento sin tocar ningún perfil.

Cuando hay datos relevantes para una consulta, la persona los usa como evidencia que concreta su respuesta. Cuando no hay nada que aplique, la persona responde igual desde su worldview — con la misma validez.

```
Consulta del equipo
        ↓
Persona lee su perfil → tiene worldview + patrones de razonamiento
        ↓
Persona lee /datos/ → busca evidencia relevante (si existe)
        ↓
Responde en primera persona, como ese usuario

— — —

Nueva persona creada mañana:
  → Definís el worldview
  → Funciona con todos los datos existentes desde el día uno

Nuevos datos cargados mañana:
  → Se agregan a /datos/
  → Todas las personas los leen automáticamente
  → No se toca ningún perfil
```

**Regla de diseño que no se rompe:** los archivos de personas no contienen citas de datos ni referencias a NPS. Eso vive en `/datos/`. La persona tiene fricciones y miedos definidos desde su perfil — si los datos los confirman, los menciona al responder; si no hay datos, responde igual.

---

## Las personas del panel

| Persona | Segmento | País | Prioridades |
|---|---|---|---|
| **Martín / Laura** | Freelancer — convierte USD a ARS (PayPal, Wise) | 🇦🇷 Argentina | Velocidad, tasa clara, proceso simple |
| **Carlos** | Comerciante — compra USD para su negocio | 🇧🇴 Bolivia | Consistencia, predecibilidad, sin sorpresas |
| **Ana** | Remesas — envía dinero a su familia en Venezuela | 🇻🇪 Venezuela | Certeza de que llega, monto completo, método accesible |
| **Diego** | Crypto — convierte USDT/BTC a moneda local | 🌐 Todos | Sin KYC largo, spread transparente, proceso simple |
| **Valentina** | Freelancer — convierte USD a COP (Nequi, Daviplata) | 🇨🇴 Colombia | Claridad del proceso, compatible con Nequi |

Ver `/personas/personas.md` para el índice completo, estado de datos por persona y segmentos en lista de espera.

---

## Datos disponibles

El panel está actualmente alimentado con:

| Fuente | Archivo | Contenido |
|---|---|---|
| NPS interno | `datos/nps/nps_historico.md` | 40 respuestas con verbatim, sin segmentar por usuario |
| Trustpilot | `datos/nps/nps_trustpilot_historico.md` | ~25 comentarios públicos |
| Cancelaciones | `datos/soporte/soporte_cancelaciones.md` | 31 razones de pedidos cancelados |
| Encuesta | `datos/entrevistas/encuesta_usuarios_2026.md` | Encuesta cuantitativa de usuarios activos y ex-usuarios |

**Pendiente para mejorar la calidad:**
- Entrevistas cualitativas (3-5 por segmento) — mayor impacto en profundidad
- NPS segmentado por tipo de usuario — conecta datos con personas específicas
- Datos directos de Carlos y Diego — actualmente sin verbatims identificados

---

## Dos formas de usar este repositorio

### Opción A — Claude Code (recomendada)

1. Abrir la carpeta `usuarios-sinteticos/` en Claude Code
2. Escribir la consulta directamente — el sistema responde desde las personas relevantes
3. No hace falta configurar nada más

El archivo `CLAUDE.md` configura el comportamiento del orquestador automáticamente.

### Opción B — Claude Projects (sin instalación)

1. Crear un nuevo Project en Claude → `Projects → New Project`
2. Copiar el contenido de `INSTRUCCIONES_CLAUDE.md` en el campo *Project instructions*
3. Subir como documentos del proyecto:
   - Todos los `personas/persona_*.md`
   - `contexto/audiencia.md`
   - Los archivos de `/datos/` disponibles
4. Compartir el Project con el equipo

> Cuando se actualicen datos o personas, re-subir los archivos modificados al Project manualmente.

---

## Ejemplos de consultas

```
"¿Cómo reaccionaría cada persona a una función de pago único (sin fragmentar)?"

"Tenemos dos versiones del mensaje de confirmación de envío. ¿Cuál genera menos ansiedad?"

"Estamos pensando en agregar un paso de verificación de identidad al onboarding. ¿Qué pasa?"

"¿Qué debería decir la notificación de 'dinero en camino' para no generar ansiedad?"
```

Ver `/consultas/_TIPOS_DE_CONSULTA.md` para plantillas y ejemplos de output esperado.

---

## Estructura del repositorio

```
personas/
  _PLANTILLA_PERSONA.md            ← usar para crear personas nuevas
  personas.md                      ← índice del panel y segmentos en lista de espera
  persona_freelancer_argentino.md  → Martín / Laura
  persona_comerciante_boliviano.md → Carlos
  persona_venezolano_remesas.md    → Ana
  persona_usuario_crypto.md        → Diego
  persona_freelancer_colombiano.md → Valentina

prompts/
  panel_completo.md       ← orquestador del panel completo
  martin_freelancer.md    ← Martín standalone
  laura_freelancer.md     ← Laura standalone (misma persona, voz femenina)
  carlos_comerciante.md
  ana_remesas.md
  diego_crypto.md
  valentina_freelancer.md

datos/
  nps/
    nps_historico.md              ← NPS interno (40 respuestas)
    nps_trustpilot_historico.md   ← Comentarios Trustpilot (~25)
  soporte/
    soporte_cancelaciones.md      ← Razones de cancelación (31 registros)
  entrevistas/
    encuesta_usuarios_2026.md     ← Encuesta cuantitativa

contexto/
  audiencia.md       ← segmentación, jobs to be done, casos de uso
  prueba-social.md   ← métricas de credibilidad y testimonios

consultas/
  _TIPOS_DE_CONSULTA.md   ← guía de preguntas útiles con ejemplos

decisiones/
  _FORMATO_DECISION.md    ← formato para registrar decisiones tomadas con el panel
```

---

## Cómo agregar datos nuevos

Agregar datos **no requiere editar ningún perfil de persona**. Solo:

1. Crear el archivo en la carpeta correspondiente siguiendo el formato:
   - NPS → `datos/nps/nps_YYYY-MM.md` (ver `_FORMATO_NPS.md`)
   - Soporte → `datos/soporte/soporte_YYYY-MM.md` (ver `_FORMATO_SOPORTE.md`)
   - Entrevistas → `datos/entrevistas/entrevista_YYYY-MM.md` (ver `_FORMATO_ENTREVISTA.md`)

2. Las personas lo leen automáticamente la próxima vez que responden.

---

## Cómo agregar una persona nueva

1. Copiar `personas/_PLANTILLA_PERSONA.md` y completar el perfil — especialmente la sección **"Cómo razona"**, que es lo que le da capacidad generativa
2. Crear el prompt standalone en `/prompts/` siguiendo el formato de los existentes
3. Agregar la persona al índice en `personas/personas.md`
4. Agregar la persona a la tabla de `CLAUDE.md`

La nueva persona funciona desde el día uno con todos los datos que ya existen en `/datos/`.

---

## Límites del sistema

- **No predice comportamiento cuantitativo:** las personas pueden decir qué les preocupa o qué prefieren, pero no cuánto pagarían, su probabilidad de churn, o un NPS exacto. Eso requiere datos reales.
- **No reemplaza investigación cualitativa:** una entrevista de 30 minutos aporta profundidad que ningún perfil puede simular completamente. El panel es para cuando no hay acceso a usuarios reales.
- **La calidad de Carlos y Diego es menor:** los datos actuales no tienen verbatims identificados directamente de esos segmentos. Sus respuestas son más orientativas que las de Martín y Ana.
- **No para decisiones de alto riesgo:** cambios de precio, pivots de negocio o eliminación de features core requieren validación con usuarios reales.
