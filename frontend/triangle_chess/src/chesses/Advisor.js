import { AREA, COL } from "@/config/config";
import { getCol, getRow } from "@/utils/utils";
import { Chess } from "./Chess";

export class Advisor extends Chess {
    constructor(position, camp) {
        super(position, camp);
        this.name = "士";
    }

    canMove() {
        // 保存返回值
        let p = [];
        // 1.斜走1格
        p.push(this.position + COL + 1, this.position + COL - 1, this.position - COL + 1, this.position - COL - 1);
        // 2.不能离开九宫格
        p = p.filter(position => getCol(position) >= 4 && getCol(position) <= 6 && ((getRow(position) >= 1 && getRow(position) <= 3) || (getRow(position) <= 10 && getRow(position) >= 8)));
        return p;
    }
}
