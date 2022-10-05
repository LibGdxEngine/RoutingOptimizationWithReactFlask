import React, {useRef, useEffect, useState} from 'react';
import mapboxgl from 'mapbox-gl';
import './App.css'
import RoutingButton from "./componenets/RoutingButton";

mapboxgl.accessToken = 'pk.eyJ1Ijoicm9oaXRpaWMiLCJhIjoiY2t2eGkyanJ3Y2c2azMwczdtOGppa3N5ZyJ9.G4VtowYp1GEpWxvh3nRFVQ';

const App = () => {
    const mapContainer = useRef(null);
    const map = useRef(null);
    const [lng, setLng] = useState(54.363816);
    const [lat, setLat] = useState(24.463347);
    const [zoom, setZoom] = useState(13);
    const start = [lng, lat];
    const [selectedPoints, setSelectedPoints] = useState([]);
    const redColor = "#f30";
    const greenColor = "#2dc506";

    useEffect(() => {
        if (map.current) return; // initialize map only once
        map.current = new mapboxgl.Map({
            container: mapContainer.current,
            style: 'mapbox://styles/mapbox/streets-v11',
            center: [lng, lat],
            zoom: zoom
        });
        map.current.on('move', () => {
            setLng(map.current.getCenter().lng.toFixed(4));
            setLat(map.current.getCenter().lat.toFixed(4));
            setZoom(map.current.getZoom().toFixed(2));
        });

        map.current.on('load', () => {
            // make an initial directions request that
            // starts and ends at the same location
            // getRoute(start);

            // Add starting point to the map
            map.current.addLayer({
                id: 'point',
                type: 'circle',
                source: {
                    type: 'geojson',
                    data: {
                        type: 'FeatureCollection',
                        features: [
                            {
                                type: 'Feature',
                                properties: {},
                                geometry: {
                                    type: 'Point',
                                    coordinates: start
                                }
                            }
                        ]
                    }
                },
                paint: {
                    'circle-radius': 10,
                    'circle-color': '#3887be'
                }
            });

            map.current.once('click', (event) => {
                const coords = Object.keys(event.lngLat).map((key) => event.lngLat[key]);

                setSelectedPoints([...selectedPoints, coords]);

                map.current.addLayer({
                    id: 'end' + Math.random(),
                    type: 'circle',
                    source: {
                        type: 'geojson',
                        data: {
                            type: 'FeatureCollection',
                            features: [
                                {
                                    type: 'Feature',
                                    properties: {},
                                    geometry: {
                                        type: 'Point',
                                        coordinates: coords
                                    }
                                }
                            ]
                        }
                    },
                    paint: {
                        'circle-radius': 10,
                        'circle-color': '#2dc506'
                    }
                });
            });
        });
    }, [map.current]);

    useEffect(() => {
        const handleMapClick = (event) => {
            const coords = Object.keys(event.lngLat).map((key) => event.lngLat[key]);
            setSelectedPoints([...selectedPoints, coords]);
            let pointColor = "";
            if (selectedPoints.length % 2 === 0) {
                pointColor = greenColor;
            } else {
                pointColor = redColor;
            }

            map.current.addLayer({
                id: 'end' + Math.random(),
                type: 'circle',
                source: {
                    type: 'geojson',
                    data: {
                        type: 'FeatureCollection',
                        features: [
                            {
                                type: 'Feature',
                                properties: {},
                                geometry: {
                                    type: 'Point',
                                    coordinates: coords
                                }
                            }
                        ]
                    }
                },
                paint: {
                    'circle-radius': 10,
                    'circle-color': pointColor
                }
            });
        };

        map.current.once('click', handleMapClick);
    }, [selectedPoints]);

    const getDistanceMatrix = async (points) => {
        let my_points = points.join(';');
        console.log(my_points);
        const response = await fetch(`https://api.mapbox.com/directions-matrix/v1/mapbox/driving/${my_points}?&access_token=pk.eyJ1IjoiYWhtZWRmYXRoeXphaW4iLCJhIjoiY2w4YzZ0Z2U2MGptdjN2bXJlbnY4MTBvMiJ9.Luaz1LmJCCPD72lY3MKNZA&annotations=distance`)
        const json = await response.json();
        return json
    }

    function getDarkColor() {
        var color = '#';
        for (var i = 0; i < 6; i++) {
            color += Math.floor(Math.random() * 10);
        }
        return color;
    }

    async function getRoute(start_point, end_point) {
        const query = await fetch(
            `https://api.mapbox.com/directions/v5/mapbox/driving/${start_point[0]},${start_point[1]};${end_point[0]},${end_point[1]}?steps=true&geometries=geojson&access_token=${mapboxgl.accessToken}`,
            {method: 'GET'}
        );
        const json = await query.json();
        const data = json.routes[0];
        const route = data.geometry.coordinates;
        let randomColor = Math.floor(Math.random() * 16777215).toString(16);
        // let randomColor = "3887be";
        const geojson = {
            type: 'Feature',
            properties: {},
            geometry: {
                type: 'LineString',
                coordinates: route
            }
        };

        map.current.addLayer({
            id: 'route' + Math.random(),
            type: 'line',
            source: {
                type: 'geojson',
                data: geojson
            },
            layout: {
                'line-join': 'round',
                'line-cap': 'round'
            },
            paint: {
                'line-color': getDarkColor(),
                'line-width': 3,
                'line-opacity': 0.75
            }
        });

        // get the sidebar and add the instructions
        const instructions = document.getElementById('instructions');
        const steps = data.legs[0].steps;

        let tripInstructions = '';
        for (const step of steps) {
            tripInstructions += `<li>${step.maneuver.instruction}</li>`;
        }
        instructions.innerHTML += `<p><strong>Trip duration: ${Math.floor(
            data.duration / 60
        )} min 🚗 </strong></p><ol>${tripInstructions}</ol>`;

    }

    function drawStraightLine(route) {
        const geojson = {
            type: 'Feature',
            properties: {},
            geometry: {
                type: 'LineString',
                coordinates: route
            }
        };

        map.current.addLayer({
            id: 'route' + Math.random(),
            type: 'line',
            source: {
                type: 'geojson',
                data: geojson
            },
            layout: {
                'line-join': 'round',
                'line-cap': 'round'
            },
            paint: {
                'line-color': "#000000",
                'line-width': 3,
                'line-opacity': 0.3,
                'line-dasharray': [2, 2],
            }
        });
    }

    const handleRouteBtnClick = async (event) => {
        let routes_list;
        try {
            getDistanceMatrix([start, ...selectedPoints]).then((data) => {
                fetch("/points", {method: 'POST', body: data['distances']}).then((res) =>
                    res.json().then((data) => {
                        // Setting a data from api
                        routes_list = data['routes'][0];
                        const points_list = [start, ...selectedPoints]

                        for (let counter = 0; counter < points_list.length - 1; counter += 1) {
                            if (counter % 2 === 0) {
                                const start_point = points_list[routes_list[counter]];
                                const end_point = points_list[routes_list[counter + 1]];
                                getRoute(start_point, end_point);
                            } else {
                                const start_point = points_list[routes_list[counter]];
                                const end_point = points_list[routes_list[counter + 1]];
                                drawStraightLine([start_point, end_point]);
                            }
                        }

                    })
                );
            });

        } catch
            (err) {
            console.log(err.message + " Exception error");
        }
    };

    return (
        <>
            <div ref={mapContainer} className="map-container"/>
            <RoutingButton onClick={handleRouteBtnClick} className="routing-button">Move</RoutingButton>
            <div id="instructions" className="instructions"></div>
        </>
    );
};

export default App;