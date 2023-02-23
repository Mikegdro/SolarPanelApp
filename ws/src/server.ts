const fs = require('fs');
require('dotenv').config();
const io = require("socket.io")(3000, {
    cors: {
        origin: ["http://localhost:8080"], // Aquí se pondrán el/los clientes que se conecten al ws
    },
});
const oneDay = 86400000;
const interval = 7200000;
let start = Date.now();

setInterval(() =>{
    let now = Date.now();
    let elapsed = now - start;
    if(elapsed >= oneDay){
        start = Date.now();
        console.log(process.env.PRIVATE_KEY);
        // Fetch a ruta de api para volcar los datos en la bd
    }
}, interval)


function authMiddleware(socket : any, next : Function){
    if(socket.handshake.auth.token){
        let isAuth = true;
        // let isAuth = fetch(api route de comprobar token);
        if(!isAuth){
            next(new Error("The token provided is not valid"));
        }
        next();
    }else if(socket.handshake.auth.id){
        let isAuth = true;
        // let isAuth = fetch(api route de comprobar id del panel en whitelist);
        if(!isAuth){
            next(new Error("The panel id provided is not registered as valid"));
        }
        next();
    }else{
        next(new Error("You need to authenticate to establish a connection"));
    }
}

io.use(authMiddleware);
io.on('connection', (socket : any) =>{
    console.log("socket connected: " + socket);
    
    socket.on('solar-panel-update', (data : PanelUpdate) =>{
        if(instanceOfPanelUpdate(data)){
            // insertLog(data);
            io.emit('panel-update', data);
            io.emit('solar-panel-photo', "hola");
        }
    });

    socket.on('solar-panel-photo', (data : any) =>{
        console.log("HA LLEGADO: ");
        console.log(data);
        // insertLog(data);
    })
})


function insertLog(data : PanelUpdate){
    let file = fs.readFileSync('logs.json');
    let fileData = JSON.parse(file);
    if(fileData[data.id]){
        fileData[data.id].push(data);
    }else{
        fileData[data.id] = [data];
    }
    let newData = JSON.stringify(fileData);
    fs.writeFile('logs.json', newData, (err : any) => {
        // error checking
        if(err) throw err;
        
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
        battery: "6235", // %
        potency: 23, // Maybe?
        image: "ddadasqwdadawadasd", // base64???
        ocvOutput: "ddadasqwdadawadasd"
    }
})

interface PanelUpdate {
    id: string// Identificador único del panel
    time: string // Fecha del update
    log: {
        sensor1: number
        sensor2: number
        sensor3: number
        sensor4: number
        motor1: number
        motor2: number
        battery: string // %
        potency: number // Maybe?
        image: string // base64???
        ocvOutput: string
    }
}

function instanceOfPanelUpdate(object: any): object is PanelUpdate {
    return 'panelId' in object;
}