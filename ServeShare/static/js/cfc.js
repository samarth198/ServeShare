const cfcLink = document.querySelector(".cfc");
const popupContainer = document.querySelector(".popup-container");
const btnClose = document.querySelector('.icon-close');

if (cfcLink) {
    cfcLink.addEventListener('click', () => {
        console.log('clicked update');
        popupContainer.classList.toggle('active')
    });
} else {
    console.log("Element with class 'cfc' not found.");
}

btnClose.addEventListener('click', () => {
    popupContainer.classList.remove('active');
});

function find() {

    var total = 0.0;
    var electricBill = document.getElementById("eb").value;
    var naturalGasBill = document.getElementById("gb").value;
    var carDistance = document.getElementById("km").value;
    var planeTaken = document.getElementById("a4").value;

    var electricEmissionsFactor = 0.00872;
    var naturalGasEmissionsFactor = 0.0002;
    var carEmissionsFactor = 0.002;
    var planeEmissionsFactor = 0.1;

    var electricFootprint = parseInt(electricBill) * electricEmissionsFactor;
    var naturalGasFootprint = parseInt(naturalGasBill) * naturalGasEmissionsFactor;
    var carFootprint = parseInt(carDistance) * carEmissionsFactor;
    var planeFootprint = parseInt(planeTaken) * planeEmissionsFactor;

    var total = electricFootprint + naturalGasFootprint + carFootprint + planeFootprint;

    const news = document.querySelector('input[name="newsp"]:checked');
    if (news.value == 'yes') {
        total = total - 0.184;
    }

    const met = document.querySelector('input[name="mesc"]:checked');
    if (met.value == 'yes') {
        total = total - 0.166;
    }

    // if (total > 2.5) {
    //     total.style.color = "red";
    // } else {
    //     total.style.color = "green";
    // }

    document.getElementById("ans").innerHTML = total;
}