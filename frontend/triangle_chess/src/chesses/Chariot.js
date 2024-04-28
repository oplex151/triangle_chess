import { AREA } from "@/config/config";
import { Chess } from "./Chess";

export class Chariot extends Chess {
    constructor(position, camp) {
        super(position, camp);
        this.name = "车";
    }

    canMove() {
        // 保存返回值
        let p = [];
        for (let i = 0; i <= AREA; i++) {
            if (i === this.position) continue;
            // 把向上下左右的可移动点位加进总的可移动点位中
            p.push(...this.getTopMoviableArea());
            p.push(...this.getLeftMoviableArea());
            p.push(...this.getRigthMoviableArea());
            p.push(...this.getDownMoviableArea());
        }
        return p;
    }
}
