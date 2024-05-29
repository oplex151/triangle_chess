import {AREABOT, AREAMID, AREATOP, COL, ROWBOT, ROWMID, ROWTOP} from "@/config/config";
import { Chess } from "./Chess";
import {GEBI, getCol, getRow} from "@/utils/utils.js";

export class Chariot extends Chess {
    constructor(position, camp, inWhichArea) {
        super(position, camp, inWhichArea);
        this.name = "车";
    }

    canMove() {
        // 保存返回值
        let p = [];
        // 把向上下左右的可移动点位加进总的可移动点位中
        p.push(...this.getVerticalMoviableArea());
        p.push(...this.getLeftMoviableArea());
        p.push(...this.getRightMoviableArea());
        return p;
    }
    getVerticalMoviableArea() {
        // 保存返回值
        let p = [];
        // 判断是否遇到了第一个棋子
        let haveFirstChess = false;
        // 获取当前的位置的行数 根据行数*行长
        // 上移动
        let MarkFlag = [1,1,1];
        let ROW = 0;
        // 判断是否需要更新位置
        switch (this.inWhichArea){
            case 0:
                MarkFlag[0] = 0;
                MarkFlag[1] = 1;
                MarkFlag[2] = 1;
                ROW = ROWBOT
                break;
            case 1:
                MarkFlag[0] = 1;
                MarkFlag[1] = 0;
                MarkFlag[2] = 1;
                ROW = ROWMID;
                break;
            case 2:
                MarkFlag[0] = 1;
                MarkFlag[1] = 1;
                MarkFlag[2] = 0;
                ROW = ROWTOP;
                break;
        }

        // 向上
        for(let i = this.position ; i <= ROW * COL ; i += COL){
            if(i ==this.position) continue;
            const chess = GEBI(i + '');
            // 第一个弈子
            if(chess?.innerText !== ''){
                p.push(i);
                haveFirstChess = true;
                break;
            }
            p.push(i);
        }

        // 重置判断是否遇到了第一个棋子
        haveFirstChess = false;
        // 向下
        for(let i = this.position ; i > (ROW - ROWBOT) * COL ; i -= COL){
            if(i == this.position) continue;

            const chess = GEBI(i + '');
            // 第一个弈子
            if(chess?.innerText !== ''){
                p.push(i);
                haveFirstChess = true;
                break;
            }
            p.push(i);
        }
        // 越棋盘
        // 未找到第一个棋子
        if(!haveFirstChess){
            // 我不在第一阵营
            if(MarkFlag[0] && ((ROW == ROWMID && getCol(this.position) <= 5)||(ROW == ROWTOP && getCol(this.position) >= 5))){
                for(let i = COL - getCol(this.position) + 1; i <= AREABOT ; i += COL ){
                    const chess = GEBI(i + '');
                    // 第一个弈子
                    if(chess?.innerText !== ''){
                        p.push(i);
                        haveFirstChess = true;
                        break;
                    }
                    p.push(i);
                }
            }
            // 重置判断是否遇到了第一个棋子
            haveFirstChess = false;
            // 我不在第二阵营
            if(MarkFlag[1] && ((ROW == ROWBOT && getCol(this.position) >= 5)||(ROW == ROWTOP && getCol(this.position) <= 5))){
                for(let i = AREABOT + COL - getCol(this.position) + 1; i <= AREAMID ; i += COL ){
                    const chess = GEBI(i + '');
                    // 第一个弈子
                    if(chess?.innerText !== ''){
                        p.push(i);
                        haveFirstChess = true;
                        break;
                    }
                    p.push(i);
                }
            }
            // 重置判断是否遇到了第一个棋子
            haveFirstChess = false;
            // 我不在第三阵营
            if(MarkFlag[2] && ((ROW == ROWMID && getCol(this.position) >= 5)||(ROW == ROWBOT && getCol(this.position) <= 5))){
                for(let i = AREAMID + COL - getCol(this.position) + 1; i <= AREATOP ; i += COL ){
                    const chess = GEBI(i + '');
                    if(chess?.innerText !== ''){
                        p.push(i);
                        haveFirstChess = true;
                        break;
                    }
                    p.push(i);
                }
            }
        }

        return p;
    }
}
