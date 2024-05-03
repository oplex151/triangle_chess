import { Camp } from "@/utils/Camp";
import { SuperChess } from '@/chesses/Super';
import { AREAMID,AREATOP,AREABOT, COL, ROWTOP,ROWMID } from "@/config/config";
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
        new Chariot(AREABOT, 0),
        new Chariot(AREABOT - 8, 0),
        new Warhosre(AREABOT - 1, 0),
        // test
        new Warhosre(AREABOT - 7, 0),

        // test
        new Gun(COL * 2 + 2, 0),

        new Gun(COL * 2 + 8, 0),

        // test
        new Soilder(COL * (6 - 5) + 1, 0),
        // test
        new Soilder(COL * (6 - 5) + 3, 0),

        new Soilder(COL * (6 - 5) + 5, 0),
        new Soilder(COL * (6 - 5) + 7, 0),
        new Soilder(COL * (6 - 5) + 9, 0),
        new Bishop(AREABOT - 6, 0),
        new Bishop(AREABOT - 2, 0),
        new Advisor(AREABOT - 5, 0),
        new Advisor(AREABOT - 3, 0),
        new Leader(AREABOT - 4, 0)
    ]),
    Bcamp: new Camp([
        new Chariot(AREAMID, 1),
        new Chariot(AREAMID - 8, 1),
        new Warhosre(AREAMID - 1, 1),
        new Warhosre(AREAMID - 7, 1),
        new Gun(COL * 7 + 2, 1),
        new Gun(COL * 7 + 8, 1),
        new Soilder(COL * 6 + 9, 1),
        new Soilder(COL * 6 + 7, 1),
        new Soilder(COL * 6 + 5, 1),
        new Soilder(COL * 6 + 3, 1),
        new Soilder(COL * 6 + 1, 1),
        new Bishop(AREAMID - 6, 1),
        new Bishop(AREAMID - 2, 1),
        new Advisor(AREAMID - 5, 1),
        new Advisor(AREAMID - 3, 1),
        new Leader(AREAMID - 4, 1)
    ]),
    Ccamp: new Camp([
        new Chariot(AREATOP, 2),
        new Chariot(AREATOP - 8, 2),
        new Warhosre(AREATOP - 1, 2),
        new Warhosre(AREATOP - 7, 2),
        new Gun(COL * (7 + 5) + 2, 2),
        new Gun(COL * (7 + 5) + 8, 2),
        new Soilder(COL * (6 + 5) + 9, 2),
        new Soilder(COL * (6 + 5) + 7, 2),
        new Soilder(COL * (6 + 5) + 5, 2),
        new Soilder(COL * (6 + 5) + 3, 2),
        new Soilder(COL * (6 + 5) + 1, 2),
        new Bishop(AREATOP - 6, 2),
        new Bishop(AREATOP - 2, 2),
        new Advisor(AREATOP - 5, 2),
        new Advisor(AREATOP - 3, 2),
        new Leader(AREATOP - 4, 2)
    ]),
};
