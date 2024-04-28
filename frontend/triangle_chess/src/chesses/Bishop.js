import { AREA, COL, ROW } from "@/config/config";
import { GEBI, getCol } from "@/utils/utils";
import { Chess } from "./Chess";

export class Bishop extends Chess {
    constructor(position, camp) {
        super(position, camp);
        this.name = "象";
    }

    canMove() {
        // 保存返回值
        let p = [];
        // 1.斜走
        // 2.路上有子会被阻拦
        // 3.无法过河
        if (getCol(this.position) <= 2) {
            p.push(GEBI(this.position + COL + 1 + '')?.innerText ? 0 : this.position + COL * 2 + 2);
            p.push(GEBI(this.position - COL + 1 + '')?.innerText ? 0 : this.position - COL * 2 + 2);
        } else if (getCol(this.position) >= 8) {
            p.push(GEBI(this.position + COL - 1 + '')?.innerText ? 0 : this.position + COL * 2 - 2);
            p.push(GEBI(this.position - COL - 1 + '')?.innerText ? 0 : this.position - COL * 2 - 2);
        } else {
            p.push(GEBI(this.position + COL + 1 + '')?.innerText ? 0 : this.position + COL * 2 + 2);
            p.push(GEBI(this.position - COL + 1 + '')?.innerText ? 0 : this.position - COL * 2 + 2);
            p.push(GEBI(this.position + COL - 1 + '')?.innerText ? 0 : this.position + COL * 2 - 2);
            p.push(GEBI(this.position - COL - 1 + '')?.innerText ? 0 : this.position - COL * 2 - 2);
        }

        p = p.filter(position => {
            // 过滤0
            if (!position) return false;
            // 实现无法过河
            if (this.camp) return position > COL * ROW / 2;
            else return position < COL * ROW / 2;
        });

        return p;
    }
}
