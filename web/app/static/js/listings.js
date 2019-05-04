/* JS Document */

/******************************

 [Table of Contents]

 4. Init Isotope


 ******************************/

$(document).ready(function () {
    "use strict";

    initIsotope();

    /*

    4. Init Isotope

    */

    function initIsotope() {
        if ($('.listings_container').length) {
            var grid = $('.listings_container');
            grid.isotope(
                {
                    itemSelector: '.listing_box',
                    layoutMode: 'fitRows',
                    getSortData:
                        {
                            price: function (itemElement) {
                                var priceEle = $(itemElement).find('.listing_price').text().replace('$', '');
                                priceEle = priceEle.replace(/\s/g, '');
                                return parseFloat(priceEle);
                            },
                            area: function (itemElement) {
                                var propertyArea = $(itemElement).find('.property_area span').text().replace(' sq ft', '');
                                console.log(propertyArea);
                                return parseFloat(propertyArea);
                            }
                        }
                });

            var sortingButtons = $('.sorting_button');

            sortingButtons.each(function () {
                $(this).on('click', function () {
                    var parent = $(this).parent().parent().find('span');
                    parent.text($(this).text());
                    var option = $(this).attr('data-isotope-option');
                    option = JSON.parse(option);
                    grid.isotope(option);
                });
            });
        }
    }

    $(document).on('click', '.tab', function(e){
        var tab = $(this);
        var target = $(this).data('target');
        document.location.hash = target;
        $(target).load(location.href + " " + target + "_inner", function(){
            var length = $(target).find('.listing').length;
            tab.find('span').text( function(i,txt) {return txt.replace(/\d+/, length); });
        });
    });

    var url = document.location.toString();
    if ( url.match('#') ) {
        $('#'+url.split('#')[1]).collapse('show');
    }
});