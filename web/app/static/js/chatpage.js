// ----------------------------------------------------
// Variables globales:
// ----------------------------------------------------
var db;
var messaging;
var myTokenMessage;
var myID;
const API = "https://selit.naval.cat:8443";
const TIMEOUT = 5000;

var productoActual;
var idProductoActual;
var anunID;
var cliID;
var otherId;
var tipoProducto;

var escucharMensajes;


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
const chatMessages = $('#chat-msgs');
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
    chatMessages.html('');
}

/**
 * Mostrar día de los mensajes.
 */
function displayDateMessage(fecha) {
    chatMessages.append(
        `<div class="messages-bubble-date">
            ${fecha}
        </div>`
    );
}

/**
 * Mostrar un nuevo mensaje en la ventana de mensajes
 */
function displayChatMessage(message, fechaUltimoMensaje) {
    // Si el mensaje no está
    if (document.getElementById(message.id) === null) {
        // Quien manda el mensaje
        var envio = (message.idEmisor === myID ? "me" : "sender");

        [tiempo, dd, mm, yyyy] = convertTimestamp(message.fecha);

        // Mostrar el día cuando este cambia. Se muestra entre dos mensajes:
        if (fechaUltimoMensaje === undefined) {
            displayDateMessage(dd + '-' + mm + '-' + yyyy);
        } else {
            [fechaAntes, ddAntes, mmAntes, yyyyAntes] = convertTimestamp(fechaUltimoMensaje);
            if (ddAntes !== dd || mmAntes !== mm || yyyyAntes !== yyyy) {
                displayDateMessage(dd + '-' + mm + '-' + yyyy);
            }
        }

        // Si el mensaje ha sido recibido o no.
        var estado = (message.estado === "recibido" ? '<i class="fas fa-check-double"></i>' : '<i class="fas fa-check"></i>');

        $('#chat-msgs').append(
            `<div class="col-12">
                <div class="messages-bubble ${envio}-bubble" id="${message.id}">
                     <div>${message.contenido}</div>
                     <div class="me-bubble-date"> 
                        <span id="${message.id}-estado">${estado}</span> 
                        <span class="date">${tiempo}</span>
                     </div>
                     <div class="${envio}-bubble-ds-arrow"></div>
                </div>
            </div>`
        );

        var objDiv = document.getElementById(chatScrollMessageDiv);
        objDiv.scrollTop = objDiv.scrollHeight;
    }
}

/**
 * Convertir timestamp a tiempo legible.
 */
function convertTimestamp(timestamp) {
    var d = new Date(timestamp.seconds * 1000);	// Convert the passed timestamp to milliseconds
    var yyyy = d.getFullYear();
    var mm = ('0' + (d.getMonth() + 1)).slice(-2);	// Months are zero based. Add leading 0.
    var dd = ('0' + d.getDate()).slice(-2);		// Add leading 0.
    var hh = d.getHours();
    var h = hh;
    var min = ('0' + d.getMinutes()).slice(-2);		// Add leading 0.

    /* American version:
    var ampm = 'AM';
    if (hh > 12) {
        h = hh - 12;
        ampm = 'PM';
    } else if (hh === 12) {
        h = 12;
        ampm = 'PM';
    } else if (hh == 0) {
        h = 12;
    }*/

    var time = h + ':' + min; // + ' ' + ampm

    return [time, dd, mm, yyyy];
}

/**
 * Cargar to_dos los mensajes de un chat
 */
function loadChatRoom(evt) {
    // Dejamos de escuchar mensajes (si estabamos).
    if (escucharMensajes !== undefined) {
        escucharMensajes();
    }
    // Limpiamos los mensajes del html.
    clearChatMessages();

    // Id del producto pulsado
    var roomId = evt.currentTarget.id;
    var productId = evt.currentTarget.name;
    var mensajesSinLeer = document.getElementById(roomId + '-msl');
    if (mensajesSinLeer !== null) {
        mensajesSinLeer.remove();
    }

    if (roomId !== undefined) {
        $('.response').show();
        $('#room-title').text("Producto Prueba " + roomId);

        // Obtener datos del producto:
        refProducto = db.collection("chat").doc(roomId);
        refProducto.get().then(function (doc) {
            if (doc.exists) {
                let producto = doc.data();
                productoActual = producto.idProducto
                idProductoActual = doc.id;
                cliID = producto.idCliente;
                anunID = producto.idAnunciante;
                otherId = ((myID === cliID) ? anunID : cliID);
                tipoProducto = producto.tipoProducto;

            } else {
                // doc.data() will be undefined in this case
                console.log("No such document!");
            }
        }).then(function () {
            try {
                if (tipoProducto === "sale") {
                    httpGet(API + "/products/" + productId, mostrarChatRoom, [roomId, false]);
                } else {
                    httpGet(API + "/auctions/" + productId, mostrarChatRoom, [roomId, true]);
                }

            } catch
                (err) {
                console.log("Fallo al cargar elemento");
            }
        })
    }
    evt.preventDefault();
}


/**
 * Carga el contenido de un chat. El otro usuario (arriba) y los mensajes.
 */
function mostrarChatRoom(response, [roomId, esSubasta]) {
    producto = JSON.parse(response);

    httpGet(API + "/users/" + otherId, mostrarOtroUsuario, [producto]);

    var refMensajes = db.collection("chat").doc(roomId).collection("mensaje").orderBy("fecha");

    var fechaAnterior = undefined;
    escucharMensajes = refMensajes
        .onSnapshot(function (snapshot) {
            snapshot.docChanges().forEach(function (change) {
                if (change.type === "added") {
                    var contenido = change.doc.get("contenido");
                    var estado = change.doc.get("estado");
                    var fecha = change.doc.get("fecha");
                    var idEmisor = change.doc.get("idEmisor");

                    displayChatMessage(new Message(change.doc.id, contenido, estado, fecha, idEmisor), fechaAnterior);
                    if (idEmisor !== myID && estado === "enviado") {
                        db.collection("chat").doc(roomId).collection("mensaje").doc(change.doc.id).update({
                            estado: "recibido"
                        });
                    }
                    fechaAnterior = fecha;
                }
                if (change.type === "modified") {
                    // Mensaje modificado.
                    var estadoId = change.doc.id + "-estado";
                    var estado = (change.doc.get("estado") === "recibido" ? '<i class="fas fa-check-double"></i>' : '<i class="fas fa-check"></i>');

                    $('#' + estadoId).html(estado);

                }
                /*
                if (change.type === "removed") {
                    // Mensaje eliminado
                    // No hace nada. Si en el futuro se quiere implementar algo
                }
                */
            });
        });
}


function mostrarOtroUsuario(response, [producto]) {
    usuario = JSON.parse(response);

    console.log(usuario);

    // Mostrar el usuario con el que se conversa en la parte superior
    if (usuario.picture.idImagen !== null) {
        imagen = API + '/pictures/' + (usuario.picture.idImagen);
    } else {
        imagen = "gravatar.get(" + usuario.email + ")";
    }

    $('#other_user').html(
        `
        <div class="row user-bubble">
            <a href="/user/${usuario.idUsuario}" class="col-5">
                <div class="row center-vertically">
                    <div class="col user-image" style="background-image: url(${imagen})"></div>
                    <strong class="col title-bubble-white chat-user-name">${usuario.first_name} ${usuario.last_name}</strong>
                </div>
            </a>
            <div class="col-6"></div>
            <div class="col-1">
                <div class="dropdown">
                  <button class="chat-user-options dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                    <i class="fas fa-ellipsis-v"></i>
                  </button>
                  <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                    <a class="dropdown-item" href="#"><i class="fas fa-euro-sign"></i> Vender Producto</a>
                    <a class="dropdown-item" href="#"><i class="far fa-flag"></i> Reportar Usuario</a>
                    <a class="dropdown-item" href="#"><i class="fas fa-times"></i> Eliminar Chat</a>
                  </div>
                </div>
            </div>
        </div>    
    `);

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

        var tipo = (tipoProducto === "sale") ? "p" : "s";

        refChat = db.collection("chat").doc(tipo + productoActual + "_a" + anunID + "_c" + cliID);
        refChat.update({
            fechaUltimoMensaje: date,
            ultimoMensaje: message
        });

        refProducto.get().then(function (doc) {
            if (!doc.get("visible").includes(otherId)) {
                refChat.update({
                    visible: firebase.firestore.FieldValue.arrayUnion(otherId)
                });
            }
        });


        refMessage = refChat.collection("mensaje");
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

        // This registration token comes from the client FCM SDKs.
        var registrationToken = myTokenMessage;

        var not = {
            data: {
                score: '850',
                time: '2:45'
            },
            token: registrationToken
        };

        // Send a message to the device corresponding to the provided
        // registration token.

        var xhr = new XMLHttpRequest();
        xhr.ontimeout = function () {
            console.error("The request notification timed out.");
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
        xhr.open("POST", 'https://fcm.googleapis.com/v1/projects/selit-7d67c/messages:send', true);
        xhr.timeout = TIMEOUT;
        xhr.setRequestHeader('Authorization', "Bearer " + authToken);
        xhr.setRequestHeader("Content-Type", "application/json; UTF-8");
        xhr.send(JSON.stringify({
            "message": {
                "token": myTokenMessage,
                "notification": {
                    "body": "This is an FCM notification message!",
                    "title": "FCM Message",
                }
            }
        }))
        //xhr.send(null);

    }
}


/*
 * Cargar la lista de chats
 */
function loadChatManager() {
    // Obtener todos los chats y poner un link en la sidebar...
    refChats = db.collection("chat").orderBy("fechaUltimoMensaje").where('visible', 'array-contains', myID);

    refChats
        .onSnapshot(function (snapshot) {
                snapshot.docChanges().forEach(function (change) {
                    if (change.type === "added") {
                        var idProducto = change.doc.get("idProducto");
                        var tipoProd = change.doc.get("tipoProducto");
                        var mensajesSinLeer = 0;

                        var refMensajesSinLeer = db.collection("chat").doc(change.doc.id).collection("mensaje").where("estado", "==", "enviado");
                        refMensajesSinLeer.get().then(snap => {
                            mensajesSinLeer = snap.size; // Mensajes sin leer

                            refMensajesSinLeer.where("idEmisor", "==", myID).get().then(snap => {
                                console.log("Se ejecuta?");
                                mensajesSinLeer = mensajesSinLeer - snap.size; // Mensajes sin leer
                                console.log(mensajesSinLeer);

                                chatRoomsList.prepend(
                                    `<a href="#" onclick="return false;" id="${change.doc.id}" name="${idProducto}">
                            
                                 </a>`
                                );

                                try {

                                    if (tipoProd === "sale") {
                                        httpGet(API + "/products/" + idProducto, mostrarChatBubble, [change.doc, false, mensajesSinLeer]);
                                    } else {
                                        httpGet(API + "/auctions/" + idProducto, mostrarChatBubble, [change.doc, true, mensajesSinLeer]);
                                    }
                                } catch
                                    (err) {
                                    console.log("Fallo al cargar elemento");
                                    console.log(err);
                                }
                            });
                        });
                    }
                    if (change.type === "modified") {
                        var idProducto = change.doc.get("idProducto");
                        var tipoProd = change.doc.get("tipoProducto");

                        if (idProductoActual !== change.doc.id) {
                            var newMessages = document.getElementById(change.doc.id + '-msl');
                            if (newMessages !== null) {
                                var num = parseInt(newMessages.textContent);
                                newMessages.textContent = (num + 1);
                            } else {
                                $('#' + change.doc.id + '-mb').append(
                                    `<div class="numberCircle" id="${change.doc.id}-msl">1</div>`);
                            }
                        }
                        
                        try {
                            if (tipoProd === "sale") {
                                httpGet(API + "/products/" + idProducto, actualizarChatBubble, [change.doc, false]);
                            } else {
                                httpGet(API + "/auctions/" + idProducto, actualizarChatBubble, [change.doc, true]);
                            }
                        } catch
                            (err) {
                            console.log("Fallo al cargar elemento");
                            console.log(err);
                        }
                    }
                    if (change.type === "removed") {
                        // Si se elimina el chat:
                        document.getElementById(change.doc.id).remove();
                    }
                });
            }
        )
    ;
}

/**
 * Mostrar un chat.
 * @param response
 * @param doc
 * @param esSubasta
 */
function mostrarChatBubble(response, [doc, esSubasta, mensajesSinLeer]) {
    producto = JSON.parse(response);
    try {
        imagen = API + '/pictures/' + (producto.media[0].idImagen);
    } catch (err) {
        imagen = "static/images/items.svg";
    }
    var nombreVendedor = ((myID === producto.owner.idUsuario) ? "Mi producto" : producto.owner.first_name + producto.owner.last_name);

    var ultimoMensaje = doc.get("ultimoMensaje");

    var mensNoLeidos = (mensajesSinLeer === 0) ? "" : '<div class="numberCircle" id="' + doc.id + '-msl">' + mensajesSinLeer + '</div>';
    // console.log(mensNoLeidos);

    $('#' + doc.id).append(
        `
            <div class="producto-bubble row" id="${doc.id}-mb">
                ${mensNoLeidos}
     
                <div class="col-3 product-image"
                    style="background-image: url(${imagen})"></div>
                <div class="col-8 row">
                    <strong class="title-bubble">${producto.title}</strong>
                    <strong class="subtitle-bubble">${nombreVendedor}</strong>
                    <strong class="message-title-bubble" id="${doc.id}-um">${ultimoMensaje}</strong>        
                </div>     
            </div>
        `
    );
}

/**
 * Mostrar un chat.
 * @param response
 * @param doc
 * @param esSubasta
 */
function actualizarChatBubble(response, [doc, esSubasta]) {
    producto = JSON.parse(response);
    try {
        imagen = API + '/pictures/' + (producto.media[0].idImagen);
    } catch (err) {
        imagen = "static/images/items.svg";
    }

    var ultimoMensaje = doc.get("ultimoMensaje");

    // Mover bubble arriba del t.odo.
    $('#' + doc.id).prependTo(chatRoomsList);

    // Actualizar el último mensaje.
    $('#' + doc.id + "-um").html(ultimoMensaje);
}

/**
 * Buscar títulos y personas en los chats.
 */
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
    xhr.open("GET", sUrl, true); // Poner a true y descomentar timeout para quitar warning (chats desordenados de tiempo)
    xhr.setRequestHeader('Authorization', myAuthID);
    xhr.timeout = TIMEOUT;
    xhr.send(null);
}


Element.prototype.remove = function () {
    this.parentElement.removeChild(this);
}
NodeList.prototype.remove = HTMLCollection.prototype.remove = function () {
    for (var i = this.length - 1; i >= 0; i--) {
        if (this[i] && this[i].parentElement) {
            this[i].parentElement.removeChild(this[i]);
        }
    }
}

$(function () {
    $('body').on('click', '.producto-bubble', function () {
        $('.producto-bubble').removeClass('active');
        $(this).closest('.producto-bubble').addClass('active');
    });
});


// Send the Instance ID token your application server, so that it can:
// - send messages back to this app
// - subscribe/unsubscribe the token from topics
function sendTokenToServer(currentToken) {
    if (!isTokenSentToServer()) {
        console.log('Sending token to server...');
        refNot = db.collection("userNotification").doc(myID.toString());
        refNot.update({
            tokenDesktop: currentToken
        });
        setTokenSentToServer(true);
    } else {
        console.log('Token already sent to server so won\'t send it again ' +
            'unless it changes');
    }
}

function isTokenSentToServer() {
    return window.localStorage.getItem('sentToServer') === '1';
}

function setTokenSentToServer(sent) {
    window.localStorage.setItem('sentToServer', sent ? '1' : '0');
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

    messaging = firebase.messaging();

    messaging.requestPermission()
        .then(function () {
            // El usuario ha aceptado que le mandemos notificaciones.
            return messaging.getToken();
        })
        .then(function (token) {
            sendTokenToServer(token);
            console.log(token);
            myTokenMessage = token;
        })
        .catch(function (err) {
            // El usuario NO ha aceptado que le mandemos notificaciones.
            console.log("Acepta los permisos para poder obtener notificaciones de los mensajes.");
            console.log(err);
        });

    messaging.onMessage(function (payload) {
        console.log('onMessage: ', payload);
    });


    // Callback fired if Instance ID token is updated.
    messaging.onTokenRefresh(function () {
        messaging.getToken().then(function (refreshedToken) {
            console.log('Token refreshed.');
            // Indicate that the new Instance ID token has not yet been sent to the
            // app server.
            setTokenSentToServer(false);
            // Send Instance ID token to app server.
            sendTokenToServer(refreshedToken);
            // ...
        }).catch(function (err) {
            console.log('Unable to retrieve refreshed token ', err);
            showToken('Unable to retrieve refreshed token ', err);
        });
    });

}