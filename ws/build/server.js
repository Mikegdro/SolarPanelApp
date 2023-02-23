"use strict";
var fs = require('fs');
require('dotenv').config();
var io = require("socket.io")(3000, {
    cors: {
        origin: ["http://localhost:8080"], // Aquí se pondrán el/los clientes que se conecten al ws
    },
});
var oneDay = 86400000;
var interval = 7200000;
var start = Date.now();
setInterval(function () {
    var now = Date.now();
    var elapsed = now - start;
    if (elapsed >= oneDay) {
        start = Date.now();
        console.log(process.env.PRIVATE_KEY);
        // Fetch a ruta de api para volcar los datos en la bd
    }
}, interval);
function authMiddleware(socket, next) {
    if (socket.handshake.auth.token) {
        var isAuth = true;
        // let isAuth = fetch(api route de comprobar token);
        if (!isAuth) {
            next(new Error("The token provided is not valid"));
        }
        next();
    }
    else if (socket.handshake.auth.id) {
        var isAuth = true;
        // let isAuth = fetch(api route de comprobar id del panel en whitelist);
        if (!isAuth) {
            next(new Error("The panel id provided is not registered as valid"));
        }
        next();
    }
    else {
        next(new Error("You need to authenticate to establish a connection"));
    }
}
io.use(authMiddleware);
io.on('connection', function (socket) {
    console.log("socket connected: " + socket);
    socket.on('solar-panel-update', function (data) {
        if (instanceOfPanelUpdate(data)) {
            // insertLog(data);
            io.emit('panel-update', data);
            io.emit('solar-panel-photo', "hola");
        }
    });
    socket.on('solar-panel-photo', function (data) {
        console.log("HA LLEGADO: ");
        console.log(data);
        // insertLog(data);
    });
});
function insertLog(data) {
    var file = fs.readFileSync('logs.json');
    var fileData = JSON.parse(file);
    if (fileData[data.id]) {
        fileData[data.id].push(data);
    }
    else {
        fileData[data.id] = [data];
    }
    var newData = JSON.stringify(fileData);
    fs.writeFile('logs.json', newData, function (err) {
        // error checking
        if (err)
            throw err;
        // console.log("New data added");
    });
}
insertLog({
    id: "panel2",
    time: "234",
    log: {
        sensor1: 12,
        sensor2: 32,
        sensor3: 52,
        sensor4: 52,
        motor1: 52,
        motor2: 23,
        battery: "6235",
        potency: 23,
        image: "ddadasqwdadawadasd",
        ocvOutput: "ddadasqwdadawadasd"
    }
});
function instanceOfPanelUpdate(object) {
    return 'panelId' in object;
}
