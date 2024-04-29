import { AREA, COL } from "@/config/config";
import { GEBI, getRow } from "@/utils/utils";
import { Chess } from "./Chess";

export class Gun extends Chess {
    constructor(position, camp) {
        super(position, camp);
        this.name = "炮";
    }

    canMove() {
        let p = [];
        // 上下左右行走
        // 吃掉某方向的第二颗非己方棋子
        p.push(...this.getTopMoviableArea());
        p.push(...this.getDownMoviableArea());
        p.push(...this.getLeftMoviableArea());
        p.push(...this.getRightMoviableArea());
        return p;
    }

    getTopMoviableArea() {
        // 保存返回值
        let p = [];
        // 判断是否遇到了第一个棋子
        let haveFirstChess = false;
        // 是否遇到第二个棋子
        let haveSecondChess = false;
        // 获取当前的位置的行数 根据行数*行长
        // 上移动
        for (let i = this.position; i <= AREA; i += COL) {
            // 不包括自己的格子
            if (i === this.position) continue;
            // 获取到新点位的变量
            const chess = GEBI(i + '');
            // 第二颗棋子之后
            if (haveSecondChess) break;
            // 第一颗棋子之后的逻辑
            if (haveFirstChess && !haveSecondChess && chess?.innerText !== "") {
                p.push(i);
                haveSecondChess = true;
            }
            if (haveFirstChess && !haveSecondChess && chess?.innerText === "") continue;
            // 第一颗棋子之前的逻辑
            if (chess?.innerText !== '') {
                haveFirstChess = true;
                continue;
            }
            p.push(i);
        }
        return p;
    }

    getDownMoviableArea() {
        // 保存返回值
        let p = [];
        // 判断是否遇到了第一个棋子
        let haveFirstChess = false;
        // 是否遇到第二个棋子
        let haveSecondChess = false;
        // 下移动
        // 获取当前的位置的行数 根据行数*行长
        for (let i = this.position; i >= 0; i -= COL) {
            // 不包括自己的格子
            if (i === this.position) continue;
            // 获取到新点位的变量
            const chess = GEBI(i + '');
            // 第二颗棋子之后
            if (haveSecondChess) break;
            // 第一颗棋子之后的逻辑
            if (haveFirstChess && !haveSecondChess && chess?.innerText !== "") {
                p.push(i);
                haveSecondChess = true;
            }
            if (haveFirstChess && !haveSecondChess && chess?.innerText === "") continue;
            // 第一颗棋子之前的逻辑
            if (chess?.innerText !== '') {
                haveFirstChess = true;
                continue;
            }
            p.push(i);
        }
        return p;
    }

    getLeftMoviableArea() {
        // 保存返回值
        let p = [];
        // 判断是否遇到了第一个棋子
        let haveFirstChess = false;
        // 是否遇到第二个棋子
        let haveSecondChess = false;
        // 获取当前的位置的行数 根据行数*行长
        // 左移动
        for (let i = this.position; i >= (getRow(this.position) - 1) * COL + 1; i--) {
            // 不包括自己的格子
            if (i === this.position) continue;
            // 获取到新点位的变量
            const chess = GEBI(i + '');
            // 第二颗棋子之后
            if (haveSecondChess) break;
            // 第一颗棋子之后的逻辑
            if (haveFirstChess && !haveSecondChess && chess?.innerText !== "") {
                p.push(i);
                haveSecondChess = true;
            }
            if (haveFirstChess && !haveSecondChess && chess?.innerText === "") continue;
            // 第一颗棋子之前的逻辑
            if (chess?.innerText !== '') {
                haveFirstChess = true;
                continue;
            }
            p.push(i);
        }
        return p;
    }

    getRightMoviableArea() {
        // 保存返回值
        let p = [];
        // 判断是否遇到了第一个棋子
        let haveFirstChess = false;
        // 是否遇到第二个棋子
        let haveSecondChess = false;
        // 获取当前的位置的行数 根据行数*行长
        // 右移动
        for (let i = this.position; i <= getRow(this.position) * COL; i++) {
            // 不包括自己的格子
            if (i === this.position) continue;
            // 获取到新点位的变量
            const chess = GEBI(i + '');
            // 第二颗棋子之后
            if (haveSecondChess) break;
            // 第一颗棋子之后的逻辑
            if (haveFirstChess && !haveSecondChess && chess?.innerText !== "") {
                p.push(i);
                haveSecondChess = true;
            }
            if (haveFirstChess && !haveSecondChess && chess?.innerText === "") continue;
            // 第一颗棋子之前的逻辑
            if (chess?.innerText !== '') {
                haveFirstChess = true;
                continue;
            }
            p.push(i);
        }
        return p;
    }
}
