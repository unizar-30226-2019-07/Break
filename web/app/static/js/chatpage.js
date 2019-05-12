// ----------------------------------------------------
// Variables globales:
// ----------------------------------------------------
var db;
var myID;
const api = "http://35.234.77.87:8080";
const TIMEOUT = 5000;

var productoActual;
var anunID;
var cliID;

class Message {
    constructor(id, contenido, estado, fecha, idEmisor) {
        this.id = id;
        this.contenido = contenido;
        this.estado = estado;
        this.fecha = fecha;
        this.idEmisor = idEmisor;
    }
}

// ----------------------------------------------------
// Targeted Elements
// ----------------------------------------------------
const chatBody = $(document);
const chatRoomsList = $('#rooms');
const chatReplyMessage = $('#replyMessage');
const chatScrollMessageDiv = "msg_scroll";


// ----------------------------------------------------
// Inicialize scripts.
// ----------------------------------------------------
$(document)
    .ready(
        function () {
            'use strict';

            initializeFirebase();

            // ----------------------------------------------------
            // Register page event listeners
            // ----------------------------------------------------
            chatBody.ready(loadChatManager);
            chatReplyMessage.on('submit', replyMessage);
            chatRoomsList.on('click', 'a', loadChatRoom);
        });


/**
 * Limpiar los mensajes del chat
 */
function clearChatMessages() {
    $('#chat-msgs').html('');
}

/**
 * Mostrar un nuevo mensaje en la ventana de mensajes
 */
function displayChatMessage(message) {
    // Si el mensaje no está
    if (document.getElementById(message.id) === null) {
        var envio = "sender";
        if (message.idEmisor === myID) {
            envio = "me";
        }
        var fecha = convertTimestamp(message.fecha);

        $('#chat-msgs').append(
            `<div class="messages-bubble ${envio}-bubble" id="${message.id}">
                        <div class="">${message.contenido}</div>
                        <div> ${message.estado}@ <span class="date">${fecha}</span></div>
                        <div class="${envio}-bubble-ds-arrow"></div>
                </div>`
        );

        var objDiv = document.getElementById(chatScrollMessageDiv);
        objDiv.scrollTop = objDiv.scrollHeight;
    }
}

function convertTimestamp(timestamp) {
    var d = new Date(timestamp.seconds * 1000);	// Convert the passed timestamp to milliseconds
    var yyyy = d.getFullYear();
    var mm = ('0' + (d.getMonth() + 1)).slice(-2);	// Months are zero based. Add leading 0.
    var dd = ('0' + d.getDate()).slice(-2);		// Add leading 0.
    var hh = d.getHours();
    var h = hh;
    var min = ('0' + d.getMinutes()).slice(-2);		// Add leading 0.
    //var ampm = 'AM';

    /* American version:
    if (hh > 12) {
        h = hh - 12;
        ampm = 'PM';
    } else if (hh === 12) {
        h = 12;
        ampm = 'PM';
    } else if (hh == 0) {
        h = 12;
    }*/

    // ie: 2013-02-18, 8:35 AM
    var time = dd + '-' + mm + '-' + yyyy + ', ' + h + ':' + min; // + ' ' + ampm

    return time;
}

/**
 * Cargar to_dos los mensajes de un chat
 */
function loadChatRoom(evt) {
    // Limpiamos los mensajes del html.
    clearChatMessages();

    // Id del producto pulsado
    var roomId = evt.currentTarget.id;
    var productId = evt.currentTarget.name;
    var tipoProducto;

    if (roomId !== undefined) {
        $('.response').show();
        $('#room-title').text("Producto Prueba " + roomId);

        // Obtener datos del producto:
        refProducto = db.collection("chat").doc(roomId);
        refProducto.get().then(function (doc) {
            if (doc.exists) {
                let producto = doc.data();
                productoActual = producto.idProducto;
                cliID = producto.idCliente;
                anunID = producto.idAnunciante;
                tipoProducto = producto.tipoProducto;

            } else {
                // doc.data() will be undefined in this case
                console.log("No such document!");
            }
        }).then(function () {
            try {
                if (tipoProducto === "sale") {
                    httpGet(api + "/products/" + productId, mostrarChatRoom, [roomId, false]);
                } else {
                    httpGet(api + "/auctions/" + productId, mostrarChatRoom, [roomId, true]);
                }

            } catch
                (err) {
                console.log("Fallo al cargar elemento");
            }
        })
    }
    evt.preventDefault();
}

function mostrarChatRoom(response, [roomId, esSubasta]) {
    producto = JSON.parse(response);

    // Mostrar el usuario con el que se conversa en la parte superior
    if (producto.owner.picture.idImagen !== null) {
        imagen = api + '/pictures/' + (producto.owner.picture.idImagen);
    } else {
        imagen = "gravatar.get(" + producto.owner.email + ")";
    }


    $('#other_user').html('')

    $('#other_user').append(
        `<div class="user-bubble row">
        <div class="col-3 user-image"
            style="background-image: url(${imagen})"></div>
         <div class="col-8 row">
            <strong class="title-bubble-white">${producto.owner.first_name} ${producto.owner.last_name}</strong>   
         </div>     
    </div>`
    );



// Mensajes pruebas creados para probar la interfaz
refMensajes = db.collection("chat").doc(roomId).collection("mensaje").orderBy("fecha");

refMensajes
    .onSnapshot(function (snapshot) {
        snapshot.docChanges().forEach(function (change) {
            if (change.type === "added") {
                var contenido = change.doc.get("contenido");
                var estado = change.doc.get("estado");
                var fecha = change.doc.get("fecha");
                var idEmisor = change.doc.get("idEmisor");

                displayChatMessage(new Message(change.doc.id, contenido, estado, fecha, idEmisor));
            }
            /*
            if (change.type === "modified") {
                // Mensaje modificado.
                // No hace nada. Si en el futuro se quiere implementar algo
            }
            if (change.type === "removed") {
                // Mensaje eliminado
                // No hace nada. Si en el futuro se quiere implementar algo
            }
            */
        });
    });
}


/**
 * Contestar con un mensaje:
 */
function replyMessage(evt) {
    evt.preventDefault();

    const message = $('#replyMessage input')
        .val()
        .trim();

    if (message !== "") {
        var date = new Date();

        //displayChatMessage(msg);
        console.log("p" + productoActual + "_a" + anunID + "_c" + cliID);
        refMessage = db.collection("chat").doc("p" + productoActual + "_a" + anunID + "_c" + cliID).collection("mensaje");
        refMessage.add({
            contenido: message, estado: "enviado", fecha: date,
            idEmisor: myID
        })
            .then(function (docRef) {
                console.log("Document written with ID: ", docRef.id);
            })
            .catch(function (error) {
                console.error("Error adding document: ", error);
            });

        // Limpiar Barra:
        $('#replyMessage input').val('');
    }
}


/**
 * Cargar la lista de chats
 */
function loadChatManager() {
    // Obtener todos los chats y poner un link en la sidebar...
    refChats = db.collection("chat");

    refChats.get()
        .then(function (querySnapshot) {

                querySnapshot.forEach(function (doc) {
                    var visible = doc.get("visible");
                    if(visible.includes(myID)){
                        var idProducto = doc.get("idProducto");
                        var tipoProducto = doc.get("tipoProducto");

                        try {

                            if (tipoProducto === "sale") {
                                httpGet(api + "/products/" + idProducto, mostrarChatBubble, [doc, false]);
                            } else {
                                httpGet(api + "/auctions/" + idProducto, mostrarChatBubble, [doc, true]);
                            }
                        } catch
                            (err) {
                            console.log("Fallo al cargar elemento");
                            console.log(err);
                        }
                    }
                });
            }
        )
        .catch(function (error) {
            console.log("Error getting documents: ", error);
        });
}


function mostrarChatBubble(response, [doc, esSubasta]) {
    producto = JSON.parse(response);
    try {
        imagen = api + '/pictures/' + (producto.media[0].idImagen);
    } catch (err) {
        imagen = "static/images/items.svg";
    }

    if (esSubasta) {
        idProducto = producto.idSubasta;
    } else {
        idProducto = producto.id_producto;
    }


    if (producto.status === "en venta") {
        $('#rooms').append(
            `<a href="#" onclick="return false;" id="${doc.id}" name="${idProducto}">
                <div class="producto-bubble row">
         
                    <div class="col-3 product-image"
                        style="background-image: url(${imagen})"></div>
                     <div class="col-8 row">
                        <strong class="title-bubble">${producto.title}</strong>
                        <strong class="subtitle-bubble">${producto.owner.first_name} ${producto.owner.last_name}</strong>       
                     </div>     
                </div>
            </a>`
        );
    }
}

function searchChats() {
    var input, filter, table, tr, td, i, txtValue;
    input = document.getElementById("inputSearchChat");
    filter = input.value.toUpperCase();
    table = document.getElementById("rooms");
    tr = table.getElementsByTagName("a");
    for (i = 0; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("div")[0];
        if (td) {
            txtValue = td.textContent || td.innerText;
            if (txtValue.toUpperCase().indexOf(filter) > -1) {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            }
        }
    }
}

/**
 * Hace una petición a la URL, cuando recibe la respuesta llama a callback con la respuesta. Se puede
 * pasar a callback argumentos (cArgumenst) extra.
 * @param sUrl
 * @param callback
 * @param cArguments
 */
function httpGet(sUrl, callback, cArguments) {
    var xhr = new XMLHttpRequest();
    xhr.ontimeout = function () {
        console.error("The request for " + url + " timed out.");
    };
    xhr.onload = function () {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                callback(xhr.responseText, cArguments);
            } else {
                console.error(xhr.statusText);
            }
        }
    };
    xhr.open("GET", sUrl, true);
    xhr.timeout = TIMEOUT;
    xhr.send(null);
}


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
    db = firebase.firestore(app);

    const messaging = firebase.messaging();
    messaging.requestPermission()
        .then(function () {
            console.log("Tenemos permiso");
            console.log(messaging.getToken());
            return messaging.getToken();
        })
        .then(function (token) {
            //console.log(token);
        })
        .catch(function (err) {
            console.log("Error Ocurred");
        })

    messaging.onMessage(function (payload) {
        console.log('onMessage: ', payload);
    })
}