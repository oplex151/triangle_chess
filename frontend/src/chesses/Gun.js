import { AREATOP,AREABOT,AREAMID, COL,ROWBOT,ROWMID,ROWTOP } from "@/config/config";
import {GEBI, getCol, getRow} from "@/utils/utils";
import { Chess } from "./Chess";

export class Gun extends Chess {
    constructor(position, camp,inWhichArea) {
        super(position, camp,inWhichArea);
        this.name = "炮";
    }

    canMove() {
        let p = [];
        // 上下左右行走
        // 吃掉某方向的第二颗非己方棋子
        p.push(...this.getVerticalMoviableArea());
        // p.push(...this.getDownMoviableArea());
        p.push(...this.getLeftMoviableArea());
        p.push(...this.getRightMoviableArea());
        return p;
    }

    getVerticalMoviableArea() {
        // 保存返回值
        let p = [];
        // 判断是否遇到了第一个棋子
        let haveFirstChess = false;
        // 是否遇到第二个棋子
        let haveSecondChess = false;
        // 获取当前的位置的行数 根据行数*行长
        // 上移动
        let MarkFlag = [1,1,1];
        let ROW = 0;
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
            if (i == this.position) continue;
            const chess = GEBI(i + '');
            // 第二个弈子
            if(haveFirstChess){
                if(chess?.innerText !== ''){
                    p.push(i);
                    haveSecondChess = true;
                    break;
                }
                else continue;
            }
            // 第一个弈子
            if(chess?.innerText !== ''){
                haveFirstChess = true;
                continue;
            }
            p.push(i);
        }

        // 重置判断是否遇到了第一个棋子
        haveFirstChess = false;
        // 重置判断是否遇到第二个棋子
        haveSecondChess = false;
        // 向下
        for(let i = this.position ; i > (ROW - ROWBOT) * COL ; i -= COL){
            if (i == this.position) continue;

            const chess = GEBI(i + '');
            // 第二个弈子
            if(haveFirstChess){
                if(chess?.innerText !== ''){
                    p.push(i);
                    haveSecondChess = true;
                    break;
                }
                else continue;
            }
            // 第一个弈子
            if(chess?.innerText !== ''){
                haveFirstChess = true;
                continue;
            }
            p.push(i);
        }
        // 越棋盘
        // 未找到第一个棋子
        if(!haveFirstChess){
            // 我不在第一阵营
            if(MarkFlag[0] && ((ROW == ROWMID && getCol(this.position) <= 5)||(ROW == ROWTOP && getCol(this.position) >= 5))){
                for(let i = COL - getCol(this.position) + 1 ; i <= AREABOT ; i += COL ){
                    const chess = GEBI(i + '');
                    // 第二个弈子
                    if(haveFirstChess){
                        if(chess?.innerText !== ''){
                            p.push(i);
                            break;
                        }
                        else continue;
                    }
                    // 第一个弈子
                    if(chess?.innerText !== ''){
                        haveFirstChess = true;
                        continue;
                    }
                    p.push(i);
                }
            }
            // 重置判断是否遇到了第一个棋子
            haveFirstChess = false;
            // 重置判断是否遇到第二个棋子
            haveSecondChess = false;

            // 我不在第二阵营
            if(MarkFlag[1]&& ((ROW == ROWBOT && getCol(this.position) >= 5)||(ROW == ROWTOP && getCol(this.position) <= 5))){
                for(let i = AREABOT + COL - getCol(this.position) + 1; i <= AREAMID ; i += COL ){
                    const chess = GEBI(i + '');
                    // 第二个弈子
                    if(haveFirstChess){
                        if(chess?.innerText !== ''){
                            p.push(i);
                            break;
                        }
                        else continue;
                    }
                    // 第一个弈子
                    if(chess?.innerText !== ''){
                        haveFirstChess = true;
                        continue;
                    }
                    p.push(i);
                }
            }
            // 重置判断是否遇到了第一个棋子
            haveFirstChess = false;
            // 重置判断是否遇到第二个棋子
            haveSecondChess = false;

            // 我不在第二阵营
            if(MarkFlag[2] && ((ROW == ROWMID && getCol(this.position) >= 5)||(ROW == ROWBOT && getCol(this.position) <= 5))){
                for(let i = AREAMID + COL - getCol(this.position)+ 1 ; i <= AREATOP ; i += COL ){
                    const chess = GEBI(i + '');
                    // 第二个弈子
                    if(haveFirstChess){
                        if(chess?.innerText !== ''){
                            p.push(i);
                            break;
                        }
                        else continue;
                    }
                    // 第一个弈子
                    if(chess?.innerText !== ''){
                        haveFirstChess = true;
                        continue;
                    }
                    p.push(i);
                }
            }
        }
        // 找到了第一个棋子
        else{
            // 未找到第二个棋子
            if(!haveSecondChess){
                // 我不在第一阵营
                if(MarkFlag[0] && ((ROW == ROWMID && getCol(this.position) <= 5)||(ROW == ROWTOP && getCol(this.position) >= 5))){
                    for(let i = COL - getCol(this.position)+ 1 ; i <= AREABOT ; i += COL ){
                        const chess = GEBI(i + '');
                        // 第二个弈子
                        if(chess?.innerText !== ''){
                            p.push(i);
                            break;
                        }
                        else continue;
                    }
                }
                // 重置判断是否遇到第二个棋子
                haveSecondChess = false;
                // 我不在第二阵营
                if(MarkFlag[1] && ((ROW == ROWBOT && getCol(this.position) >= 5)||(ROW == ROWTOP && getCol(this.position) <= 5))){
                    for(let i = AREABOT + COL - getCol(this.position) + 1; i <= AREAMID ; i += COL ){
                        const chess = GEBI(i + '');
                        // 第二个弈子
                        if(chess?.innerText !== ''){
                            p.push(i);
                            break;
                        }
                        else continue;
                    }
                }
                // 重置判断是否遇到第二个棋子
                haveSecondChess = false;
                // 我不在第二阵营
                if(MarkFlag[2] && ((ROW == ROWMID && getCol(this.position) >= 5)||(ROW == ROWBOT && getCol(this.position) <= 5))){
                    for(let i = AREAMID + COL - getCol(this.position) + 1; i <= AREATOP ; i += COL ){
                        const chess = GEBI(i + '');
                        // 第二个弈子
                        if(chess?.innerText !== ''){
                            p.push(i);
                            break;
                        }
                        else continue;
                    }
                }
            }
        }
        return p;
    }

    // getDownMoviableArea() {
    //     // 保存返回值
    //     let p = [];
    //     // 判断是否遇到了第一个棋子
    //     let haveFirstChess = false;
    //     // 是否遇到第二个棋子
    //     let haveSecondChess = false;
    //     // 下移动
    //
    //     // 获取当前的位置的行数 根据行数*行长
    //     for (let i = this.position; i >= 0; i -= COL) {
    //         // 不包括自己的格子
    //         if (i === this.position) continue;
    //         // 获取到新点位的变量
    //         const chess = GEBI(i + '');
    //         // 第二颗棋子之后
    //         if (haveSecondChess) break;
    //         // 第一颗棋子之后的逻辑
    //         if (haveFirstChess && !haveSecondChess && chess?.innerText !== "") {
    //             p.push(i);
    //             haveSecondChess = true;
    //         }
    //         if (haveFirstChess && !haveSecondChess && chess?.innerText === "") continue;
    //         // 第一颗棋子之前的逻辑
    //         if (chess?.innerText !== '') {
    //             haveFirstChess = true;
    //             continue;
    //         }
    //         p.push(i);
    //     }
    //     return p;
    // }

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
