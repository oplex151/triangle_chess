import { COL, ROW } from "@/config/config";
import { getCol, getRow } from "@/utils/utils";
import { Chess } from "./Chess";

export class Warhosre extends Chess {
    constructor(position, camp) {
        super(position, camp);
        this.name = "马";
    }

    canMove() {
        let p = [];
        // 1.上下左右 共 8个日字形点位移动
        // 首先要确定当前位置 至少是在上方第三行的位置
        // 如果返回的行数<=总行数-3 就会进行移动
        // top 加上蹩马腿判断
        if (getRow(this.position) <= ROW - 3 && !this.haveChess(this.position + COL)) {
            // 移动
            // 列出点位
            let p1 = this.position + COL * 2 + 1;
            let p2 = this.position + COL * 2 - 1;
            // 如果行数是第一行 把p2传进来
            if (getCol(this.position) === 1) p.push(p2);
            // 如果行数是第九行 把p1传进来
            else if (getCol(this.position) === COL) p.push(p1);
            // 否则返回p1 p2
            else p.push(p1, p2);
        }
        // down 加上蹩马腿判断
        if (getRow(this.position) >= 3 && !this.haveChess(this.position - COL)) {
            // 移动
            // 列出点位
            let p1 = this.position - COL * 2 + 1;
            let p2 = this.position - COL * 2 - 1;
            // 如果行数是第一行 把p2传进来
            if (getCol(this.position) === 1) p.push(p2);
            // 如果行数是第九行 把p1传进来
            else if (getCol(this.position) === COL) p.push(p1);
            // 否则返回p1 p2
            else p.push(p1, p2);
        }
        // left 加上蹩马腿判断
        if (getCol(this.position) >= 3 && !this.haveChess(this.position - 1)) {
            // 移动
            // 列出点位
            let p1 = this.position - 2 + COL;
            let p2 = this.position - 2 - COL;
            // 如果列数是第一列 把p1传进来
            if (getRow(this.position) === 1) p.push(p1);
            // 如果列数是第九列 把p2传进来
            else if (getRow(this.position) === ROW) p.push(p2);
            // 否则返回p1 p2
            else p.push(p1, p2);
        }
        // right 加上蹩马腿判断
        if (getCol(this.position) <= COL - 3 && !this.haveChess(this.position + 1)) {
            // 移动
            // 列出点位
            let p1 = this.position + 2 + COL;
            let p2 = this.position + 2 - COL;
            // 如果列数是第一列 把p2传进来
            if (getRow(this.position) === 1) p.push(p2);
            // 如果列数是第九列 把p1传进来
            else if (getRow(this.position) === ROW) p.push(p1);
            // 否则返回p1 p2
            else p.push(p1, p2);
        }
        // 2.当某方向的第一个点位被占据时，无法向该方向移动

        return p;
    }
}
