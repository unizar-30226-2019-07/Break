(function() {
  'use strict';

  // ----------------------------------------------------
  // Chat Details
  // ----------------------------------------------------
  let chat = {
    rooms: [],
    messages: [],
  };

  // ----------------------------------------------------
  // Targeted Elements
  // ----------------------------------------------------
  const chatBody = $(document);
  const chatRoomsList = $('#rooms');
  const chatReplyMessage = $('#replyMessage');
  const chatScrollMessageDiv = "msg_scroll";

  // ----------------------------------------------------
  // Helpers
  // ----------------------------------------------------
  const helpers = {
    /**
     * Limpiar los mensajes del chat
     */
    clearChatMessages: () => $('#chat-msgs').html(''),

    /**
     * Mostrar un nuevo mensaje en la ventana de mensajes
     */
    displayChatMessage: message => {
       // Si el mensaje no se encuentra en memoria
//      if (chat.messages[message.id] === undefined) {
//        chat.messages[message.id] = message;

        var envio = "me";
        if(message.enviado){
         envio = "sender";
        }

        $('#chat-msgs').append(
          `<div class="messages-bubble ${envio}-bubble">
                <div class="">${message.text}</div>
                <div> @ <span class="date">${ message.createdAt }</span></div>
                <div class="${envio}-bubble-ds-arrow"></div>
        </div>`
        );

        var objDiv = document.getElementById(chatScrollMessageDiv);
        objDiv.scrollTop = objDiv.scrollHeight;
//      }
    },

    /**
     * Cargar to_dos los mensajes de un chat
     */
    loadChatRoom: evt => {
      // Limpiamos los mensajes del html.
      helpers.clearChatMessages();

      // Id del producto pulsado
      console.log(evt);
      console.log(evt.id);


      var roomId = evt.currentTarget.id;

      if (roomId !== undefined) {
        $('.response').show();
        $('#room-title').text("Producto Prueba " + roomId);

        // Mensajes pruebas creados para probar la interfaz
        var msgs = [];

        class Message {
          constructor(id, sender_name, createdAt, text, enviado) {
            this.id = id;
            this.sender_name = sender_name;
            this.createdAt = createdAt;
            this.text = text;
            this.enviado = enviado;
           }
        }

        msgs.push(new Message(1, "Juan", "1:00", "Texto Prueba", Math.random() >= 0.5));
        msgs.push(new Message(2, "Juan", "1:01", "Texto Prueba 2", Math.random() >= 0.5));
        msgs.push(new Message(3, "Juan", "1:02", "Texto Prueba 3", Math.random() >= 0.5));
        msgs.push(new Message(4, "Juan", "1:03", "Texto Prueba 4", Math.random() >= 0.5));
        msgs.push(new Message(5, "Juan", "1:04", "Texto Prueba 5", Math.random() >= 0.5));

        // Imprime los mensajes nuevos / los ultimos:
        msgs.forEach(message => helpers.displayChatMessage(message));
      }

      evt.preventDefault();
    },

    /**
     * Contestar con un mensaje:
     */
    replyMessage: evt => {
      evt.preventDefault();

      const message = $('#replyMessage input')
        .val()
        .trim();

        let msg = {
            id: "0",
            createdAt: "now",
            text: message,
            enviado: false,
         }

      helpers.displayChatMessage(msg);

      $('#replyMessage input').val('');
    },



    /**
     * Pedir los productos a la API
     */
    requestChatsIDs: () => {
        var IDs = new Array();
        for (var i = 0; i < 10; i++) {
            IDs.push(i);
        };
        return IDs;
    },


    /**
     * Cargar la lista de chats
     */
    loadChatManager: () => {
        // Obtener todos los chats y poner un link en la sidebar...
        for (var id in helpers.requestChatsIDs()) {
            $('#rooms').append(
                `<a href="#" onclick="return false;" id="${id}">
                    <div class="producto-bubble row">
                        <div class="product-image"
                            style="background-image: url(static/images/1953-1954-Buick-Skylark.jpg"></div>
                        <strong>Producto de Prueba ${id}</strong>
                    </div>
                </a>`
            );
        }
    },
  };

  // ----------------------------------------------------
  // Register page event listeners
  // ----------------------------------------------------
  chatBody.ready(helpers.loadChatManager);
  chatReplyMessage.on('submit', helpers.replyMessage);
  chatRoomsList.on('click', 'a', helpers.loadChatRoom);
})();

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
