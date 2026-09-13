"""Ordered deterministic rules for classifying IES construction materials."""
import re

CEMENT_WORD = r"\bcement\b"


CONCRETE_PATTERNS = [
    r"\brck\d+\b",  # e.g. rck30, rck50
    r"\b\d*c\s*\d{1,2}/\d{1,2}\b",  # e.g. c20/25, 32c12/15, 101c35/45
    r"\bxc\d?\b",  # e.g. xc2, xc3
    r"\bxd\d?\b",
    r"\bxs\d?\b",
    r"\bxf\d?\b",
    r"\bxa\d?\b",
    r"\bsf2\b",  # slump-flow class
    r"\bcls\b",  # e.g., for “CLS” used in some Italian notations
]


AGGREGATES_KEYWORDS = [
    r"\baggregates?\b",  # "aggregate" or "aggregates"
    r"\brubble\b",
    r"\bfill\b",
]


CEM_PATTERNS = [
    r"\bcem\s?[i-v]",  # e.g., CEM I, CEM II, etc.
    r"\bcem\s?\d+\/?[a-zA-Z]?[\-]?[a-zA-Z]+",  # e.g., CEM IV/B-LL 32,5R
]


STEEL_KEYWORDS = [
    r"\bsteel\b",
    r"\brebar\b",
    r"\bmesh\b",
    r"\bprofile\b",
    r"\bpipe\b",
    r"\bpex\b",
]


PRECAST_KEYWORDS = [
    r"\breinforced concrete\b",
    r"\bpre-?fabricated concrete\b", # matches "prefabricated concrete" or "pre-fabricated concrete"
    r"\bpre-?cast concrete\b",       # matches "precast concrete" or "pre-cast concrete"
    r"\bpre-?cast\b",                # matches "precast" or "pre-cast"
    r"\bpre-?stressed\b"             # matches "prestressed" or "pre-stressed"
]


def contains_whole_word(word_regex, text):
    """Check if 'word_regex' is present as a whole word in 'text' (case-insensitive)."""
    return bool(re.search(word_regex, text, re.IGNORECASE))


def matches_any(pattern_list, text):
    """Return True if any regex in 'pattern_list' matches 'text' (case-insensitive)."""
    for pattern in pattern_list:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False


def in_both_name_desc(word_regex, name_text, desc_text):
    """Return True if 'word_regex' appears in both name and description."""
    return contains_whole_word(word_regex, name_text) and contains_whole_word(
        word_regex, desc_text
    )


def name_has_aggregates(name_text):
    """Return True if the product name contains an aggregator keyword."""
    for kw in AGGREGATES_KEYWORDS:
        if re.search(kw, name_text, re.IGNORECASE):
            return True
    return False


def is_steel_accessory(name_lower):
    """Return True if the product name indicates a steel accessory (e.g. rebar, pipe)."""
    for kw in STEEL_KEYWORDS:
        if re.search(kw, name_lower):
            return True
    return False


def classify_product(
    product_name: str,
    product_desc: str,
    product_app: str,
    flow_property_name: str = None,
    flow_property_mean_value: str = None,
    flow_property_reference_unit: str = None,
) -> str:
    """Classify prepared fields using ordered material predicates.

    The first matching predicate supplies the category. Volume/name rules
    identify ready-mix concrete; additive, aggregate, cement, and precast
    predicates distinguish other construction materials.
    """
    name_lower = product_name.lower()
    desc_lower = product_desc.lower()
    app_lower = product_app.lower()
    combined_text = name_lower + " " + desc_lower

    # Concrete Admixtures
    if (
        re.search(r"\badmixtures?\b", name_lower)
        or re.search(r"\badditives?\b", name_lower)
        and re.search(r"\bconcrete\b", name_lower)
    ):
        return "Mineral building products > Mortar and Concrete > Concrete additive"

    #  Aggregates based on measurement and keywords
    # Look for a measurement in mm (e.g., "10 mm", "10/20 mm") and either "aggregate" (or a close variant) or "concrete"
    if re.search(r"\b\d+\s*(?:/\s*\d+)?\s*mm\b", name_lower) and (
        re.search(r"aggregate", name_lower, re.IGNORECASE)
        or re.search(r"aggregte", name_lower, re.IGNORECASE)
        and re.search(r"concrete", name_lower, re.IGNORECASE)
    ):
        return "Mineral building products > Concrete aggregates"

    # Flow Property Rule for Concrete ---
    if (
        flow_property_name is not None
        and flow_property_mean_value is not None
        and flow_property_reference_unit is not None
    ):
        if (
            flow_property_name.strip().lower() == "volume"
            and flow_property_reference_unit.strip().lower() == "m3"
            and flow_property_mean_value.strip() in {"1", "1.0"}
        ):
            if matches_any(CONCRETE_PATTERNS, combined_text) or re.search(
                r"concrete", name_lower, re.IGNORECASE
            ):

                return "Mineral building products > Mortar and Concrete > Ready mixed concrete"


    # Cement (explicit "cement" in both name and description) ---
    if in_both_name_desc(CEMENT_WORD, name_lower, desc_lower):
        return "Cement"

    # CEM references identify cement.
    if matches_any(CEM_PATTERNS, combined_text):
        return "Cement"

    # Concrete when ready mix is in the name
    if re.search(r"ready[\s-]*mix(?:[\s-]*ed)?", name_lower, re.IGNORECASE) or re.search(r"ready[\s-]*mix(?:[\s-]*ed)?", app_lower, re.IGNORECASE):
        return "Mineral building products > Mortar and Concrete > Ready mixed concrete"

    # Precast Concrete Patterns
    if matches_any(PRECAST_KEYWORDS, combined_text):
        if re.search(r"\basphalt\b", name_lower, re.IGNORECASE) or re.search(r"\basphalt\b", desc_lower, re.IGNORECASE):
            return "Mineral building products > Asphalt"
        return "Mineral building products > Bricks, blocks and elements > Precast concrete elements and goods"

    # General concrete names exclude steel accessories.
    if re.search(r"\bconcrete\b", name_lower, re.IGNORECASE):
        if is_steel_accessory(name_lower):
            return "Other"
        return "Concrete"


    # --- Default ---
    return "Other"
