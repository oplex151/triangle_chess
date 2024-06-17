import { COL, ROWMID, ROWTOP, ROWBOT } from "@/config/config";
import { GEBI, getCol, getRow } from "@/utils/utils";
import { lives } from "../lib/live";
import { ElMessage } from "element-plus";
import main from "@/main";

export class Chess {
    constructor(position, camp, inWhichArea) {
        this.name = '';
        this.position = position;
        this.camp = camp;
        this.inWhichArea = inWhichArea;
        this.image = "";
    }

    move(to) {
        let point = GEBI(this.position + '');
        let beginPosition;
        let hoveFinish = false;

        point.innerText = '';
        point.style.backgroundImage = "";

        point.classList.remove(`camp${this.camp}`);
        beginPosition = this.position;
        this.position = to;
        point = GEBI(this.position + '');

        if (point.innerText !== '') {
            let originalCamp = null;
            for (let i = 0; i < 3; i++) {
                if (point.classList.contains(`camp${i}`)) {
                    originalCamp = i;
                    break;
                }
            }
            point.classList.remove(`camp${originalCamp}`);
            if (point?.innerText === '将') {
                let message = '';
                switch (originalCamp) {
                    case 0:
                        message = '红方淘汰';
                        break;
                    case 1:
                        message = '黑方淘汰';
                        break;
                    case 2:
                        message = '金方淘汰';
                        break;
                    default:
                        break;
                }
                ElMessage.info(message); // 使用ElMessage.info显示消息
                lives[originalCamp] = false;
                hoveFinish = true;
            }
        }

        point.innerText = this.name;
        switch (this.camp) {
            case 0:
                point.classList.add('camp0');
                //this.image = "@/assets/images/game/chess/realChess/" + this.name + "白.png";
                this.image = main.url + "/static/game/chess/realChess/" + this.name + "白.png";
                break;

            case 1:
                point.classList.add('camp1');
                //this.image = "@/assets/images/game/chess/realChess/" + this.name + "黑.png";
                this.image = main.url + "/static/game/chess/realChess/" + this.name + "黑.png";
                break;
            case 2:
                point.classList.add('camp2');
                //this.image = "@/assets/images/game/chess/realChess/" + this.name + "金.png";
                this.image = main.url + "/static/game/chess/realChess/" + this.name + "金.png";
                break;
        }
        point.classList.add('chess-background');  // 添加自定义class
        point.style.background = `url(${this.image}) center center / contain no-repeat`;
        point.style.backgroundSize = '53px'; // 将背景图片大小设置为 53px，宽度和高度均为 53px

        if (this.position <= (COL * ROWBOT)) {
            this.inWhichArea = 0;
        }
        else if ((this.position > (COL * ROWBOT)) && (this.position <= (COL * ROWMID))) {
            this.inWhichArea = 1;
        }
        else {
            this.inWhichArea = 2;
        }
        // this.inWhichArea = this.position <= COL * ROW / 2 ? 0 : 1;
        return hoveFinish;
    }

    get_A_MoviableArea() {
        let p = [];
        for (let i = this.position; i <= ROWBOT * COL; i += COL) {
            if (i === this.position) continue;
            const target = GEBI(i + '');
            if (target?.innerText) {
                if (target.classList.contains(`camp${this.camp}`)) break;
                p.push(i);
                break;
            }
            p.push(i);
        }
        return p;
    }

    get_B_MoviableArea() {
        let p = [];
        for (let i = this.position; i <= ROWMID * COL; i += COL) {
            if (i === this.position) continue;
            const target = GEBI(i + '');
            if (target?.innerText) {
                if (target.classList.contains(`camp${this.camp}`)) break;
                p.push(i);
                break;
            }
            p.push(i);
        }
        return p;
    }

    get_C_MoviableArea() {
        let p = [];
        for (let i = this.position; i <= ROWTOP * COL; i += COL) {
            if (i === this.position) continue;
            const target = GEBI(i + '');
            if (target?.innerText) {
                if (target.classList.contains(`camp${this.camp}`)) break;
                p.push(i);
                break;
            }
            p.push(i);
        }
        return p;
    }

    getLeftMoviableArea() {
        let p = [];
        for (let i = this.position; i >= (getRow(this.position) - 1) * COL + 1; i--) {
            if (i === this.position) continue;
            const target = GEBI(i + '');
            if (target?.innerText) {
                if (target.classList.contains(`camp${this.camp}`)) break;
                p.push(i);
                break;
            }
            p.push(i);
        }
        return p;
    }

    getRightMoviableArea() {
        let p = [];
        for (let i = this.position; i <= getRow(this.position) * COL; i++) {
            if (i === this.position) continue;
            const target = GEBI(i + '');
            if (target?.innerText) {
                if (target.classList.contains(`camp${this.camp}`)) break;
                p.push(i);
                break;
            }
            p.push(i);
        }
        return p;
    }

    haveChess(position) {
        return GEBI(position + '')?.innerText !== '';
    }
}