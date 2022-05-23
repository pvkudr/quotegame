const tasksListElement = document.querySelector(`.blocks__list`);
const taskElements = tasksListElement.querySelectorAll(`.blocks__item`);
// could be draggable
for (const task of taskElements) {
  task.draggable = true;
}

// after dragged add new class - selected
tasksListElement.addEventListener(`dragstart`, (evt) => {
  evt.target.classList.add(`selected`);
});

// stop dragging - remove class
tasksListElement.addEventListener(`dragend`, (evt) => {
  evt.target.classList.remove(`selected`);
});

//
tasksListElement.addEventListener(`dragover`, (evt) => {
  evt.preventDefault();
  const activeElement = tasksListElement.querySelector(`.selected`); //dragged
  const currentElement = evt.target; //dragg into

  //check not under itself of out of block
  const isMoveable =
    activeElement !== currentElement &&
    currentElement.classList.contains(`blocks__item`);
  if (!isMoveable) {
    return;
  }

  const nextElement =
    currentElement === activeElement.nextElementSibling
      ? currentElement.nextElementSibling
      : currentElement;

  tasksListElement.insertBefore(activeElement, nextElement);
});

//start the game

const quotes_bank = [
  ["not all those who wander are lost", "J.R.R. Tolkien"],
  ["the true is like salt", "J.Abercrombie"],
  ["mothers are all slightly insane", "J.D. Salinger"],
];

// let arr = message.split(' ');

function getRndInteger(min = 0, max) {
  return Math.floor(Math.random() * (max - min)) + min;
}

//refresh

const refresh_button = document.querySelector(".refresh_button");

// refresh_button.addEventListener("click", function () {
//   const rnd_number = getRndInteger(0, quotes_bank.length);
//   let qt = quotes_bank[rnd_number][0].split(" ");
//   console.log(rnd_number);
//   console.log(qt);

//   func();
// });

// create new

const new_ele = document.createElement("ul");

// link to insert point
const insert_point = document.getElementById("insert_point");
//insert point parent
const parentIp = insert_point.parentNode;

const func = () => {
  document.getElementById("b1").innerHTML = "any";
};
