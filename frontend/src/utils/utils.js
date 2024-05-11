import { COL } from "@/config/config";

// 获取id
export const GEBI = (id) => document.getElementById(id);

// 获取列数
export const getCol = (position) => !(position % COL) ? COL : position % COL;

// 获取行数
export const getRow = (position) => !(position % COL) ? position / COL : Math.ceil(position / COL);
