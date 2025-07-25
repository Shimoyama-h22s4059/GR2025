$(function() {
    const dragon = $("#dragon")[0];
    announceDragon(dragon, "");
});

function announceDragon(canvas, str, color = "#000000") {
    const image = new Image();
    image.src = "/static/img/dragon.png";

    image.onload = () => {
        const ctx = canvas.getContext("2d");
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(image, 0, 0, canvas.width, canvas.height);

        ctx.font = "80px monospace";
        ctx.fillStyle = color;
        ctx.fillText(str, 66, 116);
    };
}