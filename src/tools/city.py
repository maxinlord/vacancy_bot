import tools


async def get_cities():
    quantity_cities = 3
    cities = []
    for x in range(1, quantity_cities + 1):
        cities.append(await tools.get_text_button(f"city_{x}"))
    return cities
