import { AREATOP,AREAMID,AREABOT } from "@/config/config";
import { Chess } from "./Chess";

// 超级棋子 继承chass的种类 实现棋子的接口
export class SuperChess extends Chess {
    constructor(position, camp) {
        super(position, camp);
        // 棋子的名字
        this.name = "超级";
    }

    // canmove是数组
    canMove() {
        // 定义一个数组
        let p = [];
        // 循环遍历
        for (let i = 0; i <= AREATOP; i++) {
            // 不能走到本身的位置
            if (i === this.position) continue;
            p.push(i);
        }
        return p;
    }
}
