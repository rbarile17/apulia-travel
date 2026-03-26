#!/usr/bin/env python3

from __future__ import annotations

import argparse
from textwrap import dedent

DAYS = [
    ("LUNEDI", "Monday"),
    ("MARTEDI", "Tuesday"),
    ("MERCOLEDI", "Wednesday"),
    ("GIOVEDI", "Thursday"),
    ("VENERDI", "Friday"),
    ("SABATO", "Saturday"),
    ("DOMENICA", "Sunday"),
]

REVIEW_SPECS = [
    ("art_and_culture_review", "art_culture_review", "Arte e Cultura", "Arte e Cultura"),
    ("food_wine_review", "food_wine_review", "Enogastronomia", "Enogastronomia"),
    ("nature_sport_wellness_review", "nature_sport_wellness_review", "Natura, Sport e Benessere", "Natura, Sport e Benessere"),
    ("theatre_dance_review", "theatre_dance_review", "Teatro e Danza", "Teatro e Danza"),
    ("music_review", "music_review", "Musica", "Musica"),
    ("cinema_review", "cinema_review", "Cinema", "Cinema"),
    ("entertainment_review", "entertainment_review", "Intrattenimento", "Intrattenimento"),
    ("tradition_spirituality_review", "tradition_spirituality_review", "Tradizioni e Spiritualità", "Tradizioni e Spiritualità"),
    ("events", "events_review", "Eventi", "Meeting Incentive Congressi ed Eventi"),
    ("sea_review", "sea_review", "Mare", "Mare"),
]

POI_TYPE_SPECS = [
    ("PARCHI_NATURALI", "td:NaturalPark"),
    ("PARCHI_NAZIONALI", "td:NationalPark"),
    ("TORRI", "td:Tower"),
    ("BASILICHE", "td:Basilica"),
    ("CHIESE_ROMANICHE", "td:RomanesqueChurch"),
    ("AREE_NATURALI", "td:NaturalArea"),
    ("CHIESE_IPOGEE", "td:UndergroundChurch"),
    ("GROTTE", "td:Cave"),
    ("GROTTE_MARINE", "td:SeaCave"),
    ("FRANTOI_IPOGEI", "td:UndergroundOilMill"),
    ("INTRATTENIMENTO", "td:EntertainmentBusiness"),
    ("CHIESE", "td:Church"),
    ("MUSEI", "td:Museum"),
    ("CULTI_ORTODOSSI", "td:OrthodoxWorship"),
    ("GRAVINE", "td:Ravine"),
    ("ECOMUSEI", "td:EcoMuseum"),
    ("LAGHI", "td:Lake"),
    ("OASI_WWF", "td:WWFOasis"),
    ("RISERVE_MARINE", "td:MarineReserve"),
    ("CONVENTI", "td:Convent"),
    ("PARCHI_ARCHEOLOGICI", "td:ArecheologicalPark"),
    ("ANFITEATRI", "td:Amphitheater"),
    ("GIARDINI", "td:Garden"),
    ("BIBLIOTECHE", "td:Library"),
    ("TRULLI", "td:Trullo"),
    ("RISERVE", "td:Reserve"),
    ("SINAGOGHE", "td:Synagogue"),
    ("PORTI", "td:Port"),
    ("MULINI", "td:Mill"),
    ("SPIAGGE", "td:Beach"),
    ("MOSCHEE", "td:Mosque"),
    ("CULTO", "td:Worship"),
    ("APPRODI", "td:Landing"),
    ("MASSERIE", "td:Farmhouse"),
    ("TEATRI_STORICI", "td:HistoricTheater"),
    ("CASTELLI", "td:Castle"),
    ("PALAZZI_STORICI", "td:HistoricPalace"),
]


def indent(text: str, spaces: int) -> str:
    pad = " " * spaces
    return "\n".join(pad + line if line else line for line in text.splitlines())


def build_day_blocks() -> str:
    blocks = []
    for field_name, iri_day in DAYS:
        blocks.append(dedent(f"""\
        - p: ti:hasDayOfWeek
          o:
            value: ti:{iri_day}
            type: iri
          condition:
            function: idlab-fn:equal
            parameters:
              - [grel:valueParameter, $({field_name})]
              - [grel:valueParameter2, "true"]"""))
    return "\n".join(blocks)


def build_opening_hours_mapping(name: str, suffix: str, source_field: str) -> str:
    return dedent(f"""\
    {name}:
      sources:
        - [attrattori.json~jsonpath, "$.[*]"]
      s:
        function: grel:string_replace
        parameters:
          - [grel:valueParameter, clv:OpeningHours/$(id_attrattore)_$(nm_attrattore_it)_{suffix}]
          - [grel:p_string_find, " "]
          - [grel:p_string_replace, "_"]
      condition:
        function: grel:boolean_not
        parameters:
          - parameter: grel:bool_b
            value:
              function: idlab-fn:isNull
              parameters:
                - [idlab-fn:str, $({source_field})]
      po:
        - [a, clv:OpeningHoursSpecification]
        - [a, clv:AccessCondition]
        - p: clv:opens
          o:
            function: grel:string_substring
            parameters:
              - [grel:valueParameter, $({source_field})]
              - [grel:param_int_i_from, 0]
              - [grel:param_int_i_opt_to, 5]
        - p: clv:closes
          o:
            function: grel:string_substring
            parameters:
              - [grel:valueParameter, $({source_field})]
              - [grel:param_int_i_from, 8]
              - [grel:param_int_i_opt_to, 13]
        - p: access-condition:isAccessConditionOf
          o:
            mapping: poi
    {indent(build_day_blocks(), 8)}
    """)


def build_review_mapping(name: str, subject_suffix: str, aspect_label: str, rating_field: str) -> str:
    return dedent(f"""\
    {name}:
      sources:
        - [attrattori.json~jsonpath, "$.[*]"]
      s:
        function: grel:string_replace
        parameters:
          - [grel:valueParameter, sm:Review/$(id_attrattore)_$(nm_attrattore_it)_{subject_suffix}]
          - [grel:p_string_find, " "]
          - [grel:p_string_replace, "_"]
      po:
        - [a, sm:Review]
        - [sm:reviewAspect, "{aspect_label}"]
        - p: sm:hasRating
          o:
            value: sm:Rating/$({rating_field})
            type: iri
    """)


def build_poi_type_blocks() -> str:
    blocks = []
    for tipologia, klass in POI_TYPE_SPECS:
        blocks.append(dedent(f"""\
        - p: a
          o: [{klass}]
          condition:
            function: idlab-fn:equal
            parameters:
              - [grel:valueParameter, $(tipologia)]
              - [grel:valueParameter2, "{tipologia}"]"""))
    return "\n".join(blocks)


def render() -> str:
    opening_hours = "\n".join(
        [
            build_opening_hours_mapping(
                "openingHoursMorning",
                "opening_hours_morning",
                "orario_apertura_mattina",
            ),
            build_opening_hours_mapping(
                "openingHoursAfternoon",
                "opening_hours_afternoon",
                "orario_apertura_pomeriggio",
            ),
        ]
    )

    reviews = "\n".join(build_review_mapping(*spec) for spec in REVIEW_SPECS)

    poi_type_conditions = build_poi_type_blocks()

    return dedent(f"""\
    # ============================================================
    # AUTO-GENERATED MAPPINGS
    # ============================================================

    mappings:
    {indent(opening_hours.rstrip(), 2)}

    {indent(reviews.rstrip(), 2)}

    poi_type_conditions:
    {indent(poi_type_conditions.rstrip(), 2)}
    """)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate repetitive YARRRML mappings.")
    parser.add_argument(
        "-o",
        "--output",
        help="Output file",
    )
    args = parser.parse_args()

    content = render()

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(content)
    else:
        print(content)


if __name__ == "__main__":
    main()
