import { COL, ROW } from "@/config/config";
import { GEBI, getCol, getRow } from "@/utils/utils";

export class Chess {
    constructor(position, camp) {
        this.name = '';
        this.position = position;
        this.camp = camp;
        this.inWhichArea = camp;
    }

    move(to) {
        let point = GEBI(this.position + '');
        let boginPosition;
        let hoveFinish = false;

        point.innerText = '';
        point.classList.remove(`camp${this.camp}`);
        boginPosition = this.position;
        this.position = to;
        point = GEBI(this.position + '');

        if (point.innerText !== '') {
            point.classList.remove(`camp${this.camp ? 0 : 1}`);
            if (point?.innerText === '将') {
                alert(`恭喜${this.camp ? '黑方' : '红方'}获胜`);
                hoveFinish = true;
            }
        }

        point.innerText = this.name;
        point.classList.add(`camp${this.camp}`);
        this.inWhichArea = this.position <= COL * ROW / 2 ? 0 : 1;

        return hoveFinish;
    }

    getTopMoviableArea() {
        let p = [];
        for (let i = this.position; i <= 90; i += COL) {
            if (i === this.position) continue;
            if (GEBI(i + '')?.innerText) {
                p.push(i);
                break;
            }
            p.push(i);
        }
        return p;
    }

    getDownMoviableArea() {
        let p = [];
        for (let i = this.position; i >= 0; i -= COL) {
            if (i === this.position) continue;
            if (GEBI(i + '')?.innerText) {
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
            if (GEBI(i + '')?.innerText) {
                p.push(i);
                break;
            }
            p.push(i);
        }
        return p;
    }

    getRigthMoviableArea() {
        let p = [];
        for (let i = this.position; i <= getRow(this.position) * COL; i++) {
            if (i === this.position) continue;
            if (GEBI(i + '')?.innerText) {
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
