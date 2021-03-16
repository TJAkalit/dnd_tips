# type  1 - INTEGER, 2 - TEXT, 3 - REAL,  

tables_template = {
    "Session": {
        "id": {"type": 1, "null": False, "unique": True, },                 # Первичный ключ
        "hash_key": {"type": 2, "null": False, "unique": True, },           # Ключ для сессии
        "create_date": {"type": 1, "null": False, "unique": False, },       # Дата создания сессии
        "renew_date": {"type": 1, "null": False, "unique": False, },        # Дата последнего обновления ключа сессии
        "removed": {"type": 1, "null": True, "unique": False, },            # Пометка об удалении
        "p_k": {"exist": True, "column": "id", "autoincrement": True, },    # Инструкция первичного ключа
        "f_k": {"exist": False},                                            # Инструкция вторичных ключей
    },
    "Character": {
        "id": {"type": 1, "null": False, "unique": True, },                 # Первичный ключ
        "first_name": {"type": 2, "null": True, "unique": False, },         # Имя персонажа
        "middle_name": {"type": 2, "null": True, "unique": False, },        # Отчество персонажа
        "last_name": {"type": 2, "null": True, "unique": False, },          # Фамилия персонажа
        "sex": {"type": 1, "null": True, "unique": False },                 # Пол персонажа
        "kind": {"type": 1, "null": False, "unique": False },               # Раса, тип персонажа
        "world_id": {"type": 1, "null": False, "unique": False, },          # Ключ мира, с которым связан персонаж
        "create_date": {"type": 1, "null": False, "unique": False, },       # Дата создания персонажа
        "removed": {"type": 1, "null": True, "unique": False, },            # Пометка об удалении
        "p_k": {"exist": True, "column": "id", "autoincrement": True, },    # Инструкция первичного ключа
        "f_k": {"exist": False},                                            # Инструкция вторичных ключей
    },
    "Realm": {
        "id": {"type": 1, "null": False, "unique": False, },                # Первичный ключ
        "name": {"type": 2, "null": False, "unique": True, },               # Название мира
        "create_date": {"type": 1, "null": False, "unique": False, },       # Дата создания мира
        "removed": {"type": 1, "null": False, "unique": False, },           # Пометка на удаление
        "p_k": {"exist": True, "column": "id", "autoincrement": True, },    # Инструкция первичного ключа
        "f_k": {"exist": False},                                            # Инструкция вторичных ключей
    },
    # "Attribute": None,
    # "AttributePrototype": None,
    # "AttributeTemplate": None,
    # "AttributeTemplate_AttributePrototype": None,
    # "Class": None,
    # "CharacterClass": None,
    # "CharacterClass_Realm": None,
    # "Place": None,
    # "Place_Realm": None,
    # "PlaceTemplate": None,
    # "Place_PlaceTemplate": None,
    # "Stat": None,
    # "StatPrototype": None,
    # "StatTemplate": None,
    # "StatTemplate_StatPrototype": None
}
