
export const XYZToPosition = (x, y, z) => {
    return z*45-y*9-x+45;
}
export const PositionToXYZ = (position) => {
    position = position-1;
    let z = Math.floor((position)/45);
    position = position-z*45;
    let y = 4-Math.floor(position/9);
    position = position % 9;
    let x = 8-position;
    return [x,y,z];
}

export const ReportDecoder = (input) => {
    if(input == 'Bad_content'){
        return '违规发言'
    }
    if(input == 'Bad_behaviour'){
        return '恶意行为'
    }
    if(input == 'Bad_selfie'){
        return '违规头像或信息'
    }
    if(input == 'Other'){
        return '其他'
    }
    if(input == 'Apeal_bad_report'){
        return '恶意举报'
    }
    if(input == 'Bad_bug'){
        return '遭遇bug'
    }
    if(input == 'Ask_help'){
        return '请求帮助'
    }
    if(input == 'Other'){
        return '其他'
    }

    return input
}
