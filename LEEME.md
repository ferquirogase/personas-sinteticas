# Sistema de Usuarios Sintéticos — Saldoar

## Qué es esto

Un repositorio de personas simuladas por IA, fundamentadas en datos reales del producto
(NPS, soporte, entrevistas). Se usa para que el equipo pueda consultar reacciones,
fricciones y prioridades de usuarios cuando no es posible hacer investigación en vivo.

**Importante:** hasta que se carguen datos reales en `/datos/`, las respuestas son
orientativas — basadas en perfiles de audiencia, no en evidencia empírica directa.
Ver el campo "Estado de datos" en cada persona para saber el nivel de fundamentación actual.

---

## Estructura

```
usuarios-sinteticos/
  CLAUDE.md                    ← instrucciones para Claude Code (esta carpeta como repo)
  INSTRUCCIONES_CLAUDE.md      ← pegar esto en "Project instructions" de Claude Projects
  LEEME.md                     ← este archivo
  personas/
    _PLANTILLA_PERSONA.md      ← usar para crear nuevas personas
    personas.md                ← índice del panel completo
    persona_[nombre].md        ← una por segmento de usuario
  prompts/
    panel_completo.md          ← orquestador del panel (recomendado para uso general)
    martin_freelancer.md       ← Martín en modo standalone
    laura_freelancer.md        ← Laura en modo standalone (mismo segmento, voz femenina)
    carlos_comerciante.md      ← Carlos en modo standalone
    ana_remesas.md             ← Ana en modo standalone
    diego_crypto.md            ← Diego en modo standalone
  contexto/
    audiencia.md               ← segmentación, jobs to be done, casos de uso
    prueba-social.md           ← métricas de credibilidad y testimonios
  datos/
    nps/                       ← respuestas de NPS por período
    soporte/                   ← tickets y comentarios de soporte
    entrevistas/               ← transcripciones o resúmenes de entrevistas
  consultas/
    _TIPOS_DE_CONSULTA.md      ← guía de preguntas útiles con ejemplos de output
  decisiones/
    _FORMATO_DECISION.md       ← formato para registrar decisiones tomadas con el panel
```

---

## Dos formas de usar este repositorio

### Opción A — Claude Code (recomendada para el equipo técnico)

Si tenés Claude Code instalado y acceso al repo, el sistema funciona automáticamente:
el archivo `CLAUDE.md` configura el comportamiento del orquestador al abrir la carpeta.

1. Abrir la carpeta `usuarios-sinteticos/` en Claude Code
2. Escribir la consulta directamente — el sistema responde desde las personas relevantes
3. No hace falta configurar nada más

### Opción B — Claude Projects (para el equipo sin acceso al repo)

Para usar desde claude.ai sin necesidad de acceso técnico:

1. Crear un nuevo Project en Claude (`claude.ai → Projects → New Project`)
2. Copiar el contenido de `INSTRUCCIONES_CLAUDE.md` en el campo "Project instructions"
3. Subir como documentos del proyecto:
   - Todos los archivos de `/personas/` (los `persona_*.md`, no la plantilla)
   - `contexto/audiencia.md`
   - `contexto/prueba-social.md`
   - Los archivos de `/datos/` más recientes (cuando estén disponibles)
4. Compartir el Project con el equipo

**Nota sobre la Opción B:** cuando se actualicen datos o personas, hay que re-subir
los archivos modificados al Project manualmente. No se sincroniza automáticamente.

---

## Cómo mantener el sistema actualizado

- **Mensual:** agregar nuevo archivo de NPS en `/datos/nps/` (ver formato en `_FORMATO_NPS.md`)
- **Mensual:** agregar tickets de soporte relevantes en `/datos/soporte/`
- **Después de cada ronda de investigación:** agregar resumen en `/datos/entrevistas/`
- **Cuando cambie un segmento:** actualizar el archivo de persona correspondiente y el campo "Estado de datos"
- **Después de cada decisión basada en el panel:** registrar en `/decisiones/`
- **Si usás la Opción B:** re-subir los archivos modificados al Claude Project

---

## Reglas de uso para el equipo

- Usar para decisiones de diseño, priorización y copy
- NO usar para decisiones de negocio de alto riesgo (precio, pivots, eliminar features core)
- NO reemplaza hablar con usuarios reales — complementa cuando no hay acceso
- Si una respuesta se siente rara, revisar si los datos del segmento están desactualizados
- Registrar las decisiones tomadas en `/decisiones/` para cerrar el loop

---

## Personas disponibles

| Persona | Segmento | Volumen | Estado |
|---|---|---|---|
| Martín / Laura | Freelancer argentino/a | 40% | Activa — sin datos reales |
| Carlos | Comerciante boliviano | 30% | Activa — sin datos reales |
| Ana | Venezolana enviando remesas | 20% | Activa — sin datos reales |
| Diego | Usuario crypto | 10% | Activa — sin datos reales |

Ver `personas/personas.md` para el índice completo incluyendo segmentos en lista de espera.
