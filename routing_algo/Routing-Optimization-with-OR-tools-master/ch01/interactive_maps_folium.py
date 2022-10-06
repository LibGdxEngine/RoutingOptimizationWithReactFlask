import folium
#solution
# coordinates = [
#     [24.433461, 54.432755], [24.427946, 54.437588],
#     [24.465393, 54.352466], [24.472863, 54.350427],
#     [24.478917, 54.354531], [24.482262, 54.353828],
#     [24.472605, 54.341227], [24.468474, 54.338513],
#     [24.490922, 54.359676], [24.491713, 54.356108],
#     [24.489013, 54.356993], [24.488262, 54.356039],
# ]

coordinates = [
        [24.433461, 54.432755],	[24.427946, 54.437588],
        [24.489013, 54.356993],	[24.488262, 54.356039],
        [24.490922, 54.359676],	[24.491713, 54.356108],
        [24.472605, 54.341227],	[24.468474, 54.338513],
        [24.478917, 54.354531],	[24.482262, 54.353828],
        [24.465393, 54.352466],	[24.472863, 54.350427],
]

m = folium.Map(location=[24.474516462298226, 54.41837428048304], zoom_start=13)
folium.PolyLine(coordinates, line_color='#FF0000', line_weight=5).add_to(m)
tooltip = "Click me!"
for index, coord in enumerate(coordinates):
    icon = None
    if index % 2 == 0:
        icon = folium.Icon(color="green", icon="one")
    else:
        icon = folium.Icon(color="red", icon="two")
    folium.Marker(
        coord, popup="<i>Mt. Hood Meadows</i>", tooltip=str(index+1),
        icon=icon
    ).add_to(m)
m.save("index2.html")
