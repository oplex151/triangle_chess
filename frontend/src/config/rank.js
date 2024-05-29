//数字到段位的映射
export function getRankLevel(num){
  if (num < 0) {
    return '无';
  }
  else if (num < 5) {
    return '菜鸟';
  }
  else if (num < 10) {
    return '青铜';
  }
  else if (num < 20) {
    return '白银';
  }
  else if (num < 30) {
    return '黄金';
  }
  else if (num < 40) {
    return '白金';
  }
  else if (num < 50) {
    return '钻石';
  }
  else if (num < 60) {
    return '王者';
  }
  else {
    return '超神';
  }
}