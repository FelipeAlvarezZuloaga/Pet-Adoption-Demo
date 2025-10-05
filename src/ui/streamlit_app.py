import base64
import sys
from pathlib import Path

import streamlit as st
from elasticsearch import Elasticsearch

# Path setup to import from src
ROOT_DIR = Path(__file__).resolve().parents[2]
SRC_DIR = ROOT_DIR / "src"
for p in (ROOT_DIR, SRC_DIR):
    if str(p) not in sys.path:
        sys.path.append(str(p))

from const import DEFAULT_ES_HOST, IMAGE_DIR, INDEX_NAME

# Streamlit page configuration
st.set_page_config(page_title="🐾 Pet Adoption - Demo", page_icon="🐶", layout="wide")


@st.cache_resource  # Save connection across runs
def connect_es() -> Elasticsearch:
    """Establish a connection to Elasticsearch.

    Returns:
        Elasticsearch: The Elasticsearch client instance.
    """
    es = Elasticsearch([DEFAULT_ES_HOST], verify_certs=False, ssl_show_warn=False)
    if not es.ping():
        st.error(f"❌ Could not connect to Elasticsearch at {DEFAULT_ES_HOST}")
        st.stop()
    return es


es = connect_es()


def search_pets(query_text: str, size: int = 12) -> list:
    """Search for pets in Elasticsearch based on the query text.

    Args:
        query_text (str): The text to search for.
        size (int, optional): The number of results to return. Defaults to 12.

    Returns:
        list: A list of pet records matching the query.
    """
    body = {
        "query": {
            "multi_match": {
                "query": query_text,
                "fields": [
                    "description^3",
                    "type^2",
                    "color",
                    "name",
                ],  # Search priority
                "fuzziness": "AUTO",
            }
        }
    }
    res = es.search(index=INDEX_NAME, body=body, size=size)
    return [hit["_source"] for hit in res["hits"]["hits"]]


@st.cache_data(show_spinner=False)  # Cache image loading
def load_image_b64(path: Path) -> str | None:
    """Load an image file and encode it as a base64 string.

    Args:
        path (Path): The path to the image file.

    Returns:
        str | None: The base64-encoded image string or None if loading fails.
    """
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    except Exception:
        return None


def get_pet_image_src(pet_id: str) -> str:
    """Get the image source for a pet or a placeholder if not found.

    Args:
        pet_id (str): The ID of the pet.

    Returns:
        str: The image source URL.
    """
    img_path = IMAGE_DIR / f"{pet_id}-1.jpg"
    if img_path.exists():
        b64 = load_image_b64(img_path)
        if b64:
            return f"data:image/jpeg;base64,{b64}"
    return "https://placekitten.com/400/300"


# Custom CSS for better styling
st.markdown(
    """
    <style>
    .pet-details {
        background: linear-gradient(135deg, #333, #444);
        color: #f9f9f9;
        padding: 15px 18px;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.3);
        margin-top: 10px;
        font-size: 0.95rem;
    }
    .pet-details b {
        color: #fff;
    }
    .pet-meta {
        color: #ccc;
        font-size: 0.9rem;
        margin-bottom: 6px;
    }
    .pet-desc {
        color: #eee;
        font-size: 0.92rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# App title and description
st.title("🐾 Adopt a Pet — Demo")
st.write(
    "Enter a description, browse the image grid, and click one to reveal details below."
)

query = st.text_input("🔎 Search:", placeholder='e.g. "playful ginger cat"')

# Keep track of selected image
if "selected_pet" not in st.session_state:
    st.session_state.selected_pet = None

if query:
    with st.spinner("Searching..."):
        pets = search_pets(query)

    if not pets:
        st.warning("No results found.")
    else:
        st.success("Displaying the top 12 matches 🐕🐈")

        # Create 4x3 grid layout
        num_cols = 4
        rows = [pets[i : i + num_cols] for i in range(0, len(pets), num_cols)]

        for row in rows:
            cols = st.columns(num_cols, gap="large")
            for i, pet in enumerate(row):
                pet_id = pet.get("pet_id")
                name = pet.get("name", "Unnamed")
                type_ = pet.get("type", "Unknown")
                color = pet.get("color", "Unknown")
                desc = pet.get("description", "No description available").replace(
                    "\n", "<br>"
                )
                img_src = get_pet_image_src(pet_id)

                with cols[i]:
                    # Button invisible but captures click
                    if st.button("", key=f"btn_{pet_id}"):
                        st.session_state.selected_pet = (
                            pet_id if st.session_state.selected_pet != pet_id else None
                        )

                    # Display the pet image
                    st.markdown(
                        f"""
                        <div style="
                            border-radius:12px;
                            overflow:hidden;
                            border:3px solid {'#ffb84d' if st.session_state.selected_pet == pet_id else '#eee'};
                            transition:border-color .3s;">
                            <img src="{img_src}" style="width:100%;height:230px;object-fit:cover;">
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    # Show details when selected (without breed)
                    if st.session_state.selected_pet == pet_id:
                        st.markdown(
                            f"""
                            <div class="pet-details">
                                <b>{name}</b> ({type_})<br>
                                <div class="pet-meta">🎨 <b>Color:</b> {color}</div>
                                <div class="pet-desc">{desc}</div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

else:
    st.info("👆 Type something to start your search.")
