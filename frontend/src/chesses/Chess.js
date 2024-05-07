import { COL, ROWMID, ROWTOP, ROWBOT } from "@/config/config";
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
            let originalCamp = null;
            for(let i = 0 ; i < 3 ; i++){
                if(point.classList.contains(`camp${i}`)){
                    originalCamp = i ;
                    break;
                }
            }
            point.classList.remove(`camp${originalCamp}`);
            if (point?.innerText === '将') {
                switch (this.camp){
                    case 0:
                        alert('红方淘汰');
                        break;
                    case 1:
                        alert('黑方淘汰');
                        break;
                    case 2:
                        alert('金方淘汰');
                        break;
                    default:
                        break;
                }
                hoveFinish = true;
            }
        }

        point.innerText = this.name;

        point.classList.add(`camp${this.camp}`);

        if(this.position <= (COL * ROWBOT)) {
            this.inWhichArea = 0;
        }
        else if((this.position > (COL * ROWBOT)) && (this.position <= (COL * ROWMID))){
            this.inWhichArea = 1;
        }
        else{
            this.inWhichArea = 2;
        }
        // this.inWhichArea = this.position <= COL * ROW / 2 ? 0 : 1;
        return hoveFinish;
    }

    get_A_MoviableArea() {
        let p = [];
        for (let i = this.position; i <= ROWBOT * COL; i += COL) {
            if (i === this.position) continue;
            if (GEBI(i + '')?.innerText) {
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
            if (GEBI(i + '')?.innerText) {
                p.push(i);
                break;
            }
            p.push(i);
        }
        return p;
    }

    get_C_MoviableArea(){
        let p = [];
        for (let i = this.position; i <= ROWTOP * COL; i += COL) {
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

    getRightMoviableArea() {
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
