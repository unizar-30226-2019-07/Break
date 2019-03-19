/* JS Document */

/******************************

[Table of Contents]

4. Init Google Map
5. Preview Images


******************************/

$(document).ready(function()
{
	"use strict";

	initGoogleMap();

	/* 

	4. Init Google Map

	*/

	function initGoogleMap()
	{
		var myLatlng = new google.maps.LatLng(41.6517501, -0.9300004);
    	var mapOptions = 
    	{
    		center: myLatlng,
	       	zoom: 14,
			mapTypeId: google.maps.MapTypeId.ROADMAP,
			draggable: true,
			scrollwheel: false,
			zoomControl: true,
			zoomControlOptions:
			{
				position: google.maps.ControlPosition.RIGHT_CENTER
			},
			mapTypeControl: false,
			scaleControl: false,
			streetViewControl: false,
			rotateControl: false,
			fullscreenControl: true,
			styles:
			[
			  {
			    "featureType": "road.highway",
			    "elementType": "geometry.fill",
			    "stylers": [
			      {
			        "color": "#ffeba1"
			      }
			    ]
			  }
			]
    	}

    	// Initialize a map with options
    	map = new google.maps.Map(document.getElementById('map'), mapOptions);

		// Re-center map after window resize
		google.maps.event.addDomListener(window, 'resize', function()
		{
			setTimeout(function()
			{
				google.maps.event.trigger(map, "resize");
				map.setCenter(myLatlng);
			}, 1400);
		});
	}





});

/*

5. previewImages

*/
function previewImages() {

    var preview = document.querySelector('#preview');

    preview.innerHTML = "";

    if (this.files) {
        [].forEach.call(this.files, readAndPreview);
    }

    function readAndPreview(file) {

        // Make sure `file.name` matches our extensions criteria
        if (!/\.(jpe?g|png|gif)$/i.test(file.name)) {
        return alert(file.name + " is not an image");
    } // else...

    var reader = new FileReader();

    reader.addEventListener("load", function() {
        var new_picture = document.createElement("div");
        new_picture.className = "pic";

        var image = new Image();
        //image.height = 100;
        image.title  = file.name;
        image.src    = this.result;

        new_picture.appendChild(image)
        preview.appendChild(new_picture);
    });

    reader.readAsDataURL(file);

    }

}

document.querySelector('#file-input').addEventListener("change", previewImages);