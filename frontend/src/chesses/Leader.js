import { AREAMID,AREATOP,AREABOT, COL } from "@/config/config";
import { GEBI, getCol, getRow } from "@/utils/utils";
import { Chess } from "./Chess";

export class Leader extends Chess {
    constructor(position, camp,inWhichArea) {
        super(position, camp,inWhichArea);
        this.name = "将";
    }

    canMove() {
        // 保存返回值
        let p = [];
        // 上下左右1格移动
        p.push(this.position + 1, this.position - 1, this.position + COL, this.position - COL);
        // 不能离开九宫
        p = p.filter(position => getCol(position) >= 4 && getCol(position) <= 6 && ((getRow(position) <= 5 && getRow(position) >= 3) || (getRow(position) <= 10 && getRow(position) >= 8)||(getRow(position) <= 15 && getRow(position) >= 13)));

        // 飞将胜利
        // let route;
        // switch(this.camp){
        //     case 0:
        //         route = this.
        // }
        // // if(this.camp )
        // route = this.camp ? this.getDownMoviableArea() : this.getTopMoviableArea();
        // const chess = route.pop();
        // if (GEBI(chess + '')?.innerText === '将') p.push(chess);
        return p;
    }
}
