import { AREA, COL } from "@/config/config";
import { GEBI, getCol, getRow } from "@/utils/utils";
import { Chess } from "./Chess";

export class Leader extends Chess {
    constructor(position, camp) {
        super(position, camp);
        this.name = "将";
    }

    canMove() {
        // 保存返回值
        let p = [];
        // 上下左右1格移动
        p.push(this.position + 1, this.position - 1, this.position + COL, this.position - COL);
        // 不能离开九宫
        p = p.filter(position => getCol(position) >= 4 && getCol(position) <= 6 && ((getRow(position) >= 1 && getRow(position) <= 3) || (getRow(position) <= 10 && getRow(position) >= 8)));

        // 飞将胜利
        let route;
        route = this.camp ? this.getDownMoviableArea() : this.getTopMoviableArea();
        const chess = route.pop();
        if (GEBI(chess + '')?.innerText === '将') p.push(chess);

        return p;
    }
}
