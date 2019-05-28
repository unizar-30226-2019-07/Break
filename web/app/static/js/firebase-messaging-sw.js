importScripts('https://www.gstatic.com/firebasejs/5.9.1/firebase-app.js');
importScripts('https://www.gstatic.com/firebasejs/5.9.1/firebase-messaging.js');

// Initialize Firebase también
var config = {
    apiKey: "AIzaSyBVkzjZBaHoupJYOl3MDMtrSyBAhpSfv6Q",
    authDomain: "selit-7d67c.firebaseapp.com",
    databaseURL: "https://selit-7d67c.firebaseio.com",
    projectId: "selit-7d67c",
    storageBucket: "selit-7d67c.appspot.com",
    messagingSenderId: "663470816058"
};
firebase.initializeApp(config);

const messaging = firebase.messaging();
messaging.setBackgroundMessageHandler(function (payload) {
    const title = payload.data.title;
    const options = {
        body: payload.data.body,
        icon: payload.data.icon
    };
    return self.registration.showNotification(title, options);
});