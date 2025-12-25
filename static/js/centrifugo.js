const centrifuge = new Centrifuge('ws://localhost:8001/connection/websocket');

const questionId = 110004;

const sub = centrifuge.newSubscription(`answers:question_${questionId}`);

console.log("hello0");

sub.on('subscribed', function(ctx) {
    console.log('Подписались на канал!', ctx);
    console.log('Recoverable:', ctx.recoverable);
    console.log('Positioned:', ctx.positioned);
});

sub.on("publication", function(ctx) {
    console.log("New answer:", ctx.data);
    
    const answerHtml = `
        <div class="answer">
            <p><strong>${ctx.data.author}</strong></p>
            <p>${ctx.data.text}</p>
        </div>
    `;
    
    document.getElementById("answers-list").insertAdjacentHTML("beforeend", answerHtml);
});

sub.subscribe();
centrifuge.connect();