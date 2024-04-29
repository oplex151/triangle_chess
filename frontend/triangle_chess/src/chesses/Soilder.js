import { AREA, COL } from "@/config/config";
import { getCol } from "@/utils/utils";
import { Chess } from "./Chess";

export class Soilder extends Chess {
    constructor(position, camp) {
        super(position, camp);
        this.name = "兵";
    }

    canMove() {
        // 存储我们需要的数据
        let p = [];
        // 当士兵在任意区域时,每次只能向前移动1格
        p.push(this.position + (this.camp ? (-COL) : COL));
        // 当士兵在对方区域时,可以向左/右任意移动
        if (this.inWhichArea !== this.camp) {
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
