	mapboxgl.accessToken = 'pk.eyJ1IjoiYmx1aXNmZXJuYW5kZXMiLCJhIjoiY2t0MjRvdmY2MGhrajJubzJ3NHdtNGFhbiJ9.ETbidupITC5LM0SD_JH57A';
	    const map = new mapboxgl.Map({
	        container: 'map',
	        style: 'mapbox://styles/bluisfernandes/ckyj5i1p12jb214q9arw9dsyf',
	        center: [-70.599517, -33.416503],
	        zoom: 14
	    });

	    const geojson1 = {{ geojson }}



	    map.on('load', () => {
	        map.addSource('national-park', {
	            'type': 'geojson',
	            'data': geojson1
	        });


	        map.addLayer({
	            'id': 'x',
	            'type': 'circle',
	            'source': 'national-park',
	            'paint': {

	                'circle-radius': {
						'base': 1.75,
						'stops': [
							[12, 2],
							[22, 180]
							]
	                },
					'circle-color': {
						property: 'sensor',
						stops: [
							[0, '#e55e5e'],
							[12294, '#f1f075']
							]
					},
					'circle-opacity': 0.5
	            }
	        });
	    });


