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

});