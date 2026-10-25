import os
import re
import warnings
from pathlib import Path
import google.generativeai as genai
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from dotenv import load_dotenv

warnings.filterwarnings("ignore")
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Database disk par save hoga
qdrant = QdrantClient(path="qdrant_db")

if not qdrant.collection_exists("zentromart_kb"):
    qdrant.create_collection(
        collection_name="zentromart_kb",
        vectors_config=VectorParams(size=768, distance=Distance.COSINE),
    )

def build_index():
    kb_path = Path("kb")
    if not kb_path.exists():
        print("❌ ERROR: 'kb' folder nahi mila!")
        return
        
    md_files = list(kb_path.glob("*.md"))
    print(f"📁 {len(md_files)} files mili. Database disk par save ho raha hai...")
    
    points = []
    for doc_path in md_files:
        content = doc_path.read_text(encoding="utf-8")
        sections = re.split(r'(^##\s*\[[^\]]+\])', content, flags=re.MULTILINE)
        
        current_header = ""
        for part in sections:
            if re.match(r'^##\s*\[[^\]]+\]', part):
                current_header = part.strip()
            elif part.strip():
                chunk_text = f"{current_header}\n{part}".strip()
                match = re.search(r'\[([^\]]+)\]', current_header)
                section_id = match.group(1) if match else doc_path.stem
                
                try:
                    # Latest text-embedding-004 model
                    embedding = genai.embed_content(
                        model="models/text-embedding-004",
                        content=chunk_text
                    )["embedding"]
                    
                    points.append(PointStruct(
                        id=len(points),
                        vector=embedding,
                        payload={"text": chunk_text, "section_id": section_id}
                    ))
                except Exception:
                    pass # Agar error aaye toh ignore karein
    
    if points:
        qdrant.upsert(collection_name="zentromart_kb", points=points)
        print(f"✅ SUCCESS: {len(points)} chunks permanently disk par save ho gaye!")

def retrieve_context(query: str, k: int = 3):
    try:
        embedding = genai.embed_content(
            model="models/text-embedding-004",
            content=query
        )["embedding"]
        
        results = qdrant.query_points(
            collection_name="zentromart_kb",
            query=embedding,
            limit=k
        ).points
        
        context_text = "\n\n".join([hit.payload["text"] for hit in results])
        source_ids = [hit.payload.get("section_id", "unknown") for hit in results]
        return context_text, source_ids
    except Exception as e:
        return "", []

if __name__ == "__main__":
    build_index()