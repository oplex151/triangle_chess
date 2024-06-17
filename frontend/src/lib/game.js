import { Camp } from "@/lib/camp";
// 棋子的引入
import { XYZToPosition } from "@/lib/convert";
import { Chariot } from "@/chesses/Chariot";
import { Warhosre } from "@/chesses/Warhosre";
import { Gun } from "@/chesses/Gun";
import { Soilder } from "@/chesses/Soilder";
import { Bishop } from "@/chesses/Bishop";
import { Advisor } from "@/chesses/Advisor";
import { Leader } from "@/chesses/Leader";


// 保存一些必要的资料 new realChess(位置,阵营)
export var camps = {}

export function initChess(game_info) {
    camps = {
        Acamp: new Camp([]),
        Bcamp: new Camp([]),
        Ccamp: new Camp([]),
    };
    var pieces = game_info.pieces;
    for (let i = 0; i < pieces.length; i++) {
        var chess = null
        if (pieces[i].live == false)
            continue;
        var position = XYZToPosition(pieces[i].px, pieces[i].py, pieces[i].pz);

        switch (pieces[i].name) {
            // 这里没问题
            case "Chariot":
                chess = new Chariot(position, pieces[i].user_z, pieces[i].pz);                
                break;
            case "WarHorse":
                chess = new Warhosre(position, pieces[i].user_z, pieces[i].pz);
                break;
            case "Gun":
                chess = new Gun(position, pieces[i].user_z, pieces[i].pz);
                break;
            case "Soilder":
                chess = new Soilder(position, pieces[i].user_z, pieces[i].pz);
                break;
            case "Bishop":
                chess = new Bishop(position, pieces[i].user_z, pieces[i].pz);
                break;
            case "Advisor":
                chess = new Advisor(position, pieces[i].user_z, pieces[i].pz);
                break;
            case "Leader":
                chess = new Leader(position, pieces[i].user_z, pieces[i].pz);
                break;
            default:
                break;
        }
        // OK
        switch (pieces[i].user_z) {
            case 0:
                camps.Acamp.addChess(chess);
                break;
            case 1:
                camps.Bcamp.addChess(chess);
                break;
            case 2:
                camps.Ccamp.addChess(chess);
                break;
            default:
                break;
        }
    }
}
