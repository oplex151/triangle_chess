
import { ref } from "vue";

export const registerSockets = (methods, socket, proxy)=>{
    methods && Object.keys(methods).forEach((t)=>{
        "subscribe" !== t &&
        "unsubscribe"!== t &&
        socket.emitter.addListener(t, methods[t],proxy);
    })
}

export const removeSockets = (methods, socket, proxy)=>{
    methods && Object.keys(methods).forEach((t)=>{
        socket.emitter.removeListener(t, proxy);
    })
}

export const socket = ref("")