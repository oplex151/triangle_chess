//存放玩家是活着
export var lives = [true, true, true];
export function changeLives(livesin) {
    for (let i = 0; i < 3; i++) {
        lives[i] = livesin[i];
    }
}