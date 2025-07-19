import os
import time
from pathlib import Path
import uuid
import chromadb
from chromadb.config import Settings
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from chromadb import PersistentClient

# paths
REVIEWED_PATH = Path("agents/reviewed_chapter.txt")
VERSIONS_DIR = Path("agents/versions")
VERSIONS_DIR.mkdir(exist_ok=True)

# ChromaDB client setup
client = chromadb.PersistentClient(path="agents/vector_store")

embedding_fn = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
collection = client.get_or_create_collection(name="chapter_versions", embedding_function=embedding_fn)

# load the reviewed chapter
if not REVIEWED_PATH.exists():
    print("Reviewed chapter file does not exist.")
    exit()

reviewed_text = REVIEWED_PATH.read_text(encoding='utf-8')

# show summary of the chapter
print("\n Reviewed Chapter Preview:\n")
print(reviewed_text[:500] + "...\n")  # show first 500 characters

# ask for version label
note = input("Enter a label for this version (e.g., 'Post_human edit', 'final', etc.): ").strip()
timestamp = time.strftime("%Y%m%d_%H%M%S")
version_id = f"v_{timestamp}"

# save the version
version_filename = VERSIONS_DIR / f"{version_id}.txt"
version_filename.write_text(reviewed_text, encoding='utf-8')

# add to ChromaDB
collection.add(
    documents=[reviewed_text],
    metadatas=[{"version_id": version_id, "note": note, "timestamp": timestamp}],
    ids=[str(uuid.uuid4())]
)

print(f"Version saved as {version_filename}")
print("Stored in ChromaDB for future reference.")