// ----------------------------------------------------
// Variables globales:
// ----------------------------------------------------
var db;
var myID;
const api = "http://35.234.77.87:8080";

var productoActual;
var anunID;
var cliID;

class Message {
    constructor(id, sender_name, createdAt, text, enviado) {
        this.id = id;
        this.createdAt = createdAt;
        this.text = text;
        this.enviado = enviado;
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
    // Si el mensaje no se encuentra en memoria
// if (chat.messages[message.id] === undefined) {
// chat.messages[message.id] = message;

    var envio = "me";
    if (message.enviado) {
        envio = "sender";
    }

    $('#chat-msgs').append(
        `<div class="messages-bubble ${envio}-bubble">
                <div class="">${message.text}</div>
                <div> @ <span class="date">${message.createdAt}</span></div>
                <div class="${envio}-bubble-ds-arrow"></div>
        </div>`
    );

    var objDiv = document.getElementById(chatScrollMessageDiv);
    objDiv.scrollTop = objDiv.scrollHeight;
// }
}

/**
 * Cargar to_dos los mensajes de un chat
 */
function loadChatRoom(evt) {
    // Limpiamos los mensajes del html.
    clearChatMessages();

    // Id del producto pulsado
    var roomId = evt.currentTarget.id;

    if (roomId !== undefined) {
        $('.response').show();
        $('#room-title').text("Producto Prueba " + roomId);

        // Mensajes pruebas creados para probar la interfaz
        refMensajes = db.collection("chat").doc(roomId).collection("mensaje");

        refMensajes.get()
        .then(function (querySnapshot) {
            querySnapshot.forEach(function (doc) {
                console.log(doc.id);
                displayChatMessage(new Message(1, "Juan", "1:00", doc.id, true));
            });
        })
        .catch(function (error) {
            console.log("Error getting documents: ", error);
        });


    }

    evt.preventDefault();
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

        var minutes = date.getMinutes();
        var hour = date.getHours();

        let msg = {
            id: "0",
            createdAt: hour + ":" + minutes,
            text: message,
            enviado: false,
        }

        refChats = db.collection("chat");

        //displayChatMessage(msg);
        refChats.doc("TOK").set({
            name: "Tokyo", state: null, country: "Japan",
            capital: true, population: 9000000
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
                // doc.data() is never undefined for query doc snapshots

                var idProducto = doc.get("idProducto");
                let producto = JSON.parse(httpGet(api + "/products/" + idProducto + "?lng=0&lat=0"));

                console.log(producto);
                console.log(producto.title);
                imagen = api + '/pictures/' + (producto.media[0].idImagen);

                $('#rooms').append(
                    `<a href="#" onclick="return false;" id="${doc.id}">
                        <div class="producto-bubble row">
                            <div class="product-image"
                                style="background-image: url(${imagen})"></div>
                            <strong>${producto.title}</strong>
                        </div>
                    </a>`
                );

            });
        })
        .catch(function (error) {
            console.log("Error getting documents: ", error);
        });


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


function httpGet(theUrl) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", theUrl, false); // false for synchronous request
    xmlHttp.send(null);
    return xmlHttp.responseText;
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