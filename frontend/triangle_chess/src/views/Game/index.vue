<template>
  <div class="game-area">
    <div class="info-panel">
      <!-- Display game info here -->
      <div class="scoreboard">
        <div class="player-score">
          <span>Player 1:</span>
          <span>{{ player1Score }}</span>
        </div>
        <div class="player-score">
          <span>Player 2:</span>
          <span>{{ player2Score }}</span>
        </div>
        <div class="player-score">
          <span>Player 3:</span>
          <span>{{ player3Score }}</span>
        </div>
      </div>
      <div class="current-turn">
        <span>Current Turn:</span>
        <span>{{ currentTurn }}</span>
      </div>
      <div class="game-status">
        <span>Game Status:</span>
        <span>{{ gameStatus }}</span>
      </div>
    </div>
    <div class="chess-board">
    </div>
  </div>
</template>

<style scoped>
.game-area{
  position: relative;
}
.chess-board {
  height: 1000px; /* Adjust this value as needed */
  width: 1000px; /* Adjust this value as needed */
  background-image: url("@/assets/images/game/chessboard.jpg");
  background-size: cover;
  background-position: center;
}

.info-panel {
  position: absolute;
  top: 10px;
  left: 10px;
  background-color: rgba(255, 255, 255, 0.8);
  padding: 10px;
  border-radius: 5px;
}

.scoreboard {
  margin-bottom: 10px;
}

.player-score {
  display: flex;
  justify-content: space-between;
  margin-bottom: 5px;
}

.current-turn,
.game-status {
  display: flex;
  justify-content: space-between;
}
</style>
