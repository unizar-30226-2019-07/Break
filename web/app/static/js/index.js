/* JS Document */

/******************************

[Table of Contents]

4. Init Home Slider
5. Init Google Map
6. Init Testimonials Slider


******************************/

$(document).ready(function()
{
	"use strict";

	initHomeSlider();
	initGoogleMap();
	initTestSlider();

	/* 

	4. Init Home Slider

	*/

	function initHomeSlider()
	{
		if($('.home_slider').length)
		{
			var homeSlider = $('.home_slider');
			homeSlider.owlCarousel(
			{
				items:1,
				autoplay:true,
				autoplayTimeout:8000,
				loop:true,
				dots:false,
				nav:false,
				mouseDrag:false,
				smartSpeed:1200
			});

			if($('.home_slider_nav').length)
			{
				var next = $('.home_slider_nav');
				next.on('click', function()
				{
					homeSlider.trigger('next.owl.carousel');
				});
			}
		}
	}

	/* 

	5. Init Google Map

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
			zoomControl: false,
			zoomControlOptions:
			{
				position: google.maps.ControlPosition.RIGHT_CENTER
			},
			mapTypeControl: false,
			scaleControl: false,
			streetViewControl: false,
			rotateControl: false,
			fullscreenControl: false,
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

		function newLocation(newLat, newLng)
		{
			map.setCenter(
			{
				lat : newLat,
				lng : newLng
			});
		}

		var locationList = $('.location_contaner');
		locationList.each(function()
		{
			var loc = $(this);
			loc.on('click', function()
			{
				var newLat = loc.data('lat');
				var newLng = loc.data('lng');
				newLocation(newLat, newLng);
			});
				
		});
	}

	/* 

	6. Init Testimonials Slider

	*/

	function initTestSlider()
	{
		if($('.test_slider').length)
		{
			var testSlider = $('.test_slider');
			testSlider.owlCarousel(
			{
				items:1,
				autoplay:true,
				autoplayHoverPause:true,
				loop:true,
				nav:false,
				dots:true,
				smartSpeed:1200
			});
		}
	}

});