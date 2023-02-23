const { MongoClient } = require("mongodb");
const uri = "mongodb://mongoadmin:secret@localhost:1888/?authMechanism=DEFAULT";
const client = new MongoClient(uri);
const database = client.db("panel-logs");

const io = require("socket.io")(3000, {
    cors: {
        origin: ["http://localhost:8080"], // Aquí se pondrán el/los clientes que se conecten al ws
    },
});


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
            insertLog(data);
            io.emit('panel-update', data);
        }
    })
})


async function insertLog(data : PanelUpdate){
    const haiku = database.collection("logs");
    const result = await haiku.insertOne(data);
    console.log(`A document was inserted with the _id: ${result.insertedId}`);
}

interface PanelUpdate {
    panelId: number// Identificador único del panel
    time: string// Hora actual
    sunsetTime: string // Lo que queda para la puesta de sol
    status: {
        sunY: number // 0-1
        sunX: number // 0-1
        sensor1: number
        sensor2: number
        sensor3: number
        sensor4: number
        motor1: number
        motor2: number
        battery: string // %
        kWh: number // Maybe?
        image: string // base64???
    }
}

function instanceOfPanelUpdate(object: any): object is PanelUpdate {
    return 'panelId' in object;
}