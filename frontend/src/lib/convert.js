
export const XYZToPosition = (x, y, z) => {
    return z*45-y*9-x+45;
}
export const PositionToXYZ = (position) => {
    position = position-1;
    let z = Math.floor((position-1)/45);
    position = position-z*45;
    let y = 4-Math.floor(position/9);
    position = position%9;
    let x = 8-position;
    return [x,y,z];
}