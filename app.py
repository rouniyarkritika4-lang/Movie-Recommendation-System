import os
import html
from urllib.parse import quote_plus

import requests
import streamlit as st


# ============================================================
# SETTINGS
# ============================================================

API_BASE = os.getenv(
    "API_BASE",
    "https://movie-recommendation-system-t1c6.onrender.com"
).rstrip("/")

TMDB_IMG = "https://image.tmdb.org/t/p/w500"
TMDB_BACKDROP = "https://image.tmdb.org/t/p/original"


st.set_page_config(
    page_title="CineMatch",
    page_icon="🎬",
    layout="wide"
)


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
<style>

/* ==========================================================
   MAIN APP
   ========================================================== */

.stApp {
    background: #0b0715;
    color: white;
}

.block-container {
    margin-left: 245px;
    max-width: 1200px;
    padding-top: 25px;
    padding-bottom: 50px;
}

section[data-testid="stSidebar"] {
    display: none;
}

p,
span,
label,
div {
    color: #eee;
}


/* ==========================================================
   SEARCH
   ========================================================== */

.stTextInput {
    margin-bottom: 10px;
}

.stTextInput input {
    background: #191225 !important;
    color: white !important;
    border: 1px solid #654b8c !important;
    border-radius: 25px !important;
    padding: 12px 18px !important;
}

.stTextInput input::placeholder {
    color: #aaa !important;
}


/* ==========================================================
   BUTTONS
   ========================================================== */

.stButton button {
    background: #25173c !important;
    color: white !important;
    border: 1px solid #7652a8 !important;
    border-radius: 20px !important;
    font-weight: 600 !important;
}

.stButton button:hover {
    background: #7c3aed !important;
    color: white !important;
    border-color: #9b5cff !important;
}


/* ==========================================================
   SELECTBOX
   ========================================================== */

div[data-testid="stSelectbox"]
div[data-baseweb="select"] > div {
    background: white !important;
    color: black !important;
    border-radius: 8px !important;
}

div[data-testid="stSelectbox"]
div[data-baseweb="select"] span {
    color: black !important;
    -webkit-text-fill-color: black !important;
}

div[data-baseweb="popover"] {
    z-index: 999999 !important;
}

div[data-baseweb="popover"] [role="listbox"] {
    background: white !important;
}

div[data-baseweb="popover"] [role="option"],
div[data-baseweb="popover"] [role="option"] * {
    background: white !important;
    color: black !important;
    -webkit-text-fill-color: black !important;
}

div[data-baseweb="popover"] [role="option"]:hover {
    background: #eeeeee !important;
}


/* ==========================================================
   LEFT SIDEBAR
   ========================================================== */

.movie-sidebar {
    position: fixed;
    left: 0;
    top: 0;
    bottom: 0;

    width: 225px;

    background: #08050e;

    border-right: 1px solid #292033;

    padding: 20px 14px;

    z-index: 9990;

    overflow-y: auto;
}

.logo {
    font-size: 25px;
    font-weight: 900;

    margin-bottom: 30px;

    color: white !important;
}

.logo span {
    color: #b56cff !important;
}

.sidebar-title {
    background: #7c3aed;

    padding: 10px;

    border-radius: 6px;

    font-weight: bold;

    margin-bottom: 18px;

    color: white !important;
}

.sidebar-label {
    color: #999 !important;

    font-size: 13px;

    margin: 10px 8px;
}

.category {
    display: block;

    padding: 10px 12px;

    margin: 3px 0;

    border-radius: 6px;

    color: #ddd !important;

    text-decoration: none !important;

    transition:
        background 0.2s ease,
        color 0.2s ease;
}

.category:hover {
    background: #25173c;

    color: white !important;
}

.category.active {
    background: #6d28d9;

    color: white !important;
}


/* ==========================================================
   MOVIE GRID
   ========================================================== */

.movie-grid {
    display: grid;

    grid-template-columns:
        repeat(
            auto-fill,
            minmax(165px, 1fr)
        );

    gap: 18px;
}


/* ==========================================================
   HORIZONTAL ROW
   ========================================================== */

.movie-row {
    display: flex;

    gap: 15px;

    overflow-x: auto;

    padding:
        5px
        5px
        18px;

    scrollbar-color:
        #6d28d9
        #151020;
}

.movie-row::-webkit-scrollbar {
    height: 8px;
}

.movie-row::-webkit-scrollbar-track {
    background: #151020;

    border-radius: 10px;
}

.movie-row::-webkit-scrollbar-thumb {
    background: #6d28d9;

    border-radius: 10px;
}

.movie-row .movie-card {
    flex: 0 0 165px;
}


/* ==========================================================
   MOVIE CARD
   ========================================================== */

.movie-card {
    display: block;

    width: 100%;

    box-sizing: border-box;

    background: #151020;

    border:
        1px solid
        #292033;

    border-radius: 12px;

    overflow: hidden;

    text-decoration: none !important;

    transition:
        transform 0.2s ease,
        border-color 0.2s ease,
        box-shadow 0.2s ease;
}

.movie-card:hover {
    transform: translateY(-5px);

    border-color: #9b5cff;

    box-shadow:
        0 10px 30px
        rgba(
            124,
            58,
            237,
            0.25
        );
}


/* ==========================================================
   POSTER
   ========================================================== */

.movie-poster {
    width: 100%;

    aspect-ratio: 2 / 3;

    background:
        linear-gradient(
            135deg,
            #211832,
            #0e0a17
        );

    overflow: hidden;

    position: relative;
}

.movie-poster-img {
    width: 100%;

    height: 100%;

    display: block;

    object-fit: cover;

    object-position: center;

    background: #211832;
}


/* ==========================================================
   POSTER PLACEHOLDER
   ========================================================== */

.movie-poster-placeholder {
    width: 100%;

    height: 100%;

    display: flex;

    flex-direction: column;

    align-items: center;

    justify-content: center;

    background:
        linear-gradient(
            135deg,
            #211832,
            #0e0a17
        );

    color: #7652a8 !important;

    font-size: 42px;
}

.movie-poster-placeholder span {
    color: #888 !important;

    font-size: 11px;

    margin-top: 6px;
}


/* ==========================================================
   MOVIE INFO
   ========================================================== */

.movie-info {
    padding: 9px;
}

.movie-title {
    color: white !important;

    font-weight: bold;

    font-size: 14px;

    white-space: nowrap;

    overflow: hidden;

    text-overflow: ellipsis;
}

.movie-year {
    color: #999 !important;

    font-size: 12px;

    margin-top: 4px;
}


/* ==========================================================
   SECTION TITLES
   ========================================================== */

.section-title {
    color: white !important;

    font-size: 22px;

    font-weight: bold;

    margin-top: 25px;

    margin-bottom: 12px;
}


/* ==========================================================
   HERO
   ========================================================== */

.hero {
    min-height: 400px;

    border-radius: 18px;

    background-size: cover;

    background-position: center;

    position: relative;

    overflow: hidden;

    margin-bottom: 25px;

    border:
        1px solid
        #292033;
}

.hero-overlay {
    position: absolute;

    inset: 0;

    padding: 35px;

    display: flex;

    flex-direction: column;

    justify-content: flex-end;

    background:
        linear-gradient(
            transparent 20%,
            rgba(
                5,
                3,
                12,
                0.95
            ) 100%
        );
}

.hero-title {
    font-size: 42px;

    font-weight: 900;

    color: white !important;
}

.hero-text {
    max-width: 650px;

    color: #ddd !important;

    line-height: 1.5;
}


/* ==========================================================
   DETAILS HERO
   ========================================================== */

.details-hero {
    min-height: 430px;

    border-radius: 18px;

    background-size: cover;

    background-position: center;

    position: relative;

    overflow: hidden;

    border:
        1px solid
        #292033;
}

.details-title {
    position: absolute;

    bottom: 25px;

    left: 30px;

    color: white !important;

    font-size: 42px;

    font-weight: 900;
}


/* ==========================================================
   GENRE TAGS
   ========================================================== */

.tag {
    display: inline-block;

    background: #292033;

    padding: 6px 12px;

    border-radius: 8px;

    margin: 4px;

    color: white !important;
}


/* ==========================================================
   TRAILER BUTTON
   ========================================================== */

.trailer-button {
    display: inline-block;

    padding: 10px 20px;

    background: #7c3aed;

    color: white !important;

    border-radius: 20px;

    text-decoration: none !important;

    font-weight: bold;

    margin-top: 10px;
}

.trailer-button:hover {
    background: #9b5cff;
}


/* ==========================================================
   MOBILE
   ========================================================== */

@media (max-width: 800px) {

    .block-container {
        margin-left: 205px;
    }

    .movie-sidebar {
        width: 190px;
    }

    .hero-title,
    .details-title {
        font-size: 30px;
    }

    .hero {
        min-height: 350px;
    }

    .movie-grid {
        grid-template-columns:
            repeat(
                auto-fill,
                minmax(140px, 1fr)
            );
    }

}

</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# SAFE HTML
# ============================================================

def esc(value):
    """Safely escape values used inside HTML."""

    if value is None:
        return ""

    return html.escape(
        str(value),
        quote=True
    )


def render_html(value):
    """Render HTML safely as one line."""

    one_line = " ".join(
        line.strip()
        for line in str(value).splitlines()
        if line.strip()
    )

    if one_line:
        st.markdown(
            one_line,
            unsafe_allow_html=True
        )


# ============================================================
# IMAGE URL
# ============================================================

def normalize_image_url(
    value,
    image_type="poster"
):
    """
    Convert TMDB image paths into complete URLs.
    """

    if not value:
        return ""

    value = str(value).strip()

    if not value:
        return ""

    # Remove accidental quotes
    value = value.strip("'\"")

    # Already a complete URL
    if value.startswith("https://"):
        return value

    if value.startswith("http://"):
        return value

    # Select correct TMDB base
    if image_type == "backdrop":
        base = TMDB_BACKDROP
    else:
        base = TMDB_IMG

    # Already a TMDB path
    if value.startswith("/"):
        return base + value

    # Filename/path
    return base + "/" + value


# ============================================================
# GET IMAGE FROM MOVIE
# ============================================================

def get_image_url(
    movie,
    image_type="poster"
):
    """
    Try many common image field names.
    """

    if not isinstance(movie, dict):
        return ""

    if image_type == "poster":

        possible_fields = [
            "poster_url",
            "poster_path",
            "poster",
            "poster_image",
            "poster_image_url",
            "image_url",
            "image",
        ]

    else:

        possible_fields = [
            "backdrop_url",
            "backdrop_path",
            "backdrop",
            "backdrop_image",
            "backdrop_image_url",
            "image_url",
            "image",
        ]

    for field in possible_fields:

        value = movie.get(field)

        if value:

            result = normalize_image_url(
                value,
                image_type
            )

            if result:
                return result

    return ""


# ============================================================
# GET MOVIE ID
# ============================================================

def get_movie_id(movie):

    if not isinstance(movie, dict):
        return None

    possible_ids = [
        movie.get("tmdb_id"),
        movie.get("id"),
        movie.get("movie_id"),
    ]

    for value in possible_ids:

        if value is None:
            continue

        try:
            return int(value)

        except (
            TypeError,
            ValueError
        ):
            continue

    return None


# ============================================================
# GET MOVIE TITLE
# ============================================================

def get_movie_title(movie):

    if not isinstance(movie, dict):
        return "Unknown"

    return (
        movie.get("title")
        or movie.get("name")
        or movie.get("original_title")
        or "Unknown"
    )


# ============================================================
# GET YEAR
# ============================================================

def get_movie_year(movie):

    if not isinstance(movie, dict):
        return ""

    release_date = (
        movie.get("release_date")
        or movie.get("first_air_date")
        or ""
    )

    return str(release_date)[:4]


# ============================================================
# NORMALIZE MOVIE LIST
# ============================================================

def normalize_movies(data):

    if data is None:
        return []

    # API directly returned list
    if isinstance(data, list):
        return data

    # API returned dictionary
    if isinstance(data, dict):

        possible_keys = [
            "results",
            "movies",
            "data",
            "items",
            "recommendations",
        ]

        for key in possible_keys:

            value = data.get(key)

            if isinstance(value, list):
                return value

        # Sometimes API returns a single movie
        if (
            data.get("id")
            or data.get("tmdb_id")
            or data.get("title")
        ):
            return [data]

    return []


# ============================================================
# API
# ============================================================

@st.cache_data(ttl=600)
def api_get(
    path,
    params=None
):

    try:

        url = API_BASE + path

        response = requests.get(
            url,
            params=params,
            timeout=30
        )

        if response.status_code >= 400:

            return None, (
                f"HTTP {response.status_code}: "
                f"{response.text[:500]}"
            )

        try:

            data = response.json()

        except ValueError:

            return None, (
                "API returned invalid JSON:\n"
                + response.text[:500]
            )

        return data, None

    except requests.exceptions.Timeout:

        return None, (
            "The movie server took too long to respond."
        )

    except requests.exceptions.ConnectionError:

        return None, (
            "Could not connect to the movie server."
        )

    except Exception as e:

        return None, str(e)


# ============================================================
# NAVIGATION
# ============================================================

def go_home():

    st.session_state.view = "home"

    st.session_state.movie_id = None

    st.session_state.category = None

    st.query_params.clear()

    st.query_params["view"] = "home"

    st.rerun()


def go_movie(movie_id):

    if not movie_id:
        return

    try:

        movie_id = int(movie_id)

    except (
        TypeError,
        ValueError
    ):

        return

    st.session_state.view = "details"

    st.session_state.movie_id = movie_id

    st.query_params.clear()

    st.query_params["view"] = "details"

    st.query_params["id"] = str(movie_id)

    st.rerun()


# ============================================================
# SESSION STATE
# ============================================================

if "view" not in st.session_state:
    st.session_state.view = "home"

if "movie_id" not in st.session_state:
    st.session_state.movie_id = None

if "category" not in st.session_state:
    st.session_state.category = None


# ============================================================
# READ URL
# ============================================================

url_view = st.query_params.get("view")

url_id = st.query_params.get("id")

url_cat = st.query_params.get("cat")


if url_view in (
    "home",
    "details"
):

    st.session_state.view = url_view


if url_id:

    try:

        st.session_state.movie_id = int(
            url_id
        )

    except (
        ValueError,
        TypeError
    ):

        pass


if url_cat:

    st.session_state.category = url_cat

elif st.session_state.view == "home":

    st.session_state.category = None


# ============================================================
# CATEGORIES
# ============================================================

categories = [
    (
        "trending",
        "🔥",
        "Trending"
    ),
    (
        "popular",
        "😍",
        "Popular"
    ),
    (
        "top_rated",
        "🏆",
        "Hit Movies"
    ),
    (
        "now_playing",
        "🎟️",
        "Now Playing"
    ),
    (
        "upcoming",
        "📅",
        "Coming Soon"
    ),
]


# ============================================================
# LEFT SIDEBAR
# ============================================================

sidebar_html = (
    '<div class="movie-sidebar">'
)

sidebar_html += (
    '<div class="logo">'
    '🎬 <span>CineMatch</span>'
    '</div>'
)

sidebar_html += (
    '<div class="sidebar-title">'
    'Filters'
    '</div>'
)

sidebar_html += (
    '<div class="sidebar-label">'
    'Categories'
    '</div>'
)


for key, icon, name in categories:

    active = (
        "active"
        if (
            st.session_state.category
            == key
        )
        else ""
    )

    sidebar_html += (
        f'<a '
        f'class="category {active}" '
        f'href="?view=home'
        f'&amp;cat={esc(key)}" '
        f'target="_self">'
        f'{icon} &nbsp; '
        f'{esc(name)}'
        f'</a>'
    )


sidebar_html += "</div>"


st.markdown(
    sidebar_html,
    unsafe_allow_html=True
)


# ============================================================
# BRAND
# ============================================================

st.markdown(
    """
    <h1 style="color:white">
        🎬 CineMatch
    </h1>

    <p style="color:#999">
        Find movies and discover similar movies.
    </p>
    """,
    unsafe_allow_html=True
)


# ============================================================
# MOVIE CARD
# ============================================================

def movie_card(movie):

    if not isinstance(
        movie,
        dict
    ):
        return ""

    # --------------------------------------------------------
    # ID
    # --------------------------------------------------------

    movie_id = get_movie_id(
        movie
    )

    if not movie_id:
        return ""

    # --------------------------------------------------------
    # TITLE
    # --------------------------------------------------------

    raw_title = get_movie_title(
        movie
    )

    title = esc(
        raw_title
    )

    # --------------------------------------------------------
    # POSTER
    # --------------------------------------------------------

    poster = get_image_url(
        movie,
        "poster"
    )

    poster = esc(
        poster
    )

    # --------------------------------------------------------
    # YEAR
    # --------------------------------------------------------

    year = esc(
        get_movie_year(
            movie
        )
    )

    # --------------------------------------------------------
    # RATING
    # --------------------------------------------------------

    rating = movie.get(
        "vote_average"
    )

    rating_text = ""

    try:

        if rating is not None:

            rating_text = (
                f"⭐ {float(rating):.1f}"
            )

    except (
        TypeError,
        ValueError
    ):

        rating_text = ""

    rating_text = esc(
        rating_text
    )

    # --------------------------------------------------------
    # IMAGE
    # --------------------------------------------------------

    if poster:

        image_html = (
            f'<img '
            f'class="movie-poster-img" '
            f'src="{poster}" '
            f'alt="{title}" '
            f'loading="lazy" '
            f'onerror="'
            f'this.style.display=\'none\';'
            f'this.nextElementSibling'
            f'.style.display=\'flex\';'
            f'">'
            
            f'<div '
            f'class="movie-poster-placeholder" '
            f'style="display:none;">'
            f'🎬'
            f'<span>'
            f'Image unavailable'
            f'</span>'
            f'</div>'
        )

    else:

        image_html = (
            '<div '
            'class="movie-poster-placeholder">'
            '🎬'
            '<span>No poster</span>'
            '</div>'
        )

    # --------------------------------------------------------
    # CARD
    # --------------------------------------------------------

    return (
        f'<a '
        f'class="movie-card" '
        f'href="?view=details'
        f'&amp;id={movie_id}" '
        f'target="_self">'

        f'<div '
        f'class="movie-poster">'
        f'{image_html}'
        f'</div>'

        f'<div '
        f'class="movie-info">'

        f'<div '
        f'class="movie-title">'
        f'{title}'
        f'</div>'

        f'<div '
        f'class="movie-year">'
        f'{year} '
        f'{rating_text}'
        f'</div>'

        f'</div>'

        f'</a>'
    )


# ============================================================
# SHOW MOVIES
# ============================================================

def show_movies(
    movies,
    horizontal=False
):

    movies = normalize_movies(
        movies
    )

    if not movies:

        st.info(
            "No movies found."
        )

        return

    cards = ""

    for movie in movies:

        card = movie_card(
            movie
        )

        if card:
            cards += card

    if not cards:

        st.info(
            "Movies were found, "
            "but no valid movie cards "
            "could be created."
        )

        return

    css_class = (
        "movie-row"
        if horizontal
        else "movie-grid"
    )

    render_html(
        f'<div '
        f'class="{css_class}">'
        f'{cards}'
        f'</div>'
    )


# ============================================================
# LOAD CATEGORY
# ============================================================

def load_category(
    category,
    limit=20
):

    data, error = api_get(
        "/home",
        {
            "category": category,
            "limit": limit
        }
    )

    if error:

        return [], error

    return (
        normalize_movies(data),
        None
    )


# ============================================================
# HOME PAGE
# ============================================================

if st.session_state.view == "home":

    # ========================================================
    # SEARCH
    # ========================================================

    search = st.text_input(
        "Search movie",
        placeholder=(
            "Type: batman, avenger, love..."
        ),
        key="movie_search"
    )

    # ========================================================
    # SEARCH MODE
    # ========================================================

    if search.strip():

        query = search.strip()

        if len(query) < 2:

            st.info(
                "Type at least 2 characters."
            )

            st.stop()

        # ----------------------------------------------------
        # SEARCH API
        # ----------------------------------------------------

        data, error = api_get(
            "/tmdb/search",
            {
                "query": query
            }
        )

        if error:

            st.error(
                "Movie server could not be reached."
            )

            st.code(
                error
            )

            st.stop()

        results = normalize_movies(
            data
        )

        if not results:

            st.warning(
                "No movies found."
            )

            st.stop()

        # ----------------------------------------------------
        # DROPDOWN
        # ----------------------------------------------------

        names = []

        valid_results = []

        for movie in results[:15]:

            if not isinstance(
                movie,
                dict
            ):
                continue

            title = get_movie_title(
                movie
            )

            year = get_movie_year(
                movie
            )

            movie_id = get_movie_id(
                movie
            )

            if not movie_id:
                continue

            if year:

                display_name = (
                    f"{title} ({year})"
                )

            else:

                display_name = title

            names.append(
                display_name
            )

            valid_results.append(
                movie
            )

        if names:

            selected = st.selectbox(
                "Choose a movie",
                [
                    "-- Select a movie --"
                ] + names
            )

            if (
                selected
                != "-- Select a movie --"
            ):

                index = names.index(
                    selected
                )

                selected_movie = (
                    valid_results[index]
                )

                selected_id = (
                    get_movie_id(
                        selected_movie
                    )
                )

                if selected_id:

                    go_movie(
                        selected_id
                    )

        # ----------------------------------------------------
        # SEARCH RESULTS
        # ----------------------------------------------------

        st.markdown(
            "## 🔎 Search Results"
        )

        show_movies(
            results[:24]
        )

        st.stop()


    # ========================================================
    # CATEGORY PAGE
    # ========================================================

    if st.session_state.category:

        if st.button(
            "🏠 Back to Home"
        ):

            go_home()

        category_names = {
            key: name
            for key, icon, name
            in categories
        }

        category_name = (
            category_names.get(
                st.session_state.category,
                "Movies"
            )
        )

        st.markdown(
            f'<div '
            f'class="section-title">'
            f'🎬 '
            f'{esc(category_name)}'
            f'</div>',
            unsafe_allow_html=True
        )

        movies, error = load_category(
            st.session_state.category,
            30
        )

        if error:

            st.error(
                "Could not load this category."
            )

            st.code(
                error
            )

        else:

            show_movies(
                movies
            )

        st.stop()


    # ========================================================
    # FEATURED MOVIE
    # ========================================================

    st.markdown(
        '<div '
        'class="section-title">'
        '🎬 Featured Movie'
        '</div>',
        unsafe_allow_html=True
    )

    trending, trending_error = (
        load_category(
            "trending",
            8
        )
    )

    featured_movie = None

    if (
        not trending_error
        and trending
    ):

        featured_movie = trending[0]

    if featured_movie:

        movie_id = get_movie_id(
            featured_movie
        )

        info = None

        # ----------------------------------------------------
        # Try details endpoint
        # ----------------------------------------------------

        if movie_id:

            info, info_error = api_get(
                f"/movie/id/{movie_id}"
            )

        # ----------------------------------------------------
        # If details endpoint fails,
        # use trending object itself
        # ----------------------------------------------------

        if (
            not info
            or not isinstance(
                info,
                dict
            )
        ):

            info = featured_movie

        title = get_movie_title(
            info
        )

        overview = (
            info.get("overview")
            or featured_movie.get(
                "overview"
            )
            or "No overview available."
        )

        image = get_image_url(
            info,
            "backdrop"
        )

        if not image:

            image = get_image_url(
                featured_movie,
                "backdrop"
            )

        if not image:

            image = get_image_url(
                info,
                "poster"
            )

        if not image:

            image = get_image_url(
                featured_movie,
                "poster"
            )

        image = esc(
            image
        )

        if image:

            hero_style = (
                "background-image:"
                f"url('{image}');"
            )

        else:

            hero_style = (
                "background:"
                "linear-gradient("
                "135deg,"
                "#211832,"
                "#0b0715"
                ");"
            )

        render_html(
            f'<div '
            f'class="hero" '
            f'style="{hero_style}">'

            f'<div '
            f'class="hero-overlay">'

            f'<div '
            f'class="hero-title">'
            f'{esc(title)}'
            f'</div>'

            f'<div '
            f'class="hero-text">'
            f'{esc(overview)}'
            f'</div>'

            f'</div>'

            f'</div>'
        )

    else:

        st.info(
            "Featured movie is currently unavailable."
        )


    # ========================================================
    # HOME MOVIE ROWS
    # ========================================================

    rows = [
        (
            "trending",
            "🔥 Trending Now"
        ),
        (
            "popular",
            "😍 Popular Picks"
        ),
        (
            "top_rated",
            "🏆 Hit Movies"
        ),
        (
            "now_playing",
            "🎟️ Now Playing"
        ),
        (
            "upcoming",
            "📅 Coming Soon"
        ),
    ]


    for key, section_title in rows:

        st.markdown(
            f'<div '
            f'class="section-title">'
            f'{esc(section_title)}'
            f'</div>',
            unsafe_allow_html=True
        )

        movies, error = load_category(
            key,
            20
        )

        if error:

            st.warning(
                f"Could not load "
                f"{section_title}."
            )

        elif not movies:

            st.info(
                f"No movies available "
                f"for {section_title}."
            )

        else:

            show_movies(
                movies,
                horizontal=True
            )


# ============================================================
# DETAILS PAGE
# ============================================================

elif st.session_state.view == "details":

    movie_id = (
        st.session_state.movie_id
    )

    if not movie_id:

        st.error(
            "No movie selected."
        )

        if st.button(
            "🏠 Go Home"
        ):

            go_home()

        st.stop()


    # ========================================================
    # BACK
    # ========================================================

    if st.button(
        "🏠 Back to Home"
    ):

        go_home()


    # ========================================================
    # DETAILS API
    # ========================================================

    data, error = api_get(
        f"/movie/id/{movie_id}"
    )

    if (
        error
        or not data
        or not isinstance(
            data,
            dict
        )
    ):

        st.error(
            "Could not load movie details."
        )

        st.code(
            error or "Unknown error"
        )

        st.stop()


    # ========================================================
    # MOVIE DATA
    # ========================================================

    title = get_movie_title(
        data
    )

    overview = (
        data.get("overview")
        or "No overview available."
    )


    # ========================================================
    # BACKDROP
    # ========================================================

    backdrop = get_image_url(
        data,
        "backdrop"
    )

    if not backdrop:

        backdrop = get_image_url(
            data,
            "poster"
        )

    backdrop = esc(
        backdrop
    )


    # ========================================================
    # DETAILS
    # ========================================================

    rating = data.get(
        "vote_average"
    )

    release_date = (
        data.get("release_date")
        or data.get("first_air_date")
        or ""
    )

    year = str(
        release_date
    )[:4]

    runtime = data.get(
        "runtime"
    )

    language = (
        data.get(
            "original_language"
        )
        or ""
    ).upper()

    genres = (
        data.get("genres")
        or []
    )


    # ========================================================
    # DETAILS HERO
    # ========================================================

    if backdrop:

        hero_style = (
            "background-image:"
            f"url('{backdrop}');"
        )

    else:

        hero_style = (
            "background:"
            "linear-gradient("
            "135deg,"
            "#211832,"
            "#0b0715"
            ");"
        )

    render_html(
        f'<div '
        f'class="details-hero" '
        f'style="{hero_style}">'

        f'<div '
        f'class="details-title">'
        f'{esc(title)}'
        f'</div>'

        f'</div>'
    )


    # ========================================================
    # META
    # ========================================================

    info = []

    if rating is not None:

        try:

            info.append(
                f"⭐ {float(rating):.1f}"
            )

        except (
            TypeError,
            ValueError
        ):

            pass

    if year:

        info.append(
            year
        )

    if runtime:

        try:

            runtime_int = int(
                runtime
            )

            hours = (
                runtime_int // 60
            )

            minutes = (
                runtime_int % 60
            )

            if hours:

                info.append(
                    f"{hours}h "
                    f"{minutes}m"
                )

            else:

                info.append(
                    f"{minutes}m"
                )

        except (
            TypeError,
            ValueError
        ):

            pass

    if language:

        info.append(
            language
        )

    if info:

        st.write(
            " • ".join(info)
        )


    # ========================================================
    # GENRES
    # ========================================================

    if genres:

        genre_html = ""

        for genre in genres:

            if isinstance(
                genre,
                dict
            ):

                name = (
                    genre.get("name")
                    or ""
                )

            else:

                name = str(
                    genre
                )

            if name:

                genre_html += (
                    f'<span '
                    f'class="tag">'
                    f'{esc(name)}'
                    f'</span>'
                )

        if genre_html:

            render_html(
                genre_html
            )


    # ========================================================
    # OVERVIEW
    # ========================================================

    st.markdown(
        "### Overview"
    )

    st.write(
        overview
    )


    # ========================================================
    # TRAILER
    # ========================================================

    trailer = (
        "https://www.youtube.com/results"
        "?search_query="
        + quote_plus(
            str(title)
            + " official trailer"
        )
    )

    render_html(
        f'<a '
        f'href="{esc(trailer)}" '
        f'target="_blank" '
        f'class="trailer-button">'
        f'🎬 Watch Trailer'
        f'</a>'
    )


    # ========================================================
    # SIMILAR MOVIES
    # ========================================================

    st.markdown(
        "## 🔎 Similar Movies"
    )

    bundle, error = api_get(
        "/movie/search",
        {
            "query": title,
            "tfidf_top_n": 14,
            "genre_limit": 14,
        }
    )

    similar = []


    # ========================================================
    # TF-IDF RECOMMENDATIONS
    # ========================================================

    if (
        not error
        and isinstance(
            bundle,
            dict
        )
    ):

        tfidf = (
            bundle.get(
                "tfidf_recommendations",
                []
            )
            or []
        )

        for item in tfidf:

            if not isinstance(
                item,
                dict
            ):

                continue

            tmdb = (
                item.get("tmdb")
                or {}
            )

            if not isinstance(
                tmdb,
                dict
            ):

                continue

            tmdb_id = (
                tmdb.get("tmdb_id")
                or tmdb.get("id")
                or item.get("tmdb_id")
                or item.get("id")
            )

            if not tmdb_id:

                continue

            similar.append(
                {
                    "tmdb_id": tmdb_id,

                    "title": (
                        tmdb.get("title")
                        or item.get("title")
                        or "Unknown"
                    ),

                    "poster_url": (
                        tmdb.get(
                            "poster_url"
                        )
                    ),

                    "poster_path": (
                        tmdb.get(
                            "poster_path"
                        )
                    ),

                    "release_date": (
                        tmdb.get(
                            "release_date",
                            ""
                        )
                    ),

                    "vote_average": (
                        tmdb.get(
                            "vote_average"
                        )
                    ),
                }
            )


        # ====================================================
        # GENRE FALLBACK
        # ====================================================

        if not similar:

            genre_results = (
                bundle.get(
                    "genre_recommendations",
                    []
                )
                or []
            )

            similar = normalize_movies(
                genre_results
            )


    # ========================================================
    # FINAL FALLBACK
    # ========================================================

    if not similar:

        fallback, fallback_error = (
            api_get(
                "/recommend/genre",
                {
                    "tmdb_id": movie_id,
                    "limit": 18,
                }
            )
        )

        if not fallback_error:

            similar = normalize_movies(
                fallback
            )


    # ========================================================
    # REMOVE CURRENT MOVIE
    # ========================================================

    cleaned_similar = []

    for movie in similar:

        current_id = get_movie_id(
            movie
        )

        if (
            current_id
            and current_id == movie_id
        ):
            continue

        cleaned_similar.append(
            movie
        )

    similar = cleaned_similar


    # ========================================================
    # DISPLAY SIMILAR
    # ========================================================

    if similar:

        show_movies(
            similar,
            horizontal=True
        )

    else:

        st.info(
            "No similar movies found "
            "for this movie."
        )


# =================
# ===========================================
# FOOTER
# ============================================================

st.markdown(
    """
    <hr>

    <p style="
        text-align:center;
        color:#777;
    ">
        🎬 CineMatch
    </p>
    """,
    unsafe_allow_html=True
)