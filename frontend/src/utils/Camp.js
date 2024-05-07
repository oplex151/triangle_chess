import { Chess } from "@/chesses/Chess";

// 标志两个阵营之间共有的一些属性
export class Camp {
    // 拥有一个棋子的数组 用它来保存我方阵营里吃掉了对方阵营的棋子
    constructor(chesses) {
        this.kills = [];
        this.chesses = chesses;
    }
    // 通过get方法把它暴露出去
    get() {
        return this.chesses;
    }
}
