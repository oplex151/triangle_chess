<script setup>
// 最小化move示例
import board from '@/views/Game/board.vue'
const board = ref(null)
const Move = (data) => {
    my_camp.value = (my_camp.value+1)%3
    board.value.movePieceSuccess(data)
}
</script setup>

<template>
    <div>
        <board :my_camp=my_camp ref="board" @requireMove="Move"/>
    </div>
</template> 