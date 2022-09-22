import React, {useRef, useEffect, useState} from 'react';
import mapboxgl from 'mapbox-gl';
import './App.css'
import RoutingButton from "./componenets/RoutingButton";

mapboxgl.accessToken = 'pk.eyJ1Ijoicm9oaXRpaWMiLCJhIjoiY2t2eGkyanJ3Y2c2azMwczdtOGppa3N5ZyJ9.G4VtowYp1GEpWxvh3nRFVQ';

const App = () => {
    const mapContainer = useRef(null);
    const map = useRef(null);
    const [lng, setLng] = useState(54.365278);
    const [lat, setLat] = useState(24.467791);
    const [zoom, setZoom] = useState(12);
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


    async function getRoute(end) {
        const query = await fetch(
            `https://api.mapbox.com/directions/v5/mapbox/driving/${start[0]},${start[1]};${end[0]},${end[1]}?steps=true&geometries=geojson&access_token=${mapboxgl.accessToken}`,
            {method: 'GET'}
        );
        const json = await query.json();
        const data = json.routes[0];
        const route = data.geometry.coordinates;
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
                'line-color': '#3887be',
                'line-width': 5,
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
        )} min 🚴 </strong></p><ol>${tripInstructions}</ol>`;

    }

    const handleRouteBtnClick = async (event) => {
            try {
                fetch("/points", {method: 'POST', body: selectedPoints}).then((res) =>
                    res.json().then((data) => {
                        // Setting a data from api
                        console.log(data);
                    })
                );
            } catch
                (err) {
                console.log(err.message + " Exception error");
            }

            for (let counter = 0; counter < selectedPoints.length; counter += 1) {
                const coords = [...selectedPoints[counter]];
                console.log(coords);
                getRoute(coords);
            }
        }
    ;

    return (
        <>
            <div ref={mapContainer} className="map-container"/>
            <RoutingButton onClick={handleRouteBtnClick} className="routing-button">Move</RoutingButton>
            <div id="instructions" className="instructions"></div>
        </>
    );
};

export default App;