# Formato: Registro de Decisiones

Cada vez que el equipo use el panel de usuarios sintéticos para tomar una decisión
de producto, diseño o copy, registrarla acá. Este historial sirve para:
- Saber qué decidimos y por qué
- Detectar cuándo una decisión vieja merece revisarse (cambió el contexto, llegaron datos reales)
- Cerrar el loop entre usuarios sintéticos y validación real posterior

---

## Cómo nombrar los archivos

```
decision_YYYY-MM_[tema-corto].md
```

Ejemplos:
- `decision_2026-04_onboarding-pasos.md`
- `decision_2026-05_copy-notificacion-espera.md`
- `decision_2026-Q3_priorizacion-features.md`

---

## Estructura del archivo

```markdown
# Decisión: [título corto]

- **Fecha:** YYYY-MM-DD
- **Área:** [Producto / Diseño / Copy / Marketing / Pricing]
- **Personas consultadas:** [Martín, Carlos, Ana, Diego — las que apliquen]
- **Tomada por:** [nombre o equipo]

---

## Contexto

[¿Qué estaban evaluando? ¿Cuál era la pregunta o el problema a resolver?
2-4 oraciones. Sin historia innecesaria.]

---

## Qué dijeron las personas

[Resumen de las respuestas más relevantes de cada persona consultada.
No copy-paste de la respuesta completa — solo el insight clave.]

**Martín:** [insight en 1-2 líneas]
**Carlos:** [insight en 1-2 líneas]
**Ana:** [insight en 1-2 líneas]
**Diego:** [si aplica]

---

## Decisión tomada

[Qué decidió el equipo. Una o dos oraciones directas.]

---

## Razón

[Por qué esta decisión y no otra. Qué peso tuvo el input de los usuarios sintéticos
vs otros factores (técnicos, de negocio, de tiempo).]

---

## Validación posterior

- **¿Se validó con usuarios reales?** Sí / No / Pendiente
- **Fecha de validación:** [si aplica]
- **Resultado:** [si aplica — ¿la decisión fue correcta? ¿qué cambió?]

---

## Notas

[Cualquier contexto adicional relevante para entender esta decisión en el futuro.]
```

---

## Notas sobre el uso

- Registrar decisiones **después** de tomarlas, no durante el proceso
- Si una decisión se revisó o revirtió, no borrar el archivo original — agregar una nota al final y crear un nuevo archivo con la nueva decisión
- El campo "Validación posterior" es el más importante a largo plazo: es donde se cierra el loop entre sintético y real
