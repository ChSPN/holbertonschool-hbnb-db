from src.persistence.repository import Repository


def populate_db(db: Repository) -> None:
    from src.models.country import Country

    countries = [
        Country(name="Uruguay", code="UY"),
    ]

    models = db.get_all("Country")
    codes = [model.code for model in models]
    for country in countries:
        if country.code not in codes:
            db.save(country)

    print("DB populated")
