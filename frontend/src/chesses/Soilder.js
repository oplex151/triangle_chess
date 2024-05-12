import {AREABOT, AREATOP, AREAMID, COL, ROWTOP} from "@/config/config";
import {getCol, getRow} from "@/utils/utils";
import { Chess } from "./Chess";
// import {camp} from "@/lib/game.js";

export class Soilder extends Chess {
    constructor(position, camp,inWhichArea) {
        super(position, camp,inWhichArea);
        this.name = "兵";
    }

    canMove() {
        // 存储我们需要的数据
        let p = [];
        // 当士兵在任意区域时,每次只能向前移动1格

        // 未过河
        if(this.camp == this.inWhichArea){
            // A边界(准备过河)
            if(getRow(this.position) == 1){
                p.push(COL - (getCol(this.position) - 1) + AREABOT);
                p.push(COL - (getCol(this.position) - 1) + AREAMID);
            }
            // B边界(准备过河)
            else if(getRow(this.position) == 6){
                p.push(COL - (getCol(this.position) - 1));
                p.push(COL - (getCol(this.position) - 1) + AREAMID);
            }
            // C边界(准备过河)
            else if(getRow(this.position) == 11){
                p.push(COL - (getCol(this.position) - 1) + AREABOT);
                p.push(COL - (getCol(this.position) - 1));
            }
            // 其他(不准备过河)
            else {
                p.push(this.position - COL);
            }
        }
        // 当士兵在对方区域时,可以向左/右任意移动
        else {
            p.push(this.position + COL);
            // 判断兵位置是否在最左边或者最右边
            if (getCol(this.position) === 1) {
                p.push(this.position + 1);
            } else if (getCol(this.position) === COL) {
                p.push(this.position - 1);
            } else {
                p.push(this.position - 1, this.position + 1);
            }
        }
        return p;
    }
}
