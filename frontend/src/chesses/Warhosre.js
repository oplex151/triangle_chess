import { COL, ROWTOP,ROWMID,ROWBOT } from "@/config/config";
import { getCol, getRow } from "@/utils/utils";
import { Chess } from "./Chess";

export class Warhosre extends Chess {
    constructor(position, camp,inWhichArea) {
        super(position, camp,inWhichArea);
        this.name = "马";
    }

    canMove() {
        let p = [];
        // 1.上下左右 共 8个日字形点位移动
        // 首先要确定当前位置 至少是在上方第三行的位置
        // 如果返回的行数<=总行数-3 就会进行移动
        // top 加上蹩马腿判断
        let ROW = 0;
        switch (this.inWhichArea){
            case 0:
                ROW = ROWBOT
                break;
            case 1:
                ROW = ROWMID
                break;
            case 2:
                ROW = ROWTOP
                break;
        }

        // UP 向上
        if (getRow(this.position) <= ROW - 2 && !this.haveChess(this.position + COL)) {
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
        // 本棋盘
        if (getRow(this.position) >= 3 + ROW - ROWBOT && !this.haveChess(this.position - COL)) {
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
        // 其他棋盘
        else {
            let p1 = 0;
            let p2 = 0;
            let p3 = 0;
            let p4 = 0;

            switch (ROW){
                case ROWBOT:
                    p1 = (2 - (getRow(this.position) - (ROW - ROWBOT))) * COL + 1 + COL - getCol(this.position) + 1 + ROWBOT * COL;
                    p2 = (2 - (getRow(this.position) - (ROW - ROWBOT))) * COL - 1 + COL - getCol(this.position) + 1 + ROWBOT * COL;

                    p3 = (2 - (getRow(this.position) - (ROW - ROWBOT))) * COL + 1 + COL - getCol(this.position) + 1 + ROWMID * COL;
                    p4 = (2 - (getRow(this.position) - (ROW - ROWBOT))) * COL - 1 + COL - getCol(this.position) + 1 + ROWMID * COL;
                    if(getRow(this.position) == 1 + ROW - ROWBOT){
                        if(!this.haveChess((2 - (getRow(this.position) - (ROW - ROWBOT))) * COL - getCol(this.position) + 1 + ROWBOT * COL)){
                            if(getCol(this.position) !== 1){
                                p.push(p1);
                            }
                            if (getCol(this.position) !== COL){
                                p.push(p2);
                            }
                        }
                        if (!this.haveChess((2 - (getRow(this.position) - (ROW - ROWBOT))) * COL - getCol(this.position) + 1 + ROWMID * COL)){
                            if(getCol(this.position) !== 1){
                                p.push(p3);
                            }
                            if (getCol(this.position) !== COL){
                                p.push(p4);
                            }
                        }
                    }
                    else{
                        if(getCol(this.position) !== 1){
                            p.push(p1,p3);
                        }
                        if (getCol(this.position) !== COL){
                            p.push(p2,p4);
                        }
                    }
                    break;
                case ROWMID:
                    p1 = (2 - (getRow(this.position) - (ROW - ROWBOT))) * COL + 1 + COL - getCol(this.position) + 1 ;
                    p2 = (2 - (getRow(this.position) - (ROW - ROWBOT))) * COL - 1 + COL - getCol(this.position) + 1 ;

                    p3 = (2 - (getRow(this.position) - (ROW - ROWBOT))) * COL + 1 + COL - getCol(this.position) + 1 + ROWMID * COL;
                    p4 = (2 - (getRow(this.position) - (ROW - ROWBOT))) * COL - 1 + COL - getCol(this.position) + 1 + ROWMID * COL;
                    if(getRow(this.position) == 1 + ROW - ROWBOT){
                        if(!this.haveChess((2 - (getRow(this.position) - (ROW - ROWBOT))) * COL - getCol(this.position) + 1)){
                            if(getCol(this.position) !== 1){
                                p.push(p1);
                            }
                            if (getCol(this.position) !== COL){
                                p.push(p2);
                            }
                        }
                        if (!this.haveChess((2 - (getRow(this.position) - (ROW - ROWBOT))) * COL - getCol(this.position) + 1 + ROWMID * COL)){
                            if(getCol(this.position) !== 1){
                                p.push(p3);
                            }
                            if (getCol(this.position) !== COL){
                                p.push(p4);
                            }
                        }
                    }
                    else{
                        if(getCol(this.position) !== 1){
                            p.push(p1,p3);
                        }
                        if (getCol(this.position) !== COL){
                            p.push(p2,p4);
                        }
                    }
                    break;
                case ROWTOP:
                    p1 = (2 - (getRow(this.position) - (ROW - ROWBOT))) * COL + 1 + COL - getCol(this.position) + 1 + ROWBOT * COL;
                    p2 = (2 - (getRow(this.position) - (ROW - ROWBOT))) * COL - 1 + COL - getCol(this.position) + 1 + ROWBOT * COL;

                    p3 = (2 - (getRow(this.position) - (ROW - ROWBOT))) * COL + 1 + COL - getCol(this.position) + 1 ;
                    p4 = (2 - (getRow(this.position) - (ROW - ROWBOT))) * COL - 1 + COL - getCol(this.position) + 1 ;
                    if(getRow(this.position) == 1 + ROW - ROWBOT){
                        if(!this.haveChess((2 - (getRow(this.position) - (ROW - ROWBOT))) * COL - getCol(this.position) + 1 + ROWBOT * COL)){
                            if(getCol(this.position) !== 1){
                                p.push(p1);
                            }
                            if (getCol(this.position) !== COL){
                                p.push(p2);
                            }
                        }
                        if (!this.haveChess((2 - (getRow(this.position) - (ROW - ROWBOT))) * COL + 1 + COL - getCol(this.position) + 1)){
                            if(getCol(this.position) !== 1){
                                p.push(p3);
                            }
                            if (getCol(this.position) !== COL){
                                p.push(p4);
                            }
                        }
                    }
                    else{
                        if(getCol(this.position) !== 1){
                            p.push(p1,p3);
                        }
                        if (getCol(this.position) !== COL){
                            p.push(p2,p4);
                        }
                    }
                    break;
            }
        }

        // left 加上蹩马腿判断
        if (getCol(this.position) >= 3 && !this.haveChess(this.position - 1)) {
            // 移动
            // 列出点位
            let p1,p2,p3 = 0;
            // 不越界
            if (getRow(this.position) >= 2 + ROW - ROWBOT ) {
                p1 = this.position - 2 + COL;
                p2 = this.position - 2 - COL;
                // 如果列数是第一列 把p1传进来
                // if (getRow(this.position) === 0 + ROW - ROWBOT) p.push(p1);
                // // 如果列数是第九列 把p2传进来
                if (getRow(this.position) === ROW) p.push(p2);
                // 否则返回p1 p2
                else p.push(p1, p2);
            }
            else{
                switch (ROW){
                    case ROWBOT:
                        p1 = this.position - 2 + COL;

                        p2 = (1 - (getRow(this.position) - (ROW - ROWBOT))) * COL - 2 + COL - getCol(this.position) + 1 + ROWBOT * COL;
                        p3 = (1 - (getRow(this.position) - (ROW - ROWBOT))) * COL - 2 + COL - getCol(this.position) + 1 + ROWMID * COL;
                        p.push(p1, p2, p3);
                        break;
                    case ROWMID:
                        p1 = this.position - 2 + COL ;

                        p2 = (1 - (getRow(this.position) - (ROW - ROWBOT))) * COL - 2 + COL - getCol(this.position) + 1 ;
                        p3 = (1 - (getRow(this.position) - (ROW - ROWBOT))) * COL - 2 + COL - getCol(this.position) + 1 + ROWMID * COL;
                        p.push(p1, p2 ,p3);
                        break;
                    case ROWTOP:
                        p1 = this.position - 2 + COL;

                        p2 = (1 - (getRow(this.position) - (ROW - ROWBOT))) * COL - 2 + COL - getCol(this.position) + 1 + ROWBOT * COL;
                        p3 = (1 - (getRow(this.position) - (ROW - ROWBOT))) * COL - 2 + COL - getCol(this.position) + 1 ;
                        p.push(p1, p2 ,p3);
                        break;
                }
            }
        }


        // right 加上蹩马腿判断
        if (getCol(this.position) <= COL - 3 && !this.haveChess(this.position + 1)) {
            // 移动
            // 列出点位
            let p1,p2,p3 = 0;
            // 不越界
            if (getRow(this.position) >= 2 + ROW - ROWBOT ) {
                p1 = this.position + 2 + COL;
                p2 = this.position + 2 - COL;
                // 如果列数是第一列 把p1传进来
                // if (getRow(this.position) === 0 + ROW - ROWBOT) p.push(p1);
                // // 如果列数是第九列 把p2传进来
                if (getRow(this.position) === ROW) p.push(p2);
                // 否则返回p1 p2
                else p.push(p1, p2);
            }
            else{
                switch (ROW){
                    case ROWBOT:
                        p1 = this.position + 2 + COL;

                        p2 = (1 - (getRow(this.position) - (ROW - ROWBOT))) * COL + 2 + COL - getCol(this.position) + 1 + ROWBOT * COL;
                        p3 = (1 - (getRow(this.position) - (ROW - ROWBOT))) * COL + 2 + COL - getCol(this.position) + 1 + ROWMID * COL;
                        p.push(p1, p2, p3);
                        break;
                    case ROWMID:
                        p1 = this.position + 2 + COL ;

                        p2 = (1 - (getRow(this.position) - (ROW - ROWBOT))) * COL + 2 + COL - getCol(this.position) + 1 ;
                        p3 = (1 - (getRow(this.position) - (ROW - ROWBOT))) * COL + 2 + COL - getCol(this.position) + 1 + ROWMID * COL;
                        p.push(p1, p2 ,p3);
                        break;
                    case ROWTOP:
                        p1 = this.position + 2 + COL;

                        p2 = (1 - (getRow(this.position) - (ROW - ROWBOT))) * COL + 2 + COL - getCol(this.position) + 1 + ROWBOT * COL;
                        p3 = (1 - (getRow(this.position) - (ROW - ROWBOT))) * COL + 2 + COL - getCol(this.position) + 1 ;
                        p.push(p1, p2 ,p3);
                        break;
                }
            }
        }
        // 2.当某方向的第一个点位被占据时，无法向该方向移动

        return p;
    }
}
