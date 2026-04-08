"""
Vector store para los datos del panel de personas sintéticas de Saldoar.

Indexa los archivos de /datos/ en ChromaDB con embeddings semánticos.
En cada consulta recupera solo los fragmentos más relevantes, en lugar
de cargar todo el contexto. Escala sin degradar calidad cuando los datos crezcan.

Primera ejecución: descarga el modelo de embeddings (~90MB, una sola vez).
"""

import hashlib
import json
import re
from pathlib import Path

import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

# ─── Paths ────────────────────────────────────────────────────────────────────

DATOS_DIR = Path(__file__).parent.parent / "datos"
CHROMA_DIR = Path(__file__).parent / "chroma_db"
HASH_FILE = CHROMA_DIR / "data_hash.json"
COLLECTION_NAME = "saldoar_datos"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"


# ─── Chunking ─────────────────────────────────────────────────────────────────

def _chunk_nps(content: str, source: str) -> list[dict]:
    """
    Cada respuesta NPS es un chunk independiente.
    Formato en el archivo: **Segmento:** ... + > "cita"
    """
    chunks = []
    # Captura bloque de segmento + cita
    pattern = re.compile(
        r'(\*\*Segmento:\*\*[^\n]*\n+>?\s*"[^"]+"|> "[^"]+")',
        re.MULTILINE
    )
    for match in pattern.finditer(content):
        text = match.group(0).strip()
        if len(text) > 30:
            chunks.append({"text": text, "source": source})

    # Fallback: si el regex no matchea nada, usar párrafos
    if not chunks:
        chunks = _chunk_by_paragraph(content, source)

    return chunks


def _chunk_by_section(content: str, source: str) -> list[dict]:
    """
    Divide por secciones de nivel 2 (## Tema / ## Sección).
    Útil para soporte y encuesta donde cada sección es una unidad temática.
    """
    chunks = []
    sections = re.split(r'\n(?=## )', content)
    for section in sections:
        section = section.strip()
        if len(section) > 60 and not section.startswith("#!"):
            chunks.append({"text": section, "source": source})
    return chunks if chunks else _chunk_by_paragraph(content, source)


def _chunk_by_paragraph(content: str, source: str) -> list[dict]:
    """Fallback: divide por párrafos separados por línea en blanco."""
    paragraphs = [p.strip() for p in content.split("\n\n")]
    return [
        {"text": p, "source": source}
        for p in paragraphs
        if len(p) > 60 and not p.startswith("#") and not p.startswith("---")
    ]


def _chunk_file(filepath: Path) -> list[dict]:
    """Elige la estrategia de chunking según el archivo."""
    content = filepath.read_text(encoding="utf-8")
    source = f"{filepath.parent.name}/{filepath.name}"

    if "nps" in filepath.parent.name or "trustpilot" in filepath.name:
        return _chunk_nps(content, source)
    else:
        return _chunk_by_section(content, source)


def _load_all_data_files() -> list[Path]:
    """Lista todos los archivos de datos, excluyendo los de formato (_)."""
    files = []
    for subdir in ["nps", "soporte", "entrevistas"]:
        data_dir = DATOS_DIR / subdir
        if not data_dir.exists():
            continue
        for f in sorted(data_dir.glob("*.md")):
            if not f.name.startswith("_"):
                files.append(f)
    return files


def _compute_data_hash(files: list[Path]) -> str:
    """Hash del contenido de todos los archivos de datos. Detecta cambios."""
    h = hashlib.md5()
    for f in files:
        h.update(f.name.encode())
        h.update(f.read_bytes())
    return h.hexdigest()


# ─── Index management ─────────────────────────────────────────────────────────

def _get_client() -> chromadb.PersistentClient:
    CHROMA_DIR.mkdir(exist_ok=True)
    return chromadb.PersistentClient(path=str(CHROMA_DIR))


def _index_is_fresh(current_hash: str) -> bool:
    """True si el índice existe y los datos no cambiaron desde la última indexación."""
    if not HASH_FILE.exists():
        return False
    try:
        saved = json.loads(HASH_FILE.read_text())
        return saved.get("hash") == current_hash
    except Exception:
        return False


def build_index(force: bool = False) -> chromadb.Collection:
    """
    Construye o recarga el índice de vectores.

    Si los datos no cambiaron desde la última indexación, reutiliza el índice existente.
    Si cambiaron (o force=True), rebuilds completo.

    Primera ejecución descarga el modelo de embeddings (~90MB).
    """
    files = _load_all_data_files()
    current_hash = _compute_data_hash(files)

    embed_fn = SentenceTransformerEmbeddingFunction(model_name=EMBEDDING_MODEL)
    client = _get_client()

    if not force and _index_is_fresh(current_hash):
        return client.get_collection(name=COLLECTION_NAME, embedding_function=embed_fn)

    # Rebuilds: elimina colección anterior si existe
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = client.create_collection(
        name=COLLECTION_NAME,
        embedding_function=embed_fn,
        metadata={"hnsw:space": "cosine"},
    )

    # Indexar todos los chunks
    all_chunks = []
    for filepath in files:
        all_chunks.extend(_chunk_file(filepath))

    if all_chunks:
        # ChromaDB requiere IDs únicos
        ids = [hashlib.md5(c["text"].encode()).hexdigest() for c in all_chunks]
        # Deduplicar por ID
        seen = set()
        unique = []
        for chunk, cid in zip(all_chunks, ids):
            if cid not in seen:
                seen.add(cid)
                unique.append((chunk, cid))

        collection.add(
            documents=[c["text"] for c, _ in unique],
            ids=[cid for _, cid in unique],
            metadatas=[{"source": c["source"]} for c, _ in unique],
        )

    # Guardar hash para detectar cambios futuros
    HASH_FILE.write_text(json.dumps({"hash": current_hash, "chunks": len(unique)}))

    print(f"[vector_store] Índice construido: {len(unique)} chunks de {len(files)} archivos")
    return collection


# ─── Retrieval ────────────────────────────────────────────────────────────────

_collection_cache: chromadb.Collection | None = None


def retrieve_relevant_data(query: str, n_results: int = 10) -> str:
    """
    Recupera los fragmentos de datos más relevantes semánticamente para una consulta.

    Args:
        query: La pregunta o contexto a buscar.
        n_results: Número máximo de fragmentos a recuperar.

    Returns:
        String con los fragmentos más relevantes, con su fuente indicada.
        String vacío si no hay datos indexados.
    """
    global _collection_cache

    if _collection_cache is None:
        _collection_cache = build_index()

    total = _collection_cache.count()
    if total == 0:
        return ""

    results = _collection_cache.query(
        query_texts=[query],
        n_results=min(n_results, total),
    )

    if not results["documents"] or not results["documents"][0]:
        return ""

    chunks = []
    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        source = meta.get("source", "datos")
        chunks.append(f"*[{source}]*\n{doc}")

    return "\n\n---\n\n".join(chunks)


def invalidate_cache():
    """Fuerza rebuild del índice en la próxima consulta. Llamar si se agregan datos."""
    global _collection_cache
    _collection_cache = None
    if HASH_FILE.exists():
        HASH_FILE.unlink()
