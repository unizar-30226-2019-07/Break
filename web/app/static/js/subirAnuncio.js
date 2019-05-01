/* JS Document */

/******************************

 [Table of Contents]

 4. Init Google Map
 5. Preview Images


 ******************************/

$(document).ready(function () {
    "use strict";

    initGoogleMap();
    previewImages();

    /*

    4. Init Google Map

    */

    function initGoogleMap() {
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
        google.maps.event.addDomListener(window, 'resize', function () {
            setTimeout(function () {
                google.maps.event.trigger(map, "resize");
                map.setCenter(myLatlng);
            }, 1400);
        });
    }


});

/*

5. previewImages

*/
var numPitures = 0;
var MAX_NUM_PICTURES = 10;

function previewImages() {

    var preview = document.querySelector('#preview');

    // preview.innerHTML = "";

    if (this.files) {
        [].forEach.call(this.files, readAndPreview);
    }
    this.value = "";

    function readAndPreview(file) {

        // Make sure `file.name` matches our extensions criteria
        if (numPitures < MAX_NUM_PICTURES) {

            var reader = new FileReader();
            var type = file.type;

            reader.addEventListener("load", function () {
                var new_picture = document.createElement("div");
                new_picture.className = "col-4 col-md-3 col-lg-2 sortable";
                container = document.createElement("div");

                var image = document.createElement("div");
                image.style.backgroundImage = "url(" + this.result + ")";

                container.appendChild(image)
                new_picture.appendChild(container)

                new_picture.insertAdjacentHTML('beforeend',
                    '<div class="row"><i class="fas fa-arrow-left col-4"></i><i class="fas fa-trash col-4"></i><i class="fas fa-arrow-right col-4"></i></div>');

                picture = document.createElement('input');
                picture.type = 'hidden';
                picture.name = 'base64[]';
                picture.value = this.result.replace(/^data:.+;base64,/, "");

                new_picture.appendChild(picture)

                mime = document.createElement('input');
                mime.type = 'hidden';
                mime.name = 'mime[]';
                mime.value = type;

                new_picture.appendChild(mime)

                idImagen = document.createElement('input');
                idImagen.type = 'hidden';
                idImagen.name = 'idImagen[]';
                idImagen.value = 0;

                new_picture.appendChild(idImagen)

                preview.appendChild(new_picture);
            });

            reader.readAsDataURL(file);
            numPitures = numPitures + 1;
            if (numPitures >= MAX_NUM_PICTURES) {
                document.getElementById('file-input').setAttribute("disabled", true);
            }
        }
    }
}

document.getElementById('file-input').addEventListener("change", previewImages);

/*

6. Show number of files.

*/

/*
	By Osvaldas Valutis, www.osvaldas.info
	Available for use under the MIT License
*/
'use strict';

;(function (document, window, index) {
    var inputs = document.querySelectorAll('.inputfile');
    Array.prototype.forEach.call(inputs, function (input) {
        var label = input.nextElementSibling,
            labelVal = label.innerHTML;

        input.addEventListener('change', function (e) {
            /*
            var fileName = '';
            if( this.files && this.files.length > 1 )
                fileName = ( this.getAttribute( 'data-multiple-caption' ) || '' ).replace( '{count}', this.files.length );
            else
                fileName = "1 imagen seleccionada";

            if( fileName )
                label.querySelector( 'span' ).innerHTML = fileName;
            else
                label.innerHTML = labelVal;
            */
        });

        // Firefox bug fix
        input.addEventListener('focus', function () {
            input.classList.add('has-focus');
        });
        input.addEventListener('blur', function () {
            input.classList.remove('has-focus');
        });
    });
}(document, window, 0));

$(document).on('click', '.sortable .fa-arrow-right', function (event) {
    var element = $(this).closest('.sortable');
    element.before(element.next());
});

$(document).on('click', '.sortable .fa-arrow-left', function (event) {
    var element = $(this).closest('.sortable');
    element.after(element.prev());
});

$(document).on('click', '.sortable .fa-trash', function (event) {
    var element = $(this).closest('.sortable');
    element.remove();
});