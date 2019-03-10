/* JS Document */

/******************************

[Table of Contents]

4. Init SVG
5. Init Video
6. Init Google Map


******************************/

$(document).ready(function()
{
	"use strict";

    initImageSlider();
	initSvg();
	initVideo();
	initGoogleMap();


    /*

	4. initImageSlider

	*/
    function initImageSlider()
	{
		if($('.image_slider').length)
		{
			var homeSlider = $('.image_slider');
			homeSlider.owlCarousel(
			{
				items:1,
				autoplay:false,
				autoplayTimeout:8000,
				loop:true,
				dots:true,
				nav:false,
				mouseDrag:true,
				smartSpeed:1200
			});

			if($('.image_slider_nav_r').length)
			{
				var next = $('.image_slider_nav_r');
				next.on('click', function()
				{
					homeSlider.trigger('next.owl.carousel');
				});
			}
			if($('.image_slider_nav_l').length)
			{
				var previous = $('.image_slider_nav_l');
				previous.on('click', function()
				{
					homeSlider.trigger('prev.owl.carousel');
				});
			}
		}
	}

	/*

	4. Init SVG

	*/

	function initSvg()
	{
		if($('img.svg').length)
		{
			jQuery('img.svg').each(function()
			{
				var $img = jQuery(this);
				var imgID = $img.attr('id');
				var imgClass = $img.attr('class');
				var imgURL = $img.attr('src');

				jQuery.get(imgURL, function(data)
				{
					// Get the SVG tag, ignore the rest
					var $svg = jQuery(data).find('svg');

					// Add replaced image's ID to the new SVG
					if(typeof imgID !== 'undefined') {
					$svg = $svg.attr('id', imgID);
					}
					// Add replaced image's classes to the new SVG
					if(typeof imgClass !== 'undefined') {
					$svg = $svg.attr('class', imgClass+' replaced-svg');
					}

					// Remove any invalid XML tags as per http://validator.w3.org
					$svg = $svg.removeAttr('xmlns:a');

					// Replace image with new SVG
					$img.replaceWith($svg);
				}, 'xml');
			});
		}	
	}

	/* 

	5. Init Video

	*/

	function initVideo()
	{
		$(".youtube").colorbox(
		{
			iframe:true,
			innerWidth:640,
			innerHeight:409,
			maxWidth: '90%'
		});
	}

	/* 

	6. Init Google Map

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