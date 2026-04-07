---
description: "Índice del panel de usuarios sintéticos de Saldoar. Lista todas las personas disponibles con su segmento, volumen y estado de datos. Leer para saber qué personas están activas y cuáles están en lista de espera."
---

# Panel de Usuarios Sintéticos — Índice

---

## Personas activas

### Martín / Laura — Freelancer argentino/a
- **Archivo:** `persona_freelancer_argentino.md`
- **Prompt standalone:** `prompts/martin_freelancer.md` · `prompts/laura_freelancer.md`
- **Segmento:** Freelancer o trabajador remoto que cobra en USD y convierte a ARS
- **Volumen:** 40% del total
- **Estado de datos:** ✅ Datos reales cargados — NPS (40), Trustpilot (~25), cancelaciones (31), encuesta. Segmento más representado en verbatims.

### Carlos — Comerciante boliviano
- **Archivo:** `persona_comerciante_boliviano.md`
- **Prompt standalone:** `prompts/carlos_comerciante.md`
- **Segmento:** Dueño de negocio que compra USD para mercadería o proveedores
- **Volumen:** 30% del total
- **Estado de datos:** ⚠️ Datos parciales — fricciones transversales confirmadas, sin verbatims identificados como Carlos directamente.

### Ana — Venezolana enviando remesas
- **Archivo:** `persona_venezolano_remesas.md`
- **Prompt standalone:** `prompts/ana_remesas.md`
- **Segmento:** Emigrada venezolana que envía dinero a su familia en Venezuela
- **Volumen:** 20% del total
- **Estado de datos:** ✅ Datos reales cargados — segmento más identificable en NPS y Trustpilot. Fricciones y citas actualizadas con evidencia directa.

### Diego — Usuario crypto
- **Archivo:** `persona_usuario_crypto.md`
- **Prompt standalone:** `prompts/diego_crypto.md`
- **Segmento:** Usuario tech-forward que convierte USDT/BTC a moneda local
- **Volumen:** 10% del total
- **Estado de datos:** ❌ Sin verbatims directos — ningún comentario identificado como crypto. Perfil orientativo.

### Valentina — Freelancer colombiana
- **Archivo:** `persona_freelancer_colombiano.md`
- **Prompt standalone:** `prompts/valentina_freelancer.md`
- **Segmento:** Freelancer o trabajadora remota que cobra en USD y convierte a COP vía Nequi o Daviplata
- **Volumen:** parte del 10% Colombia (audiencia.md)
- **Estado de datos:** Muy limitado — 1 verbatim de Trustpilot + perfil de mercado. Enriquecer cuando haya NPS segmentado por país.

---

## Personas en lista de espera

Segmentos identificados en los datos pero sin persona creada aún.
Crear cuando haya suficiente evidencia real (NPS, entrevistas, tickets de soporte).

| Segmento | País | Señal de volumen | Criterio para crear |
|---|---|---|---|
| Usuario mexicano | México | 5% del volumen (emergente) | Cuando supere 8-10% del volumen |
| Empresa mediana | Todos | Sin datos aún | Consultas recurrentes del equipo sobre este segmento |
| Adulto mayor / no digital | Todos | Sin datos aún | Si aparece en soporte o NPS como segmento diferenciado |

---

## Prompt para el panel completo

Si querés consultar a todos a la vez: `prompts/panel_completo.md`

---

## Notas sobre el estado del panel

- Las personas están basadas en perfiles de audiencia y prueba social, **no en datos empíricos directos**.
- Cuando se carguen archivos en `/datos/nps/`, `/datos/soporte/` o `/datos/entrevistas/`, actualizar el estado de datos de cada persona y enriquecer sus citas y fricciones.
- Ver `/decisiones/` para el historial de qué decisiones se tomaron basadas en este panel.
