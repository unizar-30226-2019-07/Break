/* JS Document */

/******************************

[Table of Contents]

4. Init Google Map
5. Preview Images


******************************/

$(document).ready(function()
{
	"use strict";

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