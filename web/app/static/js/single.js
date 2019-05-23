/* JS Document */

/******************************

 [Table of Contents]

 4. Init SVG
 5. Init Video
 6. Init Google Map


 ******************************/

$(document).ready(function () {
    "use strict";

    initImageSlider();
    initSvg();
    initVideo();
    initGoogleMap();


    /*

	4. initImageSlider

	*/
    function initImageSlider() {
        if ($('.image_slider').length) {
            var homeSlider = $('.image_slider');
            homeSlider.owlCarousel(
                {
                    items: 1,
                    autoplay: false,
                    autoplayTimeout: 8000,
                    loop: false,
                    dots: true,
                    nav: false,
                    mouseDrag: true,
                    video: true,
                    merge: true,
                    center: true,
                    smartSpeed: 1200
                });

            if ($('.image_slider_nav_r').length) {
                var next = $('.image_slider_nav_r');
                next.on('click', function () {
                    homeSlider.trigger('next.owl.carousel');
                });
            }
            if ($('.image_slider_nav_l').length) {
                var previous = $('.image_slider_nav_l');
                previous.on('click', function () {
                    homeSlider.trigger('prev.owl.carousel');
                });
            }

            /*
            Para el video cuando se cambia de slide
            */
            homeSlider.on('translate.owl.carousel', function (e) {
                $('.owl-item video').each(function () {
                    $(this).get(0).pause();
                });
                /*
                Inicia el video cuando se cambia de slide
                */
            });
            homeSlider.on('translated.owl.carousel', function (e) {
                $('.owl-item.active video').get(0).play();
            })
        }

        if (!isMobile()) {
            $('.owl-item .item').each(function () {
                var attr = $(this).attr('data-videosrc');
                if (typeof attr !== typeof undefined && attr !== false) {
                    console.log('hit');
                    var videosrc = $(this).attr('data-videosrc');
                    $(this).prepend('<video><source src="' + videosrc + '" type="video/mp4"></video>');
                }
            });
            $('.owl-item.active video').attr('autoplay', false).attr('loop', false);
        }
    }


    /*

    4. Init SVG

    */

    function initSvg() {
        if ($('img.svg').length) {
            jQuery('img.svg').each(function () {
                var $img = jQuery(this);
                var imgID = $img.attr('id');
                var imgClass = $img.attr('class');
                var imgURL = $img.attr('src');

                jQuery.get(imgURL, function (data) {
                    // Get the SVG tag, ignore the rest
                    var $svg = jQuery(data).find('svg');

                    // Add replaced image's ID to the new SVG
                    if (typeof imgID !== 'undefined') {
                        $svg = $svg.attr('id', imgID);
                    }
                    // Add replaced image's classes to the new SVG
                    if (typeof imgClass !== 'undefined') {
                        $svg = $svg.attr('class', imgClass + ' replaced-svg');
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

    function initVideo() {
        $(".youtube").colorbox(
            {
                iframe: true,
                innerWidth: 640,
                innerHeight: 409,
                maxWidth: '90%'
            });
    }

    /*

    6. Init Google Map

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

function isMobile(width) {
    if (width == undefined) {
        width = 719;
    }
    if (window.innerWidth <= width) {
        return true;
    } else {
        return false;
    }
}


/***********************
 Editar anuncio
 ***********************/
function redirigirEditarProducto(isAuction) {
    if (isAuction == true) {
        window.location.href = "/single/" + productID + "/edit?isAuction=1";
    } else {
        window.location.href = "/single/" + productID + "/edit?isAuction=0";
    }
}

/***********************
 Borrar anuncio
 **********************/
function redirigirBorrarProducto(isAuction) {
    if (isAuction === true) {
        window.location.href = "/single/" + productID + "/delete?isAuction=1";
    } else {
        window.location.href = "/single/" + productID + "/delete?isAuction=0";
    }
}

/***********************
 Abrir un chat con el anuciante
 ***********************/
function abrirChat() {
    db = initializeFirebase();

    var tipoProducto = "sale";
    var tipo = "p";
    if (auction) {
        tipoProducto = "auction";
        tipo = "s";
    }

    var refChat = db.collection("chat").doc(tipo + productID + "_a" + anunID + "_c" + cliID);

    if (refChat.get().exists) {
        if (!refChat.get("visible").includes(otherId)) {
            var respuesta = refChat.update({
                visible: firebase.firestore.FieldValue.arrayUnion(cliID)
            });
        }
    } else {
        var respuesta = refChat.set({
            fechaUltimoMensaje: new Date(),
            idAnunciante: anunID,
            idCliente: cliID,
            idProducto: productID,
            tipoProducto: tipoProducto,
            ultimoMensaje: "",
            visible: [cliID]
        });
    }


    if (respuesta) {
        redirigirChat();
    }
}

/********************
 Abrir chat con el ganador de la subasta
 *******************/
function abrirChatGan() {
    db = initializeFirebase();

    tipoProducto = "auction";

    var refChat = db.collection("chat").doc("s" + productID + "_a" + anunID + "_c" + ganId);

    if (refChat.get().exists) {
        if (!refChat.get("visible").includes(otherId)) {
            var respuesta = refChat.update({
                visible: firebase.firestore.FieldValue.arrayUnion(anunID)
            });

            if (respuesta !== undefined) {
                redirigirChat();
            }
        }
    } else {
        var respuesta = refChat.set({
            fechaUltimoMensaje: new Date(),
            idAnunciante: anunID,
            idCliente: ganId,
            idProducto: productID,
            tipoProducto: tipoProducto,
            ultimoMensaje: "",
            visible: [anunID]
        });
        if (respuesta !== undefined) {
            redirigirChat();
        }
    }


}

function redirigirChat() {
    window.location.href = "/chat";
}

/***********************
 Inicializar firebase
 ***********************/
function initializeFirebase() {
    // Initialize Firebase
    var config = {
        apiKey: "AIzaSyBVkzjZBaHoupJYOl3MDMtrSyBAhpSfv6Q",
        authDomain: "selit-7d67c.firebaseapp.com",
        databaseURL: "https://selit-7d67c.firebaseio.com",
        projectId: "selit-7d67c",
        storageBucket: "selit-7d67c.appspot.com",
        messagingSenderId: "663470816058"
    };
    var app = firebase.initializeApp(config);

    // Return firestore database:
    return firebase.firestore(app);
}
