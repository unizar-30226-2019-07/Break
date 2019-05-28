$(document).ready(function () {
    $(document).on('click', '.wishlist', function(e) {
        e.preventDefault();
        e.stopPropagation();
        var heart = this;
        if ($(this).hasClass('in_wishlist')) {
            $.ajax({
                url: '/ajax/' + $(this).data('type') + '/' + $(heart).data('id'),
                type: 'DELETE',
                success: function(data) {
                    $(heart).removeClass('in_wishlist');
                    heart.style.pointerEvents = "none";
                    $('.popup').remove();
                    $('body').append('<div class="popup bg-success text-light">Eliminado de la lista de deseos.</div>');
                    var popup = $('.popup');
                    setTimeout(function(){
                        popup.remove();
                        heart.style.pointerEvents = "auto";
                    }, 2500);
                },
                error: function (request, status, error) {
                    if (request.status == 401) {
                        location.reload();
                    }
                }
            });
        } else {
            $.ajax({
                url: '/ajax/' + $(this).data('type') + '/' + $(heart).data('id'),
                type: 'PUT',
                success: function(data) {
                    $(heart).addClass('in_wishlist');
                    $('.popup').remove();
                    $('body').append('<div class="popup bg-success text-light">Añadido a la lista de deseos.</div>');
                    var popup = $('.popup');
                    setTimeout(function(){
                        popup.remove();
                    }, 2500);
                },
                error: function (request, status, error) {
                    if (request.status == 401) {
                        $('.popup').remove();
                        $('body').append('<div class="popup bg-warning">Para poder añadir productos a tu lista de deseos debes <a href="/register">registrarte</a> o <a href="/login">iniciar sesión</a>.</div>');
                    }
                }
            });
        }
    });

    $(document).on('click', '.popup', function(){
        $(this).remove();
    });
});