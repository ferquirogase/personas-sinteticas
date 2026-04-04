# Formato: Datos de Soporte

## Cómo nombrar los archivos

```
soporte_YYYY-MM.md          ej: soporte_2026-03.md
soporte_tema_[nombre].md    ej: soporte_tema_onboarding.md   (si es temático)
```

---

## Estructura del archivo

```markdown
# Tickets de Soporte — [Período o Tema]

- Total de tickets incluidos: [número]
- Período cubierto: [fecha inicio] al [fecha fin]

---

## Tema: [Nombre del tema, ej: "Problemas con notificaciones"]

**Frecuencia:** [N tickets] | **Segmento predominante:** [nombre de persona o "mixto"]

**Ticket #[id o referencia]**
- Mensaje del usuario: "[texto del mensaje, sin editar]"
- Resolución: [cómo se resolvió, o "sin resolver"]

**Ticket #[id o referencia]**
- Mensaje del usuario: "[texto]"
- Resolución: [...]

---

## Tema: [Otro tema]

[mismo formato]

---

## Patrones identificados este período

- [Patrón 1]: aparece en [N] tickets, principalmente en [segmento]
- [Patrón 2]: [descripción breve]
```

---

## Qué incluir y qué no

**Incluir:**
- Mensajes textuales del usuario (sin editar)
- Tickets que revelan confusión, frustración, o workarounds
- Pedidos de features recurrentes
- Errores o bugs reportados con descripción del contexto

**No incluir:**
- Tickets de billing o cuentas (datos sensibles)
- Tickets resueltos con "era un bug puntual ya corregido" sin patrón
- Información personal identificable del usuario

---

## Notas

- Priorizar calidad sobre cantidad: 20 tickets bien seleccionados > 200 sin filtro
- Los mensajes sin editar son más valiosos que los resumidos
