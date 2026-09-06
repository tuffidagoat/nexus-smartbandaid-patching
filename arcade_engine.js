// Dynamic Arcade Environment Engine Loop Initialization
const canvas = document.getElementById('arcadeCanvas');
const ctx = canvas.getContext('2d');

let gravity = 0.5;
let keys = {};

let bridgeActive = window.bridgeActive;
let dragonActive = window.dragonActive;
let rockX = window.rockX;

let player = {
    x: 130, 
    y: 160,
    width: 20,
    height: 35,
    vx: 0,
    vy: 0,
    speed: window.playerSpeed,
    jumpForce: 10,
    grounded: false,
    lives: 3,
    gameState: "PLAYING"
};

// Start with ONLY the left green spawn platform hardcoded
let platforms = [
    {x: 0, y: 260, w: 200, h: 40, type: "ground"}
];

// 🔥 DYNAMIC COLLISION PATCH INJECTION
// The grey arena ground ONLY becomes solid if the patch data stream registers it!
if (bridgeActive) {
    // Inject the wood bridge planks structure
    platforms.push({x: 200, y: 260, w: 220, h: 10, type: "bridge"});
    // Inject the grey boss arena platform layout block
    platforms.push({x: 420, y: 240, w: 180, h: 60, type: "boss_arena"});
}

window.addEventListener('keydown', (e) => {
    if(["Space", "ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight"].includes(e.code)) {
        e.preventDefault();
    }
    keys[e.code] = true;
    
    if (player.gameState !== "PLAYING" && e.code === "KeyR") {
        player.lives = 3;
        player.x = 130;
        player.y = 160;
        player.vx = 0;
        player.vy = 0;
        player.gameState = "PLAYING";
    }
});
window.addEventListener('keyup', (e) => { keys[e.code] = false; });

function update() {
    if (player.gameState !== "PLAYING") return;
    
    if (keys['ArrowLeft'] || keys['KeyA']) player.vx = -player.speed;
    else if (keys['ArrowRight'] || keys['KeyD']) player.vx = player.speed;
    else player.vx = 0;
    
    if ((keys['Space'] || keys['ArrowUp'] || keys['KeyW']) && player.grounded) {
        player.vy = -player.jumpForce;
        player.grounded = false;
    }
    
    player.vy += gravity;
    player.x += player.vx;
    
    for (let plat of platforms) {
        if (player.x < plat.x + plat.w && player.x + player.width > plat.x && player.y < plat.y + plat.h && player.y + player.height > plat.y) {
            if (player.vx > 0) player.x = plat.x - player.width; 
            else if (player.vx < 0) player.x = plat.x + plat.w; 
            player.vx = 0;
        }
    }
    
    player.y += player.vy;
    player.grounded = false;
    for (let plat of platforms) {
        if (player.x < plat.x + plat.w && player.x + player.width > plat.x && player.y < plat.y + plat.h && player.y + player.height > plat.y) {
            if (player.vy > 0) {
                player.y = plat.y - player.height;
                player.vy = 0;
                player.grounded = true;
            } else if (player.vy < 0) {
                player.y = plat.y + plat.h;
                player.vy = 0;
            }
        }
    }
    
    if (player.x < 0) player.x = 0;
    if (player.x + player.width > canvas.width) player.x = canvas.width - player.width;
    
    if (player.y > canvas.height) {
        player.lives--;
        if (player.lives <= 0) {
            player.gameState = "GAMEOVER";
        } else {
            player.x = 130;
            player.y = 160;
            player.vx = 0;
            player.vy = 0;
        }
    }
    
    if (player.x > 440 && player.grounded && dragonActive) {
        player.gameState = "VICTORY";
    }
}

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = '#87CEEB';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    // VISUAL TIP FOR JUDGES: Keep the arena visually drawn in v1 so they can see they are clipping through it!
    if (!bridgeActive) {
        ctx.fillStyle = 'rgba(68, 68, 68, 0.3)'; // Renders ghosted translucent grey arena
        ctx.fillRect(420, 240, 180, 60);
    }
    
    for (let plat of platforms) {
        if (plat.type === "ground") ctx.fillStyle = '#228B22';
        else if (plat.type === "boss_arena") ctx.fillStyle = '#444'; // Fully solid grey stone arena
        else if (plat.type === "bridge") ctx.fillStyle = '#8B4513';
        ctx.fillRect(plat.x, plat.y, plat.w, plat.h);
    }
    
    ctx.fillStyle = '#808080';
    ctx.beginPath();
    ctx.arc(rockX, 225, 15, 0, Math.PI * 2);
    ctx.fill();
    
    if (dragonActive) {
        ctx.fillStyle = '#4B0082';
        ctx.fillRect(520, 140, 50, 100);
        ctx.fillStyle = '#FFD700';
        ctx.font = "bold 11px Arial";
        ctx.fillText("🐉 BOSS", 525, 120);
    }
    
    ctx.fillStyle = '#FF0000';
    ctx.fillRect(player.x, player.y, player.width, player.height);
    
    ctx.fillStyle = '#000';
    ctx.font = "bold 14px Arial";
    ctx.fillText("💖 Lives: " + "❤️".repeat(player.lives), 15, 25);
    
    if (!bridgeActive) {
        ctx.fillStyle = '#D8000C';
        ctx.fillText("⚠️ Missing Data Architecture: Level Unbeatable in v1 Build!", 15, 50);
        ctx.fillStyle = '#555';
        ctx.font = "11px Arial";
        ctx.fillText("⚡ Legacy Physics: Arena Platform Unregistered in Memory Map", 15, 70);
    } else {
        ctx.fillStyle = '#4F8A10';
        ctx.fillText("✅ Smart Patch Active: Network Patch Bridge Constructed!", 15, 50);
        ctx.fillStyle = '#005A9C';
        ctx.font = "11px Arial";
        ctx.fillText("⚡ Physics Core Upgraded: Arena Ground Objects Fully Instantiated!", 15, 70);
    }
    
    if (player.gameState === "GAMEOVER") {
        ctx.fillStyle = 'rgba(0, 0, 0, 0.75)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = '#FFF';
        ctx.font = "bold 30px Arial";
        ctx.fillText("GAME OVER", 210, 130);
        ctx.font = "16px Arial";
        ctx.fillText("You fell into the unpatched file gap!", 170, 170);
        ctx.fillText("Press 'R' to respawn player clone", 190, 200);
    } else if (player.gameState === "VICTORY") {
        ctx.fillStyle = 'rgba(0, 0, 0, 0.8)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = '#FFD700';
        ctx.font = "bold 32px Arial";
        ctx.fillText("⚡ VICTORY! ⚡", 190, 130);
        ctx.fillStyle = '#FFF';
        ctx.font = "16px Arial";
        ctx.fillText("You successfully crossed the dynamic patch bridge", 120, 170);
        ctx.fillText("and challenged the structural code boss node!", 140, 190);
        ctx.fillText("Press 'R' to clear run cache loops", 190, 230);
    }
}

function gameLoop() {
    update();
    draw();
    requestAnimationFrame(gameLoop);
}

canvas.focus();
gameLoop();
