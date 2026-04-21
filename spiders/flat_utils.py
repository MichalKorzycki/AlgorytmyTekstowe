def text_to_float(txt):
    return float(''.join(c for c in txt if c in [str(i) for i in range(10)]))


def flat_to_dict(soup):
    value = [flat for flat in soup.find_all('span', class_="details-price__item")][0]
    price = text_to_float(value.text)
    details_list = soup.find_all('div', class_="details-highlighted-parameters__item-value")
    rooms = details_list[0].text
    area = details_list[1].text
    floor = details_list[2].text
    title = [flat for flat in soup.find_all('h1')][0].text
    return {
        'price': price,
        'area': area,
        'rooms': rooms,
        'floor': floor,
        'title': title,
    }