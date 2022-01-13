	mapboxgl.accessToken = 'pk.eyJ1IjoiYmx1aXNmZXJuYW5kZXMiLCJhIjoiY2t0MjRvdmY2MGhrajJubzJ3NHdtNGFhbiJ9.ETbidupITC5LM0SD_JH57A';
	    const map = new mapboxgl.Map({
	        container: 'map',
	        style: 'mapbox://styles/mapbox/dark-v10',
	        center: [-70.65278285,-33.45468124995],
	        zoom: 12
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
						property: 'color',
						stops: [
							[0, '#f1f075'],
							[12294, '#e55e5e']
							]
					},
					'circle-opacity': 0.5
	            }
	        });
	    });


