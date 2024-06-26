import {  COL, ROWMID, ROWTOP, ROWBOT } from "@/config/config";
import { GEBI, getCol } from "@/utils/utils";
import { Chess } from "./Chess";

export class Bishop extends Chess {
    constructor(position, camp,inWhichArea) {
        super(position, camp,inWhichArea);
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
            if (this.camp === 0) return position >= 1 && position <= COL * ROWBOT;
            else if (this.camp === 1) return position > COL * ROWBOT && position <= COL * ROWMID;
            else return position > COL * ROWMID && position < COL * ROWTOP;
        });

        return p;
    }
}
