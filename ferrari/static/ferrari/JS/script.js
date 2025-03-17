// menu
const menu = document.querySelector('.menu')
const nav = document.querySelector('.nav')
menu.onclick = () => {
    menu.classList.toggle('active');
    nav.classList.toggle('active');
};

//chnage car
const body = document.body;
const nextBtn = document.querySelector('.btn-conteiner');
const models = document.querySelectorAll('.display');

function firstBack() {
    const active = document.querySelector('.display.active');
    if (active) {
        const activeUrl = active.classList[1];
        body.style.background = `url(${activeUrl})`;
        body.style.backgroundSize = 'cover';
        body.style.backgroundPosition = 'center';
    }
}
firstBack();

nextBtn.addEventListener('click', () => {

    let foundActive = false;
    models.forEach(model => {
        if (model.classList.contains('active') && !foundActive) {
            model.classList.remove('active');
            foundActive = true;
        } else if (foundActive && !model.classList.contains('active')) {
            model.classList.add('active');
            const imageUrl = model.classList[1];
            body.style.background = `url(${imageUrl})`;
            body.style.backgroundSize = 'cover';
            body.style.backgroundPosition = 'center';
            foundActive = false;
        }
    });

    if (foundActive) {
        models[0].classList.add('active');
        const imageUrl = models[0].classList[1];
        body.style.background = `url(${imageUrl})`;
        body.style.backgroundSize = 'cover';
        body.style.backgroundPosition = 'center';
    }
});
