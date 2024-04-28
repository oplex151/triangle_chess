import { Camp } from "@/utils/Camp";
import { SuperChess } from '@/chesses/Super';
import { AREA, COL, ROW } from "@/config/config";
// 棋子的引入
import { Chariot } from "@/chesses/Chariot";
import { Warhosre } from "@/chesses/Warhosre";
import { Gun } from "@/chesses/Gun";
import { Soilder } from "@/chesses/Soilder";
import { Bishop } from "@/chesses/Bishop";
import { Advisor } from "@/chesses/Advisor";
import { Leader } from "@/chesses/Leader";

// 保存一些必要的资料 new 棋子(位置,阵营)
export const camps = {
    Acamp: new Camp([
        new Chariot(1, 0),
        new Chariot(9, 0),
        new Warhosre(2, 0),
        new Warhosre(8, 0),
        new Gun(COL * 2 + 2, 0),
        new Gun(COL * 2 + 8, 0),
        new Soilder(COL * 3 + 1, 0),
        new Soilder(COL * 3 + 3, 0),
        new Soilder(COL * 3 + 5, 0),
        new Soilder(COL * 3 + 7, 0),
        new Soilder(COL * 3 + 9, 0),
        new Bishop(3, 0),
        new Bishop(7, 0),
        new Advisor(4, 0),
        new Advisor(6, 0),
        new Leader(5, 0)
    ]),
    Bcamp: new Camp([
        new Chariot(AREA, 1),
        new Chariot(AREA - 8, 1),
        new Warhosre(AREA - 1, 1),
        new Warhosre(AREA - 7, 1),
        new Gun(COL * 7 + 2, 1),
        new Gun(COL * 7 + 8, 1),
        new Soilder(COL * 6 + 9, 1),
        new Soilder(COL * 6 + 7, 1),
        new Soilder(COL * 6 + 5, 1),
        new Soilder(COL * 6 + 3, 1),
        new Soilder(COL * 6 + 1, 1),
        new Bishop(AREA - 6, 1),
        new Bishop(AREA - 2, 1),
        new Advisor(AREA - 5, 1),
        new Advisor(AREA - 3, 1),
        new Leader(AREA - 4, 1)
    ]),

};
