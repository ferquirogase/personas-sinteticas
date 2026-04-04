# Formato: Datos de NPS

## Cómo nombrar los archivos

```
nps_YYYY-MM.md         ej: nps_2026-03.md
nps_YYYY-Q[1-4].md     ej: nps_2025-Q4.md   (si es por trimestre)
```

---

## Estructura del archivo

```markdown
# NPS — [Período] (ej: Marzo 2026)

- Score general: [número]
- Respuestas totales: [número]
- Promotores: [%] | Pasivos: [%] | Detractores: [%]

---

## Respuestas abiertas — Promotores (score 9-10)

**Segmento:** [nombre de persona si se puede identificar, o "sin identificar"]
> "[respuesta textual]"

**Segmento:** [...]
> "[respuesta textual]"

---

## Respuestas abiertas — Pasivos (score 7-8)

**Segmento:** [...]
> "[respuesta textual]"

---

## Respuestas abiertas — Detractores (score 0-6)

**Segmento:** [...]
> "[respuesta textual]"

---

## Temas recurrentes este período

- [Tema 1]: [N] menciones — [promotor / pasivo / detractor]
- [Tema 2]: [N] menciones — [promotor / pasivo / detractor]
- [Tema 3]: [N] menciones — [promotor / pasivo / detractor]
```

---

## Notas

- Incluir respuestas abiertas completas, sin editar ni resumir
- Si no se puede identificar el segmento, dejarlo como "sin identificar"
- Los temas recurrentes ayudan al modelo a conectar patrones entre períodos
- Agregar un archivo nuevo por período, no sobreescribir el anterior
