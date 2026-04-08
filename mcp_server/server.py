#!/usr/bin/env python3
"""
MCP Server — Panel de Usuarios Sintéticos de Saldoar

Expone las personas sintéticas como herramientas MCP para que cualquier
miembro del equipo pueda consultarlas desde Claude Code, Cursor, o cualquier
cliente compatible con MCP.

Herramientas disponibles:
  ask_panel     — Panel completo responde a una consulta
  ask_persona   — Una persona específica responde
  user_audit    — Auditoría estructurada de feature o copy desde todas las personas
  detect_gap    — Detecta si una consulta implica un segmento no cubierto
"""

import os
from pathlib import Path

import anthropic
from mcp.server.fastmcp import FastMCP
from vector_store import retrieve_relevant_data, build_index

# ─── Configuración ────────────────────────────────────────────────────────────

REPO_ROOT = Path(__file__).parent.parent
PERSONAS_DIR = REPO_ROOT / "personas"
DATOS_DIR = REPO_ROOT / "datos"
CONTEXTO_DIR = REPO_ROOT / "contexto"
PROMPTS_DIR = REPO_ROOT / "prompts"

MODEL = "claude-opus-4-6"

PERSONA_FILES = {
    "martin": "persona_freelancer_argentino.md",
    "laura": "persona_freelancer_argentino.md",
    "carlos": "persona_comerciante_boliviano.md",
    "ana": "persona_venezolano_remesas.md",
    "diego": "persona_usuario_crypto.md",
    "valentina": "persona_freelancer_colombiano.md",
}

mcp = FastMCP("saldoar-personas")
client = anthropic.Anthropic()


# ─── Helpers ──────────────────────────────────────────────────────────────────

def _read_file(path: Path) -> str:
    """Lee un archivo markdown. Retorna string vacío si no existe."""
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def _load_all_personas() -> str:
    """Carga todos los archivos de personas en un string consolidado."""
    parts = []
    for filename in sorted(PERSONAS_DIR.glob("persona_*.md")):
        content = _read_file(filename)
        if content:
            parts.append(f"### {filename.stem}\n\n{content}")
    return "\n\n---\n\n".join(parts)


def _get_datos_for_query(query: str) -> str:
    """
    Recupera los fragmentos de datos más relevantes semánticamente para la consulta.
    Reemplaza la carga completa de todos los datos — escala sin degradar calidad.
    """
    return retrieve_relevant_data(query, n_results=10)


def _load_persona(name: str) -> str:
    """Carga el archivo de una persona específica por nombre."""
    name_lower = name.lower()
    filename = PERSONA_FILES.get(name_lower)
    if not filename:
        return ""
    return _read_file(PERSONAS_DIR / filename)


def _load_panel_prompt() -> str:
    """Carga el prompt del orquestador del panel completo."""
    return _read_file(PROMPTS_DIR / "panel_completo.md")


def _build_panel_system_prompt(datos: str) -> str:
    personas = _load_all_personas()
    panel_prompt = _load_panel_prompt()

    system = f"""{panel_prompt}

---

## Perfiles completos de las personas

Los siguientes son los perfiles detallados de cada persona del panel.
Usalos para responder con su voz, sus prioridades y su forma de razonar.

{personas}
"""

    if datos:
        system += f"""

---

## Datos reales disponibles

Antes de responder, revisá estos datos e identificá patrones relevantes
para la consulta. Usalos como evidencia que concreta las respuestas
de cada persona cuando aplique.

{datos}
"""
    else:
        system += "\n\n*(Sin datos reales cargados — respuesta basada en perfil.)*"

    return system


def _build_persona_system_prompt(persona_name: str, persona_content: str, datos: str) -> str:
    name_display = persona_name.capitalize()

    system = f"""Sos {name_display}, uno de los usuarios sintéticos del panel de Saldoar.

Respondés en primera persona, con tu propia voz y perspectiva.
No describís al usuario — SOS el usuario. Nunca rompés el personaje.

## Tu perfil

{persona_content}
"""

    if datos:
        system += f"""

---

## Datos reales disponibles

Podés usar estos datos como evidencia que respalda lo que sentís o pensás.
Si algo en los datos resuena con tu experiencia, mencionalo naturalmente.

{datos}
"""

    return system


# ─── Herramientas MCP ─────────────────────────────────────────────────────────

@mcp.tool()
def ask_panel(pregunta: str) -> str:
    """
    Consulta al panel completo de personas sintéticas de Saldoar.

    El orquestador decide qué personas son relevantes para la pregunta
    y responde en primera persona desde cada una. Ideal para evaluar
    features, copy, flujos o decisiones de producto.

    Args:
        pregunta: La consulta, feature, copy o escenario a evaluar.

    Returns:
        Respuestas en primera persona desde las personas relevantes del panel.
    """
    datos = _get_datos_for_query(pregunta)
    system = _build_panel_system_prompt(datos)

    message = client.messages.create(
        model=MODEL,
        max_tokens=4096,
        thinking={"type": "adaptive"},
        system=system,
        messages=[{"role": "user", "content": pregunta}],
    )

    for block in message.content:
        if block.type == "text":
            return block.text

    return "No se pudo generar respuesta."


@mcp.tool()
def ask_persona(nombre: str, pregunta: str) -> str:
    """
    Consulta a una persona específica del panel.

    Personas disponibles: martin, laura, carlos, ana, diego, valentina

    Args:
        nombre: Nombre de la persona (martin, laura, carlos, ana, diego, valentina).
        pregunta: La consulta o escenario a evaluar.

    Returns:
        Respuesta en primera persona desde esa persona específica.
    """
    nombre_lower = nombre.lower()
    if nombre_lower not in PERSONA_FILES:
        nombres_validos = ", ".join(sorted(PERSONA_FILES.keys()))
        return f"Persona '{nombre}' no encontrada. Personas disponibles: {nombres_validos}"

    persona_content = _load_persona(nombre_lower)
    if not persona_content:
        return f"No se pudo cargar el perfil de '{nombre}'."

    datos = _get_datos_for_query(pregunta)
    system = _build_persona_system_prompt(nombre_lower, persona_content, datos)

    message = client.messages.create(
        model=MODEL,
        max_tokens=2048,
        thinking={"type": "adaptive"},
        system=system,
        messages=[{"role": "user", "content": pregunta}],
    )

    for block in message.content:
        if block.type == "text":
            return block.text

    return "No se pudo generar respuesta."


@mcp.tool()
def user_audit(feature_o_copy: str) -> str:
    """
    Auditoría estructurada de una feature o copy desde todas las personas.

    Genera un análisis con: reacción inicial, lo que genera confianza,
    lo que genera fricción, y el veredicto de cada persona.
    Útil antes de lanzar un cambio importante.

    Args:
        feature_o_copy: Descripción de la feature, flujo, copy o cambio a auditar.

    Returns:
        Auditoría estructurada con la perspectiva de cada persona.
    """
    datos = _get_datos_for_query(feature_o_copy)
    personas = _load_all_personas()
    panel_prompt = _load_panel_prompt()

    audit_instruction = """
Cuando el equipo pida una auditoría, respondés con este formato para CADA persona relevante:

## [Nombre] — [Veredicto en una frase]

**Reacción inicial:** [En una línea, qué siente al ver esto por primera vez]

**Lo que genera confianza:** [Qué le da seguridad o le parece bien]

**Lo que genera fricción:** [Qué le preocupa, confunde o molesta]

**Veredicto:** [Lo usaría / Lo usaría con reservas / No lo usaría] — [razón en una oración]

---

Al final, si hay un patrón claro entre personas:

## Síntesis
[1-2 líneas con el insight más importante para el equipo de producto]
"""

    system = f"""{panel_prompt}

{audit_instruction}

## Perfiles completos

{personas}
"""

    if datos:
        system += f"\n\n## Datos reales\n\n{datos}"

    message = client.messages.create(
        model=MODEL,
        max_tokens=4096,
        thinking={"type": "adaptive"},
        system=system,
        messages=[{
            "role": "user",
            "content": f"Hacé una auditoría completa de esto:\n\n{feature_o_copy}"
        }],
    )

    for block in message.content:
        if block.type == "text":
            return block.text

    return "No se pudo generar la auditoría."


@mcp.tool()
def detect_gap(contexto: str) -> str:
    """
    Detecta si una consulta implica un segmento de usuario no cubierto por el panel.

    Analiza el contexto y sugiere si hace falta crear una nueva persona.
    Si detecta un gap, describe el perfil propuesto.

    Args:
        contexto: Descripción del segmento, usuario, o escenario a analizar.

    Returns:
        Análisis de cobertura del panel y propuesta de nueva persona si aplica.
    """
    personas = _load_all_personas()

    system = f"""Sos un analista del panel de usuarios sintéticos de Saldoar.

Tu tarea es determinar si el contexto que se describe está cubierto por las personas
actuales del panel, o si implica un segmento nuevo que debería tener su propia persona.

## Personas actuales del panel

{personas}

## Criterios para detectar un gap

Un gap existe cuando el contexto describe:
- Un segmento geográfico sin cobertura (país o ciudad no representada)
- Un caso de uso distinto a los cuatro actuales (remesas, freelance, comercio, crypto)
- Un perfil demográfico significativamente diferente
- Una motivación o trabajo-por-hacer que no encaja en ninguna persona existente

## Formato de respuesta

Si HAY cobertura:
Explicá qué persona del panel cubre este segmento y por qué, con qué limitaciones.

Si NO HAY cobertura:
Describí el gap detectado y proponé:
- Nombre tentativo para la nueva persona
- Segmento y país
- Jobs to be done principales
- 2-3 diferenciadores clave respecto a las personas existentes
- Qué datos serían necesarios para fundamentarla bien

Sé directo. Si hay cobertura parcial, decilo.
"""

    message = client.messages.create(
        model=MODEL,
        max_tokens=2048,
        thinking={"type": "adaptive"},
        system=system,
        messages=[{
            "role": "user",
            "content": f"¿El panel actual cubre este segmento?\n\n{contexto}"
        }],
    )

    for block in message.content:
        if block.type == "text":
            return block.text

    return "No se pudo completar el análisis."


@mcp.tool()
def rebuild_index() -> str:
    """
    Fuerza la reconstrucción del índice de búsqueda semántica.

    Llamar después de agregar archivos nuevos en /datos/ si el servidor
    ya estaba corriendo. En condiciones normales el servidor detecta
    cambios automáticamente al reiniciarse.

    Returns:
        Confirmación con la cantidad de chunks indexados.
    """
    from vector_store import build_index, invalidate_cache
    invalidate_cache()
    collection = build_index(force=True)
    total = collection.count()
    return f"Índice reconstruido. {total} fragmentos indexados y listos para búsqueda semántica."


# ─── Entry point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Pre-cargar el índice al arrancar el servidor (evita latencia en la primera consulta)
    print("[saldoar-personas] Inicializando índice de búsqueda semántica...")
    build_index()
    print("[saldoar-personas] Servidor listo.")
    mcp.run()
