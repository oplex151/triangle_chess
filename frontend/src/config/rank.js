//数字到段位的映射
export function getRankLevel(num){
  if (num < 0) {
    return '无';
  }
  else if (num < 1) {
    return '菜鸟';
  }
  else if (num < 2) {
    return '青铜';
  }
  else if (num < 3) {
    return '白银';
  }
  else if (num < 4) {
    return '黄金';
  }
  else if (num < 5) {
    return '白金';
  }
  else if (num < 6) {
    return '钻石';
  }
  else if (num < 7) {
    return '王者';
  }
  else {
    return '超神';
  }
}