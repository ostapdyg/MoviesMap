def read_data(year):
    """
    (int) -> dict
    Read a file locations.list and return a dict {location:number of films}
    for the specific year
    """
    print('Reading database...')
    with open('locations.list',
                  mode='r',
                  encoding='utf-8',
                  errors='ignore') as input_file:
        line = ''
        while not line.startswith('='):
            line = input_file.readline()
        locations = {}
        errors = 0
        i = 0
        films_num = 0
        while not line.startswith('-------'):
            try:
                i += 1
                line = input_file.readline()
                film_data = line.split('\t')
                film_name = film_data[0]
                film_year = int(film_name[film_name.find('(') + 1:
                                          film_name.find('(')+5])
                if film_data[-1].startswith('('):
                    film_address = film_data[-2]
                else:
                    film_address = film_data[-1]
                film_address = ', '.join(film_address.strip().split(', ')[-2:])
                if film_year == year:
                    films_num += 1
                    if film_address in locations:
                        locations[film_address] += 1
                    else:
                        locations[film_address] = 1
            except ValueError:
                errors += 1
    print('%i analysed, %i errors' % (i, errors))
    return locations, films_num


def create_map(year, locations):
    """
    (int, dict) -> int
    Create a map of films for the specific year and save it to MoviesMap.html
        locations: dict of {location: number of films}
    """
    import folium
    from geopy.geocoders import Photon
    from geopy.exc import GeocoderTimedOut
    import math

    def get_color(num):
        """
        (int) -> str
        Return a color depending on num
        >>> get_color(1)
        '#05fa20
        >>> get_color(1000)
        '#9e6120
        >>> get_color(10000)
        '#ff2020'
        """
        color = '#'
        red = int(num ** (1 / 2)*5)
        if red > 255:
            color += 'ff'
            red = 255
        else:
            color += '0' + hex(red)[2:] if red < 16 else hex(red)[2:]
        green = 255 - red
        color += '20' if green < 16 else hex(green)[2:]
        color += '20'
        return color

    geolocator = Photon()
    fmap = folium.Map(location=[49, 24], zoom_start=5)
    fg_films = folium.FeatureGroup(name='Фільми на %i рік'%year)
    fg_pp = folium.FeatureGroup(name='Населення країн')
    fg_pp.add_child(folium.GeoJson(data=open('world.json', 'r',
                                             encoding='utf-8-sig').read(),
                                   tooltip=folium.features.GeoJsonTooltip(
                                       fields=['NAME', 'POP2005'],
                                       aliases=['', '']),
                                   style_function=lambda x:
                                   {'opacity':0,
                                       'fillColor': '#f0f0f0' if
                                   x['properties']['POP2005'] < 10000000
                                   else '#b0b0b0' if
                                   x['properties']['POP2005'] < 50000000
                                   else '#808080' if
                                   x['properties']['POP2005'] < 100000000
                                   else '#404040' if
                                   x['properties']['POP2005'] < 500000000
                                   else '#101010'}))
    i = 0
    errors = 0
    total = len(locations.keys())
    bar = 20
    print("Generating map...")
    for address in locations.keys():
        i += 1
        percent = i / total
        print('\r[' + '▋' * int(percent * bar) +
              ' ' * (bar - int(percent * bar)) + ']' +
              str(int(percent * 100)) + '%', end='')
        try:
            location = geolocator.geocode(address)
            if location is None:
                location = geolocator.geocode(address[address.find(',')+2:])
            if location is not None:
                lat = location.latitude
                lon = location.longitude
                color = get_color(locations[address])
                fg_films.add_child(
                    folium.CircleMarker(location=[lat, lon],
                                        radius=4+int(
                                            math.sqrt(locations[address])/3),
                                        popup=address+': \n%i фільм(ів)' %
                                        locations[address],
                                        color=color,
                                        fill_color=color,
                                        fill_opacity=0.5,
                                        stroke=0
                                        ))
            else:
                errors += 1
        except GeocoderTimedOut:
            errors += 1
    print('\n %i found, %i errors' % (i-errors, errors))
    fmap.add_tile_layer(name='CartoDB', tiles='CartoDB')
    fmap.add_child(fg_pp)
    fmap.add_child(fg_films)
    fmap.add_child(folium.LayerControl())
    fmap.save('MoviesMap.html')

    return 0


def main():
    year = 0
    while(year <= 1850)or(year >= 2200):
        try:
            year = int(input('Input a year:'))
        except TypeError:
            print('Invalid input')
    films, num = read_data(year)
    print('%i films on %i addresses found for %i' %
          (num, len(films.keys()), year))
    create_map(year, films)
    print('Map created')
    return 0


main()
