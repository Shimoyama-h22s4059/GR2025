$(function() {
    const canvasHandwritten = $("#canvas-handwritten");
    const canvas = canvasHandwritten[0];
    const ctx = canvas.getContext("2d");

    initializeCanvas(canvas); // キャンバスの初期化

    let lastX = 0;
    let lastY = 0;
    let drawing = false;

    let lineWidth = 5;
    let debug = 0;

    canvas.addEventListener("mousedown", (e) => {
        drawing = true;
        [lastX, lastY] = [e.offsetX, e.offsetY];
    });

    canvas.addEventListener("mouseup", () => {
        drawing = false;
    });

    canvas.addEventListener("mousemove", (e) => {
        if (!drawing) return;

        ctx.strokeStyle = "black";
        ctx.lineWidth = lineWidth;
        ctx.lineCap = "round";

        ctx.beginPath();
        ctx.moveTo(lastX, lastY);          // 前回の位置
        ctx.lineTo(e.offsetX, e.offsetY);  // 現在の位置
        ctx.stroke();

        [lastX, lastY] = [e.offsetX, e.offsetY];  // 座標更新
    });

    const canvasClearButton = $("#button-canvas-clear");
    canvasClearButton.on("click", function () {
        initializeCanvas(canvas);
    }); // 初期化

    const lineWidthSelector = $("#line-width-selector");
    lineWidthSelector.on("input", function(e) {
        const lineWidthValue = $("#line-width-value");
        lineWidthValue.text(e.target.value);
        lineWidth = e.target.value;
    });

    const predictButton = $("#button-predict");
    predictButton.on("click", function() {
        const dataURL = canvas.toDataURL("image/png");
        console.log(dataURL);

        $.ajax({
            type: "POST",
            url: "/predict",
            contentType: "application/json",
            data: JSON.stringify({image: dataURL}),
            success: function (data) {
                announceDragon(dragon, data.prediction);
            },
            error: function() {
                announceDragon(dragon, "E");
            }
        });
    });

    const dragon = $("#dragon")[0];
    announceDragon(dragon, ""); // 初期化

    const debugSelector = $("#debug-selector");
    debugSelector.on("input", function(e) {
        const debugValue = $("#debug-value");
        debugValue.text(e.target.value);
        debug = e.target.value;
    });

    const applyDebugButton = $("#button-apply-debug");
    applyDebugButton.on("click", function () {
        debug = debugSelector.val();
        console.log(debug);
        announceDragon(dragon, debug);
    });
});

function initializeCanvas(canvas) {
    const ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = "white";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
}

function announceDragon(canvas, str) {
    const image = new Image();
    image.src = "/static/img/dragon.png";

    image.onload = () => {
        const ctx = canvas.getContext("2d");
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(image, 0, 0, canvas.width, canvas.height);

        ctx.font = "80px monospace";
        ctx.fillStyle = "black";
        ctx.fillText(str, 66, 116);
    };
}