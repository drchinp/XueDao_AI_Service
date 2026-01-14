from chroma_client import get_collection

col = get_collection("pedagogy_frameworks")

docs = [
    "Constructive alignment requires learning outcomes, teaching activities, and assessment to be aligned.",
    "Bloom’s Taxonomy verbs: remember, understand, apply, analyze, evaluate, create.",
    "Good learning outcomes are measurable and observable."
]

col.add(
    documents=docs,
    metadatas=[{"framework": "pedagogy"} for _ in docs],
    ids=["p1", "p2", "p3"]
)

print("Pedagogy seeded")
