/* JS Document */

/*******************************************************************************
 *
 * [Table of Contents]
 *
 * 4. Init Milestones
 *
 *
 * *****************************/

$(document)
    .ready(
        function () {
            "use strict";

            initMilestones();

            /*

            4. Init Milestones

             */

            function initMilestones() {
                if ($('.milestone_counter').length) {
                    var milestoneItems = $('.milestone_counter');

                    milestoneItems
                        .each(function (i) {
                            var ele = $(this);
                            var endValue = ele.data('end-value');
                            var eleValue = ele.text();

                            /* Use data-sign-before and data-sign-after to add signs
                            infront or behind the counter number */
                            var signBefore = "";
                            var signAfter = "";

                            if (ele.attr('data-sign-before')) {
                                signBefore = ele
                                    .attr('data-sign-before');
                            }

                            if (ele.attr('data-sign-after')) {
                                signAfter = ele
                                    .attr('data-sign-after');
                            }

                            var milestoneScene = new ScrollMagic.Scene(
                                {
                                    triggerElement: this,
                                    triggerHook: 'onEnter',
                                    reverse: false
                                })
                                .on(
                                    'start',
                                    function () {
                                        var counter = {
                                            value: eleValue
                                        };
                                        var counterTween = TweenMax
                                            .to(
                                                counter,
                                                4,
                                                {
                                                    value: endValue,
                                                    roundProps: "value",
                                                    ease: Circ.easeOut,
                                                    onUpdate: function () {
                                                        document
                                                            .getElementsByClassName('milestone_counter')[i].innerHTML = signBefore
                                                            + counter.value
                                                            + signAfter;
                                                    }
                                                });
                                    }).addTo(ctrl);
                        });
                }
            }

        });