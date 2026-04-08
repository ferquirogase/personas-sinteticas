#!/usr/bin/env python3
"""
MCP Server — Panel de Usuarios Sintéticos de Saldoar

No requiere API key propia. El servidor prepara el contexto (personas + datos
relevantes) y lo devuelve a Claude Code, que ejecuta la inferencia usando la
cuenta del usuario.

Herramientas disponibles:
  ask_panel     — Contexto completo del panel para responder una consulta
  ask_persona   — Contexto de una persona específica
  user_audit    — Contexto estructurado para auditoría de feature o copy
  detect_gap    — Contexto para detectar segmentos no cubiertos
  rebuild_index — Fuerza reindexación del vector store
"""

from pathlib import Path

from mcp.server.fastmcp import FastMCP
from vector_store import retrieve_relevant_data, build_index, start_watcher

# ─── Configuración ────────────────────────────────────────────────────────────

REPO_ROOT = Path(__file__).parent.parent
PERSONAS_DIR = REPO_ROOT / "personas"
PROMPTS_DIR = REPO_ROOT / "prompts"

PERSONA_FILES = {
    "martin": "persona_freelancer_argentino.md",
    "laura": "persona_freelancer_argentino.md",
    "carlos": "persona_comerciante_boliviano.md",
    "ana": "persona_venezolano_remesas.md",
    "diego": "persona_usuario_crypto.md",
    "valentina": "persona_freelancer_colombiano.md",
}

mcp = FastMCP("saldoar-personas")


# ─── Helpers ──────────────────────────────────────────────────────────────────

def _read_file(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def _load_all_personas() -> str:
    parts = []
    for filename in sorted(PERSONAS_DIR.glob("persona_*.md")):
        content = _read_file(filename)
        if content:
            parts.append(f"### {filename.stem}\n\n{content}")
    return "\n\n---\n\n".join(parts)


def _load_persona(name: str) -> str:
    filename = PERSONA_FILES.get(name.lower())
    if not filename:
        return ""
    return _read_file(PERSONAS_DIR / filename)


def _load_panel_prompt() -> str:
    return _read_file(PROMPTS_DIR / "panel_completo.md")


def _datos_section(query: str) -> str:
    datos = retrieve_relevant_data(query, n_results=10)
    if not datos:
        return "*(Sin datos reales disponibles para esta consulta — responder desde perfil.)*"
    return f"## Datos reales relevantes\n\n{datos}"


# ─── Herramientas MCP ─────────────────────────────────────────────────────────

@mcp.tool()
def ask_panel(pregunta: str) -> str:
    """
    Prepara el contexto completo del panel para responder una consulta.

    Devuelve los perfiles de todas las personas + los datos más relevantes
    para la pregunta. Claude Code usa este contexto con la cuenta del usuario
    para generar las respuestas en primera persona.

    Args:
        pregunta: La consulta, feature, copy o escenario a evaluar.

    Returns:
        Contexto completo listo para que Claude genere las respuestas del panel.
    """
    personas = _load_all_personas()
    panel_prompt = _load_panel_prompt()
    datos = _datos_section(pregunta)

    return f"""{panel_prompt}

---

## Perfiles completos de las personas

{personas}

---

{datos}

---

## Consulta del equipo

{pregunta}

---

Respondé ahora desde las personas relevantes, siguiendo el formato del prompt de arriba.
"""


@mcp.tool()
def ask_persona(nombre: str, pregunta: str) -> str:
    """
    Prepara el contexto de una persona específica para responder una consulta.

    Personas disponibles: martin, laura, carlos, ana, diego, valentina

    Args:
        nombre: Nombre de la persona (martin, laura, carlos, ana, diego, valentina).
        pregunta: La consulta o escenario a evaluar.

    Returns:
        Contexto de esa persona listo para que Claude genere su respuesta.
    """
    nombre_lower = nombre.lower()
    if nombre_lower not in PERSONA_FILES:
        nombres_validos = ", ".join(sorted(PERSONA_FILES.keys()))
        return f"Persona '{nombre}' no encontrada. Disponibles: {nombres_validos}"

    perfil = _load_persona(nombre_lower)
    if not perfil:
        return f"No se pudo cargar el perfil de '{nombre}'."

    datos = _datos_section(pregunta)
    nombre_display = nombre_lower.capitalize()

    return f"""Sos {nombre_display}, usuario sintético del panel de Saldoar.

Respondés en primera persona, con tu propia voz. No describís al usuario — SOS el usuario.
Nunca rompés el personaje.

## Tu perfil

{perfil}

---

{datos}

---

## Consulta

{pregunta}

---

Respondé ahora como {nombre_display}, en primera persona.
"""


@mcp.tool()
def user_audit(feature_o_copy: str) -> str:
    """
    Prepara el contexto para una auditoría estructurada de feature o copy.

    Devuelve instrucciones de formato + perfiles + datos relevantes.
    Claude Code genera el análisis con reacción, fricción y veredicto
    de cada persona.

    Args:
        feature_o_copy: Descripción de la feature, flujo, copy o cambio a auditar.

    Returns:
        Contexto estructurado listo para que Claude genere la auditoría.
    """
    personas = _load_all_personas()
    panel_prompt = _load_panel_prompt()
    datos = _datos_section(feature_o_copy)

    return f"""{panel_prompt}

---

## Formato de auditoría

Para CADA persona relevante, respondé con esta estructura:

### [Nombre] — [veredicto en una frase]

**Reacción inicial:** [qué siente al ver esto por primera vez]

**Lo que genera confianza:** [qué le da seguridad o le parece bien]

**Lo que genera fricción:** [qué le preocupa, confunde o molesta]

**Veredicto:** Lo usaría / Lo usaría con reservas / No lo usaría — [razón en una oración]

---

Al final, si hay un patrón claro:

### Síntesis para el equipo
[1-2 líneas con el insight más importante]

---

## Perfiles completos

{personas}

---

{datos}

---

## Qué auditar

{feature_o_copy}

---

Generá la auditoría completa ahora.
"""


@mcp.tool()
def detect_gap(contexto: str) -> str:
    """
    Prepara el contexto para detectar si una consulta implica un segmento
    no cubierto por el panel actual.

    Args:
        contexto: Descripción del segmento, usuario o escenario a analizar.

    Returns:
        Contexto listo para que Claude analice la cobertura del panel.
    """
    personas = _load_all_personas()

    return f"""Analizá si el siguiente contexto está cubierto por las personas actuales
del panel de usuarios sintéticos de Saldoar, o si implica un segmento nuevo.

## Personas actuales del panel

{personas}

## Criterios para detectar un gap

Un gap existe cuando el contexto describe:
- Un segmento geográfico sin cobertura
- Un caso de uso distinto a los actuales (remesas, freelance, comercio, crypto)
- Un perfil demográfico significativamente diferente
- Una motivación que no encaja en ninguna persona existente

## Formato de respuesta

Si HAY cobertura: explicá qué persona cubre el segmento y con qué limitaciones.

Si NO HAY cobertura: describí el gap y proponé nombre, segmento, país,
jobs to be done principales, diferenciadores clave, y qué datos harían falta.

---

## Contexto a analizar

{contexto}

---

Analizá ahora.
"""


@mcp.tool()
def rebuild_index() -> str:
    """
    Fuerza la reconstrucción del índice de búsqueda semántica.

    Útil si se agregaron archivos en /datos/ con el servidor corriendo
    y el watcher automático no los detectó.

    Returns:
        Confirmación con cantidad de chunks indexados.
    """
    from vector_store import invalidate_cache
    invalidate_cache()
    collection = build_index(force=True)
    return f"Índice reconstruido: {collection.count()} fragmentos indexados."


# ─── Entry point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("[saldoar-personas] Inicializando índice de búsqueda semántica...")
    build_index()
    start_watcher()
    print("[saldoar-personas] Servidor listo. No requiere API key propia.")
    mcp.run()
