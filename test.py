import folium
from geopy.geocoders import GeoNames


def get_color(num):
    """
    (int) -> str
    Return a color depending on num
    >>> get_color(1)
    '#05fa20
    """
    color = '#'
    red = int(num ** (1 / 2) * 5)
    if red > 255:
        color += 'ff'
        red = 255
    else:
        color += '0' + hex(red)[2:] if red < 16 else hex(red)[2:]
    green = 255 - red
    color += '20' if green < 16 else hex(green)[2:]
    color += '20'
    return color

def main():
    geolocator = GeoNames(username='cauron')
    print('start')
    print('done')
    testmap = folium.Map(location=[49,24], zoom_start=5)
    fg_pp = folium.FeatureGroup(name='Населення країн')
    fg_pp.add_child(folium.GeoJson(data=open('world.json', 'r',
                                                 encoding='utf-8-sig').read(),
                                       style_function=lambda x:
                                       {'fillColor': 'red' if x['properties']['POP2005']<10000000
                                       else '#404040' if x['properties']['POP2005']<50000000
                                       else 'red' if x['properties']['POP2005']<100000000
                                       else 'green' if x['properties']['POP2005']<500000000
                                       else 'yellow'}))
    i = 0
    for i in range(50):
        c = i**2 * i
        testmap.add_child(folium.CircleMarker(location=[i,i],
                                              popup=str(c)+get_color(c),
                                              radius=10,
                                              fill_color=get_color(c),
                                              fill_opacity=1))
    testmap.add_child(fg_pp)
    testmap.save('Map1.html')


for i in range(1000):
    print(i*10, get_color(i*10))